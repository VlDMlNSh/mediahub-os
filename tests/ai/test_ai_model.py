import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "contracts/ai/ai-model.schema.json"
SCHEMA_PATH = ROOT / "schemas/ai/ai-model.schema.json"


class AIModelContractTests(unittest.TestCase):

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
        properties = self.contract["properties"]

        self.assertEqual(
            self.contract["$id"],
            "mediahub.ai.ai-model",
        )

        self.assertEqual(
            properties["schema_id"]["const"],
            "mediahub.ai.ai-model",
        )

        self.assertEqual(
            properties["schema_version"]["const"],
            "1.0.0",
        )

        self.assertEqual(
            properties["owner"]["const"],
            "mediahub-ai",
        )

    def test_boundary(self):
        self.assertEqual(self.contract["type"], "object")
        self.assertFalse(self.contract["additionalProperties"])

    def test_required_fields(self):
        self.assertEqual(
            self.contract["required"],
            [
                "schema_id",
                "schema_version",
                "owner",
                "model_id",
                "provider_id",
                "model_name",
                "model_version",
                "model_family",
                "status",
            ],
        )

    def test_status_values(self):
        self.assertEqual(
            self.contract["properties"]["status"]["enum"],
            [
                "active",
                "inactive",
                "deprecated",
            ],
        )

    def test_nullable_metadata(self):
        self.assertEqual(
            self.contract["properties"]["model_version"]["type"],
            ["string", "null"],
        )
        self.assertEqual(
            self.contract["properties"]["model_family"]["type"],
            ["string", "null"],
        )

    def test_contract_matches_schema(self):
        self.assertEqual(self.contract, self.schema)


if __name__ == "__main__":
    unittest.main()
