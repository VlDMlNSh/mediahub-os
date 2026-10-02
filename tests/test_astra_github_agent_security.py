import ast
import importlib.util
import os
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "astra_github_agent.py"


def load_agent(monkeypatch, **env):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    spec = importlib.util.spec_from_file_location("astra_github_agent_security", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_safe_env_drops_inherited_secrets(monkeypatch):
    monkeypatch.setenv("ASTRA_TEST_SECRET", "must-not-leak")
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-leak")
    agent = load_agent(monkeypatch, ASTRA_NODE_ID="mh-dev-02")
    env = agent._safe_env()
    assert "ASTRA_TEST_SECRET" not in env
    assert "OPENAI_API_KEY" not in env


def test_provider_credentials_are_opt_in(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "provider-secret")
    agent = load_agent(monkeypatch, ASTRA_NODE_ID="mh-dev-02")
    assert "OPENROUTER_API_KEY" not in agent._safe_env()
    assert agent._safe_env(include_provider_credentials=True)["OPENROUTER_API_KEY"] == "provider-secret"


def test_extra_environment_is_allowlisted(monkeypatch):
    agent = load_agent(monkeypatch, ASTRA_NODE_ID="mh-dev-02")
    env = agent._safe_env({
        "OPENAI_BASE_URL": "https://example.invalid",
        "ARBITRARY_SECRET": "must-not-leak",
    })
    assert env["OPENAI_BASE_URL"] == "https://example.invalid"
    assert "ARBITRARY_SECRET" not in env


def test_remote_must_be_canonical(monkeypatch):
    agent = load_agent(
        monkeypatch,
        ASTRA_GITHUB_REPO="VlDMlNSh/mediahub-os",
        ASTRA_GITHUB_REMOTE="https://evil.example/repo.git",
        ASTRA_NODE_ID="mh-dev-02",
    )
    try:
        agent._canonical_remote()
    except RuntimeError:
        pass
    else:
        raise AssertionError("non-canonical remote was accepted")


def test_canonical_node_branch_is_strict(monkeypatch):
    agent = load_agent(monkeypatch, ASTRA_NODE_ID="mh-dev-02")
    assert agent._canonical_node_branch() == "astra-node/mh-dev-02"
    monkeypatch.setenv("ASTRA_NODE_ID", "evil-node")
    agent.NODE_ID = "evil-node"
    try:
        agent._canonical_node_branch()
    except ValueError:
        pass
    else:
        raise AssertionError("non-canonical node id was accepted")


def test_no_direct_subprocess_calls_outside_wrapper():
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    direct_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "run" and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                direct_calls.append(node.lineno)
    assert direct_calls == [next(
        n.lineno for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and n.name == "run"
    ) + 1]


def test_publication_uses_force_with_lease():
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert '"push","--force-with-lease","origin",branch' in source
