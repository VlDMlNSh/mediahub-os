import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas/domain/property.schema.json"

class PropertySchemaTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            SCHEMA.read_text(encoding="utf-8")
        )

    def test_schema_identity(self):
        self.assertEqual(
            self.data["$id"],
            "mediahub://schemas/domain/property.schema.json",
        )

    def test_required_fields(self):
        expected = {
            "id",
            "type",
            "value",
            "unit",
            "constraints",
            "metadata",
        }
        self.assertEqual(
            set(self.data["required"]),
            expected,
        )

    def test_property_types(self):
        expected = {
            "BOOLEAN",
            "INTEGER",
            "FLOAT",
            "STRING",
            "ENUM",
            "TIMESTAMP",
            "DURATION",
            "OBJECT",
            "ARRAY",
        }
        self.assertEqual(
            set(self.data["properties"]["type"]["enum"]),
            expected,
        )

    def test_unit_is_explicit(self):
        self.assertIn(
            "unit",
            self.data["properties"],
        )

    def test_value_is_defined(self):
        self.assertIn(
            "value",
            self.data["properties"],
        )

if __name__ == "__main__":
    unittest.main()
