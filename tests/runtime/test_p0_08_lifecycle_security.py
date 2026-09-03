import ast
from pathlib import Path

from mediahub_runtime.plugin_lifecycle import PluginState


RUNTIME = Path(__file__).parents[2] / "runtime" / "mediahub_runtime"


def test_lifecycle_source_has_no_privileged_runtime_bindings():
    source = (RUNTIME / "plugin_lifecycle.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    assert not {"subprocess", "socket", "os", "pathlib"} & (imported_modules | imported_from)

    privileged_names = {
        "StateAuthority",
        "Persistence",
        "Credential",
        "credential",
        "grant",
        "authorize",
        "authorize_capability",
    }
    runtime_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
    }
    assert not privileged_names & runtime_names


def test_running_is_not_an_authorization_state():
    assert PluginState.RUNNING.value == "running"
    assert PluginState.ENABLED.value == "enabled"
    assert PluginState.RUNNING != PluginState.ENABLED
