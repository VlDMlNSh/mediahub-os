import pytest

from ops.mediahub_lifecycle_contract import (
    LifecycleState,
    MigrationContract,
    PersistenceContract,
    VersionIdentity,
    transition,
)


def v(n): return VersionIdentity("mediahub-state",n,f"digest-{n}")

def test_version_and_persistence_contract_are_bounded():
    assert PersistenceContract("state-authority",v(1)).durable is False

def test_invalid_authority_rejected():
    with pytest.raises(ValueError): PersistenceContract("other",v(1))

def test_migration_requires_revision_change():
    with pytest.raises(ValueError): MigrationContract("m1",v(1),v(1),True)

def test_lifecycle_is_monotonic_and_explicit():
    state=LifecycleState.ABSENT
    for target in (LifecycleState.CANDIDATE,LifecycleState.VALIDATED,LifecycleState.AUTHORIZED,LifecycleState.PUBLISHED,LifecycleState.APPLIED,LifecycleState.SUPERSEDED):
        state=transition(state,target)
    assert state is LifecycleState.SUPERSEDED

def test_invalid_transition_rejected():
    with pytest.raises(ValueError): transition(LifecycleState.CANDIDATE,LifecycleState.PUBLISHED)

def test_physical_durability_is_not_implied():
    c=PersistenceContract("state-authority",v(1),False)
    assert c.durable is False

def test_migration_rejects_malformed_types():
    valid = VersionIdentity("mediahub-state", 1, "digest-1")
    with pytest.raises(ValueError):
        MigrationContract("", valid, VersionIdentity("mediahub-state", 2, "digest-2"), True)
    with pytest.raises(TypeError):
        MigrationContract("m1", object(), valid, True)
    with pytest.raises(TypeError):
        MigrationContract("m1", valid, object(), True)
    with pytest.raises(TypeError):
        MigrationContract("m1", valid, VersionIdentity("mediahub-state", 2, "digest-2"), 1)

def test_migration_rejects_unchanged_revision():
    current = VersionIdentity("mediahub-state", 3, "digest-3")
    with pytest.raises(ValueError):
        MigrationContract("m1", current, current, True)
