import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/ai/ECC-INTEGRATION.md"
MANIFEST = ROOT / "oss/manifests/ecc.yaml"


class ECCIntegrationContractTests(unittest.TestCase):
    def test_integration_is_target_gated_and_mediahub_owned(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Status: design/qualification-gated", text)
        self.assertIn("MediaHub remains authoritative", text)
        self.assertIn("ECC agents MUST NOT mutate State Authority directly.", text)
        self.assertIn("ECC agents MUST NOT bypass authorization", text)

    def test_no_wholesale_import_or_default_hooks(self):
        manifest = MANIFEST.read_text(encoding="utf-8")
        self.assertIn("wholesale_source_import: false", manifest)
        self.assertIn("hooks_enabled_by_default: false", manifest)
        self.assertIn("commands_enabled_by_default: false", manifest)

    def test_credentials_are_outside_agent_configuration(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Provider credentials remain outside the repository and outside agent prompts.", text)
        self.assertNotIn("OPENAI_API_KEY", text)
        self.assertNotIn("OPENROUTER_API_KEY", text)
        self.assertNotIn("ANTHROPIC_API_KEY", text)

    def test_required_qualification_is_fail_closed(self):
        manifest = MANIFEST.read_text(encoding="utf-8")
        self.assertIn("fail_closed: true", manifest)
        self.assertIn("release_blocking: true", manifest)
        self.assertIn("independent-review", manifest)


if __name__ == "__main__":
    unittest.main()
