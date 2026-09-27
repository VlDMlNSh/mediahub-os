import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts/mobile/mobile-api-compatibility.schema.json"

class MobileApiCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CONTRACT.open(encoding="utf-8") as handle:
            cls.data = json.load(handle)

    def test_metadata(self):
        self.assertEqual(self.data["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.data["$id"], "mediahub://contracts/mobile/mobile-api-compatibility.schema.json")
        self.assertEqual(self.data["properties"]["schema_id"]["const"], "mediahub.mobile.api_compatibility")
        self.assertEqual(self.data["properties"]["schema_version"]["const"], "1.0.0")

    def test_two_mobile_roles_are_explicit(self):
        role = self.data["properties"]["client"]["properties"]["role"]
        self.assertEqual(set(role["enum"]), {"core", "remote"})

    def test_platform_and_connectivity_are_bounded(self):
        client = self.data["properties"]["client"]["properties"]
        self.assertEqual(set(client["platform"]["enum"]), {"ios", "ipados"})
        self.assertEqual(
            set(self.data["properties"]["connectivity"]["enum"]),
            {"online", "offline", "degraded"},
        )

    def test_no_auth_or_ai_authority_fields(self):
        top_level = set(self.data["properties"])
        self.assertNotIn("credential", top_level)
        self.assertNotIn("authorization", top_level)
        self.assertNotIn("ai_tier", top_level)
        self.assertNotIn("state_authority", top_level)

    def test_compatibility_version_fields_are_explicit(self):
        api = self.data["properties"]["api"]["properties"]
        self.assertEqual(set(api), {"server_version", "selected_version"})

if __name__ == "__main__":
    unittest.main()
