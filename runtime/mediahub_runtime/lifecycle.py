"""Deterministic lifecycle transition validator for P0-06."""

from enum import Enum

from .errors import InvalidStateTransition


class LifecycleState(str, Enum):
    PROVISIONING = "PROVISIONING"
    INITIALIZING = "INITIALIZING"
    SELF_TEST = "SELF_TEST"
    READY = "READY"
    DEGRADED = "DEGRADED"
    SAFE_MODE = "SAFE_MODE"
    RECOVERY = "RECOVERY"


_TRANSITIONS = {
    LifecycleState.PROVISIONING: {LifecycleState.INITIALIZING},
    LifecycleState.INITIALIZING: {LifecycleState.SELF_TEST},
    LifecycleState.SELF_TEST: {
        LifecycleState.READY,
        LifecycleState.DEGRADED,
        LifecycleState.SAFE_MODE,
    },
    LifecycleState.READY: {LifecycleState.DEGRADED, LifecycleState.SAFE_MODE},
    LifecycleState.DEGRADED: {LifecycleState.READY, LifecycleState.SAFE_MODE},
    LifecycleState.SAFE_MODE: {LifecycleState.RECOVERY},
    LifecycleState.RECOVERY: {LifecycleState.INITIALIZING},
}


class LifecycleStateMachine:
    """Isolated deterministic validator; never canonical state authority."""

    def __init__(self, initial=LifecycleState.PROVISIONING):
        self._state = LifecycleState(initial)

    @property
    def state(self):
        return self._state

    def transition(self, target):
        target = LifecycleState(target)
        allowed = _TRANSITIONS.get(self._state, set())
        if target not in allowed:
            raise InvalidStateTransition(
                "transition {} -> {} is not permitted".format(self._state.value, target.value)
            )
        self._state = target
        return self._state

    def enter_safe_mode(self):
        return self.transition(LifecycleState.SAFE_MODE)
