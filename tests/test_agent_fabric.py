from pathlib import Path
import pytest
from mediahub_runtime.agent_fabric import AgentClaim, AgentFabricError, ClaimStore

def mk(task_id, paths, now=100.0):
    return AgentClaim("builder", task_id, "test", tuple(paths), (), (), "ACTIVE", now, now, now + 900, "base")

def test_exact_collision(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("mediahub_runtime.agent_fabric.time.time", lambda: 100.0)
    s=ClaimStore(tmp_path); s.acquire(mk("A", ["src/a.py"]))
    with pytest.raises(AgentFabricError, match="claim_collision"):
        s.acquire(mk("B", ["src/a.py"]))

def test_parent_child_collision(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("mediahub_runtime.agent_fabric.time.time", lambda: 100.0)
    s=ClaimStore(tmp_path); s.acquire(mk("A", ["src"]))
    with pytest.raises(AgentFabricError, match="claim_collision"):
        s.acquire(mk("B", ["src/a.py"]))

def test_heartbeat(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("mediahub_runtime.agent_fabric.time.time", lambda: 100.0)
    s=ClaimStore(tmp_path); s.acquire(mk("A", ["src/a.py"]))
    c=s.heartbeat("A", now=200.0, lease_seconds=300)
    assert (c.status, c.expiry) == ("ACTIVE", 500.0)

def test_release(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("mediahub_runtime.agent_fabric.time.time", lambda: 100.0)
    s=ClaimStore(tmp_path); s.acquire(mk("A", ["src/a.py"])); s.release("A")
    assert s.list_claims()[0].status == "CLOSED"


def test_lease_expiry_allows_reacquire(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("mediahub_runtime.agent_fabric.time.time", lambda: 100.0)
    s=ClaimStore(tmp_path)
    s.acquire(mk("A", ["src/a.py"], now=100.0))
    monkeypatch.setattr("mediahub_runtime.agent_fabric.time.time", lambda: 1000.0)
    s.acquire(mk("B", ["src/a.py"], now=1000.0))
    claims={c.task_id:c for c in s.list_claims()}
    assert claims["A"].status == "EXPIRED"
    assert claims["B"].status == "ACTIVE"
