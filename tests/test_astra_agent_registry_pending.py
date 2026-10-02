import json
import tempfile
import unittest
from pathlib import Path

from mediahub_runtime.astra_gateway import AgentRegistry


class PendingAgentRegistryTests(unittest.TestCase):
    def test_unresolved_pending_candidate_without_capabilities_is_non_selectable(self):
        registry = {
            "agents": [
                {
                    "id": "colibri",
                    "enabled": True,
                    "tier": "candidate_coding_or_agent",
                    "activation": "review_and_qualification_required",
                    "qualification": "pending",
                    "identity_status": "UNRESOLVED",
                },
                {
                    "id": "unlazy",
                    "enabled": True,
                    "tier": "candidate_developer_tool",
                    "activation": "review_and_qualification_required",
                    "qualification": "pending",
                    "identity_status": "UNRESOLVED",
                },
                {
                    "id": "ollama",
                    "enabled": True,
                    "tier": "local",
                    "capabilities": ["coding"],
                },
            ]
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "agent-registry.json"
            path.write_text(json.dumps(registry), encoding="utf-8")
            loaded = AgentRegistry(path)
            self.assertEqual(loaded.select("coding").agent_id, "ollama")


if __name__ == "__main__":
    unittest.main()
