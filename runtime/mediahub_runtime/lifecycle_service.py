"""P0-06 lifecycle service boundary."""

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
    """Coordinates lifecycle operations without owning canonical state."""

    def __init__(self, consumer_boundary, state_machine=None):
        if not isinstance(consumer_boundary, ConsumerBoundary):
            raise TypeError("consumer_boundary_required")
        self._consumer = consumer_boundary
        self._machine = state_machine or LifecycleStateMachine()
        if not isinstance(self._machine, LifecycleStateMachine):
            raise TypeError("lifecycle_machine_required")

    @staticmethod
    def request(target, context):
        if not isinstance(context, AuthorizationContext):
            raise ConsumerBoundaryError("authorization_denied")
        try:
            target = LifecycleState(target)
        except (TypeError, ValueError) as exc:
            raise ConsumerBoundaryError("invalid_request") from exc
        return LifecycleRequest(target, context)

    def validate_transition(self, request, current):
        """Validate a transition without changing any state."""
        if not isinstance(request, LifecycleRequest):
            raise ConsumerBoundaryError("invalid_request")
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
        """Fail closed until authoritative lifecycle-state storage is defined."""
        if not isinstance(request, LifecycleRequest):
            raise ConsumerBoundaryError("invalid_request")
        raise ConsumerBoundaryError("operation_rejected")

    def enter_safe_mode(self, context):
        return self.transition(self.request(LifecycleState.SAFE_MODE, context))
