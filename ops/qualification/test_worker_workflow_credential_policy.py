"""Static regression tests for the distributed worker's checkout credential policy.

These tests do not dispatch workflows, access credentials, or execute a worker.
Run with: python -m unittest ops.qualification.test_worker_workflow_credential_policy
"""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "astra-distributed-local-worker.yml"


def policy_violations(source):
    """Return policy violations for source text; safe for synthetic mutation fixtures."""
    violations = []
    permissions = re.search(
        r"(?m)^permissions:\n((?:^[ \t]+[^\n]*\n)+)", source
    )
    if permissions is None:
        violations.append("workflow permissions block must be explicit")
    else:
        block = permissions.group(1)
        if not re.search(r"(?m)^  contents: read\s*$", block):
            violations.append("workflow must explicitly set contents: read")
        if re.search(r"(?m)^  contents: write\s*$", block):
            violations.append("workflow must not grant contents: write")

    checkout_blocks = re.findall(
        r"(?ms)^      - uses: actions/checkout@[^\n]+\n(.*?)(?=^      - |^  [a-zA-Z0-9_-]+:|\Z)",
        source,
    )
    if len(checkout_blocks) != 3:
        violations.append(
            f"expected exactly three checkout steps, found {len(checkout_blocks)}"
        )
    for index, block in enumerate(checkout_blocks, start=1):
        if not re.search(
            r"(?m)^          persist-credentials: false\s*$", block
        ):
            violations.append(
                f"checkout {index} must set persist-credentials: false"
            )
        if re.search(
            r"(?m)^          persist-credentials: true\s*$", block
        ):
            violations.append(
                f"checkout {index} must not persist credentials"
            )
    if re.search(r"(?m)^  contents: write\s*$", source):
        violations.append("workflow must not contain top-level contents: write")
    return violations


class WorkerWorkflowCredentialPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_current_workflow_satisfies_credential_policy(self):
        self.assertEqual([], policy_violations(self.source))

    def test_rejects_synthetic_write_permission_regression(self):
        marker = "\n  contents: read\n"
        self.assertIn(marker, self.source, "fixture must target current permission")
        mutated = self.source.replace(marker, "\n  contents: write\n", 1)
        violations = policy_violations(mutated)
        self.assertIn(
            "workflow must explicitly set contents: read", violations
        )
        self.assertIn("workflow must not grant contents: write", violations)

    def test_rejects_synthetic_persisted_checkout_credential_regression(self):
        marker = "          persist-credentials: false"
        self.assertIn(marker, self.source, "fixture must target current checkout policy")
        mutated = self.source.replace(marker, "          persist-credentials: true")
        violations = policy_violations(mutated)
        self.assertGreaterEqual(
            sum("must not persist credentials" in item for item in violations),
            1,
        )
        self.assertGreaterEqual(
            sum("must set persist-credentials: false" in item for item in violations),
            1,
        )

    def test_rejects_missing_checkout_steps(self):
        checkout_pattern = re.compile(
            r"(?ms)^      - uses: actions/checkout@[^\n]+\n.*?"
            r"(?=^      - |^  [a-zA-Z0-9_-]+:|\Z)"
        )
        matches = list(checkout_pattern.finditer(self.source))
        self.assertEqual(3, len(matches), "fixture must start with three checkout steps")
        mutated = self.source
        for match in reversed(matches[1:]):
            mutated = mutated[:match.start()] + mutated[match.end():]
        self.assertEqual(1, len(checkout_pattern.findall(mutated)))
        violations = policy_violations(mutated)
        self.assertTrue(
            any("expected exactly three checkout steps" in item for item in violations),
            violations,
        )


if __name__ == "__main__":
    unittest.main()
