import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTRACT = (
    ROOT / "contracts/ai/ai-provider-registry.schema.json"
)

SCHEMA = (
    ROOT / "schemas/ai/ai-provider-registry.schema.json"
)


class AIProviderRegistryContractTests(unittest.TestCase):

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
            "mediahub.ai.ai-provider-registry",
        )

        self.assertEqual(
            properties["schema_version"]["const"],
            "1.0.0",
        )

        self.assertEqual(
            properties["owner"]["const"],
            "mediahub-ai",
        )

    def test_registry_boundary(self):
        properties = self.data["properties"]

        for field in (
            "providers",
            "default_provider_id",
            "selection_policy",
            "timestamp",
        ):
            self.assertIn(field, properties)

    def test_provider_entries_are_references(self):
        provider = (
            self.data["properties"]["providers"]
            ["items"]
        )

        self.assertEqual(
            set(provider["required"]),
            {
                "provider_id",
                "enabled",
                "priority",
            },
        )

        self.assertEqual(
            provider["properties"]["provider_id"]["type"],
            "string",
        )

    def test_selection_policy(self):
        self.assertEqual(
            self.data["properties"]["selection_policy"]["enum"],
            [
                "EXPLICIT",
                "PRIORITY",
                "CAPABILITY",
                "FAILOVER",
            ],
        )

    def test_default_provider_is_nullable(self):
        self.assertEqual(
            set(
                self.data["properties"]
                ["default_provider_id"]["type"]
            ),
            {"string", "null"},
        )

    def test_required_fields(self):
        self.assertEqual(
            set(self.data["required"]),
            {
                "schema_id",
                "schema_version",
                "owner",
                "providers",
                "default_provider_id",
                "selection_policy",
                "timestamp",
            },
        )

    def test_contract_matches_schema(self):
        schema = json.loads(
            SCHEMA.read_text(encoding="utf-8")
        )

        self.assertEqual(
            self.data,
            schema,
        )


if __name__ == "__main__":
    unittest.main()
