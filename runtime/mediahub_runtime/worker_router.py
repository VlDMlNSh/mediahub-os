"""Bounded agent-worker routing for MediaHub development tasks.

Claude Code is treated as an agent worker, not as a provider credential route.
The worker is opt-in and uses read/edit/write tools only; Ollama remains the
local fallback. No API keys are accepted by this module.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class WorkerRouterError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class WorkerDecision:
    worker_id: str
    mode: str
    reason: str


class ClaudeCodeWorker:
    worker_id = "claude-code"

    def __init__(self, repo: str | Path | None = None, timeout: int = 300):
        self.repo = Path(repo or os.environ.get("MEDIAHUB_REPO", Path.cwd())).resolve()
        self.timeout = max(1, min(int(timeout), 900))

    def available(self) -> bool:
        return shutil.which("claude") is not None

    def run(self, prompt: str) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise WorkerRouterError("invalid_prompt")
        if not self.available():
            raise WorkerRouterError("claude_code_unavailable")
        if not self.repo.is_dir():
            raise WorkerRouterError("repository_unavailable")
        command = [
            "claude", "--print",
            "--output-format", "text",
            "--allowed-tools", "Read,Glob,Grep,Edit,Write",
            "--disallowed-tools", "Bash,WebFetch,WebSearch,NotebookEdit",
            "--append-system-prompt",
            "Work only inside the supplied repository. Do not use shell commands, credentials, network access, destructive operations, git mutations, or production actions. Make only the requested bounded code changes and report what changed.",
            prompt,
        ]
        try:
            result = subprocess.run(
                command, cwd=self.repo, text=True, capture_output=True,
                timeout=self.timeout, check=False, env={"PATH": os.environ.get("PATH", "")},
            )
        except subprocess.TimeoutExpired as exc:
            raise WorkerRouterError("claude_code_timeout") from exc
        if result.returncode != 0:
            raise WorkerRouterError("claude_code_failed")
        output = result.stdout.strip()
        if not output:
            raise WorkerRouterError("empty_worker_result")
        return output


class WorkerRouter:
    def __init__(self, claude: ClaudeCodeWorker | None = None):
        self._claude = claude or ClaudeCodeWorker()

    def decide(self) -> WorkerDecision:
        enabled = os.environ.get("MEDIAHUB_ENABLE_CLAUDE_CODE_WORKER", "0").lower() in {"1", "true", "yes"}
        if enabled and self._claude.available():
            return WorkerDecision("claude-code", "agent", "explicit_opt_in")
        return WorkerDecision("ollama", "local_model", "claude_code_unavailable_or_disabled")

    def execute(self, prompt: str) -> tuple[WorkerDecision, str]:
        decision = self.decide()
        if decision.worker_id == "claude-code":
            try:
                return decision, self._claude.run(prompt)
            except WorkerRouterError:
                fallback = WorkerDecision("ollama", "local_model", "claude_code_failed")
                raise WorkerRouterError("worker_fallback_requires_model_adapter")
        raise WorkerRouterError("ollama_worker_requires_model_adapter")