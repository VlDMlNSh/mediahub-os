#!/usr/bin/env python3
"""Produce one fresh, signed distributed-verification attestation on a target node."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any

AUTH_SCHEMA = "mediahub.astra.distributed.auth.v1"
NODE_SCHEMA = "mediahub.astra.distributed-node-attestation.v1"
PHASE = "distributed_verification"
SAFE_NODES = {
    "mh-dev-01": {"hostnames": {"mh-dev-01"}, "user": "mediahub-runner"},
    "mh-dev-02": {"hostnames": {"mh-dev-02"}, "user": "mediahub"},
    "Voktors-Mac-mini.local": {
        "hostnames": {"Voktors-Mac-mini.local", "Voktors-Mini.Dlink"},
        "user": "voktor",
    },
}
PRODUCER_PREFIX = "node-agent:"
SHA_LEN = {40, 64}


def _canonical_body(data: dict[str, Any]) -> bytes:
    return json.dumps(
        {k: v for k, v in data.items() if k != "signature"},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def validate_identity(node_id: str, hostname: str) -> tuple[bool, str]:
    spec = SAFE_NODES.get(node_id)
    if spec is None:
        return False, "unsupported_node_id"
    if hostname not in spec["hostnames"]:
        return False, "hostname_node_binding_mismatch"
    return True, ""


def current_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        timeout=15,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def build_attestation(
    *,
    command_id: str,
    node_id: str,
    target_sha: str,
    current_node: str,
    current_user: str,
    current_head: str,
    observed_at: int,
    checks: dict[str, bool],
    hmac_key: str,
) -> dict[str, Any]:
    spec = SAFE_NODES.get(node_id)
    blocked: list[str] = []
    if spec is None:
        blocked.append("unsupported_node_id")
    else:
        if current_node not in spec["hostnames"]:
            blocked.append("node_identity_mismatch")
        if current_user != spec["user"]:
            blocked.append("user_identity_mismatch")
    if not command_id:
        blocked.append("missing_command_id")
    if not target_sha or len(target_sha) not in SHA_LEN:
        blocked.append("invalid_target_sha")
    if not current_head or len(current_head) not in SHA_LEN:
        blocked.append("current_head_unavailable")
    elif target_sha.lower() != current_head.lower():
        blocked.append("target_sha_mismatch")
    if not hmac_key:
        blocked.append("hmac_key_missing")
    for name, passed in checks.items():
        if passed is not True:
            blocked.append(f"check_failed:{name}")

    status = "PASS" if not blocked else "BLOCKED"
    payload: dict[str, Any] = {
        "schema": NODE_SCHEMA,
        "command_id": command_id,
        "node_id": node_id,
        "target_sha": target_sha,
        "producer_identity": f"{PRODUCER_PREFIX}{node_id}",
        "phase": PHASE,
        "status": status,
        "returncode": 0 if status == "PASS" else 2,
        "completed_at": int(observed_at),
        "auth_schema_version": AUTH_SCHEMA,
        "hostname": current_node,
        "current_user": current_user,
        "current_head": current_head,
        "observations": dict(checks),
        "checks": {name: {"status": "PASS" if passed else "BLOCKED"} for name, passed in checks.items()},
        "blocked_reasons": sorted(set(blocked)),
        "secret_values": "SUPPRESSED",
    }
    payload["signature"] = (
        hmac.new(hmac_key.encode("utf-8"), _canonical_body(payload), hashlib.sha256).hexdigest()
        if hmac_key
        else ""
    )
    return payload


def validate_context(
    *, node_id: str, hostname: str, target_sha: str, current_head: str, command_id: str, hmac_key: str
) -> list[str]:
    blocked: list[str] = []
    ok, reason = validate_identity(node_id, hostname)
    if not ok:
        blocked.append(reason)
    if not command_id:
        blocked.append("missing_command_id")
    if not target_sha or len(target_sha) not in SHA_LEN:
        blocked.append("invalid_target_sha")
    if not current_head or len(current_head) not in SHA_LEN:
        blocked.append("current_head_unavailable")
    elif target_sha.lower() != current_head.lower():
        blocked.append("target_sha_mismatch")
    if not hmac_key:
        blocked.append("missing_hmac_key")
    return blocked


def run_check(root: Path, argv: list[str], timeout: int = 300) -> dict[str, Any]:
    started = time.monotonic()
    try:
        p = subprocess.run(
            argv,
            cwd=root,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "returncode": p.returncode,
            "status": "PASS" if p.returncode == 0 else "BLOCKED",
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout": p.stdout[-4000:],
            "stderr": p.stderr[-4000:],
        }
    except Exception as exc:
        return {
            "returncode": 2,
            "status": "BLOCKED",
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout": "",
            "stderr": repr(exc),
        }


def collect_attestation(
    *,
    root: Path,
    node_id: str,
    hostname: str,
    command_id: str,
    target_sha: str,
    hmac_key: str,
    current_head: str | None = None,
) -> dict[str, Any]:
    now = int(time.time())
    current_head = current_head or ""
    blocked = validate_context(
        node_id=node_id,
        hostname=hostname,
        target_sha=target_sha,
        current_head=current_head,
        command_id=command_id,
        hmac_key=hmac_key,
    )
    observations = {
        "identity": not any(
            x in blocked for x in ("unsupported_node_id", "hostname_node_binding_mismatch")
        ),
        "command_binding": "missing_command_id" not in blocked,
        "target_sha": "invalid_target_sha" not in blocked and "target_sha_mismatch" not in blocked,
    }
    checks: dict[str, Any] = {}
    if not blocked:
        checks["compile"] = run_check(
            root, ["python3", "-m", "compileall", "-q", "ops", "runtime"]
        )
        checks["mesh_contract"] = run_check(
            root,
            [
                "python3",
                "-m",
                "unittest",
                "-q",
                "tests/test_mesh_registry_admission.py",
                "tests/test_mesh_runtime_contract.py",
            ],
            300,
        )
        checks["controller_contract"] = run_check(
            root,
            [
                "python3",
                "-m",
                "unittest",
                "-q",
                "tests/test_astra_github_agent_contract.py",
                "tests/test_autonomous_gold_mission.py",
            ],
            300,
        )
        observations.update(
            {
                "compile": checks["compile"]["status"] == "PASS",
                "mesh_contract": checks["mesh_contract"]["status"] == "PASS",
                "controller_contract": checks["controller_contract"]["status"] == "PASS",
            }
        )
    else:
        for key in ("compile", "mesh_contract", "controller_contract"):
            observations[key] = False

    status = "PASS" if not blocked and all(observations.values()) and all(
        item["status"] == "PASS" for item in checks.values()
    ) else "BLOCKED"

    payload: dict[str, Any] = {
        "schema": NODE_SCHEMA,
        "command_id": command_id,
        "node_id": node_id,
        "target_sha": target_sha,
        "producer_identity": f"{PRODUCER_PREFIX}{node_id}",
        "phase": PHASE,
        "status": status,
        "returncode": 0 if status == "PASS" else 2,
        "completed_at": now,
        "auth_schema_version": AUTH_SCHEMA,
        "hostname": hostname,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "current_head": current_head,
        "observations": observations,
        "checks": checks,
        "blocked_reasons": sorted(set(blocked)),
        "secret_values": "SUPPRESSED",
    }
    payload["signature"] = hmac.new(
        hmac_key.encode("utf-8") if hmac_key else b"",
        _canonical_body(payload),
        hashlib.sha256,
    ).hexdigest() if hmac_key else ""
    return payload


def main() -> int:
    root = Path(os.environ.get("ASTRA_WORKTREE", Path.cwd()))
    node_id = os.environ.get("ASTRA_EXPECTED_NODE_ID", "")
    hostname = platform.node()
    command_id = os.environ.get("ASTRA_COMMAND_ID", "")
    target_sha = os.environ.get("ASTRA_TARGET_SHA", "")
    hmac_key = os.environ.get("ASTRA_COMMAND_HMAC_KEY", "")
    output = Path(
        os.environ.get(
            "ASTRA_NODE_ATTESTATION_OUTPUT",
            str(root / ".astra-state" / f"{node_id}.json"),
        )
    )

    try:
        head_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
        current_head = head_result.stdout.strip() if head_result.returncode == 0 else ""
        result = collect_attestation(
            root=root,
            node_id=node_id,
            hostname=hostname,
            command_id=command_id,
            target_sha=target_sha,
            hmac_key=hmac_key,
            current_head=current_head,
        )
    except Exception as exc:
        result = {
            "schema": NODE_SCHEMA,
            "command_id": command_id,
            "node_id": node_id,
            "target_sha": target_sha,
            "producer_identity": f"{PRODUCER_PREFIX}{node_id}",
            "phase": PHASE,
            "status": "BLOCKED",
            "returncode": 2,
            "completed_at": int(time.time()),
            "auth_schema_version": AUTH_SCHEMA,
            "hostname": hostname,
            "current_head": "",
            "observations": {},
            "checks": {},
            "blocked_reasons": [f"producer_exception:{type(exc).__name__}"],
            "secret_values": "SUPPRESSED",
        }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return int(result["returncode"])


if __name__ == "__main__":
    raise SystemExit(main())
