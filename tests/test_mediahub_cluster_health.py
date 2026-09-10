import pytest

from ops.mediahub_cluster_health import (
    HealthObservationDenied,
    LocalClusterHealth,
    NodeHealth,
    NodeHealthObservation,
)


def observation(node_id="node-a", health=NodeHealth.HEALTHY, source_sha="sha"):
    return NodeHealthObservation(node_id, health, source_sha)


def test_health_observation_requires_identity_and_provenance():
    health = LocalClusterHealth()
    with pytest.raises(HealthObservationDenied):
        health.observe(observation(node_id=""))
    with pytest.raises(HealthObservationDenied):
        health.observe(observation(source_sha=""))


def test_unknown_health_fails_closed():
    with pytest.raises(HealthObservationDenied):
        LocalClusterHealth().observe(observation(health=NodeHealth.UNKNOWN))


def test_healthy_observation_is_recorded():
    health = LocalClusterHealth()
    item = health.observe(observation())
    assert item.health is NodeHealth.HEALTHY
    assert health.get("node-a") == item


def test_degraded_and_failed_are_observations_not_authorization():
    health = LocalClusterHealth()
    health.observe(observation(health=NodeHealth.DEGRADED))
    assert not health.is_eligible_for_observation_only("node-a")
    health.observe(observation(health=NodeHealth.FAILED))
    assert not health.is_eligible_for_observation_only("node-a")


def test_healthy_is_only_observation_eligibility_signal():
    health = LocalClusterHealth()
    health.observe(observation())
    assert health.is_eligible_for_observation_only("node-a")


def test_unknown_node_has_no_health_evidence():
    assert LocalClusterHealth().get("unknown") is None


def test_health_does_not_expose_membership_or_authority():
    health = LocalClusterHealth()
    assert not hasattr(health, "membership")
    assert not hasattr(health, "state_authority")
