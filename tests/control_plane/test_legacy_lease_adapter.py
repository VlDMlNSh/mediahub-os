from pathlib import Path
from ops.ai.task_lease import TaskLease
from runtime.mediahub_control_plane.legacy_lease_adapter import LegacyLeaseAdapter

def test_legacy_lease_maps_without_bypassing_control_plane(tmp_path: Path):
    lease = TaskLease(tmp_path / "lease.json", "task-1", "agent-1")
    lease.path.write_text('{"task_id":"task-1","worker_id":"agent-1","created_at":100,"expires_at":200}', encoding="utf-8")
    mapped = LegacyLeaseAdapter(lease).to_model(3)
    assert mapped.task_id == "task-1"
    assert mapped.agent_id == "agent-1"
    assert mapped.generation == 3
