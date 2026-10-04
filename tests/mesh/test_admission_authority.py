import unittest

from ops.mesh.admission import admit_executor

NODE = {"status": "ACTIVE", "node_id": "mh-dev-01", "role": "provider_execution"}
BASE = {
    "schema_version": "mediahub.mesh.capability.v1",
    "capability_id": "codex",
    "provider": "codex",
    "version": "1",
    "executable": "/usr/bin/codex",
    "identity_sha256": "a" * 64,
    "qualification_state": "QUALIFIED",
}

class AdmissionAuthorityTests(unittest.TestCase):
    def test_qualified_none_is_inventory_only(self):
        capability = dict(BASE, authority="NONE")
        result = admit_executor(NODE, capability, {"qualification_required": True})
        self.assertFalse(result.admitted)
        self.assertIn("EXECUTION authority", result.reason)

    def test_qualified_execution_is_admitted(self):
        capability = dict(BASE, authority="EXECUTION")
        result = admit_executor(NODE, capability, {"qualification_required": True})
        self.assertTrue(result.admitted)

if __name__ == "__main__":
    unittest.main()
