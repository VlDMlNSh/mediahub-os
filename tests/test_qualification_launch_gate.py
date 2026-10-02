import json
import tempfile
import unittest
from pathlib import Path

from ops.qualification.qualification_launch_gate import evaluate, load_schema


class TestQualificationLaunchGate(unittest.TestCase):
    def test_missing_evidence_is_fail_closed(self):
        result = evaluate({}, load_schema())
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["launch_ready"])
        self.assertTrue(result["failed_gates"])

    def test_all_gates_without_launch_inputs_remain_blocked(self):
        schema = load_schema()
        evidence = {"gates": {gate: "PASS" for gate in schema["gates"] if gate != "G11_LAUNCH"}}
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["missing_launch_inputs"])

    def test_g11_requires_explicit_human_authorization(self):
        schema = load_schema()
        evidence = {
            "gates": {gate: "PASS" for gate in schema["gates"] if gate != "G11_LAUNCH"},
            "launch": {key: "present" for key in schema["launch_contract"]["required_inputs"]},
        }
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("G11_LAUNCH_HUMAN_AUTHORIZATION", result["failed_gates"])

    def test_g11_human_authorization_is_not_implicit(self):
        schema = load_schema()
        evidence = {
            "gates": {
                **{gate: "PASS" for gate in schema["gates"] if gate != "G11_LAUNCH"},
                "G11_LAUNCH": "HUMAN_AUTHORIZED",
            },
            "launch": {key: "present" for key in schema["launch_contract"]["required_inputs"]},
        }
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "LAUNCH_READY")

    def test_complete_evidence_reaches_launch_ready_only(self):
        schema = load_schema()
        evidence = {
            "gates": {
                **{gate: "PASS" for gate in schema["gates"] if gate != "G11_LAUNCH"},
                "G11_LAUNCH": "HUMAN_AUTHORIZED",
            },
            "launch": {key: "present" for key in schema["launch_contract"]["required_inputs"]},
        }
        result = evaluate(evidence, schema)
        self.assertEqual(result["status"], "LAUNCH_READY")
        self.assertTrue(result["launch_ready"])

if __name__ == "__main__":
    unittest.main()
