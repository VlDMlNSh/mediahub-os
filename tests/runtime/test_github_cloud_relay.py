import importlib.util
import json


def load_relay():
    spec = importlib.util.spec_from_file_location(
        "github_cloud_relay",
        "/home/mediahub/mediahub-os/tools/github_cloud_relay.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def contract():
    return {
        "schema_id": "mediahub.astra.github-cloud-task",
        "schema_version": "1.0.0",
        "owner": "mediahub-ai",
        "task_id": "task-1",
        "request_id": "req-1",
        "session_id": "session-1",
        "operation": "tinyfish.web.run",
        "approval_state": "not_required",
        "url": "https://example.com",
        "goal": "Extract the page title as JSON",
    }


def test_relay_is_free_by_default(tmp_path, monkeypatch):
    relay = load_relay()
    path = tmp_path / "task-1.json"
    path.write_text(json.dumps(contract()), encoding="utf-8")
    monkeypatch.delenv("MEDIAHUB_ALLOW_METERED_TINYFISH", raising=False)
    monkeypatch.setenv("TINYFISH_API_KEY", "test-only")
    monkeypatch.setattr(relay, "DONE", tmp_path / "done")

    relay.process(path)

    result = json.loads((tmp_path / "done" / "task-1.result.json").read_text())
    assert result["error"] == "metered_tinyfish_disabled"


def test_relay_requires_github_secret_after_opt_in(tmp_path, monkeypatch):
    relay = load_relay()
    path = tmp_path / "task-1.json"
    path.write_text(json.dumps(contract()), encoding="utf-8")
    monkeypatch.setenv("MEDIAHUB_ALLOW_METERED_TINYFISH", "true")
    monkeypatch.setenv("TINYFISH_API_KEY", "")
    monkeypatch.setattr(relay, "DONE", tmp_path / "done")

    relay.process(path)

    result = json.loads((tmp_path / "done" / "task-1.result.json").read_text())
    assert result["error"] == "tinyfish_not_configured_in_github"


def test_relay_polls_and_stores_goal_result(tmp_path, monkeypatch):
    relay = load_relay()
    path = tmp_path / "task-1.json"
    path.write_text(json.dumps(contract()), encoding="utf-8")
    monkeypatch.setenv("MEDIAHUB_ALLOW_METERED_TINYFISH", "true")
    monkeypatch.setenv("TINYFISH_API_KEY", "test-only")
    monkeypatch.setattr(relay, "DONE", tmp_path / "done")
    responses = iter([
        {"run_id": "run-1"},
        {"run_id": "run-1", "status": "COMPLETED", "result": {"title": "Example Domain"}},
    ])
    monkeypatch.setattr(relay, "request_json", lambda request: next(responses))
    monkeypatch.setattr(relay.time, "sleep", lambda _: None)

    relay.process(path)

    result = json.loads((tmp_path / "done" / "task-1.result.json").read_text())
    assert result["status"] == "completed"
    assert result["run_id"] == "run-1"
    assert result["result"]["title"] == "Example Domain"


def test_openrouter_relay_uses_github_secret_only(tmp_path, monkeypatch):
    relay = load_relay()
    task = contract() | {"task_id": "or-1", "operation": "openrouter.infer", "prompt": "hello", "model": "openai/gpt-5.2"}
    task.pop("url", None)
    task.pop("goal", None)
    path = tmp_path / "or-1.json"
    path.write_text(json.dumps(task), encoding="utf-8")
    monkeypatch.setenv("OPENROUTER_API_KEY", "github-secret-test")
    monkeypatch.setenv("MEDIAHUB_ALLOW_METERED_OPENROUTER", "true")
    monkeypatch.setattr(relay, "DONE", tmp_path / "done")
    captured = {}
    def fake_request(request):
        captured["auth"] = request.headers.get("Authorization")
        captured["body"] = request.data.decode()
        return {"id": "gen-1", "model": "openai/gpt-5.2", "choices": [{"message": {"content": "OK"}}], "usage": {"total_tokens": 3}}
    monkeypatch.setattr(relay, "request_json", fake_request)
    relay.process(path)
    result = json.loads((tmp_path / "done" / "or-1.result.json").read_text())
    assert result["provider_id"] == "openrouter"
    assert result["output"] == "OK"
    assert "github-secret-test" not in json.dumps(result)
    assert captured["auth"] == "Bearer github-secret-test"
