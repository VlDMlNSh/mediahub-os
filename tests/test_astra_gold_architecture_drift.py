import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).parents[1]
REF = ROOT / "architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md"
QUAL = ROOT / "architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml"
UNIFIED = ROOT / "architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml"

EXPECTED_PATHS = [
    "CODEX_FCC",
    "CLAUDE_FCC",
    "CODEX_OMNIROUTE",
    "CLAUDE_OMNIROUTE",
    "CLAUDE_CODE_DIRECT",
]
EXPECTED_GATES = [
    "G0_IDENTITY", "G1_BOUNDARY", "G2_CONTROL_PLANE", "G3_EXECUTION_PATH",
    "G4_23_WAVE_QUALIFICATION", "G5_CONCURRENCY", "G6_RECOVERY",
    "G7_INTEGRATED_A3", "G8_PRE_SOAK", "G9_24H_SOAK",
    "G10_LAUNCH_READY", "G11_LAUNCH",
]


class TestAstraGoldArchitectureDrift(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref = REF.read_text(encoding="utf-8")
        cls.qual = yaml.safe_load(QUAL.read_text(encoding="utf-8"))
        cls.unified = yaml.safe_load(UNIFIED.read_text(encoding="utf-8"))

    def test_canonical_sources_are_explicit(self):
        u = self.unified
        self.assertEqual(u["version"], 1.1)
        self.assertEqual(
            u["reference_architecture"],
            "architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md",
        )
        self.assertEqual(
            u["qualification_contract"],
            "architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml",
        )
        self.assertEqual(u["contract_alignment"], "CANONICAL_SEMANTIC_ALIGNMENT")
        self.assertEqual(u["reconciliation"]["contract_version"], 2)
        self.assertEqual(
            u["reconciliation"]["canonical_sources"],
            [
                "architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md",
                "architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml",
                "architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml",
            ],
        )

    def test_authority_and_fail_closed_contract_cannot_drift(self):
        q = self.qual["authority"]
        u = self.unified["authority"]
        self.assertEqual(q["final"], "HUMAN")
        self.assertEqual(q["coordination"], "A0-ASTRA")
        self.assertEqual(q["architecture"], "A1")
        self.assertEqual(q["implementation"], "A2")
        self.assertEqual(q["independent_verification"], "A3")
        self.assertEqual(q["executor_authority"], "EXECUTOR_ONLY")
        self.assertEqual(q["state_authority"], "A0-ASTRA")
        self.assertEqual(u["human"]["role"], "final_architecture_production_security_authority")
        self.assertEqual(u["astra"]["role"], "single_coordination_authority")
        self.assertEqual(u["architect"]["role"], "architecture_contracts")
        self.assertEqual(u["builder"]["role"], "bounded_implementation")
        self.assertEqual(u["verifier"]["role"], "independent_verification")
        self.assertTrue(self.qual["principles"]["fail_closed"])
        self.assertTrue(u["qualification"]["fail_closed"])
        self.assertTrue(u["rules"]["missing_or_contradictory_evidence_blocks"])

    def test_gate_and_executor_contracts_are_identical(self):
        q = self.qual["gates"]
        self.assertEqual(list(q), EXPECTED_GATES)
        self.assertEqual(
            q["G4_23_WAVE_QUALIFICATION"]["mandatory_paths"],
            EXPECTED_PATHS,
        )
        self.assertEqual(q["G4_23_WAVE_QUALIFICATION"]["minimum_rounds_per_mandatory_path"], 23)
        self.assertEqual(u := self.unified["qualification"]["rounds_minimum"], 23)
        self.assertEqual(
            self.unified["execution"]["mandatory_paths"],
            EXPECTED_PATHS,
        )
        self.assertEqual(
            self.unified["qualification"]["gate_contract"],
            EXPECTED_GATES,
        )

    def test_lifecycle_and_reconciliation_contract_are_present(self):
        q = self.qual
        u = self.unified
        self.assertEqual(
            q["lifecycle"],
            [
                "DISCOVER", "PREFLIGHT", "ADMIT", "QUALIFY", "EXECUTE",
                "VERIFY", "INTEGRATE", "RECONCILE", "PRE_SOAK",
                "SOAK_24H", "LAUNCH_READY", "LAUNCHED", "BLOCKED", "ROLLBACK",
            ],
        )
        for state in ["RECONCILIATION", "RECONCILIATION_REQUIRED", "BLOCKED", "FAILED"]:
            self.assertIn(state, u["states"])
        checks = u["reconciliation"]["checks"]
        required = [
            "architecture_vs_implementation",
            "registry_vs_runtime_identity",
            "state_vs_evidence",
            "tested_sha_vs_source_sha",
            "provider_model_identity_vs_evidence",
            "qualification_state_vs_gate_state",
            "candidate_admission_vs_inventory",
            "control_plane_vs_worker_state",
            "evidence_completeness",
        ]
        self.assertEqual(checks, required)
        self.assertEqual(u["reconciliation"]["failure_state"], "RECONCILIATION_REQUIRED")
        self.assertEqual(u["reconciliation"]["admission_rule"], "any_drift_or_ambiguity_blocks")

    def test_launch_and_evidence_invariants_cannot_drift(self):
        q = self.qual
        u = self.unified
        self.assertTrue(q["principles"]["self_qualification"] is False)
        self.assertTrue(q["principles"]["self_promotion"] is False)
        self.assertTrue(q["principles"]["launch_without_a3"] is False)
        self.assertTrue(q["principles"]["launch_without_recovery"] is False)
        self.assertTrue(q["principles"]["launch_without_soak"] is False)
        self.assertEqual(q["launch_contract"]["decision"], "HUMAN_ONLY")
        self.assertTrue(q["gates"]["G11_LAUNCH"]["human_authorization_required"])
        self.assertTrue(u["rules"]["gold_active_requires_human_launch"])
        self.assertTrue(u["rules"]["evidence_is_immutable"])
        self.assertTrue(u["qualification"]["fresh_evidence_required"])
        self.assertFalse(u["qualification"]["historical_evidence_reuse"])
        self.assertEqual(
            q["promotion"]["states"],
            [
                "REGISTERED", "CREDENTIAL_PRESENT", "AUTH_SUCCESS",
                "MODEL_DISCOVERY_PASS", "PROBE_PASS", "EXECUTION_PASS",
                "RESULT_VALIDATION_PASS", "A3_VERIFIED", "ASTRA_GOLD_ELIGIBLE",
                "LAUNCH_READY", "LAUNCHED",
            ],
        )
        self.assertEqual(
            self.unified["evidence"],
            [
                "command_id", "node_id", "component_id", "executor_id",
                "provider_or_model_id", "transport_id", "source_sha", "round",
                "timestamp", "exit_status", "timeout", "marker", "workspace",
                "verification_status", "evidence_digest",
            ],
        )

    def test_reference_architecture_contains_reconciliation_and_launch_guards(self):
        self.assertIn("Reconciliation Contract", self.ref)
        self.assertIn("RECONCILIATION_REQUIRED", self.ref)
        self.assertIn("GOLD_ACTIVE", self.ref)
        self.assertIn("Human launch authorization", self.ref)
        self.assertIn("24H SOAK", self.ref)


if __name__ == "__main__":
    unittest.main()
