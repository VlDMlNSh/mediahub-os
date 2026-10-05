import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_LABEL = "mh-dev-01-canonical"
WORKFLOWS = (
    ROOT / ".github/workflows/astra-autonomous-supervisor.yml",
    ROOT / ".github/workflows/astra-gold-24h-soak.yml",
)


class CanonicalRunnerRoutingTests(unittest.TestCase):
    def test_canonical_workflows_use_unique_runner_label(self):
        for workflow in WORKFLOWS:
            text = workflow.read_text(encoding="utf-8")
            self.assertIn(CANONICAL_LABEL, text, workflow.name)
            self.assertNotIn("runs-on: [self-hosted, linux, x64]", text, workflow.name)
            self.assertNotIn("runs-on: [self-hosted, mediahub-runner]", text, workflow.name)

if __name__ == "__main__":
    unittest.main()
