import unittest
from pathlib import Path
import yaml

SCHEMA = Path("architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml")

class TestAstraGoldQualificationLaunchSchema(unittest.TestCase):
    @classmethod
    def load(cls):
        return yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))

    def test_canonical_gate_order_and_fail_closed(self):
        data = self.load()
        self.assertEqual(list(data["gates"]), [
            "G0_IDENTITY", "G1_BOUNDARY", "G2_CONTROL_PLANE", "G3_EXECUTION_PATH",
            "G4_23_WAVE_QUALIFICATION", "G5_CONCURRENCY", "G6_RECOVERY",
            "G7_INTEGRATED_A3", "G8_PRE_SOAK", "G9_24H_SOAK",
            "G10_LAUNCH_READY", "G11_LAUNCH"
        ])
        self.assertTrue(data["principles"]["fail_closed"])
        self.assertFalse(data["principles"]["launch_without_a3"])
        self.assertFalse(data["principles"]["launch_without_soak"])

    def test_mandatory_executor_matrix_is_exactly_defined(self):
        q = self.load()["gates"]["G4_23_WAVE_QUALIFICATION"]
        self.assertEqual(q["mandatory_paths"], [
            "CODEX_FCC", "CLAUDE_FCC", "CODEX_OMNIROUTE",
            "CLAUDE_OMNIROUTE", "CLAUDE_CODE_DIRECT"
        ])
        self.assertEqual(q["minimum_rounds_per_mandatory_path"], 23)

    def test_launch_requires_human_and_full_evidence(self):
        data = self.load()
        self.assertTrue(data["gates"]["G11_LAUNCH"]["human_authorization_required"])
        self.assertEqual(data["launch_contract"]["decision"], "HUMAN_ONLY")
        self.assertIn("A3_verification_record", data["launch_contract"]["required_inputs"])
        self.assertIn("soak_record", data["launch_contract"]["required_inputs"])

    def test_local_model_and_desktop_agent_cannot_gain_authority(self):
        data = self.load()
        model = data["component_specific_admission"]["local_model"]
        agent = data["component_specific_admission"]["candidate_desktop_agent"]
        self.assertTrue(model["model_is_not_executor"])
        self.assertTrue(model["model_is_not_authority"])
        self.assertTrue(agent["agent_is_not_authority"])


    def test_openopc_candidate_is_qualified_separately_without_authority(self):
        data = self.load()
        candidate = data["candidate_component_admission"]["autonomous_development_system"]
        openopc = candidate["openopc"]
        self.assertEqual(openopc["qualification"], "NOT_PROVEN")
        self.assertEqual(openopc["authority"], "none")
        self.assertFalse(openopc["provider_selection"])
        self.assertFalse(openopc["credential_creation"])
        self.assertFalse(openopc["state_authority"])
        self.assertFalse(openopc["architecture_authority"])
        self.assertFalse(openopc["self_promotion"])
        self.assertFalse(openopc["self_qualification"])
        self.assertEqual(openopc["qualification_rounds"]["minimum"], 23)
        self.assertTrue(openopc["qualification_rounds"]["fresh_evidence_per_round"])
        self.assertTrue(openopc["qualification_rounds"]["isolated_workspace_per_round"])
        self.assertTrue(openopc["security_attention"]["versioned_release_required_for_gold"])


    def test_expanded_candidate_inventory_is_not_implicitly_qualified(self):
        data = self.load()
        candidates = data["candidate_review_inventory"]["candidates"]
        ids = {item["id"] for item in candidates}
        expected = {
            "openopc", "sol-pi", "colibri", "webtool-deepseek",
            "deepseek-harness", "stagewise", "minicpm-v-4.5-8b-1mk",
            "free-coding-models", "freellmapi", "unlazy", "naabu",
            "codex-chatgpt-web",
        }
        self.assertTrue(expected.issubset(ids))
        for item in candidates:
            self.assertEqual(item["status"], "NOT_PROVEN")
        admission = data["candidate_review_inventory"]["admission"]
        self.assertEqual(admission["minimum_fresh_rounds"], 23)
        self.assertTrue(admission["fresh_evidence_only"])
        self.assertTrue(admission["no_implicit_promotion"])
        self.assertTrue(admission["no_self_qualification"])


    def test_category_specific_candidate_controls_exist(self):
        data = self.load()
        controls = data["candidate_review_inventory"]["category_specific_controls"]
        for category in ["local_model", "gateway_or_router", "browser_bridge",
                         "coding_harness_or_ide", "security_tool", "unresolved_identity"]:
            self.assertIn(category, controls)
        self.assertIn("minicpm-v-4.5-8b-1mk", controls["local_model"]["examples"])
        self.assertIn("freellmapi", controls["gateway_or_router"]["examples"])
        self.assertIn("free-coding-models", controls["gateway_or_router"]["examples"])
        self.assertIn("webtool-deepseek", controls["browser_bridge"]["examples"])
        self.assertIn("codex-chatgpt-web", controls["browser_bridge"]["examples"])
        self.assertIn("naabu", controls["security_tool"]["examples"])
        self.assertIn("colibri", controls["unresolved_identity"]["examples"])
        self.assertIn("unlazy", controls["unresolved_identity"]["examples"])

    def test_reference_architecture_and_unified_model_alignment_contract(self):
        reference = Path("architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md").read_text(encoding="utf-8")
        unified = yaml.safe_load(Path("architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml").read_text(encoding="utf-8"))
        self.assertIn("Human is the final authority", reference)
        self.assertIn("RECONCILIATION_REQUIRED", reference)
        self.assertEqual(unified["reference_architecture"], "architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md")
        self.assertEqual(unified["qualification_contract"], "architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml")
        self.assertTrue(unified["contract_alignment"].startswith("CANONICAL"))
        self.assertTrue(unified["reconciliation"]["required"])
        self.assertEqual(unified["reconciliation"]["failure_state"], "RECONCILIATION_REQUIRED")
        self.assertEqual(len(unified["qualification"]["gate_contract"]), 12)
        self.assertTrue(unified["rules"]["missing_or_contradictory_evidence_blocks"])
        self.assertTrue(unified["rules"]["gold_active_requires_human_launch"])
        self.assertTrue(unified["rules"]["evidence_is_immutable"])

    def test_session_115_wave_contract_is_exact_and_fail_closed(self):
        source = Path("ops/qualification/session_115_wave.py").read_text(encoding="utf-8")
        self.assertIn('"total_observations_minimum":115', source)
        self.assertIn('"rounds_minimum_per_path":ROUNDS', source)
        self.assertIn('ROUNDS=23', source)
        for path in ["CODEX_FCC", "CLAUDE_FCC", "CODEX_OMNIROUTE",
                     "CLAUDE_OMNIROUTE", "CLAUDE_CODE_DIRECT"]:
            self.assertIn(f'"{path}"', source)
        self.assertIn('status="BLOCKED"', source)
        self.assertIn('"verification_status":"UNVERIFIED"', source)

    def test_g5_verifier_requires_fresh_shared_authority(self):
        from ops.qualification.verify_g5_coordination_attestation import verify
        import tempfile, json
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "attestation.json"
            base = {"node_id":"n1","running_agent_source_sha":"a"*64,
                    "coordination_authority_id":"A0","coordination_state":"shared",
                    "coordination_transport":"shared-store","active_claim_count":1,
                    "reservation_result":"PASS"}
            p.write_text(json.dumps(base), encoding="utf-8")
            self.assertEqual(verify(p)["status"], "BLOCKED")
            base["fresh"] = True
            p.write_text(json.dumps(base), encoding="utf-8")
            self.assertEqual(verify(p)["status"], "PASS")

    def test_g6_verifier_is_fresh_and_fail_closed(self):
        from ops.qualification.verify_g6_recovery_evidence import verify
        import tempfile, json
        scenarios = {name: {"status":"PASS"} for name in (
            "timeout","executor_failure","transport_interruption","stale_claim",
            "worker_restart","duplicate_controller","replay_idempotency")}
        scenarios["result_publication_recovery"] = {
            "status":"PASS","published_result_identity":"r1","source_sha":"a"*40,
            "remote_branch_tip":"b"*40,"local_processed_state_reconciliation":"PASS",
            "duplicate_execution_detected":False,"evidence_rewritten":False}
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"g6.json"
            payload={"fresh":False,"scenarios":scenarios}
            p.write_text(json.dumps(payload),encoding="utf-8")
            self.assertEqual(verify(p)["status"],"BLOCKED")
            payload["fresh"]=True
            p.write_text(json.dumps(payload),encoding="utf-8")
            self.assertEqual(verify(p)["status"],"PASS")

    def test_a3_verifier_requires_independence_and_exact_sha(self):
        from ops.qualification.verify_a3_evidence import verify
        import tempfile, json
        checks={name:{"status":"PASS"} for name in (
            "focused_tests","regression","contracts","architecture_conformance",
            "security","concurrency","failure","recovery","exact_sha_evidence")}
        payload={"fresh":True,"verifier_role":"A3","independence_attested":True,
                 "source_evidence_path":"/external/g4.json","a3_evidence_path":"/external/a3.json",
                 "source_sha":"a"*40,"verified_sha":"a"*40,"evidence_sha256":"b"*64,**checks}
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"a3.json"
            p.write_text(json.dumps(payload),encoding="utf-8")
            self.assertEqual(verify(p)["status"],"PASS")
            payload["verified_sha"]="c"*40
            p.write_text(json.dumps(payload),encoding="utf-8")
            self.assertEqual(verify(p)["status"],"BLOCKED")

    def test_g8_bundle_requires_all_prerequisites_and_115(self):
        from ops.qualification.verify_g8_pre_soak_bundle import verify
        import tempfile, json
        base={k:{"status":"PASS"} for k in ("g4_115","g5_coordination","g6_recovery","a3_independent","clean_worktree","fresh_bundle")}
        base["g4_115"].update(observations=115,paths=5)
        base["g5_coordination"]["max_parallel"]=2
        base["a3_independent"]["independence_attested"]=True
        base["clean_worktree"]["dirty"]=False
        base["fresh"]=True
        base["bundle_sha256"]="b"*64
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"g8.json"; p.write_text(json.dumps(base),encoding="utf-8")
            self.assertEqual(verify(p)["status"],"PASS")
            base["g6_recovery"]["status"]="BLOCKED"
            p.write_text(json.dumps(base),encoding="utf-8")
            self.assertEqual(verify(p)["status"],"BLOCKED")

    def test_g8_rejects_source_sha_mismatch(self):
        from ops.qualification.verify_g8_pre_soak_bundle import verify
        import tempfile, json
        base={k:{"status":"PASS"} for k in ("g4_115","g5_coordination","g6_recovery","a3_independent","clean_worktree","fresh_bundle")}
        base["g4_115"].update(observations=115,paths=5)
        base["g5_coordination"]["max_parallel"]=2
        base["a3_independent"].update(independence_attested=True,source_sha="a"*40)
        base["clean_worktree"]["dirty"]=False
        base.update(fresh=True,bundle_sha256="b"*64,source_sha="c"*40)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"g8.json"; p.write_text(json.dumps(base),encoding="utf-8")
            self.assertEqual(verify(p)["status"], "BLOCKED")
            self.assertEqual(verify(p)["reason"], "bundle_source_sha_mismatch")

    def test_current_state_reducer_is_fail_closed(self):
        from ops.qualification.current_qualification_state import build
        state=build({"gates":{"G4_23_WAVE_QUALIFICATION":"PASS"},
                      "gate_evidence":{"G4_23_WAVE_QUALIFICATION":{"fresh":False}}})
        self.assertEqual(state["status"],"BLOCKED")
        self.assertIn("G4_23_WAVE_QUALIFICATION",state["failed_gates"])
        self.assertIn("G5_CONCURRENCY",state["failed_gates"])

    def test_reducer_separates_physical_blockers(self):
        from ops.qualification.geometric_progress_controller import reduce_state
        e={"gates":{"G0_IDENTITY":"PASS","G1_BOUNDARY":"PASS","G2_CONTROL_PLANE":"PASS",
                    "G3_EXECUTION_PATH":"PASS","G4_23_WAVE_QUALIFICATION":"BLOCKED",
                    "G5_CONCURRENCY":"PASS","G6_RECOVERY":"BLOCKED","G7_INTEGRATED_A3":"PASS",
                    "G8_PRE_SOAK":"BLOCKED","G9_24H_SOAK":"BLOCKED"}}
        s=reduce_state(e)
        self.assertEqual(s["next"]["gate"],"G4_23_WAVE_QUALIFICATION")
        self.assertEqual(s["next"]["kind"],"PHYSICAL")
        self.assertEqual(s["physical_blockers"],4)

    def test_launch_gate_consumes_effective_canonical_state(self):
        from ops.qualification.qualification_launch_gate import evaluate, load_schema
        evidence={"gates":{"G0_IDENTITY":"PASS","G1_BOUNDARY":"PASS","G2_CONTROL_PLANE":"PASS",
                           "G3_EXECUTION_PATH":"PASS","G4_23_WAVE_QUALIFICATION":"PASS"},
                  "gate_evidence":{"G4_23_WAVE_QUALIFICATION":{"status":"PASS","fresh":False}}}
        result=evaluate(evidence, load_schema())
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["next_blocker"], "G4_23_WAVE_QUALIFICATION")
        self.assertEqual(result["gate_results"]["G4_23_WAVE_QUALIFICATION"], "BLOCKED")

    def test_geometric_progress_controller_halves_active_budget(self):
        from ops.qualification.geometric_progress_controller import plan
        e={"gates":{"G0_IDENTITY":"BLOCKED"}}
        self.assertEqual(plan(e,1,8)["active_work_budget_target_hours"],8.0)
        self.assertEqual(plan(e,2,8)["active_work_budget_target_hours"],4.0)
        self.assertEqual(plan(e,3,8)["active_work_budget_target_hours"],2.0)
        self.assertEqual(plan(e,5,8)["active_work_budget_target_hours"],0.5)

    def test_geometric_controller_never_removes_mandatory_24h_soak(self):
        from ops.qualification.geometric_progress_controller import plan
        e={"gates":{"G0_IDENTITY":"PASS","G1_BOUNDARY":"PASS","G2_CONTROL_PLANE":"PASS",
                    "G3_EXECUTION_PATH":"PASS","G4_23_WAVE_QUALIFICATION":"PASS",
                    "G5_CONCURRENCY":"PASS","G6_RECOVERY":"PASS","G7_INTEGRATED_A3":"PASS",
                    "G8_PRE_SOAK":"PASS","G9_24H_SOAK":"BLOCKED"}}
        r=plan(e,6,8)
        self.assertEqual(r["next_gate"],"G9_24H_SOAK")
        self.assertEqual(r["mandatory_wall_clock_hours"],24)

if __name__ == "__main__":
    unittest.main()
