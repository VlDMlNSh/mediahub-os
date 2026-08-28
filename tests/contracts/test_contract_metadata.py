import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts/core/contract-metadata.schema.json"

class ContractMetadataTests(unittest.TestCase):

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
            "mediahub://contracts/core/contract-metadata.schema.json"
        )

    def test_required_metadata_fields(self):
        required = set(self.data["required"])

        self.assertEqual(
            required,
            {
                "schema_id",
                "schema_version",
                "owner",
                "required",
                "optional",
                "constraints",
            },
        )

    def test_property_definitions_exist(self):
        properties = self.data["properties"]

        for name in (
            "schema_id",
            "schema_version",
            "owner",
            "required",
            "optional",
            "constraints",
        ):
            self.assertIn(name, properties)

    def test_schema_version_is_semver_like(self):
        pattern = self.data["properties"]["schema_version"]["pattern"]

        self.assertEqual(
            pattern,
            "^[0-9]+\\.[0-9]+\\.[0-9]+$"
        )

if __name__ == "__main__":
    unittest.main()
