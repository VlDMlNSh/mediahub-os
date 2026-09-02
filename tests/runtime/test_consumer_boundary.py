import pytest

from mediahub_runtime.authorization import AuthorizationContext, AuthorizationPolicy
from mediahub_runtime.consumer_boundary import ConsumerBoundary, ConsumerBoundaryError
from mediahub_runtime.generation import Generation
from mediahub_runtime.in_memory_state import InMemoryStateAuthority
from mediahub_runtime.proposals import Proposal
from datetime import datetime, timedelta, timezone


def make_boundary():
    grants = set()
    for operation in ("begin", "commit", "abort", "snapshot", "restore"):
        grants.add(("runtime", "state", operation))
    authority = InMemoryStateAuthority(
        Generation("g1", "bin1", "schema1", "0", "integrity1"),
        {"value": 1},
        authorization_policy=AuthorizationPolicy(grants),
    )
    return ConsumerBoundary(authority)


def request(boundary, operation):
    return boundary.request(operation, AuthorizationContext("runtime", "state"))


def test_read_is_immutable_and_consistent():
    boundary = make_boundary()
    state = boundary.read()
    assert state.payload["value"] == 1
    with pytest.raises(TypeError):
        state.payload["value"] = 2


def test_transaction_isolated_until_commit():
    boundary = make_boundary()
    tx = boundary.begin(request(boundary, "begin"), {"value": 2})
    assert boundary.read().payload["value"] == 1
    boundary.commit(request(boundary, "commit"), tx)
    assert boundary.read().payload["value"] == 2


def test_caller_payload_is_copied_at_update():
    boundary = make_boundary()
    payload = {"value": 2}
    tx = boundary.begin(request(boundary, "begin"))
    boundary.update(tx, payload)
    payload["value"] = 99
    boundary.commit(request(boundary, "commit"), tx)
    assert boundary.read().payload["value"] == 2


def test_operation_context_mismatch_is_rejected():
    boundary = make_boundary()
    with pytest.raises(ConsumerBoundaryError) as exc:
        boundary.begin(request(boundary, "commit"), {"value": 2})
    assert exc.value.code == "invalid_request"


def test_unauthorized_consumer_is_sanitized():
    boundary = make_boundary()
    denied = boundary.request("begin", AuthorizationContext("ui", "state"))
    with pytest.raises(ConsumerBoundaryError) as exc:
        boundary.begin(denied, {"value": 2})
    assert exc.value.code == "authorization_denied"


def test_stale_transaction_fails_closed():
    boundary = make_boundary()
    tx1 = boundary.begin(request(boundary, "begin"), {"value": 2})
    tx2 = boundary.begin(request(boundary, "begin"), {"value": 3})
    boundary.commit(request(boundary, "commit"), tx1)
    with pytest.raises(ConsumerBoundaryError) as exc:
        boundary.commit(request(boundary, "commit"), tx2)
    assert exc.value.code == "stale_transaction"
    assert boundary.read().payload["value"] == 2


def test_snapshot_and_restore_require_explicit_boundary_operations():
    boundary = make_boundary()
    snapshot = boundary.snapshot(request(boundary, "snapshot"))
    tx = boundary.begin(request(boundary, "begin"), {"value": 2})
    boundary.commit(request(boundary, "commit"), tx)
    boundary.restore(request(boundary, "restore"), snapshot)
    assert boundary.read().payload["value"] == 1


def test_ai_proposal_validation_has_no_mutation_path():
    boundary = make_boundary()
    proposal = Proposal(
        "p1", "set", "value", 0.9, "g1", datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    validated = boundary.validate_proposal(proposal)
    assert validated == proposal
    assert boundary.read().payload["value"] == 1
    assert not hasattr(boundary, "execute_proposal")


def test_consumer_transaction_does_not_expose_authority_api():
    boundary = make_boundary()
    tx = boundary.begin(request(boundary, "begin"))
    assert not hasattr(tx, "commit")
    assert not hasattr(tx, "restore")
