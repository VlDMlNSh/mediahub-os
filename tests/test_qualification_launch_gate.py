import unittest

from ops.qualification.qualification_launch_gate import evaluate, load_schema


class TestQualificationLaunchGate(unittest.TestCase):
    def _complete_fresh_evidence(self, schema, human_authorized=True):
        gates = {
            gate: "PASS"
            for gate in schema["gates"]
            if gate != "G11_LAUNCH"
        }
        gates["G11_LAUNCH"] = "HUMAN_AUTHORIZED" if human_authorized else "BLOCKED"
        gate_evidence = {
            gate: {"status": "PASS", "fresh": True}
            for gate in (
                "G4_23_WAVE_QUALIFICATION",
                "G5_CONCURRENCY",
                "G6_RECOVERY",
                "G7_INTEGRATED_A3",
                "G8_PRE_SOAK",
            )
        }
        gate_evidence["G7_INTEGRATED_A3"]["independence_attested"] = True
        return {
            "gates": gates,
            "gate_evidence": gate_evidence,
            "launch": {
                key: "present"
                for key in schema["launch_contract"]["required_inputs"]
            },
        }

    def test_missing_evidence_is_fail_closed(self):
        result = evaluate({}, load_schema())
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["launch_ready"])
        self.assertTrue(result["failed_gates"])

    def test_all_gates_without_launch_inputs_remain_blocked(self):
        schema = load_schema()
        evidence = {
            "gates": {
                gate: "PASS"
                for gate in schema["gates"]
                if gate != "G11_LAUNCH"
            }
        }
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["missing_launch_inputs"])

    def test_g11_requires_explicit_human_authorization(self):
        schema = load_schema()
        evidence = self._complete_fresh_evidence(schema, human_authorized=False)
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("G11_LAUNCH", result["failed_gates"])

    def test_pass_status_without_fresh_gate_evidence_remains_blocked(self):
        schema = load_schema()
        evidence = self._complete_fresh_evidence(schema)
        evidence["gate_evidence"]["G4_23_WAVE_QUALIFICATION"]["fresh"] = False
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("G4_23_WAVE_QUALIFICATION", result["failed_gates"])

    def test_g11_human_authorization_is_not_implicit(self):
        schema = load_schema()
        evidence = self._complete_fresh_evidence(schema)
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "LAUNCH_READY")

    def test_complete_evidence_reaches_launch_ready_only(self):
        schema = load_schema()
        evidence = self._complete_fresh_evidence(schema)
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "LAUNCH_READY")
        self.assertTrue(result["launch_ready"])


if __name__ == "__main__":
    unittest.main()
