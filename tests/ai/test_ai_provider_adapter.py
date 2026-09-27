import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTRACT = ROOT / "contracts/ai/ai-provider-adapter.schema.json"
SCHEMA = ROOT / "schemas/ai/ai-provider-adapter.schema.json"


class AIProviderAdapterContractTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_contract_matches_schema(self):
        self.assertEqual(self.contract, self.schema)

    def test_schema_is_json_schema_2020_12(self):
        self.assertEqual(
            self.contract["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )

    def test_metadata(self):
        properties = self.contract["properties"]

        self.assertEqual(
            properties["schema_id"]["const"],
            "mediahub.ai.ai-provider-adapter",
        )
        self.assertEqual(
            properties["schema_version"]["const"],
            "1.0.0",
        )
        self.assertEqual(
            properties["owner"]["const"],
            "mediahub-ai",
        )

    def test_adapter_boundary(self):
        properties = self.contract["properties"]

        for field in (
            "adapter_id",
            "provider_id",
            "provider_type",
            "capabilities",
            "operations",
            "availability",
            "state",
        ):
            self.assertIn(field, properties)

    def test_required_fields(self):
        required = set(self.contract["required"])

        for field in (
            "schema_id",
            "schema_version",
            "owner",
            "adapter_id",
            "provider_id",
            "provider_type",
            "capabilities",
            "operations",
            "availability",
            "state",
        ):
            self.assertIn(field, required)

    def test_provider_types(self):
        self.assertEqual(
            self.contract["properties"]["provider_type"]["enum"],
            ["remote", "local", "hybrid"],
        )

    def test_operations(self):
        self.assertEqual(
            self.contract["properties"]["operations"]["items"]["enum"],
            ["infer", "health", "metadata"],
        )

    def test_availability_states(self):
        self.assertEqual(
            self.contract["properties"]["availability"]["enum"],
            [
                "available",
                "unavailable",
                "degraded",
                "unknown",
            ],
        )

    def test_runtime_states(self):
        self.assertEqual(
            self.contract["properties"]["state"]["enum"],
            [
                "uninitialized",
                "initializing",
                "ready",
                "degraded",
                "failed",
                "stopped",
            ],
        )


if __name__ == "__main__":
    unittest.main()
