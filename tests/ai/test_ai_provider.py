import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts/ai/ai-provider.schema.json"


class AIProviderContractTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            CONTRACT.read_text(encoding="utf-8")
        )

    def test_schema_is_json_schema_2020_12(self):
        self.assertEqual(
            self.data["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )

    def test_metadata(self):
        properties = self.data["properties"]

        self.assertEqual(
            properties["schema_id"]["const"],
            "mediahub.ai.ai-provider",
        )

        self.assertEqual(
            properties["schema_version"]["const"],
            "1.0.0",
        )

        self.assertEqual(
            properties["owner"]["const"],
            "mediahub-ai",
        )

    def test_provider_boundary(self):
        properties = self.data["properties"]

        self.assertIn("provider_id", properties)
        self.assertIn("provider_type", properties)
        self.assertIn("model", properties)
        self.assertIn("capabilities", properties)
        self.assertIn("authentication", properties)
        self.assertIn("availability", properties)

    def test_provider_types(self):
        self.assertEqual(
            self.data["properties"]["provider_type"]["enum"],
            ["remote", "local", "hybrid"],
        )

    def test_availability_states(self):
        self.assertEqual(
            self.data["properties"]["availability"]["enum"],
            [
                "available",
                "unavailable",
                "degraded",
                "unknown",
            ],
        )

    def test_required_fields(self):
        required = set(self.data["required"])

        for field in (
            "schema_id",
            "schema_version",
            "owner",
            "provider_id",
            "provider_type",
            "model",
            "capabilities",
            "authentication",
            "availability",
        ):
            self.assertIn(field, required)


if __name__ == "__main__":
    unittest.main()
