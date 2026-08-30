import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUEST_CONTRACT = ROOT / "contracts/ai/ai-inference-request.schema.json"
REQUEST_SCHEMA = ROOT / "schemas/ai/ai-inference-request.schema.json"

RESPONSE_CONTRACT = ROOT / "contracts/ai/ai-inference-response.schema.json"
RESPONSE_SCHEMA = ROOT / "schemas/ai/ai-inference-response.schema.json"


class AIInferenceContractTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.request = json.loads(
            REQUEST_CONTRACT.read_text(encoding="utf-8")
        )
        cls.response = json.loads(
            RESPONSE_CONTRACT.read_text(encoding="utf-8")
        )

    def test_request_contract_matches_schema(self):
        self.assertEqual(
            REQUEST_CONTRACT.read_bytes(),
            REQUEST_SCHEMA.read_bytes(),
        )

    def test_response_contract_matches_schema(self):
        self.assertEqual(
            RESPONSE_CONTRACT.read_bytes(),
            RESPONSE_SCHEMA.read_bytes(),
        )

    def test_request_metadata(self):
        self.assertEqual(
            self.request["properties"]["schema_id"]["const"],
            "mediahub.ai.ai-inference-request",
        )
        self.assertEqual(
            self.request["properties"]["schema_version"]["const"],
            "1.0.0",
        )
        self.assertEqual(
            self.request["properties"]["owner"]["const"],
            "mediahub-ai",
        )

    def test_response_metadata(self):
        self.assertEqual(
            self.response["properties"]["schema_id"]["const"],
            "mediahub.ai.ai-inference-response",
        )
        self.assertEqual(
            self.response["properties"]["schema_version"]["const"],
            "1.0.0",
        )
        self.assertEqual(
            self.response["properties"]["owner"]["const"],
            "mediahub-ai",
        )

    def test_request_boundary(self):
        properties = self.request["properties"]

        for field in (
            "request_id",
            "provider_id",
            "model",
            "operation",
            "input",
            "parameters",
            "metadata",
        ):
            self.assertIn(field, properties)

    def test_response_boundary(self):
        properties = self.response["properties"]

        for field in (
            "request_id",
            "provider_id",
            "model",
            "status",
            "output",
            "usage",
            "error",
            "metadata",
        ):
            self.assertIn(field, properties)

    def test_request_operations(self):
        self.assertEqual(
            self.request["properties"]["operation"]["enum"],
            [
                "generate",
                "classify",
                "embed",
                "transcribe",
                "transform",
            ],
        )

    def test_response_statuses(self):
        self.assertEqual(
            self.response["properties"]["status"]["enum"],
            [
                "completed",
                "failed",
                "partial",
            ],
        )

    def test_request_required_fields(self):
        required = set(self.request["required"])

        for field in (
            "schema_id",
            "schema_version",
            "owner",
            "request_id",
            "operation",
            "input",
        ):
            self.assertIn(field, required)

    def test_response_required_fields(self):
        required = set(self.response["required"])

        for field in (
            "schema_id",
            "schema_version",
            "owner",
            "request_id",
            "status",
        ):
            self.assertIn(field, required)

    def test_provider_selection_is_optional(self):
        self.assertNotIn("provider_id", self.request["required"])
        self.assertNotIn("model", self.request["required"])


if __name__ == "__main__":
    unittest.main()
