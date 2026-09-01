"""Deterministic appliance lifecycle state machine."""

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
    LifecycleState.INITIALIZING: {LifecycleState.SELF_TEST, LifecycleState.SAFE_MODE},
    LifecycleState.SELF_TEST: {LifecycleState.READY, LifecycleState.SAFE_MODE},
    LifecycleState.READY: {LifecycleState.DEGRADED, LifecycleState.SAFE_MODE, LifecycleState.RECOVERY},
    LifecycleState.DEGRADED: {LifecycleState.READY, LifecycleState.SAFE_MODE, LifecycleState.RECOVERY},
    LifecycleState.SAFE_MODE: {LifecycleState.RECOVERY},
    LifecycleState.RECOVERY: {LifecycleState.SELF_TEST, LifecycleState.SAFE_MODE},
}


class LifecycleStateMachine:
    """State machine that permits only explicit fail-closed transitions."""

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
        if self._state == LifecycleState.SAFE_MODE:
            return self._state
        if LifecycleState.SAFE_MODE not in _TRANSITIONS.get(self._state, set()):
            raise InvalidStateTransition(
                "cannot enter SAFE_MODE from {}".format(self._state.value)
            )
        self._state = LifecycleState.SAFE_MODE
        return self._state
