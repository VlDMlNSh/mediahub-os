import os
from pathlib import Path

import pytest

from mediahub_runtime import ClaudeCodeWorker, WorkerRouter, WorkerRouterError


def test_worker_defaults_to_local_model_without_opt_in(monkeypatch, tmp_path):
    monkeypatch.delenv("MEDIAHUB_ENABLE_CLAUDE_CODE_WORKER", raising=False)
    worker = ClaudeCodeWorker(repo=tmp_path)
    decision = WorkerRouter(worker).decide()
    assert decision.worker_id == "ollama"
    assert decision.mode == "local_model"


def test_worker_opt_in_selects_claude_code_when_available(monkeypatch, tmp_path):
    monkeypatch.setenv("MEDIAHUB_ENABLE_CLAUDE_CODE_WORKER", "1")
    worker = ClaudeCodeWorker(repo=tmp_path)
    monkeypatch.setattr(worker, "available", lambda: True)
    decision = WorkerRouter(worker).decide()
    assert decision.worker_id == "claude-code"
    assert decision.reason == "explicit_opt_in"


def test_worker_command_is_bounded_and_does_not_enable_dangerous_flags(tmp_path, monkeypatch):
    worker = ClaudeCodeWorker(repo=tmp_path)
    monkeypatch.setattr(worker, "available", lambda: True)
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        class Result:
            returncode = 0
            stdout = "done"
        return Result()

    monkeypatch.setattr("mediahub_runtime.worker_router.subprocess.run", fake_run)
    assert worker.run("inspect") == "done"
    command = captured["command"]
    assert "--dangerously-skip-permissions" not in command
    assert "Bash" in command[command.index("--disallowed-tools") + 1]
    assert all("OPENROUTER_API_KEY" not in str(v) and "TINYFISH_API_KEY" not in str(v) for v in command)


def test_worker_rejects_empty_prompt(tmp_path):
    worker = ClaudeCodeWorker(repo=tmp_path)
    with pytest.raises(WorkerRouterError, match="invalid_prompt"):
        worker.run("")
