import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "config/ai/openrouter-glm52.json"


class OpenRouterGLM52ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_uses_canonical_provider_contract(self):
        self.assertEqual(self.data["schema_id"], "mediahub.ai.ai-provider")
        self.assertEqual(self.data["schema_version"], "1.0.0")
        self.assertEqual(self.data["owner"], "mediahub-ai")

    def test_exact_model_slug(self):
        self.assertEqual(self.data["provider_id"], "openrouter-glm52")
        self.assertEqual(self.data["provider_type"], "remote")
        self.assertEqual(self.data["model"], "z-ai/glm-5.2")

    def test_secret_is_not_embedded(self):
        serialized = MANIFEST.read_text(encoding="utf-8")
        forbidden = ("sk-or-", "OPENROUTER_API_KEY=", "Authorization: Bearer")
        for marker in forbidden:
            self.assertNotIn(marker, serialized)

    def test_required_capabilities(self):
        self.assertTrue(
            {"text", "reasoning", "tool_calling", "structured_output"}
            .issubset(set(self.data["capabilities"]))
        )


if __name__ == "__main__":
    unittest.main()
