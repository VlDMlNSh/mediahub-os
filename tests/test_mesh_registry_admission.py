import unittest
from datetime import datetime, timezone
from ops.mesh.registry import register_node, record_heartbeat
from ops.mesh.admission import admit_executor

NODE={"schema_version":"mediahub.mesh.node.v1","node_id":"mh-dev-02","role":"provider_execution","status":"ACTIVE","capabilities":["ecc"],"executors":["ollama"],"artifact_transports":["torrent"],"resources":{"ram_gib":16,"disk_free_gib":20},"last_heartbeat":"2026-10-03T00:00:00Z"}
CAP={"schema_version":"mediahub.mesh.capability.v1","capability_id":"ecc","provider":"ecc","version":"1","executable":"/bin/ecc","identity_sha256":"a"*64,"authority":"NONE","qualification_state":"NOT_PROVEN","sandbox":"bwrap","creates_credentials":False}

class MeshRegistryAdmissionTests(unittest.TestCase):
    def test_duplicate_node_rejected(self):
        self.assertFalse(register_node(NODE,{"mh-dev-02"}).accepted)
    def test_heartbeat_rejected_for_retired(self):
        hb={"schema_version":"mediahub.mesh.heartbeat.v1","node_id":"mh-dev-02","issued_at":datetime.now(timezone.utc).isoformat(),"sequence":1,"runtime_state":"ACTIVE","capability_digest":"b"*64,"resource_summary":{}}
        self.assertFalse(record_heartbeat(hb,datetime.now(timezone.utc),"RETIRED").accepted)
    def test_auxiliary_capability_cannot_select_provider(self):
        policy={"provider_selection":False,"credential_creation":False,"qualification_required":True}
        self.assertFalse(admit_executor(NODE,CAP,policy).admitted)
    def test_unqualified_executor_is_blocked(self):
        policy={"provider_selection":True,"credential_creation":True,"qualification_required":True}
        self.assertFalse(admit_executor(NODE,CAP,policy).admitted)

if __name__=="__main__":
    unittest.main()
