"""Contract tests for the controller-only Gemini reusable-workflow transport."""
from pathlib import Path
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

    def test_negative_fixture_rejects_untrusted_controller_ref(self):
        trusted = TRUSTED_CONTROLLER_REF
        untrusted = trusted.replace("@refs/heads/main", "@refs/heads/feature/untrusted")
        self.assertTrue(caller_ref_allowed("workflow_dispatch", trusted))
        self.assertFalse(caller_ref_allowed("workflow_dispatch", untrusted))
        self.assertFalse(caller_ref_allowed("workflow_call", trusted))
        bad = list(self.children)
        bad[0] = bad[0].replace(trusted, untrusted)
        self.assertIn("child 1 must pin the trusted controller ref", contract_errors(self.controller, bad))

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


if __name__ == "__main__":
    unittest.main()
