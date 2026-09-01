import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class DevelopmentHostArchitectureTests(unittest.TestCase):
    def test_host_policy_is_offline_first(self):
        cfg = json.loads((ROOT / "config/dev-host.json").read_text())
        self.assertEqual(cfg["network"]["default"], "offline_first")

    def test_secrets_are_external(self):
        cfg = json.loads((ROOT / "config/dev-host.json").read_text())
        self.assertEqual(cfg["paths"]["secrets"], "KEYCHAIN_OR_ENV_ONLY")

    def test_authority_boundaries(self):
        cfg = json.loads((ROOT / "config/dev-host.json").read_text())
        self.assertEqual(cfg["authority"]["canonical_governance_write"], "FORBIDDEN")
        self.assertEqual(cfg["authority"]["worker_direct_master_write"], "FORBIDDEN")
        self.assertEqual(cfg["authority"]["product_deploy"], "RELEASE_ARTIFACT_ONLY")

if __name__ == "__main__":
    unittest.main()
