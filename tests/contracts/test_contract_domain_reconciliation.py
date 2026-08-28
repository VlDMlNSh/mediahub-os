import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_DIR = ROOT / "schemas/domain"
IDENTITY_CONTRACT = (
    ROOT / "contracts/identity/identity-boundary.schema.json"
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class ContractDomainReconciliationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.domain = {
            p.stem.replace(".schema", ""): load(p)
            for p in DOMAIN_DIR.glob("*.schema.json")
        }

        cls.identity = load(IDENTITY_CONTRACT)

        cls.identity_names = set(
            cls.identity["properties"]["identities"]["properties"]
        )

    def test_domain_schema_count(self):
        self.assertEqual(len(self.domain), 16)

    def test_canonical_domain_entities_exist(self):
        for name in (
            "device",
            "component",
            "endpoint",
            "capability",
            "property",
            "binding",
            "relationship",
            "event",
        ):
            self.assertIn(name, self.domain)

    def test_identity_boundary_matches_domain(self):
        for identity in (
            "device_id",
            "binding_id",
            "capability_id",
            "event_id",
            "adapter_id",
            "adapter_instance_id",
            "command_id",
            "execution_id",
            "request_id",
            "correlation_id",
            "causation_id",
            "recovery_id",
        ):
            self.assertIn(identity, self.identity_names)

        self.assertNotIn(
            "universal_id",
            self.identity_names,
        )

    def test_device_component_endpoint_boundary(self):
        self.assertIn(
            "id",
            set(self.domain["device"]["required"]),
        )

        self.assertIn(
            "id",
            set(self.domain["component"]["required"]),
        )

        endpoint_required = set(
            self.domain["endpoint"]["required"]
        )

        self.assertIn("device_id", endpoint_required)
        self.assertIn("component_id", endpoint_required)

    def test_entity_ids_remain_distinct_from_runtime_ids(self):
        self.assertIn(
            "id",
            set(self.domain["event"]["required"]),
        )

        self.assertIn("event_id", self.identity_names)
        self.assertIn("execution_id", self.identity_names)
        self.assertIn("request_id", self.identity_names)
