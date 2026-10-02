"""Tests for the ASTRA GOLD governance contract and generated current-truth.

These lock the strengthening measures added after the reference-scheme review:
a single gate registry, numeric thresholds, invariant enforcement, credential
lifecycle, the human approval record and the cloud-executor extension.
"""

import copy
import unittest
from pathlib import Path

import yaml

from ops.qualification.render_current_truth import render
from ops.qualification.verify_astra_gold_governance import verify

ROOT = Path(__file__).parents[1]
GOVERNANCE = ROOT / "architecture" / "ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml"
QUALIFICATION = ROOT / "architecture" / "ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml"
UNIFIED = ROOT / "architecture" / "ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml"
REFERENCE = ROOT / "architecture" / "ASTRA-GOLD-REFERENCE-ARCHITECTURE.md"
CURRENT_TRUTH = ROOT / "docs" / "qualification" / "CURRENT-TRUTH.generated.md"


def _load():
    governance = yaml.safe_load(GOVERNANCE.read_text(encoding="utf-8"))
    qualification = yaml.safe_load(QUALIFICATION.read_text(encoding="utf-8"))
    unified = yaml.safe_load(UNIFIED.read_text(encoding="utf-8"))
    reference = REFERENCE.read_text(encoding="utf-8")
    return governance, qualification, unified, reference


class GovernanceContractTests(unittest.TestCase):
    def test_contract_validates(self):
        governance, qualification, unified, reference = _load()
        result = verify(governance, qualification, unified, reference, ROOT)
        self.assertEqual(result["failures"], [])
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["gates"], 12)

    def test_gate_registry_matches_canonical_sources(self):
        governance, qualification, unified, _ = _load()
        registry = [gate["id"] for gate in governance["gate_registry"]["gates"]]
        self.assertEqual(registry, list(qualification["gates"]))
        self.assertEqual(registry, list(unified["qualification"]["gate_contract"]))

    def test_thresholds_are_positive_and_mirror_gates(self):
        governance, qualification, _unified, _ = _load()
        thresholds = governance["runtime_thresholds"]
        self.assertGreater(thresholds["heartbeat_ttl_seconds"], 0)
        self.assertGreater(thresholds["lease_ttl_seconds"], 0)
        self.assertGreater(thresholds["executor_timeout_seconds"], 0)
        self.assertEqual(
            thresholds["max_parallel_autonomous_claims"],
            qualification["gates"]["G5_CONCURRENCY"]["max_parallel_autonomous_claims"],
        )
        self.assertEqual(
            thresholds["soak_duration_hours"],
            qualification["gates"]["G9_24H_SOAK"]["duration_hours"],
        )

    def test_every_invariant_is_bound_to_an_existing_test(self):
        governance, _, _, _ = _load()
        invariants = governance["invariant_registry"]["invariants"]
        self.assertGreaterEqual(len(invariants), 16)
        for invariant in invariants:
            self.assertTrue((ROOT / invariant["enforced_by"]).exists(), invariant["id"])

    def test_credential_lifecycle_is_fail_closed(self):
        governance, _, _, _ = _load()
        lifecycle = governance["credential_lifecycle"]
        self.assertFalse(lifecycle["credentials_in_git"])
        self.assertFalse(lifecycle["credentials_in_evidence"])
        self.assertTrue(lifecycle["rotation_required"])
        self.assertTrue(lifecycle["revocation_supported"])
        self.assertTrue(lifecycle["audit_required"])

    def test_human_approval_record_covers_launch_inputs(self):
        governance, qualification, _, _ = _load()
        approval = governance["human_approval_record"]
        self.assertEqual(approval["decision_authority"], "HUMAN_ONLY")
        self.assertTrue(approval["unsigned_approval_rejected"])
        self.assertEqual(
            approval["covers_launch_inputs"],
            qualification["launch_contract"]["required_inputs"],
        )

    def test_cloud_executor_candidates_carry_no_authority(self):
        governance, _, _, _ = _load()
        classes = governance["executor_classes"]
        self.assertEqual(
            classes["mandatory_execution_paths"],
            ["CODEX_FCC", "CLAUDE_FCC", "CODEX_OMNIROUTE", "CLAUDE_OMNIROUTE", "CLAUDE_CODE_DIRECT"],
        )
        candidates = classes["candidate_cloud_executor_paths"]
        self.assertTrue(candidates)
        for candidate in candidates:
            self.assertEqual(candidate["authority"], "none")
            self.assertEqual(candidate["status"], "NOT_PROVEN")
        rules = classes["rules"]
        self.assertEqual(rules["executor_authority"], "EXECUTOR_ONLY")
        self.assertTrue(rules["gateway_path_is_not_native_provider_qualification"])
        self.assertTrue(rules["no_cloud_executor_authority"])

    def test_tampered_governance_is_rejected(self):
        governance, qualification, unified, reference = _load()
        tampered = copy.deepcopy(governance)
        tampered["runtime_thresholds"]["max_parallel_autonomous_claims"] = 99
        result = verify(tampered, qualification, unified, reference, ROOT)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("max_parallel_autonomous_claims" in f for f in result["failures"]))

    def test_tampered_gate_name_is_rejected(self):
        governance, qualification, unified, reference = _load()
        tampered = copy.deepcopy(governance)
        tampered["gate_registry"]["gates"][0]["name"] = "WrongName"
        result = verify(tampered, qualification, unified, reference, ROOT)
        self.assertEqual(result["status"], "FAIL")

    def test_generated_current_truth_is_up_to_date(self):
        governance, _, _, _ = _load()
        expected = render(governance, None)
        self.assertTrue(CURRENT_TRUTH.exists(), "CURRENT-TRUTH.generated.md is missing")
        self.assertEqual(CURRENT_TRUTH.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
