import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# schemas/ is the single canonical schema source (audit defect D2).
CONTRACT = ROOT / "schemas/core/contract-metadata.schema.json"


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
            "mediahub://schemas/core/contract-metadata.schema.json"
        )

    def test_required_metadata_fields(self):
        self.assertEqual(
            set(self.data["required"]),
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
        self.assertEqual(
            self.data["properties"]["schema_version"]["pattern"],
            "^[0-9]+\\.[0-9]+\\.[0-9]+$"
        )
