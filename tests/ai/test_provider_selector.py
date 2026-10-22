import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTER = ROOT / ".github" / "ai" / "model-router.yml"
CONTROLLER = ROOT / ".github" / "workflows" / "gemini-batch-dispatch-controller.yml"


class ExecutorRoutingPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.router = ROUTER.read_text(encoding="utf-8")
        cls.controller = CONTROLLER.read_text(encoding="utf-8")

    def test_gemini_cloud_transport_is_controller_only(self):
        self.assertIn(
            "permitted_cloud_agent_transport: .github/workflows/gemini-batch-dispatch-controller.yml",
            self.router,
        )
        self.assertIn("permitted_cloud_agent_transport_only: true", self.router)
        self.assertIn("secrets.MEDIAHUB_GITHUB_TOKEN", self.controller)
        self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", self.controller)

    def test_claude_is_local_ollama_only(self):
        self.assertIn("local_claude_runtime: ollama", self.router)
        self.assertIn("local_claude_host: Alamo", self.router)
        self.assertIn("local_claude_only: true", self.router)

    def test_paid_and_unapproved_fallbacks_are_disabled(self):
        self.assertIn("paid_fallback: false", self.router)
        self.assertIn("unknown_route_behavior: fail_closed", self.router)
        for forbidden in (
            "api.openai.com",
            "api.anthropic.com",
            "generativelanguage.googleapis.com",
            "openrouter.ai",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GEMINI_API_KEY",
            "OPENROUTER_API_KEY",
        ):
            self.assertNotIn(forbidden, self.router)

    def test_direct_provider_smoke_workflows_are_absent(self):
        for path in (
            ".github/workflows/mediahub-openai-smoke.yml",
            ".github/workflows/mediahub-anthropic-smoke.yml",
            ".github/workflows/mediahub-gemini-smoke.yml",
            ".github/workflows/mediahub-openrouter-smoke.yml",
        ):
            self.assertFalse((ROOT / path).exists(), path)

    def test_unknown_routes_fail_closed_and_human_release_gate_remains(self):
        self.assertIn("unknown_route_behavior: fail_closed", self.router)
        self.assertIn("production_authorization: human", self.router)


if __name__ == "__main__":
    unittest.main()
