import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTER = ROOT / ".github" / "ai" / "model-router.yml"
CONTROLLER = ROOT / ".github" / "workflows" / "gemini-batch-dispatch-controller.yml"
FCC_CONTROLLER = ROOT / ".github" / "workflows" / "mediahub-fcc-free-claude-worker.yml"


class ExecutorRoutingPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.router = ROUTER.read_text(encoding="utf-8")
        cls.controller = CONTROLLER.read_text(encoding="utf-8")

    def test_gemini_cloud_transport_is_controller_only(self):
        self.assertIn("permitted_cloud_agent_transports:", self.router)
        self.assertIn(
            "  - .github/workflows/gemini-batch-dispatch-controller.yml",
            self.router,
        )
        self.assertIn(
            "  - .github/workflows/mediahub-fcc-free-claude-worker.yml",
            self.router,
        )
        self.assertIn("permitted_cloud_agent_transport_allowlist_only: true", self.router)
        self.assertIn("secrets.MEDIAHUB_GITHUB_TOKEN", self.controller)
        self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", self.controller)

    def test_local_claude_route_uses_ollama_llama_on_approved_third_host(self):
        self.assertIn("local_claude_runtime: fcc_ollama", self.router)
        self.assertIn("local_claude_model: llama3.2:3b", self.router)
        self.assertIn("local_claude_host: Voktors-Mini.Dlink", self.router)
        self.assertIn("local_claude_only: true", self.router)

    def test_cloud_claude_route_is_free_only_and_admission_gated(self):
        self.assertIn("cloud_claude_runtime: fcc_openrouter_free", self.router)
        self.assertIn(
            "cloud_claude_transport: .github/workflows/mediahub-fcc-free-claude-worker.yml",
            self.router,
        )
        self.assertIn("cloud_claude_free_only: true", self.router)
        fcc = FCC_CONTROLLER.read_text(encoding="utf-8")
        self.assertIn('SOURCE_REF" == "refs/heads/main"', fcc)
        self.assertIn('TRIGGER_ACTOR" == "$REPO_OWNER"', fcc)
        self.assertIn('TARGET_SHA" == "$CURRENT_SHA"', fcc)
        self.assertIn('endswith(":free")', fcc)
        self.assertIn("@anthropic-ai/claude-code@2.1.282", fcc)

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
