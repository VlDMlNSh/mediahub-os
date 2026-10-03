import unittest
from ops.p2p.replication import plan_replication, plan_recovery

class RecoveryTests(unittest.TestCase):
    def test_replication_ignores_verified_replica(self):
        p=plan_replication({"artifact_id":"a1"},[{"replica_id":"r1","state":"AVAILABLE"},{"replica_id":"r2","state":"FAILED"}])
        self.assertEqual(p.targets,("r2",))
    def test_no_verified_source_blocks(self):
        p=plan_recovery({"artifact_id":"a1"},[{"replica_id":"r1","state":"FAILED"}])
        self.assertTrue(p.blocked)
    def test_verified_source_recovers(self):
        p=plan_recovery({"artifact_id":"a1"},[{"replica_id":"r1","state":"VERIFIED"}])
        self.assertFalse(p.blocked)

if __name__=="__main__": unittest.main()
