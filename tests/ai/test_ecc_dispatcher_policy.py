import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
POLICY = ROOT / "oss" / "adapters" / "ecc" / "dispatcher-policy.yaml"


class EccDispatcherPolicyTests(unittest.TestCase):
    def setUp(self):
        self.text = POLICY.read_text(encoding="utf-8")

    def test_policy_is_fail_closed_and_target_gated(self):
        self.assertIn("status: target-gated", self.text)
        self.assertIn("fail_closed: true", self.text)

    def test_unknown_and_unlisted_agents_are_blocked(self):
        self.assertIn("unknown_agent: blocked", self.text)
        self.assertIn("unlisted_agent: blocked", self.text)

    def test_ecc_unavailable_is_degraded(self):
        self.assertIn("ecc_unavailable: degraded", self.text)

    def test_all_initial_roles_are_advisory(self):
        for role in (
            "planner",
            "architect",
            "spec-miner",
            "tdd-guide",
            "code-reviewer",
            "security-reviewer",
            "agent-architecture-audit",
        ):
            self.assertIn(f"  {role}:", self.text)
        self.assertIn("authority: advisory", self.text)

    def test_agents_cannot_gain_authority(self):
        for needle in (
            "state_authority_mutation_from_agent: false",
            "provider_selection_authority_from_agent: false",
            "release_authorization_from_agent: false",
            "production_authorization_from_agent: false",
            "direct_state_authority_mutation: false",
        ):
            self.assertIn(needle, self.text)

    def test_mutation_requires_mediahub_verification(self):
        self.assertIn("mutation_requires_reviewable_mediahub_change: true", self.text)
        self.assertIn("mutation_requires_verification: true", self.text)
        self.assertIn("mutation_requires_existing_release_gates: true", self.text)
        self.assertIn("production_authorization: human", self.text)


if __name__ == "__main__":
    unittest.main()
