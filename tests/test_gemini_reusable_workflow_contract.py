"""Contract tests for the controller-only Gemini reusable-workflow transport."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILD_PATHS = (
    ROOT / ".github/workflows/gemini-autonomous-engineering.yml",
    ROOT / ".github/workflows/gemini-agent-2.yml",
    ROOT / ".github/workflows/gemini-agent-3.yml",
)
EXPECTED_SECRETS = ("GEMINI_API_KEY", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3")
TRUSTED_CONTROLLER_REF = "VlDMlNSh/mediahub-os/.github/workflows/gemini-batch-dispatch-controller.yml@refs/heads/main"
TRUSTED_GUARD = "github.workflow_ref == '" + TRUSTED_CONTROLLER_REF + "'"


def caller_ref_allowed(event_name: str, workflow_ref: str) -> bool:
    return event_name == "workflow_dispatch" and workflow_ref == TRUSTED_CONTROLLER_REF


def contract_errors(controller: str, children: list[str]) -> list[str]:
    errors = []
    if "workflow_dispatch:" not in controller or "confirm:" not in controller or 'default: "no"' not in controller:
        errors.append("controller must retain explicit manual confirmation")
    if "MEDIAHUB_GITHUB_TOKEN" in controller or "api.github.com/repos/" in controller or "secrets: inherit" in controller:
        errors.append("controller must not use REST child dispatch, transport token, or inherited secrets")
    for name in (
        "gemini-autonomous-engineering.yml",
        "gemini-agent-2.yml",
        "gemini-agent-3.yml",
    ):
        if controller.count(f"uses: ./.github/workflows/{name}") != 1:
            errors.append(f"controller must call {name} exactly once")
    for index, child in enumerate(children):
        if "workflow_call:" not in child:
            errors.append(f"child {index + 1} must expose workflow_call")
        if "workflow_dispatch:" in child:
            errors.append(f"child {index + 1} must not expose workflow_dispatch")
        if "MEDIAHUB_GITHUB_TOKEN" in child or "secrets: inherit" in child:
            errors.append(f"child {index + 1} violates secret isolation")
        if TRUSTED_GUARD not in child:
            errors.append(f"child {index + 1} must pin the trusted controller ref")
        if "contains(github.workflow_ref" in child or "startsWith(github.workflow_ref" in child:
            errors.append(f"child {index + 1} must not use a loose controller-ref predicate")
        if EXPECTED_SECRETS[index] not in child:
            errors.append(f"child {index + 1} must declare its explicit provider secret")
        if "ghcr.io/github/github-mcp-server@sha256:" not in child:
            errors.append(f"child {index + 1} must pin the GitHub MCP server image digest")
        if "ghcr.io/github/github-mcp-server:v0.27.0" in child:
            errors.append(f"child {index + 1} uses a mutable GitHub MCP server tag")
        for line in child.splitlines():
            if "uses:" not in line:
                continue
            if "./.github/workflows/" in line:
                continue
            if not re.search(r"uses:\s+[^\s@]+@[0-9a-f]{40}(?:\s|$)", line):
                errors.append(f"child {index + 1} has a mutable external action ref: {line.strip()}")
    for secret in EXPECTED_SECRETS:
        expected = chr(36) + "{{ secrets." + secret + " }}"
        if expected not in controller:
            errors.append(f"controller must pass {secret} explicitly")
    return errors


class GeminiReusableWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller = CONTROLLER_PATH.read_text(encoding="utf-8")
        cls.children = [path.read_text(encoding="utf-8") for path in CHILD_PATHS]

    def test_current_contract_is_valid(self):
        self.assertEqual(contract_errors(self.controller, self.children), [])

    def test_trusted_controller_context_matrix(self):
        trusted = TRUSTED_CONTROLLER_REF
        self.assertTrue(caller_ref_allowed("workflow_dispatch", trusted))

        untrusted_contexts = (
            ("workflow_call", trusted),
            ("push", trusted),
            ("workflow_dispatch", trusted.replace("@refs/heads/main", "@refs/heads/feature/untrusted")),
            ("workflow_dispatch", trusted.replace("VlDMlNSh/mediahub-os", "attacker/mediahub-os")),
            ("workflow_dispatch", trusted.replace("gemini-batch-dispatch-controller.yml", "gemini-agent-2.yml")),
            ("workflow_dispatch", trusted.replace("@refs/heads/main", "@refs/tags/main")),
        )
        for event_name, workflow_ref in untrusted_contexts:
            with self.subTest(event_name=event_name, workflow_ref=workflow_ref):
                self.assertFalse(caller_ref_allowed(event_name, workflow_ref))

    def test_negative_fixture_rejects_untrusted_controller_ref(self):
        trusted = TRUSTED_CONTROLLER_REF
        untrusted = trusted.replace("@refs/heads/main", "@refs/heads/feature/untrusted")
        bad = list(self.children)
        bad[0] = bad[0].replace(trusted, untrusted)
        self.assertIn("child 1 must pin the trusted controller ref", contract_errors(self.controller, bad))

    def test_negative_fixture_rejects_mutable_action_refs(self):
        bad = list(self.children)
        bad[2] = bad[2].replace(
            "google-github-actions/run-gemini-cli@f77273f4c914e4bf38440cf36a0369cb64a37489",
            "google-github-actions/run-gemini-cli@v0",
        )
        self.assertTrue(any(
            "child 3 has a mutable external action ref" in error
            for error in contract_errors(self.controller, bad)
        ))

    def test_negative_fixture_rejects_mutable_container_tag(self):
        bad = list(self.children)
        bad[0] = bad[0].replace(
            "ghcr.io/github/github-mcp-server@sha256:cbca61d547beec9b819b26bbfe6ac66ba6b373f1d6b64e8291e346bf524633e2",
            "ghcr.io/github/github-mcp-server:v0.27.0",
        )
        errors = contract_errors(self.controller, bad)
        self.assertIn("child 1 must pin the GitHub MCP server image digest", errors)
        self.assertIn("child 1 uses a mutable GitHub MCP server tag", errors)

    def test_negative_fixture_rejects_direct_dispatch(self):
        bad = list(self.children)
        bad[0] = bad[0] + "\non:\n  workflow_dispatch: {}\n"
        self.assertIn("child 1 must not expose workflow_dispatch", contract_errors(self.controller, bad))

    def test_negative_fixture_rejects_inherited_secrets(self):
        bad_controller = self.controller + "\nsecrets: inherit\n"
        self.assertIn("controller must not use REST child dispatch, transport token, or inherited secrets",
                      contract_errors(bad_controller, self.children))

    def test_negative_fixture_rejects_transport_token_leak(self):
        bad = list(self.children)
        bad[1] = bad[1] + "\n# MEDIAHUB_GITHUB_TOKEN\n"
        self.assertIn("child 2 violates secret isolation", contract_errors(self.controller, bad))

    def test_negative_fixture_rejects_untrusted_controller_branch(self):
        bad = list(self.children)
        bad[0] = bad[0].replace(
            TRUSTED_GUARD,
            "github.workflow_ref == 'VlDMlNSh/mediahub-os/.github/workflows/"
            "gemini-batch-dispatch-controller.yml@refs/heads/feature/untrusted'",
        )
        self.assertIn(
            "child 1 must pin the trusted controller ref",
            contract_errors(self.controller, bad),
        )

    def test_negative_fixture_rejects_loose_controller_path_match(self):
        bad = list(self.children)
        bad[2] = bad[2].replace(
            TRUSTED_GUARD,
            "contains(github.workflow_ref, '/.github/workflows/"
            "gemini-batch-dispatch-controller.yml@')",
        )
        errors = contract_errors(self.controller, bad)
        self.assertIn("child 3 must pin the trusted controller ref", errors)
        self.assertIn("child 3 must not use a loose controller-ref predicate", errors)


    def test_controller_jobs_are_all_gated_by_explicit_yes(self):
        import yaml

        controller = yaml.load(CONTROLLER_PATH.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        dispatch = controller.get("on", {}).get("workflow_dispatch", {})
        confirm = dispatch.get("inputs", {}).get("confirm", {})
        self.assertEqual(confirm.get("default"), "no")
        self.assertEqual(confirm.get("options"), ["no", "yes"])
        jobs = controller.get("jobs", {})
        self.assertEqual(set(jobs), {"agent1", "agent2", "agent3", "probe", "assert_probe_context", "summarize"})
        for job_name in ("agent1", "agent2", "agent3"):
            with self.subTest(job=job_name):
                condition = jobs[job_name].get("if", "").replace(" ", "")
                self.assertIn("github.event_name=='workflow_dispatch'", condition)
                self.assertIn("inputs.mode=='agents'", condition)
                self.assertIn("inputs.confirm=='yes'", condition)
        summary_condition = jobs["summarize"].get("if", "").replace(" ", "")
        self.assertIn("always()&&github.event_name=='workflow_dispatch'", summary_condition)
        self.assertIn("inputs.mode=='agents'", summary_condition)
        self.assertIn("inputs.confirm=='yes'", summary_condition)
        self.assertEqual(jobs["probe"]["permissions"], {})
        self.assertEqual(jobs["probe"]["uses"], "./.github/workflows/gemini-reusable-context-probe-wave284.yml")
        self.assertEqual(jobs["assert_probe_context"]["permissions"], {})
        self.assertEqual(jobs["assert_probe_context"]["needs"], ["probe"])

    def test_trusted_caller_guard_is_the_engineer_job_condition(self):
        import yaml

        required_guards = (
            "inputs.probe_only != true",
            "needs.caller_context.outputs.trusted_controller == 'true'",
            "github.event_name == 'workflow_dispatch'",
            "github.workflow_ref == '" + TRUSTED_CONTROLLER_REF + "'",
        )
        for index, path in enumerate(CHILD_PATHS):
            with self.subTest(child=index + 1):
                workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
                engineer = workflow.get("jobs", {}).get("engineer", {})
                condition = " ".join(engineer.get("if", "").split())
                for guard in required_guards:
                    with self.subTest(guard=guard):
                        self.assertIn(
                            guard,
                            condition,
                            "engineer must be gated by probe mode, observed trusted-caller result, event, and exact controller ref",
                        )
                self.assertEqual(
                    engineer.get("needs"),
                    ["caller_context", "reject_untrusted_caller"],
                    "engineer must depend on caller-context observation and fail-closed caller rejection",
                )


if __name__ == "__main__":
    unittest.main()
