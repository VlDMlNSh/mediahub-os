import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas/domain"


def load(name):
    return json.loads(
        (SCHEMA_DIR / name).read_text(encoding="utf-8")
    )


class DomainReconciliationTests(unittest.TestCase):

    def test_domain_schema_count(self):
        files = list(SCHEMA_DIR.glob("*.schema.json"))
        self.assertEqual(len(files), 16)

    def test_device_is_canonical_entity(self):
        data = load("device.schema.json")
        self.assertIn("id", data["required"])

    def test_component_and_endpoint_reference_device(self):
        component = load("component.schema.json")
        endpoint = load("endpoint.schema.json")

        self.assertIn("id", component["required"])
        self.assertIn("device_id", endpoint["required"])
        self.assertIn("component_id", endpoint["required"])

    def test_capability_and_property_are_distinct(self):
        capability = load("capability.schema.json")
        property_ = load("property.schema.json")

        self.assertIn("id", capability["required"])
        self.assertIn("id", property_["required"])

        self.assertNotEqual(
            set(capability["required"]),
            set(property_["required"]),
        )

    def test_actual_and_desired_state_are_distinct(self):
        state = load("state.schema.json")
        desired = load("desired_state.schema.json")

        self.assertIn("confidence", state["required"])
        self.assertIn("priority", desired["required"])

        self.assertNotIn("confidence", desired["required"])
        self.assertNotIn("priority", state["required"])

    def test_operational_boundaries_are_distinct(self):
        health = load("health.schema.json")
        availability = load("availability.schema.json")
        trust = load("trust.schema.json")
        lifecycle = load("lifecycle.schema.json")

        self.assertIn("status", health["required"])
        self.assertIn("status", availability["required"])
        self.assertIn("status", trust["required"])
        self.assertIn("state", lifecycle["required"])

    def test_protocol_binding_is_not_device_identity(self):
        binding = load("binding.schema.json")

        self.assertIn("protocol", binding["required"])
        self.assertIn("adapter", binding["required"])
        self.assertIn("endpoint", binding["required"])

        self.assertNotIn("device_id", binding["required"])
        self.assertNotIn("hardware_id", binding["required"])

    def test_relationship_uses_entity_references(self):
        relationship = load("relationship.schema.json")

        self.assertEqual(
            relationship["properties"]["source"]["type"],
            "string",
        )
        self.assertEqual(
            relationship["properties"]["target"]["type"],
            "string",
        )

    def test_event_is_immutable_fact_boundary(self):
        event = load("event.schema.json")

        required = set(event["required"])

        self.assertIn("id", required)
        self.assertIn("timestamp", required)
        self.assertIn("subject", required)
        self.assertIn("payload", required)
        self.assertIn("correlation_id", required)
        self.assertIn("causation_id", required)



    def test_event_is_immutable_fact_boundary(self):
        event = load("event.schema.json")

        required = set(event["required"])

        self.assertIn("id", required)
        self.assertIn("timestamp", required)
        self.assertIn("subject", required)
        self.assertIn("payload", required)
        self.assertIn("correlation_id", required)
        self.assertIn("causation_id", required)


