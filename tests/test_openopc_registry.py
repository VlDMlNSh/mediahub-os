import json
import unittest
from pathlib import Path

REGISTRY = Path("profiles/agent-registry.json")


class TestOpenOPCRegistry(unittest.TestCase):
    @classmethod
    def load(cls):
        return json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_openopc_is_registered_as_candidate_only(self):
        data = self.load()
        agent = next(item for item in data["agents"] if item["id"] == "openopc")
        self.assertEqual(agent["tier"], "candidate_autonomous_development_system")
        self.assertEqual(agent["qualification"], "pending")
        self.assertEqual(agent["authority"], "none")
        self.assertFalse(agent["provider_selection"])
        self.assertFalse(agent["credential_creation"])
        self.assertFalse(agent["state_authority"])
        self.assertEqual(agent["source"], "https://github.com/HKUDS/OpenOPC")

    def test_openopc_does_not_enter_mandatory_executor_matrix(self):
        data = self.load()
        self.assertIn("openopc", data["hybrid_fabric"]["candidate_autonomous_systems"])
        self.assertNotIn("openopc", data["hybrid_fabric"]["local_agents"])
        self.assertNotIn("openopc", data["hybrid_fabric"]["registered_agents"])
        self.assertEqual(data["hybrid_fabric"]["qualification_states"]["openopc"], "NOT_PROVEN")


if __name__ == "__main__":
    unittest.main()
