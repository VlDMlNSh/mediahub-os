import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts/identity/identity-boundary.schema.json"

EXPECTED_IDENTITIES = {
    "device_id",
    "binding_id",
    "adapter_id",
    "adapter_instance_id",
    "capability_id",
    "event_id",
    "command_id",
    "execution_id",
    "request_id",
    "correlation_id",
    "causation_id",
    "recovery_id",
}


class IdentityBoundaryTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with CONTRACT.open(encoding="utf-8") as f:
            cls.data = json.load(f)

    def test_schema_metadata(self):
        self.assertEqual(
            self.data["$schema"],
            "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertEqual(
            self.data["$id"],
            "mediahub://contracts/identity/identity-boundary.schema.json"
        )

    def test_instance_metadata_contract(self):
        properties = self.data["properties"]

        self.assertIn("schema_id", properties)
        self.assertIn("schema_version", properties)
        self.assertIn("owner", properties)
        self.assertIn("identities", properties)

        self.assertEqual(
            properties["schema_id"]["const"],
            "mediahub.identity.boundary"
        )
        self.assertEqual(
            properties["schema_version"]["const"],
            "1.0.0"
        )
        self.assertEqual(
            properties["owner"]["const"],
            "MediaHub OS Foundation"
        )

    def test_identity_separation(self):
        identities = set(
            self.data["properties"]["identities"]["properties"]
        )

        self.assertEqual(
            identities,
            EXPECTED_IDENTITIES
        )

        self.assertNotIn(
            "universal_id",
            identities
        )
