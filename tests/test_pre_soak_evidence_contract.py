import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "ops" / "qualification" / "verify_pre_soak_bundle.py"
FILES = (
    "transport-health.json",
    "runtime-e2e.json",
    "scheduler-e2e.json",
    "fencing.json",
    "recovery.json",
    "backup-restore.json",
    "provider-model.json",
)


class PreSoakEvidenceContractTests(unittest.TestCase):
    def write_bundle(self, root: Path, *, captured_at=None, target_sha="a" * 40, node_id="mh-dev-01"):
        for name in FILES:
            payload = {
                "schema": "mediahub.pre-soak-evidence.v1",
                "status": "PASS",
                "captured_at": int(time.time() if captured_at is None else captured_at),
                "target_sha": target_sha,
                "node_id": node_id,
            }
            (root / name).write_text(json.dumps(payload), encoding="utf-8")

    def run_verify(self, root: Path):
        return subprocess.run(
            [sys.executable, str(VERIFY), str(root),
             "--target-sha", "a" * 40, "--node-id", "mh-dev-01"],
            text=True, capture_output=True, check=False,
        )

    def test_fresh_exact_sha_and_node_bound_bundle_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_bundle(root)
            result = self.run_verify(root)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_stale_bundle_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_bundle(root, captured_at=int(time.time()) - 901)
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("stale", result.stderr)

    def test_wrong_sha_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_bundle(root, target_sha="b" * 40)
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("target_sha mismatch", result.stderr)

    def test_wrong_node_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_bundle(root, node_id="mh-dev-02")
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("node_id mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
