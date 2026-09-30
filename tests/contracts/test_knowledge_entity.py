import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts/knowledge/knowledge-entity.schema.json"


class KnowledgeEntityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CONTRACT.open(encoding="utf-8") as handle:
            cls.data = json.load(handle)

    def test_contract_identity(self):
        self.assertEqual(
            self.data["$id"],
            "mediahub://contracts/knowledge/knowledge-entity.schema.json",
        )
        self.assertEqual(
            self.data["properties"]["schema_id"]["const"],
            "mediahub.knowledge.entity",
        )
        self.assertEqual(
            self.data["properties"]["schema_version"]["const"],
            "1.0.0",
        )

    def test_authority_and_provenance_are_explicit(self):
        self.assertIn("authority_ref", self.data["required"])
        provenance = self.data["properties"]["provenance"]
        self.assertEqual(set(provenance["required"]), {"source_ref", "observed_at"})

    def test_lifecycle_preserves_unresolved_and_historical_states(self):
        self.assertEqual(
            set(self.data["properties"]["lifecycle"]["enum"]),
            {"candidate", "active", "historical", "removed", "unresolved"},
        )

    def test_contract_does_not_define_authority_mutation_fields(self):
        properties = set(self.data["properties"])
        self.assertNotIn("command", properties)
        self.assertNotIn("authorization", properties)
        self.assertNotIn("state_mutation", properties)
        self.assertNotIn("device_action", properties)


if __name__ == "__main__":
    unittest.main()
