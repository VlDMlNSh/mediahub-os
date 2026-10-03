from __future__ import annotations
from datetime import datetime, timezone
from .validators import validate_node, validate_capability, validate_heartbeat
from .state import transition_node_state, transition_replica_state

def run_checks() -> dict:
    now=datetime.now(timezone.utc)
    node={"schema_version":"mediahub.mesh.node.v1","node_id":"verification-node","role":"verification","status":"ACTIVE","capabilities":[],"executors":[],"artifact_transports":[],"resources":{"ram_gib":1,"disk_free_gib":1},"last_heartbeat":now.isoformat()}
    capability={"schema_version":"mediahub.mesh.capability.v1","capability_id":"verification","provider":"builtin","version":"1","executable":"/bin/true","identity_sha256":"a"*64,"authority":"NONE","qualification_state":"NOT_PROVEN","sandbox":"none"}
    heartbeat={"schema_version":"mediahub.mesh.heartbeat.v1","node_id":"verification-node","issued_at":now.isoformat(),"sequence":1,"runtime_state":"ACTIVE","capability_digest":"b"*64,"resource_summary":{}}
    return {
        "node":validate_node(node).valid,
        "capability":validate_capability(capability).valid,
        "heartbeat":validate_heartbeat(heartbeat,now).valid,
        "node_transition":transition_node_state("STALE","heartbeat")=="ACTIVE",
        "replica_transition":transition_replica_state("VERIFIED","available")=="AVAILABLE",
    }

if __name__=="__main__":
    import json
    result=run_checks()
    print(json.dumps(result,sort_keys=True))
    raise SystemExit(0 if all(result.values()) else 1)
