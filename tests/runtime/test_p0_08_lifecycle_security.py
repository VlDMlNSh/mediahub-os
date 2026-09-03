from pathlib import Path

from mediahub_runtime.plugin_lifecycle import PluginState


RUNTIME = Path(__file__).parents[2] / "runtime" / "mediahub_runtime"


def test_lifecycle_source_has_no_privileged_runtime_bindings():
    source = (RUNTIME / "plugin_lifecycle.py").read_text(encoding="utf-8")
    forbidden = (
        "StateAuthority",
        "Persistence",
        "subprocess",
        "socket",
        "credential",
        "grant",
        "authorize",
    )
    assert not any(term in source for term in forbidden)


def test_running_is_not_an_authorization_state():
    assert PluginState.RUNNING.value == "running"
    assert PluginState.ENABLED.value == "enabled"
    assert PluginState.RUNNING != PluginState.ENABLED
