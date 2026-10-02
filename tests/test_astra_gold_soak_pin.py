import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOAK = ROOT / ".github" / "workflows" / "astra-gold-24h-soak.yml"
AGENT = ROOT / "astra_github_agent.py"
PIN_RE = re.compile(r'test "\$blob_sha" = "([0-9a-f]{40})"')


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = ("blob " + str(len(data)) + "\0").encode()
    return hashlib.sha1(header + data).hexdigest()


class SoakPinTests(unittest.TestCase):
    def test_soak_preflight_pin_matches_committed_agent(self):
        match = PIN_RE.search(SOAK.read_text(encoding="utf-8"))
        self.assertIsNotNone(
            match, "astra-gold-24h-soak.yml must pin the canonical agent blob"
        )
        self.assertEqual(
            match.group(1),
            git_blob_sha(AGENT),
            "soak pin drift: re-freeze the pin in the same change that edits "
            "astra_github_agent.py",
        )


if __name__ == "__main__":
    unittest.main()
