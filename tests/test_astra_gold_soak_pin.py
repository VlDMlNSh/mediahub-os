import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOAK = ROOT / ".github" / "workflows" / "astra-gold-24h-soak.yml"
LITERAL_PIN = re.compile(r'test "\$blob_sha" = "[0-9a-f]{40}"')


class SoakAgentBindingTests(unittest.TestCase):
    """The soak must bind to the exact agent it runs, not to a stale constant.

    A hardcoded agent blob literal cannot be maintained while the Astra agent is
    continuously updated on main, and it produced guaranteed drift (main's own
    pin diverged from main's agent). Worker identity is instead bound by
    ops/qualification/verify_transport_health.py, which compares the worker's
    reported agent_source_sha against the actual agent bytes.
    """

    def setUp(self):
        self.text = SOAK.read_text(encoding="utf-8")

    def test_preflight_derives_and_records_the_live_agent_blob(self):
        self.assertIn("git hash-object astra_github_agent.py", self.text)
        self.assertIn('echo "agent_blob_sha=$blob_sha"', self.text)

    def test_no_hardcoded_agent_blob_literal(self):
        self.assertIsNone(
            LITERAL_PIN.search(self.text),
            "a hardcoded agent blob literal reintroduces soak pin drift",
        )


if __name__ == "__main__":
    unittest.main()
