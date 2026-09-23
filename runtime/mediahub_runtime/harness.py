"""MediaHub-native execution harness.

The harness is deliberately below Astra/Gateway policy: it executes only an
already-admitted argv vector under a strict allowlist, never through a shell,
and returns bounded evidence suitable for validation/audit.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


class HarnessError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class HarnessPolicy:
    allowed_executables: frozenset[str]
    allowed_roots: tuple[Path, ...]
    timeout_seconds: float = 30.0
    max_output_bytes: int = 1_048_576


@dataclass(frozen=True)
class HarnessResult:
    status: str
    returncode: int | None
    stdout: str
    stderr: str
    stdout_sha256: str
    stderr_sha256: str
    output_bytes: int


DEFAULT_POLICY = HarnessPolicy(
    allowed_executables=frozenset({
        "git", "python3", "pytest", "ruff", "mypy",
        "bash", "ls", "find", "grep", "head", "tail", "cat",
        "diff", "cmp", "stat", "realpath", "pwd", "whoami", "id",
        "du", "df", "free", "uptime",
    }),
    allowed_roots=(Path("/home/mediahub/mediahub-os").resolve(),),
)


class MediaHubHarness:
    """Bounded argv executor; no shell, no sudo, no credential injection."""

    def __init__(self, policy: HarnessPolicy = DEFAULT_POLICY):
        self.policy = policy

    def run(self, argv: Sequence[str], cwd: str | Path = "/home/mediahub/mediahub-os") -> HarnessResult:
        self._validate(argv, cwd)
        workdir = Path(cwd).resolve()
        try:
            completed = subprocess.run(
                list(argv),
                cwd=workdir,
                shell=False,
                capture_output=True,
                text=False,
                timeout=self.policy.timeout_seconds,
                env=self._safe_env(),
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise HarnessError("execution_timeout") from exc
        except OSError as exc:
            raise HarnessError("execution_failed") from exc

        stdout = completed.stdout[: self.policy.max_output_bytes]
        stderr = completed.stderr[: self.policy.max_output_bytes]
        if len(completed.stdout) > self.policy.max_output_bytes or len(completed.stderr) > self.policy.max_output_bytes:
            raise HarnessError("output_limit_exceeded")
        return HarnessResult(
            status="completed" if completed.returncode == 0 else "failed",
            returncode=completed.returncode,
            stdout=stdout.decode("utf-8", errors="replace"),
            stderr=stderr.decode("utf-8", errors="replace"),
            stdout_sha256=hashlib.sha256(stdout).hexdigest(),
            stderr_sha256=hashlib.sha256(stderr).hexdigest(),
            output_bytes=len(stdout) + len(stderr),
        )

    def _validate(self, argv: Sequence[str], cwd: str | Path) -> None:
        if not argv or any(not isinstance(item, str) or not item for item in argv):
            raise HarnessError("invalid_argv")
        executable = Path(argv[0]).name
        if executable not in self.policy.allowed_executables:
            raise HarnessError("executable_not_allowed")
        workdir = Path(cwd).resolve()
        if not any(workdir == root or root in workdir.parents for root in self.policy.allowed_roots):
            raise HarnessError("cwd_not_allowed")
        forbidden = {"sudo", "rm", "reset", "--hard", "push", "--force", "curl", "wget"}
        if any(item in forbidden for item in argv):
            raise HarnessError("argument_not_allowed")
        if executable == "bash" and tuple(argv[1:]) != ("-n",):
            raise HarnessError("argument_not_allowed")
        if any(any(marker in item.lower() for marker in ("api_key", "token", "secret", "password", "credential")) for item in argv):
            raise HarnessError("credential_argument_rejected")

    @staticmethod
    def _safe_env() -> dict[str, str]:
        allowed = {"PATH", "HOME", "LANG", "LC_ALL", "PYTHONPATH", "TMPDIR"}
        return {key: value for key, value in os.environ.items() if key in allowed}
