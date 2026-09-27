import pytest
from runtime.mediahub_control_plane.model import Task
from runtime.mediahub_control_plane.dependencies import dependencies_satisfied, validate_dependency_graph, idempotency_identity

def test_dependencies_satisfied():
    assert dependencies_satisfied(Task("b", "x", dependencies=("a",)), {"a"})

def test_missing_dependency_rejected():
    with pytest.raises(ValueError):
        validate_dependency_graph([Task("a", "x", dependencies=("missing",))])

def test_cycle_rejected():
    with pytest.raises(ValueError):
        validate_dependency_graph([Task("a", "x", dependencies=("b",)), Task("b", "x", dependencies=("a",))])

def test_idempotency_identity():
    assert idempotency_identity(Task("t", "x", idempotency_key="k")) == "k"
