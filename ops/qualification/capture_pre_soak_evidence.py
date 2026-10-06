#!/usr/bin/env python3
"""Capture fresh pre-soak evidence on the canonical Astra node.

This producer never fabricates PASS. Each artifact records the exact current
revision, capture time, and a bounded observable check or an explicit blocker.
Secrets are never read or emitted.
"""
from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
import re
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence"
AGENT = ROOT / "astra_github_agent.py"
NODE = platform.node()
NOW = int(time.time())


def run(argv: list[str], timeout: int = 90) -> tuple[int, str, str]:
    p = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True,
                       timeout=timeout, check=False)
    return p.returncode, p.stdout[-4000:], p.stderr[-4000:]


EXPECTED_TARGET_SHA = ""


def current_head() -> str:
    rc, out, _ = run(["git", "rev-parse", "HEAD"], 10)
    if rc != 0 or not re.fullmatch(r"[0-9a-f]{40}", out.strip()):
        raise RuntimeError("cannot determine exact current HEAD")
    return out.strip()


def write(name: str, status: str, check: str, reason: str = "", **extra: object) -> None:
    payload = {
        "schema": "mediahub.pre-soak-evidence.v1",
        "status": status,
        "captured_at": NOW,
        "target_sha": EXPECTED_TARGET_SHA,
        "node_id": NODE,
        "check": check,
        "reason": reason,
        "secret_values": "SUPPRESSED",
        **extra,
    }
    (EVIDENCE / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")


def main() -> int:
    global EXPECTED_TARGET_SHA
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-sha", required=True)
    parser.add_argument("--provider-evidence", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.target_sha):
        raise SystemExit("BLOCK: invalid target SHA")
    EXPECTED_TARGET_SHA = args.target_sha
    if current_head() != EXPECTED_TARGET_SHA:
        raise SystemExit("BLOCK: signed target SHA does not equal current HEAD")
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    blocked = False

    # Transport identity is directly observable on the canonical worker.
    agent_sha = hashlib.sha256(AGENT.read_bytes()).hexdigest()
    workers = subprocess.run(["pgrep", "-af", "astra_github_agent.py"],
                             cwd=ROOT, text=True, capture_output=True, check=False)
    if NODE == "mh-dev-01" and workers.returncode == 0 and agent_sha:
        write("transport-health.json", "PASS", "canonical_worker_identity",
              agent_source_sha=agent_sha, worker_present=True)
    else:
        blocked = True
        write("transport-health.json", "BLOCKED", "canonical_worker_identity",
              "canonical mh-dev-01 worker identity could not be independently observed",
              agent_source_sha=agent_sha, worker_present=workers.returncode == 0)

    # Runtime E2E: use the installed local model only; no network or secrets.
    ollama = shutil.which("ollama")
    if not ollama:
        blocked = True
        write("runtime-e2e.json", "BLOCKED", "ollama_live_smoke",
              "ollama executable is not available on the canonical node")
    else:
        rc, out, err = run([ollama, "run", "qwen2.5-coder:3b",
                            "Return exactly MEDIAHUB_OLLAMA_LIVE_OK and nothing else."], 90)
        if rc == 0 and "MEDIAHUB_OLLAMA_LIVE_OK" in out:
            write("runtime-e2e.json", "PASS", "ollama_live_smoke",
                  model="qwen2.5-coder:3b", marker_present=True)
        else:
            blocked = True
            write("runtime-e2e.json", "BLOCKED", "ollama_live_smoke",
                  "bounded live marker was not observed", returncode=rc,
                  marker_present="MEDIAHUB_OLLAMA_LIVE_OK" in out)

    # A3 provider evidence is produced on the provider node and handed over as a
    # fresh, sanitized artifact. The canonical node never receives provider secrets.
    provider_payload = {}
    try:
        provider_payload = json.loads(args.provider_evidence.read_text(encoding="utf-8"))
    except Exception:
        provider_payload = {"status": "BLOCKED", "reason": "invalid_provider_evidence"}

    provider_blocked = []
    if provider_payload.get("schema") != "mediahub.provider-model-qualification.v1":
        provider_blocked.append("invalid_schema")
    if provider_payload.get("status") != "PASS":
        provider_blocked.append("status_not_PASS")
    if provider_payload.get("target_sha") != EXPECTED_TARGET_SHA:
        provider_blocked.append("target_sha_mismatch")
    if provider_payload.get("repo_revision") != EXPECTED_TARGET_SHA:
        provider_blocked.append("repo_revision_mismatch")
    if provider_payload.get("node_id") != "mh-dev-02":
        provider_blocked.append("provider_node_identity_mismatch")
    if not isinstance(provider_payload.get("evidence_digest"), str) or not provider_payload.get("evidence_digest").startswith("sha256:"):
        provider_blocked.append("evidence_digest_invalid")
    summary = provider_payload.get("summary") if isinstance(provider_payload.get("summary"), dict) else {}
    if int(summary.get("qualified_providers", 0)) < 1:
        provider_blocked.append("no_qualified_provider")
    qualified = [
        item for item in provider_payload.get("providers", [])
        if isinstance(item, dict) and item.get("verification_state") == "QUALIFIED"
    ]
    if not qualified:
        provider_blocked.append("no_qualified_provider_record")

    provider_status = "PASS" if not provider_blocked else "BLOCKED"
    if provider_status != "PASS":
        blocked = True
    write(
        "provider-model.json",
        provider_status,
        "node_local_a3_provider_qualification",
        ";".join(provider_blocked),
        qualification=provider_payload,
        provider_node="mh-dev-02",
    )

    # Runtime gates are produced by exercising the real runtime modules. The
    # producer is fail-closed: it reports PASS only on the canonical node and
    # only when every module observation holds.
    prereq = ROOT / "ops" / "qualification" / "produce_runtime_prereq_evidence.py"
    prereq_run = subprocess.run(
        [sys.executable, str(prereq), "--out", str(EVIDENCE)],
        cwd=ROOT, text=True, capture_output=True, timeout=300, check=False,
    )
    if prereq_run.returncode != 0:
        blocked = True

    return 2 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
