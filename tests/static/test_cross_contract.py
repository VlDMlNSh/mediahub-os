import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class CrossContractTests(unittest.TestCase):

    def load(self, relative_path):
        path = ROOT / relative_path
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)

    def test_core_contract_matches_core_schema(self):
        contract = self.load(
            "contracts/core/contract-metadata.schema.json"
        )
        schema = self.load(
            "schemas/core/contract-metadata.schema.json"
        )

        self.assertEqual(
            schema["$id"],
            "mediahub://schemas/core/contract-metadata.schema.json",
        )

        self.assertEqual(
            schema["properties"]["schema_id"]["type"],
            "string",
        )

        self.assertIn("schema_id", contract["properties"])

    def test_identity_contract_matches_identity_schema(self):
        contract = self.load(
            "contracts/identity/identity-boundary.schema.json"
        )
        schema = self.load(
            "schemas/identity/identity-boundary.schema.json"
        )

        self.assertEqual(
            schema["$id"],
            "mediahub://schemas/identity/identity-boundary.schema.json",
        )

        self.assertEqual(
            contract["properties"]["schema_id"]["const"],
            schema["properties"]["schema_id"]["const"],
        )

        self.assertEqual(
            contract["properties"]["schema_version"]["const"],
            schema["properties"]["schema_version"]["const"],
        )

    def test_identity_property_sets_match(self):
        contract = self.load(
            "contracts/identity/identity-boundary.schema.json"
        )
        schema = self.load(
            "schemas/identity/identity-boundary.schema.json"
        )

        contract_ids = set(
            contract["properties"]["identities"]["properties"]
        )

        schema_ids = set(
            schema["properties"]["identities"]["properties"]
        )

        self.assertEqual(contract_ids, schema_ids)
        self.assertNotIn("universal_id", contract_ids)
        self.assertNotIn("universal_id", schema_ids)

if __name__ == "__main__":
    unittest.main()
