import unittest

from ops.mesh.validators import validate_node_profile


class MeshNodeProfileTests(unittest.TestCase):
    def test_valid_profile(self):
        profile = {
            "schema_version": "mediahub.mesh.node-profile.v1",
            "node_id": "mh-dev-02",
            "role": "provider_execution",
            "resources": {"ram_gib": 16, "swap_gib": 2},
            "capabilities": ["codex-cli", "ollama"],
            "executors": ["codex", "ollama"],
            "artifact_transports": ["torrent"],
            "inventory_source": {
                "producer": "ops/qualification/inventory_local_components.py",
                "schema_version": "mediahub.local-component-inventory.v1"
            }
        }
        self.assertTrue(validate_node_profile(profile).valid)

    def test_missing_node_identity_is_rejected(self):
        profile = {
            "schema_version": "mediahub.mesh.node-profile.v1",
            "role": "provider_execution",
            "resources": {"ram_gib": 16},
            "capabilities": [],
            "executors": [],
            "artifact_transports": [],
            "inventory_source": {
                "producer": "inventory",
                "schema_version": "mediahub.local-component-inventory.v1"
            }
        }
        self.assertFalse(validate_node_profile(profile).valid)

    def test_inventory_does_not_imply_qualification(self):
        profile = {
            "schema_version": "mediahub.mesh.node-profile.v1",
            "node_id": "Voktor-Mini-Astra",
            "role": "provider_execution",
            "resources": {"ram_gib": 16},
            "capabilities": ["ollama"],
            "executors": ["ollama"],
            "artifact_transports": ["torrent"],
            "inventory_source": {
                "producer": "inventory",
                "schema_version": "mediahub.local-component-inventory.v1"
            }
        }
        self.assertNotIn("qualification_state", profile)


if __name__ == "__main__":
    unittest.main()
