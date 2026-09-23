"""GitHub-hosted credential boundary for MediaHub cloud/web tasks."""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / ".mediahub" / "tasks" / "inbox"
DONE = ROOT / ".mediahub" / "tasks" / "done"

ALLOWED = {"tinyfish.web.run", "openrouter.infer"}
TINYFISH_API = "https://agent.tinyfish.ai"
OPENROUTER_API = "https://openrouter.ai/api/v1/chat/completions"
MAX_RESULT_BYTES = 262_144
MAX_TASK_BYTES = 131_072
MAX_PROMPT_CHARS = 65_536
MAX_OPENROUTER_OUTPUT_TOKENS = 1200
MAX_OPENROUTER_TASKS_PER_RUN = 1
POLL_SECONDS = 2
MAX_POLLS = 150


def write_result(task_id: str, payload: dict[str, Any]) -> None:
    DONE.mkdir(parents=True, exist_ok=True)
    (DONE / f"{task_id}.result.json").write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def fail(task_id: str, code: str) -> None:
    write_result(task_id, {"task_id": task_id, "status": "failed", "error": code})


def request_json(request: urllib.request.Request, limit: int = MAX_RESULT_BYTES) -> dict[str, Any]:
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read(limit + 1)
    if len(raw) > limit:
        raise ValueError("response_too_large")
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise TypeError("invalid_json_object")
    return data


def process(path: Path, *, openrouter_tasks_seen: int = 0) -> int:
    if path.stat().st_size > MAX_TASK_BYTES:
        fail(path.stem, "task_too_large")
        return openrouter_tasks_seen
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    task_id = data.get("task_id")
    operation = data.get("operation")
    if not isinstance(task_id, str) or not task_id or "/" in task_id or len(task_id) > 128:
        return openrouter_tasks_seen
    if operation not in ALLOWED:
        fail(task_id, "operation_not_allowed")
        return openrouter_tasks_seen
    if data.get("schema_id") != "mediahub.astra.github-cloud-task" or data.get("schema_version") != "1.0.0":
        fail(task_id, "invalid_task_contract")
        return openrouter_tasks_seen
    if data.get("owner") != "mediahub-ai" or data.get("approval_state") not in {"not_required", "approved"}:
        fail(task_id, "invalid_task_contract")
        return openrouter_tasks_seen
    if not isinstance(data.get("request_id"), str) or not isinstance(data.get("session_id"), str):
        fail(task_id, "invalid_task_contract")
        return openrouter_tasks_seen

    allowed_fields = ({"schema_id", "schema_version", "owner", "task_id", "request_id", "session_id", "operation", "approval_state", "prompt", "model"}
                      if operation == "openrouter.infer" else
                      {"schema_id", "schema_version", "owner", "task_id", "request_id", "session_id", "operation", "approval_state", "url", "goal"})
    if set(data) != allowed_fields:
        fail(task_id, "invalid_task_contract")
        return openrouter_tasks_seen

    if operation == "openrouter.infer":
        openrouter_tasks_seen += 1
        if openrouter_tasks_seen > MAX_OPENROUTER_TASKS_PER_RUN:
            fail(task_id, "openrouter_run_budget_exceeded")
            return openrouter_tasks_seen

        if os.environ.get("MEDIAHUB_ALLOW_METERED_OPENROUTER", "").lower() != "true":
            fail(task_id, "metered_openrouter_disabled")
            return openrouter_tasks_seen

        prompt = data.get("prompt")
        model = data.get("model") or os.environ.get("MEDIAHUB_OPENROUTER_MODEL", "")
        if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > MAX_PROMPT_CHARS:
            fail(task_id, "invalid_prompt")
            return openrouter_tasks_seen
        if not isinstance(model, str) or not model.strip() or len(model) > 256:
            fail(task_id, "openrouter_model_not_configured")
            return openrouter_tasks_seen
        if any(marker in prompt.lower() for marker in ("api_key", "password", "secret", "token=")):
            fail(task_id, "credential_data_in_prompt")
            return openrouter_tasks_seen
        key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not key:
            fail(task_id, "openrouter_not_configured_in_github")
            return openrouter_tasks_seen

        payload = json.dumps(
            {
                "model": model.strip(),
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": MAX_OPENROUTER_OUTPUT_TOKENS,
                "temperature": 0.1,
                "stream": False,
            },
            separators=(",", ":"),
        ).encode("utf-8")
        request = urllib.request.Request(
            OPENROUTER_API,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
                "X-OpenRouter-Title": "MediaHub OS",
            },
            method="POST",
        )
        try:
            response = request_json(request)
            choices = response.get("choices")
            message = choices[0].get("message") if isinstance(choices, list) and choices else None
            output = message.get("content") if isinstance(message, dict) else None
            if not isinstance(output, str) or not output:
                fail(task_id, "openrouter_empty_result")
                return openrouter_tasks_seen
            safe = {
                "task_id": task_id,
                "status": "completed",
                "provider_id": "openrouter",
                "model": response.get("model", model.strip()),
                "generation_id": response.get("id"),
                "request_sha256": hashlib.sha256(payload).hexdigest(),
                "output": output,
                "usage": response.get("usage"),
            }
            # Never persist or return credential material.
            write_result(task_id, safe)
            return openrouter_tasks_seen
        except (urllib.error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
            fail(task_id, "openrouter_execution_failed")
            return openrouter_tasks_seen

    url, goal = data.get("url"), data.get("goal")
    if not isinstance(url, str) or not url.startswith(("https://", "http://")):
        fail(task_id, "invalid_target_url")
        return openrouter_tasks_seen
    if not isinstance(goal, str) or not goal.strip() or len(goal) > 16000:
        fail(task_id, "invalid_goal")
        return openrouter_tasks_seen
    if any(marker in goal.lower() for marker in ("api_key", "password", "secret", "token=")):
        fail(task_id, "credential_data_in_goal")
        return openrouter_tasks_seen
    if os.environ.get("MEDIAHUB_ALLOW_METERED_TINYFISH", "").lower() != "true":
        fail(task_id, "metered_tinyfish_disabled")
        return openrouter_tasks_seen
    key = os.environ.get("TINYFISH_API_KEY", "").strip()
    if not key:
        fail(task_id, "tinyfish_not_configured_in_github")
        return openrouter_tasks_seen

    payload = json.dumps(
        {
            "url": url,
            "goal": goal,
            "browser_profile": "lite",
            "agent_config": {"max_duration_seconds": 300},
        },
        separators=(",", ":"),
    ).encode("utf-8")
    start = urllib.request.Request(
        f"{TINYFISH_API}/v1/automation/run-async",
        data=payload,
        headers={"Content-Type": "application/json", "X-API-Key": key},
        method="POST",
    )
    try:
        created = request_json(start)
        run_id = created.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            fail(task_id, "tinyfish_invalid_response")
            return openrouter_tasks_seen
        for _ in range(MAX_POLLS):
            poll = urllib.request.Request(
                f"{TINYFISH_API}/v1/runs/{run_id}",
                headers={"X-API-Key": key},
                method="GET",
            )
            state = request_json(poll)
            status = state.get("status")
            if status in {"COMPLETED", "FAILED", "CANCELLED"}:
                result = state.get("result")
                result_bytes = (
                    json.dumps(result, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
                    if result is not None
                    else b""
                )
                if len(result_bytes) > MAX_RESULT_BYTES:
                    fail(task_id, "result_too_large")
                    return openrouter_tasks_seen
                if status == "COMPLETED" and (
                    not isinstance(result, dict) or result.get("status") == "failure" or result.get("error")
                ):
                    final_status = "goal_failed"
                else:
                    final_status = status.lower()
                write_result(
                    task_id,
                    {
                        "task_id": task_id,
                        "status": final_status,
                        "run_id": run_id,
                        "request_sha256": hashlib.sha256(payload).hexdigest(),
                        "result": result,
                        "error_code": state.get("error", {}).get("code")
                        if isinstance(state.get("error"), dict)
                        else None,
                    },
                )
                return openrouter_tasks_seen
            time.sleep(POLL_SECONDS)
        fail(task_id, "tinyfish_poll_timeout")
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        fail(task_id, "relay_execution_failed")
    return openrouter_tasks_seen


if __name__ == "__main__":
    INBOX.mkdir(parents=True, exist_ok=True)
    openrouter_tasks_seen = 0
    for task_file in sorted(INBOX.glob("*.json")):
        try:
            openrouter_tasks_seen = process(task_file, openrouter_tasks_seen=openrouter_tasks_seen)
        except (OSError, ValueError, TypeError, TimeoutError):
            fail(task_file.stem, "relay_execution_failed")

