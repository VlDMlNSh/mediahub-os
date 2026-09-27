from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).parents[2] / "ops" / "ai" / "github_site_observer.py"


def load_module():
    spec = importlib.util.spec_from_file_location("github_site_observer", MODULE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_observer_defaults_to_read_only_github_control_plane(monkeypatch, tmp_path):
    monkeypatch.setenv("MEDIAHUB_ROOT", str(tmp_path))
    module = load_module()
    assert module.REPO == "VlDMlNSh/mediahub-os"
    assert module.BRANCH == "engineering/mh21-godmode-openrouter"
    assert module.REMOTE == tmp_path / ".autonomous" / "github_remote.json"


def test_observer_writes_remote_sha(monkeypatch, tmp_path):
    monkeypatch.setenv("MEDIAHUB_ROOT", str(tmp_path))
    module = load_module()
    monkeypatch.setattr(module, "fetch", lambda: {"repo": module.REPO, "branch": module.BRANCH, "sha": "abc", "updated_at": 1, "source": "github-api-readonly"})
    assert module.once() == 0
    assert '"sha": "abc"' in module.REMOTE.read_text(encoding="utf-8")


def test_observer_fails_closed_on_transport_error(monkeypatch, tmp_path):
    monkeypatch.setenv("MEDIAHUB_ROOT", str(tmp_path))
    module = load_module()
    monkeypatch.setattr(module, "fetch", lambda: (_ for _ in ()).throw(module.URLError("offline")))
    assert module.once() == 2
    assert '"state": "UNAVAILABLE"' in module.REMOTE.read_text(encoding="utf-8")
