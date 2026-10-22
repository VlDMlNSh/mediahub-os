"""Bounded agent-worker routing for MediaHub development tasks.

Claude Code is an agent worker; Ollama is the default local model worker.
No API keys are accepted by this module and Ollama is restricted to loopback.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
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
            "claude", "--print", "--output-format", "text",
            "--allowed-tools", "Read,Glob,Grep,Edit,Write",
            "--disallowed-tools", "Bash,WebFetch,WebSearch,NotebookEdit",
            "--append-system-prompt",
            "Work only inside the supplied repository. Do not use shell commands, credentials, network access, destructive operations, git mutations, or production actions. Make only the requested bounded code changes and report what changed.",
            prompt,
        ]
        try:
            result = subprocess.run(command, cwd=self.repo, text=True,
                                    capture_output=True, timeout=self.timeout,
                                    check=False, env={"PATH": os.environ.get("PATH", "")})
        except subprocess.TimeoutExpired as exc:
            raise WorkerRouterError("claude_code_timeout") from exc
        if result.returncode != 0:
            raise WorkerRouterError("claude_code_failed")
        output = result.stdout.strip()
        if not output:
            raise WorkerRouterError("empty_worker_result")
        return output


class OllamaWorker:
    worker_id = "ollama"

    def __init__(self, model: str | None = None, endpoint: str | None = None,
                 timeout: int = 300):
        self.model = model or os.environ.get("MEDIAHUB_OLLAMA_MODEL", "qwen2.5-coder:3b")
        self.endpoint = endpoint or os.environ.get("MEDIAHUB_OLLAMA_ENDPOINT", "http://127.0.0.1:11434")
        self.timeout = max(1, min(int(timeout), 900))
        if not self.endpoint.startswith("http://127.0.0.1:"):
            raise WorkerRouterError("ollama_endpoint_must_be_loopback")

    def available(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self.endpoint}/api/tags", timeout=min(self.timeout, 10)) as response:
                payload = json.load(response)
            return any(item.get("name") == self.model for item in payload.get("models", []))
        except (OSError, ValueError, urllib.error.URLError):
            return False

    def run(self, prompt: str) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise WorkerRouterError("invalid_prompt")
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode()
        request = urllib.request.Request(
            f"{self.endpoint}/api/generate", data=payload,
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                result = json.load(response)
        except urllib.error.URLError as exc:
            raise WorkerRouterError("ollama_request_failed") from exc
        except (OSError, ValueError) as exc:
            raise WorkerRouterError("ollama_invalid_response") from exc
        output = result.get("response", "").strip()
        if not output:
            raise WorkerRouterError("empty_worker_result")
        return output


class WorkerRouter:
    def __init__(self, claude: ClaudeCodeWorker | None = None,
                 ollama: OllamaWorker | None = None):
        self._claude = claude or ClaudeCodeWorker()
        self._ollama = ollama or OllamaWorker()

    def decide(self) -> WorkerDecision:
        enabled = os.environ.get("MEDIAHUB_ENABLE_CLAUDE_CODE_WORKER", "0").lower() in {"1", "true", "yes"}
        if enabled and self._claude.available():
            return WorkerDecision("claude-code", "agent", "explicit_opt_in")
        if self._ollama.available():
            return WorkerDecision("ollama", "local_model", "claude_code_unavailable_or_disabled")
        return WorkerDecision("ollama", "local_model", "local_worker_unavailable")

    def execute(self, prompt: str) -> tuple[WorkerDecision, str]:
        decision = self.decide()
        if decision.worker_id == "claude-code":
            try:
                return decision, self._claude.run(prompt)
            except WorkerRouterError:
                if self._ollama.available():
                    fallback = WorkerDecision("ollama", "local_model", "claude_code_failed")
                    return fallback, self._ollama.run(prompt)
                raise WorkerRouterError("worker_fallback_unavailable")
        return decision, self._ollama.run(prompt)
