import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas/domain/device.schema.json"

class DeviceSchemaTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with SCHEMA.open(encoding="utf-8") as handle:
            cls.data = json.load(handle)

    def test_schema_identity(self):
        self.assertEqual(
            self.data["$id"],
            "mediahub://schemas/domain/device.schema.json",
        )

    def test_device_required_fields(self):
        expected = {
            "id",
            "type",
            "identity",
            "location",
            "components",
            "endpoints",
            "capabilities",
            "configuration",
            "state",
            "desired_state",
            "health",
            "availability",
            "trust",
            "lifecycle",
            "bindings",
            "relationships",
            "metadata",
        }

        self.assertEqual(
            set(self.data["required"]),
            expected,
        )

    def test_mediahub_identity_is_primary(self):
        identity = self.data["properties"]["identity"]

        self.assertIn("mediahub_id", identity["required"])
        self.assertEqual(
            identity["properties"]["mediahub_id"]["type"],
            "string",
        )

    def test_protocol_ids_are_references(self):
        identity = self.data["properties"]["identity"]

        self.assertIn(
            "protocol_ids",
            identity["properties"],
        )

        self.assertEqual(
            identity["properties"]["protocol_ids"]["type"],
            "array",
        )

    def test_hardware_ids_are_references(self):
        identity = self.data["properties"]["identity"]

        self.assertIn(
            "hardware_ids",
            identity["properties"],
        )

        self.assertEqual(
            identity["properties"]["hardware_ids"]["type"],
            "array",
        )
