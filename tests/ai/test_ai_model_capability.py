import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = ROOT / "contracts/ai/ai-model-capability.schema.json"
SCHEMA_PATH = ROOT / "schemas/ai/ai-model-capability.schema.json"


class AIModelCapabilityContractTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(
            CONTRACT_PATH.read_text(encoding="utf-8")
        )
        cls.schema = json.loads(
            SCHEMA_PATH.read_text(encoding="utf-8")
        )

    def test_schema_is_json_schema_2020_12(self):
        self.assertEqual(
            self.contract["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )

    def test_metadata(self):
        self.assertEqual(
            self.contract["$id"],
            "mediahub.ai.ai-model-capability",
        )
        self.assertEqual(
            self.contract["properties"]["schema_id"]["const"],
            "mediahub.ai.ai-model-capability",
        )
        self.assertEqual(
            self.contract["properties"]["schema_version"]["const"],
            "1.0.0",
        )
        self.assertEqual(
            self.contract["properties"]["owner"]["const"],
            "mediahub-ai",
        )

    def test_boundary(self):
        properties = self.contract["properties"]

        for field in [
            "model_id",
            "provider_id",
            "capability_type",
            "operations",
            "context_window",
            "availability",
        ]:
            self.assertIn(field, properties)

        self.assertFalse(
            self.contract["additionalProperties"]
        )

    def test_required_fields(self):
        required = set(self.contract["required"])

        for field in [
            "schema_id",
            "schema_version",
            "owner",
            "model_id",
            "provider_id",
            "capability_type",
            "operations",
            "context_window",
            "availability",
        ]:
            self.assertIn(field, required)

    def test_capability_types(self):
        self.assertEqual(
            self.contract["properties"]["capability_type"]["enum"],
            [
                "text",
                "vision",
                "audio",
                "multimodal",
                "embedding",
            ],
        )

    def test_operations(self):
        self.assertEqual(
            self.contract["properties"]["operations"]["items"]["enum"],
            [
                "infer",
                "stream",
                "embed",
            ],
        )

    def test_availability_states(self):
        self.assertEqual(
            self.contract["properties"]["availability"]["enum"],
            [
                "available",
                "degraded",
                "unavailable",
            ],
        )

    def test_contract_matches_schema(self):
        self.assertEqual(self.contract, self.schema)


if __name__ == "__main__":
    unittest.main()
