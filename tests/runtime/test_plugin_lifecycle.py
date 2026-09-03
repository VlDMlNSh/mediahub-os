import pytest

from mediahub_runtime.plugin_lifecycle import PluginLifecycle, PluginLifecycleError, PluginState


def test_lifecycle_follows_explicit_happy_path():
    lifecycle = PluginLifecycle()
    for state in (
        PluginState.VALIDATED,
        PluginState.REGISTERED,
        PluginState.ENABLED,
        PluginState.RUNNING,
        PluginState.STOPPING,
        PluginState.STOPPED,
        PluginState.DISABLED,
    ):
        assert lifecycle.transition(state) is state


def test_lifecycle_rejects_invalid_transition():
    lifecycle = PluginLifecycle()
    with pytest.raises(PluginLifecycleError):
        lifecycle.transition(PluginState.RUNNING)


def test_stopping_blocks_new_state_changing_requests():
    lifecycle = PluginLifecycle(PluginState.RUNNING)
    lifecycle.transition(PluginState.STOPPING)
    assert not lifecycle.accepts_new_state_changing_requests()


def test_lifecycle_does_not_expose_authority_or_grants():
    lifecycle = PluginLifecycle(PluginState.ENABLED)
    assert not hasattr(lifecycle, "grant")
    assert not hasattr(lifecycle, "authorize")
    assert not hasattr(lifecycle, "state_authority")
    assert lifecycle.accepts_new_state_changing_requests()
