"""P0-06 lifecycle service over the frozen P0-05 boundary."""

from collections.abc import Mapping
from dataclasses import dataclass

from .authorization import AuthorizationContext
from .consumer_boundary import ConsumerBoundary, ConsumerBoundaryError
from .lifecycle import LifecycleState, LifecycleStateMachine


@dataclass(frozen=True)
class LifecycleRequest:
    """Explicit, inert lifecycle intent."""

    target: LifecycleState
    context: AuthorizationContext


class LifecycleService:
    """Coordinates lifecycle transitions without owning canonical state."""

    CAPABILITY = "runtime.lifecycle.transition"

    def __init__(self, consumer_boundary, state_machine=None):
        if not isinstance(consumer_boundary, ConsumerBoundary):
            raise TypeError("consumer_boundary_required")
        self._consumer = consumer_boundary
        self._machine = state_machine or LifecycleStateMachine()
        if not isinstance(self._machine, LifecycleStateMachine):
            raise TypeError("lifecycle_machine_required")

    @classmethod
    def request(cls, target, context):
        if not isinstance(context, AuthorizationContext):
            raise ConsumerBoundaryError("authorization_denied")
        if context.capability != cls.CAPABILITY:
            raise ConsumerBoundaryError("authorization_denied")
        try:
            target = LifecycleState(target)
        except (TypeError, ValueError) as exc:
            raise ConsumerBoundaryError("invalid_request") from exc
        return LifecycleRequest(target, context)

    def validate_transition(self, request, current):
        """Validate a transition without changing canonical state."""
        if not isinstance(request, LifecycleRequest):
            raise ConsumerBoundaryError("invalid_request")
        if request.context.capability != self.CAPABILITY:
            raise ConsumerBoundaryError("authorization_denied")
        try:
            current = LifecycleState(current)
            target = LifecycleState(request.target)
            if current == target:
                raise ConsumerBoundaryError("invalid_request")
            validator = LifecycleStateMachine(initial=current)
            return validator.transition(target)
        except ConsumerBoundaryError:
            raise
        except Exception as exc:
            raise ConsumerBoundaryError("operation_rejected") from exc

    def transition(self, request):
        """Atomically publish one validated lifecycle transition through P0-05."""
        if not isinstance(request, LifecycleRequest):
            raise ConsumerBoundaryError("invalid_request")
        if request.context.capability != self.CAPABILITY:
            raise ConsumerBoundaryError("authorization_denied")

        before = self._consumer.read()
        current = self._read_lifecycle_state(before)
        target = self.validate_transition(request, current)

        operation = self._consumer.request("begin", request.context)
        tx = self._consumer.begin(operation)
        try:
            after_begin = self._consumer.read()
            if not self._same_revision(before, after_begin):
                self._consumer.abort(
                    self._consumer.request("abort", request.context), tx
                )
                raise ConsumerBoundaryError("stale_transaction")

            candidate = self._payload_copy(after_begin.payload)
            lifecycle = candidate.get("lifecycle")
            if not isinstance(lifecycle, dict):
                lifecycle = {}
                candidate["lifecycle"] = lifecycle
            lifecycle["state"] = target.value

            self._consumer.update(tx, candidate)
            return self._consumer.commit(
                self._consumer.request("commit", request.context), tx
            )
        except ConsumerBoundaryError:
            try:
                self._consumer.abort(
                    self._consumer.request("abort", request.context), tx
                )
            except ConsumerBoundaryError:
                pass
            raise
        except Exception as exc:
            try:
                self._consumer.abort(
                    self._consumer.request("abort", request.context), tx
                )
            except ConsumerBoundaryError:
                pass
            raise ConsumerBoundaryError("operation_rejected") from exc

    def enter_safe_mode(self, context):
        return self.transition(self.request(LifecycleState.SAFE_MODE, context))

    @staticmethod
    def _read_lifecycle_state(state):
        try:
            lifecycle = state.payload["lifecycle"]
            return LifecycleState(lifecycle["state"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ConsumerBoundaryError("operation_rejected") from exc

    @staticmethod
    def _same_revision(left, right):
        return (
            left.generation == right.generation
            and left.state_version == right.state_version
        )

    @classmethod
    def _payload_copy(cls, value):
        if isinstance(value, Mapping):
            return {key: cls._payload_copy(item) for key, item in value.items()}
        if isinstance(value, tuple):
            return [cls._payload_copy(item) for item in value]
        if isinstance(value, list):
            return [cls._payload_copy(item) for item in value]
        return value
