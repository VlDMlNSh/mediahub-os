import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AstraGoldRegistryTests(unittest.TestCase):
    def test_ecc_is_explicit_non_authoritative_auxiliary(self):
        registry = json.loads((ROOT / "profiles/agent-registry.json").read_text(encoding="utf-8"))
        ecc = next(item for item in registry["agents"] if item["id"] == "ecc")
        self.assertEqual(ecc["authority"], "none")
        self.assertFalse(ecc["provider_selection"])
        self.assertFalse(ecc["credential_creation"])
        self.assertFalse(ecc["state_authority"])
        self.assertIn("ecc", registry["hybrid_fabric"]["auxiliary_agents"])

    def test_claude_code_and_claude_provider_are_distinct(self):
        registry = json.loads((ROOT / "profiles/agent-registry.json").read_text(encoding="utf-8"))
        ids = {item["id"] for item in registry["agents"]}
        self.assertIn("claude-code", ids)
        self.assertIn("claude", ids)
        self.assertEqual(
            registry["hybrid_fabric"]["architectural_distinction"]["claude_code"],
            "local execution client",
        )


if __name__ == "__main__":
    unittest.main()
