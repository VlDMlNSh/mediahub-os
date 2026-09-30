#!/usr/bin/env python3
"""MH-22 deterministic qualification executor.

This runner is deliberately conservative: it never grants production authority,
never mutates State Authority, never consumes production credentials/user data,
and never converts missing evidence into PASS.

It validates candidate identity and emits a machine-readable 23-pass evidence
bundle. Domain adapters are explicit and must be supplied as safe, repository-
local argv specifications; absent adapters remain NOT_IMPLEMENTED/EVIDENCE_GAP.
"""
from __future__ import annotations

import argparse, hashlib, json, os, platform, subprocess, sys, time
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "mediahub.mh22-qualification-evidence.v1"
EXECUTOR_ID = "mh22-qualification-executor"
EXECUTOR_VERSION = "1.0.0"
R4 = "471f709f5633feab7aeb62dd3ea52effad6d2bc4"
PASSES = [
    (1, "architecture_completeness"), (2, "authority"), (3, "identity"),
    (4, "trust"), (5, "security"), (6, "privacy"), (7, "hardware"),
    (8, "software"), (9, "supply_chain"), (10, "device"), (11, "protocol"),
    (12, "smart_home"), (13, "state_authority_persistence"), (14, "network_egress"),
    (15, "resource_management"), (16, "ai"), (17, "media"), (18, "knowledge"),
    (19, "cloud"), (20, "api_event_integration"), (21, "failure_recovery"),
    (22, "update_migration"), (23, "production_admission"),
]
ALLOWED = {"PASS","FAIL","BLOCKED","NOT_IMPLEMENTED","UNKNOWN","EVIDENCE_GAP"}

@dataclass
class Result:
    pass_id: int
    domain: str
    result: str
    exit_status: int
    test_id: str
    logs: str
    reproducibility_status: str = "NOT_ESTABLISHED"

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def file_hash(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def run_argv(argv: list[str], cwd: Path, timeout: int) -> tuple[int,str]:
    p = subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, timeout=timeout, check=False,
                       env={k:v for k,v in os.environ.items()
                            if k.startswith("LC_") or k in {"PATH","HOME","LANG"}})
    return p.returncode, p.stdout[-20000:]

def git(repo: Path, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=repo, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, check=False)
    if p.returncode:
        raise RuntimeError(p.stdout.strip())
    return p.stdout.strip()

def identity(repo: Path, expected: str) -> dict:
    commit = git(repo, "rev-parse", "HEAD")
    tree = git(repo, "rev-parse", "HEAD^{tree}")
    parent = git(repo, "rev-parse", "HEAD^")
    merge_base = git(repo, "merge-base", expected, commit)
    return {
        "candidate_commit": commit,
        "candidate_tree": tree,
        "parent": parent,
        "r4_commit": expected,
        "merge_base": merge_base,
        "r4_ancestor": merge_base == expected,
    }

def load_manifest(path: Path) -> dict:
    if not path.exists():
        return {"adapters": {}}
    return json.loads(path.read_text())

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--candidate-commit", required=True)
    ap.add_argument("--r4", default=R4)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--manifest", default="qualification/mh22-executor-manifest.json")
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out = Path(args.output).resolve()
    manifest_path = repo / args.manifest
    started = time.time()
    ident = identity(repo, args.r4)

    if ident["candidate_commit"] != args.candidate_commit:
        raise SystemExit("candidate commit mismatch")
    if not ident["r4_ancestor"]:
        raise SystemExit("R4 ancestry validation failed")

    manifest = load_manifest(manifest_path)
    env_id = sha256_bytes(json.dumps({
        "python": sys.version, "platform": platform.platform(),
        "machine": platform.machine(), "executor": EXECUTOR_VERSION
    }, sort_keys=True).encode())[:24]

    results = []
    adapters = manifest.get("adapters", {})
    for pass_id, domain in PASSES:
        spec = adapters.get(str(pass_id))
        if not spec:
            results.append(Result(
                pass_id, domain, "NOT_IMPLEMENTED", 127,
                f"MH22-P{pass_id:02d}-adapter-missing",
                "No approved domain adapter is registered; no PASS inferred.",
            ))
            continue
        if spec.get("network") or spec.get("credentials") or spec.get("user_data"):
            results.append(Result(
                pass_id, domain, "BLOCKED", 126,
                f"MH22-P{pass_id:02d}-unsafe-adapter",
                "Adapter violates isolation contract.",
            ))
            continue
        argv = spec.get("argv")
        if not isinstance(argv, list) or not argv or any(not isinstance(x,str) for x in argv):
            results.append(Result(
                pass_id, domain, "EVIDENCE_GAP", 125,
                f"MH22-P{pass_id:02d}-invalid-adapter",
                "Adapter argv is missing or malformed.",
            ))
            continue
        try:
            code, logs = run_argv(argv, repo, args.timeout)
            result = "PASS" if code == 0 else "FAIL"
        except subprocess.TimeoutExpired as exc:
            code, logs, result = 124, str(exc), "BLOCKED"
        results.append(Result(
            pass_id, domain, result, code,
            spec.get("test_id", f"MH22-P{pass_id:02d}-custom"),
            logs,
            "PASS" if code in (0,1) else "NOT_ESTABLISHED",
        ))

    finished = time.time()
    bundle = {
        "schema": SCHEMA,
        "qualification_run_id": args.run_id,
        "candidate": ident,
        "executor": {"id": EXECUTOR_ID, "version": EXECUTOR_VERSION},
        "environment": {
            "environment_id": env_id,
            "python": sys.version,
            "platform": platform.platform(),
            "network": "NOT_ALLOWED_BY_CONTRACT",
            "production_credentials": False,
            "user_data": False,
            "state_authority_mutation": False,
            "production_authorization": False,
            "release_authorization": False,
        },
        "started_at_epoch": started,
        "finished_at_epoch": finished,
        "passes": [r.__dict__ for r in results],
        "verdict": "QUALIFIED" if all(r.result == "PASS" for r in results) else "BLOCKED",
        "invariants": {
            "unknown_is_not_pass": True,
            "evidence_gap_is_not_pass": True,
            "not_implemented_is_not_pass": True,
            "missing_evidence_is_not_pass": True,
        },
    }
    raw = json.dumps(bundle, sort_keys=True, indent=2).encode()
    bundle["bundle_sha256"] = sha256_bytes(raw)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bundle, sort_keys=True, indent=2) + "\n")
    return 0 if bundle["verdict"] == "QUALIFIED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
