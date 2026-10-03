import unittest

from ops.mesh.admission import admit_executor


def node(status="ACTIVE"):
    return {"node_id": "mh-test-01", "role": "worker", "status": status}


def capability(authority="NONE", qualification_state="QUALIFIED", capability_id="codex"):
    return {
        "schema_version": "mediahub.mesh.capability.v1",
        "capability_id": capability_id,
        "provider": "codex",
        "version": "0.1",
        "executable": "/usr/bin/codex",
        "identity_sha256": "a" * 64,
        "authority": authority,
        "qualification_state": qualification_state,
    }


class MeshAdmissionBoundaryTests(unittest.TestCase):
    def test_inactive_node_is_rejected(self):
        result = admit_executor(node("DISCOVERED"), capability(), {})
        self.assertFalse(result.admitted)
        self.assertEqual(result.reason, "node is not active")

    def test_missing_identity_is_rejected(self):
        result = admit_executor({"status": "ACTIVE", "node_id": "", "role": "worker"}, capability(), {})
        self.assertFalse(result.admitted)
        self.assertEqual(result.reason, "node identity or role missing")

    def test_control_authority_is_rejected_for_executor(self):
        result = admit_executor(node(), capability(authority="CONTROL"), {})
        self.assertFalse(result.admitted)
        self.assertEqual(result.reason, "unsupported capability authority")

    def test_unqualified_capability_is_rejected_by_default(self):
        result = admit_executor(node(), capability(qualification_state="DISCOVERED"), {})
        self.assertFalse(result.admitted)
        self.assertEqual(result.reason, "qualification required")

    def test_qualified_execution_capability_is_admitted(self):
        result = admit_executor(node(), capability(authority="EXECUTION"), {})
        self.assertTrue(result.admitted)

    def test_auxiliary_capability_cannot_gain_authority(self):
        result = admit_executor(
            node(),
            capability(authority="EXECUTION", capability_id="openflux"),
            {"provider_selection": False, "credential_creation": False},
        )
        self.assertFalse(result.admitted)
        self.assertEqual(result.reason, "auxiliary capability authority must remain NONE")


if __name__ == "__main__":
    unittest.main()
