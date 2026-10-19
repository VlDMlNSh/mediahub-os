"""Semantic regression tests for the distributed worker checkout credential policy.

These tests parse YAML and never dispatch a workflow or access credentials.
Run with: python -m unittest ops.qualification.test_worker_workflow_credential_policy
"""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "astra-distributed-local-worker.yml"


def _permission_value_is_write(value):
    """Recognize GitHub Actions write permission values after YAML parsing."""
    return isinstance(value, str) and value.strip().lower() == "write"


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys instead of silently overriding them."""


def _construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                None, None, "mapping keys must be hashable", key_node.start_mark
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate mapping key {key!r}", key_node.start_mark
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def policy_violations(source):
    """Return policy violations based on parsed GitHub Actions workflow structure."""
    violations = []
    try:
        workflow = yaml.load(source, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        return [f"workflow YAML must parse successfully: {exc}"]

    if not isinstance(workflow, dict):
        return ["workflow document must be a YAML mapping"]

    permissions = workflow.get("permissions")
    if not isinstance(permissions, dict):
        violations.append("workflow permissions must be an explicit mapping")
    else:
        contents = permissions.get("contents")
        if not isinstance(contents, str) or contents.strip().lower() != "read":
            violations.append("workflow must explicitly set contents: read")
        if any(_permission_value_is_write(value) for value in permissions.values()):
            violations.append("workflow must not grant write permissions")
        if isinstance(permissions, str) and permissions.strip().lower() == "write-all":
            violations.append("workflow must not grant write-all permissions")

    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        violations.append("workflow must define a non-empty jobs mapping")
        jobs = {}

    checkout_steps = []
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            violations.append(f"job {job_name!r} must be a mapping")
            continue

        job_permissions = job.get("permissions")
        if isinstance(job_permissions, str):
            if job_permissions.strip().lower() == "write-all":
                violations.append(f"job {job_name!r} must not grant write-all permissions")
        elif job_permissions is not None:
            if not isinstance(job_permissions, dict):
                violations.append(f"job {job_name!r} permissions must be a mapping")
            elif any(_permission_value_is_write(value) for value in job_permissions.values()):
                violations.append(f"job {job_name!r} must not grant write permissions")

        steps = job.get("steps", [])
        if not isinstance(steps, list):
            violations.append(f"job {job_name!r} steps must be a list")
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            if isinstance(uses, str) and uses.split("@", 1)[0].lower() == "actions/checkout":
                checkout_steps.append((job_name, step))

    if len(checkout_steps) != 3:
        violations.append(f"expected exactly three checkout steps, found {len(checkout_steps)}")

    for index, (job_name, step) in enumerate(checkout_steps, start=1):
        with_config = step.get("with", {})
        if not isinstance(with_config, dict):
            violations.append(f"checkout {index} in job {job_name!r} must have a 'with' mapping")
            continue
        persist = with_config.get("persist-credentials")
        if persist is not False:
            violations.append(
                f"checkout {index} in job {job_name!r} must set persist-credentials: false"
            )

    return violations


class WorkerWorkflowCredentialPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_current_workflow_satisfies_credential_policy(self):
        self.assertEqual([], policy_violations(self.source))

    def test_rejects_workflow_level_write_permission(self):
        mutated = self.source.replace("  contents: read", "  contents: write", 1)
        violations = policy_violations(mutated)
        self.assertTrue(any("workflow must explicitly set contents: read" in item for item in violations))
        self.assertTrue(any("workflow must not grant write permissions" in item for item in violations))

    def test_rejects_job_level_block_write_permission(self):
        marker = "  mh-dev-01-claude:\n"
        self.assertIn(marker, self.source)
        mutated = self.source.replace(marker, marker + "    permissions:\n      contents: write\n", 1)
        self.assertTrue(any("must not grant write permissions" in item for item in policy_violations(mutated)))

    def test_rejects_job_level_flow_style_write_permission(self):
        marker = "  mh-dev-01-claude:\n"
        self.assertIn(marker, self.source)
        mutated = self.source.replace(marker, marker + "    permissions: { contents: write }\n", 1)
        self.assertTrue(any("must not grant write permissions" in item for item in policy_violations(mutated)))

    def test_rejects_quoted_job_level_write_permission(self):
        marker = "  mh-dev-01-claude:\n"
        self.assertIn(marker, self.source)
        mutated = self.source.replace(marker, marker + "    permissions:\n      contents: 'write'\n", 1)
        self.assertTrue(any("must not grant write permissions" in item for item in policy_violations(mutated)))

    def test_rejects_write_all_permissions(self):
        marker = "  mh-dev-01-claude:\n"
        self.assertIn(marker, self.source)
        mutated = self.source.replace(marker, marker + "    permissions: write-all\n", 1)
        self.assertTrue(any("write-all" in item for item in policy_violations(mutated)))

    def test_rejects_persisted_checkout_credentials(self):
        marker = "          persist-credentials: false"
        self.assertIn(marker, self.source)
        mutated = self.source.replace(marker, "          persist-credentials: true", 1)
        self.assertTrue(any("persist-credentials: false" in item for item in policy_violations(mutated)))

    def test_rejects_missing_checkout_steps(self):
        marker = "      - uses: actions/checkout@v4"
        self.assertEqual(3, self.source.count(marker))
        mutated = self.source.replace(marker, "      - uses: actions/checkout@v4 # removed by mutation", 1)
        # Mutating a comment does not remove a step; instead remove one complete checkout block.
        import re
        mutated = re.sub(
            r"(?ms)^      - uses: actions/checkout@[^\n]+\n.*?(?=^      - |^  [a-zA-Z0-9_-]+:|\Z)",
            "",
            self.source,
            count=1,
        )
        self.assertTrue(any("expected exactly three checkout steps" in item for item in policy_violations(mutated)))

    def test_rejects_duplicate_workflow_permission_keys(self):
        duplicate = self.source.replace(
            "permissions:\n  contents: read",
            "permissions:\n  contents: read\n  contents: write",
            1,
        )
        self.assertTrue(any("YAML must parse" in item for item in policy_violations(duplicate)))

    def test_rejects_duplicate_job_permission_keys(self):
        marker = "  mh-dev-01-claude:\n"
        duplicate = self.source.replace(
            marker,
            marker + "    permissions:\n      contents: read\n      contents: write\n",
            1,
        )
        self.assertTrue(any("YAML must parse" in item for item in policy_violations(duplicate)))

    def test_rejects_invalid_yaml(self):
        self.assertTrue(any("YAML must parse" in item for item in policy_violations("permissions: [broken")))


if __name__ == "__main__":
    unittest.main()
