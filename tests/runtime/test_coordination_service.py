import pytest

from mediahub_runtime import (
    AuthorizationContext,
    AuthorizationPolicy,
    ConsumerBoundary,
    Generation,
    InMemoryStateAuthority,
    LifecycleRequest,
    LifecycleService,
    LifecycleState,
    RuntimeCoordinationService,
)
from mediahub_runtime.coordination_service import (
    CoordinationRequest,
    CoordinationResult,
    CoordinationServiceError,
)


def make_services():
    capability = LifecycleService.CAPABILITY
    policy = AuthorizationPolicy(
        {
            ("runtime", capability, "begin"),
            ("runtime", capability, "commit"),
            ("runtime", capability, "abort"),
        }
    )
    authority = InMemoryStateAuthority(
        Generation("g1", "bin1", "schema1", "0", "integrity1"),
        {"lifecycle": {"state": LifecycleState.PROVISIONING.value}},
        authorization_policy=policy,
    )
    boundary = ConsumerBoundary(authority)
    lifecycle = LifecycleService(boundary)
    return authority, lifecycle, RuntimeCoordinationService(lifecycle)


def make_request(lifecycle, target=LifecycleState.INITIALIZING):
    context = AuthorizationContext("runtime", LifecycleService.CAPABILITY)
    return lifecycle.request(target, context)


def test_coordinate_delegates_only_approved_lifecycle_operation():
    authority, lifecycle, coordinator = make_services()
    request = coordinator.request(
        RuntimeCoordinationService.OPERATION_LIFECYCLE_TRANSITION,
        make_request(lifecycle),
    )

    result = coordinator.coordinate(request)

    assert isinstance(result, CoordinationResult)
    assert result.operation == "lifecycle.transition"
    assert result.result.payload["lifecycle"]["state"] == LifecycleState.INITIALIZING.value
    assert authority.read().payload["lifecycle"]["state"] == LifecycleState.INITIALIZING.value


def test_unknown_operation_is_rejected_before_execution():
    _, lifecycle, coordinator = make_services()

    with pytest.raises(CoordinationServiceError) as exc:
        coordinator.request("arbitrary.operation", make_request(lifecycle))

    assert exc.value.code == "invalid_request"


def test_non_lifecycle_request_is_rejected():
    _, _, coordinator = make_services()

    with pytest.raises(CoordinationServiceError) as exc:
        coordinator.request(
            RuntimeCoordinationService.OPERATION_LIFECYCLE_TRANSITION,
            object(),
        )

    assert exc.value.code == "invalid_request"


def test_sequence_requires_explicit_tuple_and_stops_on_failure():
    authority, lifecycle, coordinator = make_services()
    first = coordinator.request(
        RuntimeCoordinationService.OPERATION_LIFECYCLE_TRANSITION,
        make_request(lifecycle, LifecycleState.INITIALIZING),
    )
    second = coordinator.request(
        RuntimeCoordinationService.OPERATION_LIFECYCLE_TRANSITION,
        make_request(lifecycle, LifecycleState.PROVISIONING),
    )

    with pytest.raises(CoordinationServiceError) as exc:
        coordinator.coordinate_sequence((first, second))

    assert exc.value.code == "operation_rejected"
    assert authority.read().payload["lifecycle"]["state"] == LifecycleState.INITIALIZING.value


def test_sequence_rejects_unbounded_or_mutable_input():
    _, lifecycle, coordinator = make_services()
    request = coordinator.request(
        RuntimeCoordinationService.OPERATION_LIFECYCLE_TRANSITION,
        make_request(lifecycle),
    )

    with pytest.raises(CoordinationServiceError):
        coordinator.coordinate_sequence([request])
    with pytest.raises(CoordinationServiceError):
        coordinator.coordinate_sequence(tuple([request] * 17))


def test_coordination_does_not_expose_consumer_or_authority_handles():
    _, lifecycle, coordinator = make_services()
    request = coordinator.request(
        RuntimeCoordinationService.OPERATION_LIFECYCLE_TRANSITION,
        make_request(lifecycle),
    )

    assert isinstance(request, CoordinationRequest)
    assert not hasattr(coordinator, "_authority")
    assert not hasattr(coordinator, "execute")
    assert not hasattr(coordinator, "run_command")
    assert not hasattr(request, "transaction")


def test_failed_lifecycle_operation_is_sanitized_and_state_remains_canonical():
    authority, lifecycle, coordinator = make_services()
    bad_context = AuthorizationContext("runtime", "runtime.other")
    lifecycle_request = LifecycleRequest(LifecycleState.INITIALIZING, bad_context)
    request = coordinator.request(
        RuntimeCoordinationService.OPERATION_LIFECYCLE_TRANSITION,
        lifecycle_request,
    )

    with pytest.raises(CoordinationServiceError) as exc:
        coordinator.coordinate(request)

    assert exc.value.code == "authorization_denied"
    assert authority.read().payload["lifecycle"]["state"] == LifecycleState.PROVISIONING.value


def test_no_direct_consumer_boundary_or_state_authority_import_path():
    import inspect
    import mediahub_runtime.coordination_service as module

    source = inspect.getsource(module)
    assert "InMemoryStateAuthority" not in source
    assert "StateAuthority" not in source
    assert "subprocess" not in source
    assert "socket" not in source
