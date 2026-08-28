import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schemas"

class FoundationSchemaTests(unittest.TestCase):

    def load(self, relative_path):
        path = SCHEMA_ROOT / relative_path
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)

    def test_core_schema_metadata(self):
        data = self.load("core/contract-metadata.schema.json")

        self.assertEqual(
            data["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(
            data["$id"],
            "mediahub://schemas/core/contract-metadata.schema.json",
        )

        required = {
            "schema_id",
            "schema_version",
            "owner",
            "required",
            "optional",
            "constraints",
        }

        self.assertTrue(required.issubset(set(data["required"])))

    def test_identity_schema_metadata(self):
        data = self.load("identity/identity-boundary.schema.json")

        self.assertEqual(
            data["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(
            data["$id"],
            "mediahub://schemas/identity/identity-boundary.schema.json",
        )
        self.assertEqual(
            data["properties"]["schema_version"]["const"],
            "1.0.0",
        )

    def test_identity_schema_preserves_identity_separation(self):
        data = self.load("identity/identity-boundary.schema.json")

        identities = set(
            data["properties"]["identities"]["properties"]
        )

        expected = {
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

        self.assertEqual(identities, expected)
        self.assertNotIn("universal_id", identities)

    def test_all_schema_files_are_valid_json(self):
        files = sorted(SCHEMA_ROOT.glob("**/*.json"))

        self.assertGreaterEqual(len(files), 2)

        for path in files:
            with path.open(encoding="utf-8") as handle:
                data = json.load(handle)

            self.assertIsInstance(data, dict)
            self.assertIn("$schema", data)
            self.assertIn("$id", data)

            self.assertNotIn(b"&quot;", path.read_bytes())

if __name__ == "__main__":
    unittest.main()
