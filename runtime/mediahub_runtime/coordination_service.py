"""P0-06 runtime coordination service over approved service requests."""

from dataclasses import dataclass

from .consumer_boundary import ConsumerBoundaryError
from .lifecycle_service import LifecycleRequest, LifecycleService


class CoordinationServiceError(RuntimeError):
    """Stable, sanitized error exposed by the coordination service."""

    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class CoordinationRequest:
    """Explicit inert request for one approved runtime operation."""

    operation: str
    request: object


@dataclass(frozen=True)
class CoordinationResult:
    """Value-semantic result of one coordinated runtime operation."""

    operation: str
    result: object


class RuntimeCoordinationService:
    """Sequence approved runtime operations without owning canonical state."""

    OPERATION_LIFECYCLE_TRANSITION = "lifecycle.transition"

    def __init__(self, lifecycle_service):
        if not isinstance(lifecycle_service, LifecycleService):
            raise TypeError("lifecycle_service_required")
        self._lifecycle = lifecycle_service

    @classmethod
    def request(cls, operation, request):
        if operation != cls.OPERATION_LIFECYCLE_TRANSITION:
            raise CoordinationServiceError("invalid_request")
        if not isinstance(request, LifecycleRequest):
            raise CoordinationServiceError("invalid_request")
        return CoordinationRequest(operation, request)

    def coordinate(self, request):
        if not isinstance(request, CoordinationRequest):
            raise CoordinationServiceError("invalid_request")
        if request.operation != self.OPERATION_LIFECYCLE_TRANSITION:
            raise CoordinationServiceError("invalid_request")

        try:
            result = self._lifecycle.transition(request.request)
            return CoordinationResult(request.operation, result)
        except ConsumerBoundaryError as exc:
            raise CoordinationServiceError(exc.code) from exc
        except Exception as exc:
            raise CoordinationServiceError("operation_rejected") from exc

    def coordinate_sequence(self, requests):
        """Run an explicit bounded sequence; stop immediately on failure."""
        if type(requests) is not tuple:
            raise CoordinationServiceError("invalid_request")
        if len(requests) > 16:
            raise CoordinationServiceError("operation_rejected")

        results = []
        for request in requests:
            results.append(self.coordinate(request))
        return tuple(results)
