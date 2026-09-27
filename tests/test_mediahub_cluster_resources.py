import pytest

from ops.mediahub_cluster_resources import (
    ClusterResourceLedger,
    ResourceCapacity,
    ResourceDenied,
    ResourceReservation,
)


def reservation(workload="w1", node="node-a", cpu=2, memory=2048, gpu=0):
    return ResourceReservation(workload, node, ResourceCapacity(cpu, memory, gpu))


def ledger():
    return ClusterResourceLedger({"node-a": ResourceCapacity(8, 8192, 1)})


def test_reservation_is_admitted_within_capacity():
    item = ledger().reserve(reservation())
    assert item.workload_id == "w1"


def test_cpu_overcommit_is_denied():
    l = ledger()
    l.reserve(reservation(cpu=6))
    with pytest.raises(ResourceDenied):
        l.reserve(reservation("w2", cpu=3))


def test_memory_overcommit_is_denied():
    l = ledger()
    l.reserve(reservation(memory=7000))
    with pytest.raises(ResourceDenied):
        l.reserve(reservation("w2", memory=2000))


def test_gpu_overcommit_is_denied():
    l = ledger()
    l.reserve(reservation(gpu=1))
    with pytest.raises(ResourceDenied):
        l.reserve(reservation("w2", gpu=1))


def test_duplicate_workload_is_denied():
    l = ledger()
    l.reserve(reservation())
    with pytest.raises(ResourceDenied):
        l.reserve(reservation())


def test_unknown_node_is_denied():
    with pytest.raises(ResourceDenied):
        ledger().reserve(reservation(node="unknown"))


def test_invalid_resource_values_are_denied():
    with pytest.raises(ResourceDenied):
        ledger().reserve(reservation(cpu=0))
    with pytest.raises(ResourceDenied):
        ledger().reserve(reservation(memory=0))
    with pytest.raises(ResourceDenied):
        ledger().reserve(reservation(gpu=-1))


def test_release_frees_capacity_deterministically():
    l = ledger()
    l.reserve(reservation(cpu=6))
    l.release("w1")
    assert l.reserved("w1") is None
    l.reserve(reservation("w2", cpu=8))
    assert l.reserved("w2") is not None


def test_release_unknown_workload_fails_closed():
    with pytest.raises(ResourceDenied):
        ledger().release("unknown")


def test_reservation_does_not_expose_authority_or_network():
    l = ledger()
    assert not hasattr(l, "state_authority")
    assert not hasattr(l, "network")


def test_replace_moves_reservation_atomically():
    l = ledger()
    l.reserve(reservation(cpu=6))
    replaced = l.replace(reservation(node="node-a", cpu=8))
    assert replaced.capacity.cpu == 8
    assert l.reserved("w1").node_id == "node-a"


def test_can_replace_does_not_mutate_ledger():
    l = ledger()
    l.reserve(reservation(cpu=6))
    candidate = reservation(node="node-a", cpu=8)
    assert l.can_replace(candidate)
    assert l.reserved("w1").capacity.cpu == 6
