import json
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from ops.mesh.validators import validate_node, validate_capability, validate_heartbeat
from ops.mesh.state import transition_node_state, transition_replica_state
from ops.mesh.artifacts import verify_artifact, admit_verified_artifact
from ops.p2p.ipfs import ipfs_available
from ops.p2p.replication import plan_recovery

ROOT = Path(__file__).parents[1]

class MeshContractTests(unittest.TestCase):
    def test_schema_ids_and_required_fields(self):
        expected = {
            "node.schema.json":"mediahub.mesh.node.v1",
            "capability.schema.json":"mediahub.mesh.capability.v1",
            "heartbeat.schema.json":"mediahub.mesh.heartbeat.v1",
            "artifact.schema.json":"mediahub.mesh.artifact.v1",
        }
        for name, schema_id in expected.items():
            data=json.loads((ROOT/"architecture"/"mesh"/name).read_text())
            self.assertEqual(data["$id"], schema_id)
            self.assertTrue(data["required"])

    def test_node_validation_fail_closed(self):
        self.assertFalse(validate_node({}).valid)
        node={"schema_version":"mediahub.mesh.node.v1","node_id":"mh-dev-02","role":"provider_execution","status":"ACTIVE","capabilities":[],"executors":[],"artifact_transports":[],"resources":{"ram_gib":16,"disk_free_gib":20},"last_heartbeat":"2026-10-03T00:00:00Z"}
        self.assertTrue(validate_node(node).valid)

    def test_capability_identity_and_authority(self):
        good={"schema_version":"mediahub.mesh.capability.v1","capability_id":"ecc","provider":"ecc","version":"1","executable":"/bin/ecc","identity_sha256":"a"*64,"authority":"NONE","qualification_state":"NOT_PROVEN"}
        self.assertTrue(validate_capability(good).valid)
        good["authority"]="CONTROL"
        self.assertTrue(validate_capability(good).valid)
        good["identity_sha256"]="bad"
        self.assertFalse(validate_capability(good).valid)

    def test_stale_heartbeat_blocks(self):
        now=datetime.now(timezone.utc)
        hb={"schema_version":"mediahub.mesh.heartbeat.v1","node_id":"mh-dev-02","issued_at":(now-timedelta(minutes=3)).isoformat(),"sequence":1,"runtime_state":"ACTIVE","capability_digest":"b"*64,"resource_summary":{}}
        self.assertFalse(validate_heartbeat(hb,now).valid)

    def test_invalid_state_transition_rejected(self):
        self.assertEqual(transition_node_state("STALE","heartbeat"),"ACTIVE")
        self.assertEqual(transition_replica_state("VERIFIED","available"),"AVAILABLE")
        with self.assertRaises(ValueError):
            transition_node_state("RETIRED","activate")

    def test_artifact_hash_is_authoritative(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"artifact"
            p.write_bytes(b"MEDIAHUB-MESH")
            import hashlib
            digest=hashlib.sha256(b"MEDIAHUB-MESH").hexdigest()
            vr=verify_artifact(p,digest)
            self.assertTrue(vr.verified)
            manifest={"schema_version":"mediahub.mesh.artifact.v1","artifact_id":"a1","sha256":digest,"size":p.stat().st_size,"type":"test","origin":"unit","transport":["torrent"],"replicas":[],"verification_state":"VERIFIED"}
            self.assertTrue(admit_verified_artifact(manifest,vr))
            self.assertFalse(admit_verified_artifact({**manifest,"sha256":"0"*64},vr))

    def test_recovery_without_source_is_blocked(self):
        artifact={"artifact_id":"a1"}
        self.assertTrue(plan_recovery(artifact,[{"replica_id":"r1","state":"FAILED"}]).blocked)
        self.assertFalse(plan_recovery(artifact,[{"replica_id":"r1","state":"AVAILABLE"}]).blocked)

if __name__ == "__main__":
    unittest.main()

# Isolated Mesh/P2P CI coverage is executed by .github/workflows/mesh-p2p-verify.yml.
