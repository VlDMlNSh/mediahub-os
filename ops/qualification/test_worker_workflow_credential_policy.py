"""Static regression tests for the distributed worker's checkout credential policy.

These tests do not dispatch workflows, access credentials, or execute a worker.
Run with: python -m unittest ops.qualification.test_worker_workflow_credential_policy
"""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "astra-distributed-local-worker.yml"


class WorkerWorkflowCredentialPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_does_not_grant_repository_write_permission(self):
        permissions = re.search(
            r"(?m)^permissions:\n((?:^[ \t]+[^\n]*\n)+)", self.source
        )
        self.assertIsNotNone(permissions, "workflow permissions block must be explicit")
        self.assertRegex(permissions.group(1), r"(?m)^  contents: read\s*$")
        self.assertNotRegex(permissions.group(1), r"(?m)^  contents: write\s*$")

    def test_every_checkout_disables_persisted_credentials(self):
        checkout_blocks = re.findall(
            r"(?ms)^      - uses: actions/checkout@[^\n]+\n(.*?)(?=^      - |^  [a-zA-Z0-9_-]+:|\Z)",
            self.source,
        )
        self.assertGreaterEqual(len(checkout_blocks), 1, "expected checkout steps")
        for index, block in enumerate(checkout_blocks, start=1):
            with self.subTest(checkout=index):
                self.assertRegex(
                    block,
                    r"(?m)^          persist-credentials: false\s*$",
                    "every checkout must explicitly disable persisted credentials",
                )
                self.assertNotRegex(block, r"(?m)^          persist-credentials: true\s*$")

    def test_workflow_has_no_repository_write_permission_marker(self):
        self.assertNotRegex(self.source, r"(?m)^  contents: write\s*$")


if __name__ == "__main__":
    unittest.main()
