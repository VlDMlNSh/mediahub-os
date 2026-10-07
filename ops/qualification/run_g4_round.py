#!/usr/bin/env python3
"""Execute exactly one real G4 transport round and emit cryptographically bound evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

IDENTITY = {
    "CODEX_FCC": ("codex", "fcc"),
    "CLAUDE_FCC": ("claude", "fcc"),
    "CODEX_OMNIROUTE": ("codex", "omniroute"),
    "CLAUDE_OMNIROUTE": ("claude", "omniroute"),
    "CLAUDE_CODE_DIRECT": ("claude_code", "native"),
}

COMMANDS = {
    "CODEX_FCC": ["fcc-codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check"],
    "CLAUDE_FCC": ["fcc-claude"],
    "CODEX_OMNIROUTE": ["omniroute", "launch-codex"],
    "CLAUDE_OMNIROUTE": ["omniroute", "launch"],
    "CLAUDE_CODE_DIRECT": ["claude"],
}


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def load_env_file(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise RuntimeError("fcc_env_file_missing")
    values = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def claude_fcc_env() -> dict[str, str]:
    env = os.environ.copy()
    candidates = []
    explicit = env.get("ASTRA_FCC_ENV_FILE", "").strip()
    if explicit:
        candidates.append(Path(explicit))
    candidates.extend([
        Path.home() / ".config" / "mediahub" / "fcc.env",
        Path.home() / "Library" / "Application Support" / "MediaHub" / "fcc.env",
    ])
    for path in candidates:
        if path.is_file():
            vals = load_env_file(path)
            env.update(vals)
            host = vals.get("HOST", "127.0.0.1")
            port = vals.get("PORT", "8093")
            env["ANTHROPIC_BASE_URL"] = f"http://{host}:{port}"
            token = vals.get("ANTHROPIC_AUTH_TOKEN", "")
            if token:
                env["ANTHROPIC_AUTH_TOKEN"] = token
                env["ANTHROPIC_API_KEY"] = token
            env["ASTRA_FCC_TRANSPORT"] = "fcc"
            env["ASTRA_FCC_MODEL"] = vals.get("MODEL", "")
            env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
            env["ENABLE_MODEL_THINKING"] = "false"
            env["ENABLE_OPUS_THINKING"] = "false"
            env["ENABLE_SONNET_THINKING"] = "false"
            env["ENABLE_HAIKU_THINKING"] = "false"
            env["CLAUDE_CODE_DISABLE_THINKING"] = "1"
            env["MAX_THINKING_TOKENS"] = "0"
            return env
    raise RuntimeError("fcc_env_file_missing")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--path", required=True, choices=sorted(IDENTITY))
    p.add_argument("--round", required=True, type=int)
    p.add_argument("--source-sha", required=True)
    p.add_argument("--workspace", type=Path, default=Path.cwd())
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    if a.source_sha != subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=a.workspace, text=True
    ).strip():
        raise SystemExit("target_sha_not_current_head")
    if subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=a.workspace, text=True
    ).strip():
        raise SystemExit("dirty_qualification_workspace")

    executor, transport = IDENTITY[a.path]
    marker = f"G4_{a.path}_OK"
    command_id = "g4-" + hashlib.sha256(
        f"G4|{a.source_sha}|{a.path}|{a.round}".encode()
    ).hexdigest()[:24]

    if a.path == "CLAUDE_FCC":
        argv = COMMANDS[a.path] + ["-p", f"Return exactly {marker}.", "--output-format", "text", "--max-turns", "1"]
    elif a.path == "CLAUDE_OMNIROUTE":
        argv = COMMANDS[a.path] + ["--", "-p", f"Return exactly {marker}.", "--output-format", "text", "--max-turns", "1"]
    elif a.path == "CLAUDE_CODE_DIRECT":
        argv = COMMANDS[a.path] + ["-p", f"Return exactly {marker}.", "--output-format", "text", "--max-turns", "1"]
    elif a.path == "CODEX_FCC":
        argv = COMMANDS[a.path] + [f"Return exactly {marker}."]
    else:
        argv = COMMANDS[a.path] + ["exec", "--sandbox", "read-only", "--skip-git-repo-check", f"Return exactly {marker}."]

    started = time.time()
    try:
        proc = subprocess.run(
            argv,
            cwd=a.workspace,
            text=True,
            capture_output=True,
            timeout=a.timeout,
            check=False,
            env=claude_fcc_env() if a.path == "CLAUDE_FCC" else os.environ.copy(),
        )
        rc = proc.returncode
        stdout = proc.stdout[-20000:]
        stderr = proc.stderr[-12000:]
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        rc = 124
        stdout = (exc.stdout or "")[-20000:] if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "")[-12000:] if isinstance(exc.stderr, str) else ""
        timed_out = True

    completed = time.time()
    combined = stdout + "\n" + stderr
    marker_present = marker in stdout and rc == 0 and not timed_out
    row = {
        "command_id": command_id,
        "path": a.path,
        "round": a.round,
        "source_sha": a.source_sha,
        "executor_identity": executor,
        "provider_or_transport_identity": transport,
        "workspace": str(a.workspace.resolve()),
        "started_at": started,
        "completed_at": completed,
        "exit_status": rc,
        "timeout": timed_out,
        "marker": marker,
        "marker_present": marker_present,
        "result_schema": "g4-round-v1",
        "verification_status": "PASS" if marker_present else "BLOCKED",
        "output_sha256": "sha256:" + hashlib.sha256(combined.encode()).hexdigest(),
        "command_argv": argv[:3] + ["<redacted-prompt>"],
    }
    row["evidence_digest"] = digest(row)
    a.out.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if marker_present else 2


if __name__ == "__main__":
    raise SystemExit(main())
