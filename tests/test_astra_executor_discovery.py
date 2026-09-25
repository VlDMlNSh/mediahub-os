from pathlib import Path
import json
import os
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
import ops.astra_executor_discovery as d

def test_inventory_is_fail_closed_and_secret_free(monkeypatch, tmp_path):
    monkeypatch.setattr(d, "ROOT", tmp_path)
    monkeypatch.setattr(d, "STATE", tmp_path / ".autonomous")
    monkeypatch.setattr(d, "STATUS", tmp_path / ".autonomous" / "executor_capabilities.json")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "SECRET-VALUE")
    monkeypatch.setattr(d.shutil, "which", lambda _: None)
    payload = d.discover()
    text = d.STATUS.read_text()
    assert "SECRET-VALUE" not in text
    assert payload["policy"].startswith("fail-closed")
    assert all(x["qualification"] == "UNQUALIFIED" for x in payload["executors"])

def test_known_executor_is_qualified_only_after_version_probe(monkeypatch, tmp_path):
    monkeypatch.setattr(d, "ROOT", tmp_path)
    monkeypatch.setattr(d, "STATE", tmp_path / ".autonomous")
    monkeypatch.setattr(d, "STATUS", tmp_path / ".autonomous" / "executor_capabilities.json")
    monkeypatch.setattr(d.shutil, "which", lambda name: "/usr/local/bin/goose" if name == "goose" else None)
    class Result:
        returncode = 0
        stdout = "goose 1.2.3\n"
        stderr = ""
    monkeypatch.setattr(d.subprocess, "run", lambda *a, **k: Result())
    payload = d.discover()
    goose = next(x for x in payload["executors"] if x["name"] == "goose")
    assert goose["status"] == "HEALTHY"
    assert goose["qualification"] == "QUALIFIED"
    assert goose["version"] == "goose 1.2.3"

def test_probe_uses_fixed_command_not_user_input(monkeypatch):
    spec = d.ExecutorSpec("x", "goose", ("code_generation",), (), ("--version",))
    monkeypatch.setattr(d.shutil, "which", lambda _: "/bin/goose")
    seen = {}
    class Result:
        returncode = 0
        stdout = "ok"
        stderr = ""
    def fake_run(argv, **kwargs):
        seen["argv"] = argv
        return Result()
    monkeypatch.setattr(d.subprocess, "run", fake_run)
    d._probe(spec)
    assert seen["argv"] == ["/bin/goose", "--version"]
