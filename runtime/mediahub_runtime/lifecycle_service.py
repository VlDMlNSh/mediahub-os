"""P0-06 lifecycle service over the frozen consumer boundary."""

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
    """Coordinates lifecycle transitions without becoming a state authority."""

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

    @property
    def state(self):
        return self._machine.state

    def transition(self, request):
        """Validate lifecycle intent; publication remains explicitly gated.

        The lifecycle state machine is consulted for transition validity only.
        Actual lifecycle-state publication is intentionally not implemented
        until the P0-06 contract defines its authoritative state mapping.
        """
        if not isinstance(request, LifecycleRequest):
            raise ConsumerBoundaryError("invalid_request")
        try:
            target = LifecycleState(request.target)
        except (TypeError, ValueError) as exc:
            raise ConsumerBoundaryError("invalid_request") from exc
        current = self._machine.state
        if target == current:
            raise ConsumerBoundaryError("operation_rejected")
        raise ConsumerBoundaryError("operation_rejected")

    def enter_safe_mode(self, context):
        return self.transition(self.request(LifecycleState.SAFE_MODE, context))
