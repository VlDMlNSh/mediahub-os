import json
import unittest
from pathlib import Path


class DeepSeekModelRegistryTests(unittest.TestCase):
    def test_direct_deepseek_registry_uses_current_documented_model_and_paid_class(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads(
            (root / "ops" / "qualification" / "provider_model_registry.json").read_text(
                encoding="utf-8"
            )
        )
        provider = next(p for p in registry["providers"] if p.get("id") == "deepseek-1")
        self.assertEqual(provider["provider"], "DeepSeek")
        self.assertEqual(provider["credential_env"], ["DEEPSEEK_API_KEY"])
        self.assertEqual(provider["base_url"], "https://api.deepseek.com/v1")
        self.assertEqual(provider["models"], ["deepseek-flash"])
        self.assertEqual(provider["cost_class"], "paid_api")
        self.assertEqual(provider["persistence_class"], "api")


if __name__ == "__main__":
    unittest.main()
