import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas/domain/capability.schema.json"

class CapabilitySchemaTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            SCHEMA.read_text(encoding="utf-8")
        )

    def test_schema_identity(self):
        self.assertEqual(
            self.data["$id"],
            "mediahub://schemas/domain/capability.schema.json",
        )

    def test_status_values(self):
        self.assertEqual(
            set(self.data["properties"]["status"]["enum"]),
            {
                "AVAILABLE",
                "ENABLED",
                "DISABLED",
                "LIMITED",
                "UNAVAILABLE",
                "UNKNOWN",
            },
        )

    def test_discovery_state_values(self):
        self.assertEqual(
            set(self.data["properties"]["discovery_state"]["enum"]),
            {
                "DECLARED",
                "DISCOVERED",
                "VALIDATED",
                "INFERRED",
                "CONFIGURED",
            },
        )

    def test_inferred_is_distinct_from_validated(self):
        states = set(
            self.data["properties"]["discovery_state"]["enum"]
        )
        self.assertIn("INFERRED", states)
        self.assertIn("VALIDATED", states)
        self.assertNotEqual("INFERRED", "VALIDATED")

    def test_safety_classes(self):
        self.assertEqual(
            set(self.data["properties"]["safety_class"]["enum"]),
            {
                "LOW_RISK",
                "CONTROLLED",
                "CRITICAL",
                "SAFETY_SENSITIVE",
            },
        )

if __name__ == "__main__":
    unittest.main()
