"""P0-08 explicit plugin lifecycle state machine.

Lifecycle state is descriptive only. It never grants capability, authorization,
State Authority access, persistence, execution, network, or credential access.
"""

from __future__ import annotations

from enum import Enum


class PluginLifecycleError(ValueError):
    """Raised when a lifecycle transition is invalid."""


class PluginState(str, Enum):
    DISCOVERED = "discovered"
    VALIDATED = "validated"
    REGISTERED = "registered"
    ENABLED = "enabled"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    REJECTED = "rejected"
    FAILED = "failed"
    DISABLED = "disabled"


_ALLOWED_TRANSITIONS = {
    PluginState.DISCOVERED: frozenset({PluginState.VALIDATED, PluginState.REJECTED}),
    PluginState.VALIDATED: frozenset({PluginState.REGISTERED, PluginState.REJECTED}),
    PluginState.REGISTERED: frozenset({PluginState.ENABLED, PluginState.DISABLED}),
    PluginState.ENABLED: frozenset({PluginState.RUNNING, PluginState.DISABLED}),
    PluginState.RUNNING: frozenset({PluginState.STOPPING, PluginState.FAILED, PluginState.DISABLED}),
    PluginState.STOPPING: frozenset({PluginState.STOPPED, PluginState.FAILED}),
    PluginState.STOPPED: frozenset({PluginState.DISABLED}),
    PluginState.REJECTED: frozenset(),
    PluginState.FAILED: frozenset({PluginState.DISABLED}),
    PluginState.DISABLED: frozenset(),
}


class PluginLifecycle:
    """Finite-state lifecycle manager with no implicit privilege transitions."""

    def __init__(self, initial: PluginState = PluginState.DISCOVERED) -> None:
        if type(initial) is not PluginState:
            raise PluginLifecycleError("invalid initial state")
        self._state = initial

    @property
    def state(self) -> PluginState:
        return self._state

    def can_transition(self, target: PluginState) -> bool:
        return type(target) is PluginState and target in _ALLOWED_TRANSITIONS[self._state]

    def transition(self, target: PluginState) -> PluginState:
        if not self.can_transition(target):
            raise PluginLifecycleError("invalid lifecycle transition")
        self._state = target
        return self._state

    def accepts_new_state_changing_requests(self) -> bool:
        return self._state in {PluginState.ENABLED, PluginState.RUNNING}

    def is_terminal(self) -> bool:
        return self._state in {PluginState.REJECTED, PluginState.DISABLED}
