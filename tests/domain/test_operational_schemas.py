import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas/domain"


def load(name):
    return json.loads(
        (SCHEMA_DIR / name).read_text(encoding="utf-8")
    )


class OperationalSchemaTests(unittest.TestCase):

    def test_health_schema(self):
        data = load("health.schema.json")
        self.assertEqual(
            data["$id"],
            "mediahub://schemas/domain/health.schema.json",
        )
        self.assertEqual(
            set(data["required"]),
            {"status", "timestamp", "source", "details"},
        )

    def test_trust_schema(self):
        data = load("trust.schema.json")
        self.assertEqual(
            data["$id"],
            "mediahub://schemas/domain/trust.schema.json",
        )
        self.assertEqual(
            set(data["required"]),
            {"status", "source", "timestamp"},
        )

    def test_lifecycle_schema(self):
        data = load("lifecycle.schema.json")
        self.assertEqual(
            data["$id"],
            "mediahub://schemas/domain/lifecycle.schema.json",
        )
        self.assertEqual(
            set(data["required"]),
            {"state", "timestamp", "reason"},
        )

    def test_binding_schema(self):
        data = load("binding.schema.json")
        self.assertEqual(
            data["$id"],
            "mediahub://schemas/domain/binding.schema.json",
        )
        self.assertEqual(
            set(data["required"]),
            {
                "id",
                "protocol",
                "adapter",
                "endpoint",
                "priority",
                "status",
            },
        )
        self.assertEqual(
            data["properties"]["priority"]["minimum"],
            0,
        )

    def test_relationship_schema(self):
        data = load("relationship.schema.json")
        self.assertEqual(
            data["$id"],
            "mediahub://schemas/domain/relationship.schema.json",
        )
        self.assertEqual(
            data["properties"]["source"]["type"],
            "string",
        )
        self.assertEqual(
            data["properties"]["target"]["type"],
            "string",
        )

    def test_event_schema(self):
        data = load("event.schema.json")
        self.assertEqual(
            data["$id"],
            "mediahub://schemas/domain/event.schema.json",
        )
        self.assertEqual(
            set(data["required"]),
            {
                "id",
                "type",
                "version",
                "timestamp",
                "source",
                "subject",
                "payload",
                "severity",
                "priority",
                "correlation_id",
                "causation_id",
                "metadata",
            },
        )
        self.assertEqual(
            data["properties"]["payload"]["type"],
            "object",
        )

    def test_event_correlation_is_nullable(self):
        data = load("event.schema.json")
        self.assertEqual(
            set(data["properties"]["correlation_id"]["type"]),
            {"string", "null"},
        )
        self.assertEqual(
            set(data["properties"]["causation_id"]["type"]),
            {"string", "null"},
        )


