from datetime import datetime, timedelta, timezone

import pytest

from runtime.mediahub_control_plane.agent_registry import AgentRegistry, Heartbeat
from runtime.mediahub_control_plane.model import Agent, AgentStatus


def t(): return datetime(2026, 9, 25, tzinfo=timezone.utc)

def agent(): return Agent(agent_id="a1", node_id="n1", version="1", capabilities=("linux",))


def test_register_is_stable_and_reconnects_same_identity():
    r = AgentRegistry(30, 90)
    assert r.register(agent(), t()).status == AgentStatus.ONLINE
    r.heartbeat(Heartbeat("a1", "n1", t(), version="2", capabilities=("linux", "git")))
    assert r.get("a1").status == AgentStatus.IDLE
    assert r.get("a1").version == "2"


def test_identity_cannot_move_between_nodes():
    r = AgentRegistry(30, 90)
    r.register(agent(), t())
    with pytest.raises(ValueError): r.register(Agent("a1", "n2", "1"), t())
    with pytest.raises(ValueError): r.heartbeat(Heartbeat("a1", "n2", t()))


def test_reconcile_uses_degraded_then_offline_thresholds():
    r = AgentRegistry(30, 90)
    r.register(agent(), t())
    r.heartbeat(Heartbeat("a1", "n1", t()))
    assert r.reconcile(t() + timedelta(seconds=31))["a1"] == AgentStatus.DEGRADED
    assert r.reconcile(t() + timedelta(seconds=91))["a1"] == AgentStatus.OFFLINE


def test_unhealthy_heartbeat_degrades_agent():
    r = AgentRegistry(30, 90)
    r.register(agent(), t())
    assert r.heartbeat(Heartbeat("a1", "n1", t(), health="degraded")).status == AgentStatus.DEGRADED


def test_repeated_failures_quarantine_agent_until_success():
    r = AgentRegistry(30, 90, failure_quarantine_threshold=2)
    r.register(agent(), t())
    r.heartbeat(Heartbeat("a1", "n1", t()))
    assert r.record_failure("a1").status == AgentStatus.IDLE
    assert r.record_failure("a1").status == AgentStatus.DEGRADED
    assert r.failure_count("a1") == 2
    assert r.record_success("a1").status == AgentStatus.IDLE
    assert r.failure_count("a1") == 0


def test_quarantine_threshold_must_be_positive():
    with pytest.raises(ValueError): AgentRegistry(30, 90, failure_quarantine_threshold=0)
