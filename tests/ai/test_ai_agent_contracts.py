import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts/ai"


class AIAgentContractTests(unittest.TestCase):
    def load(self, name):
        with (CONTRACTS / name).open(encoding="utf-8") as handle:
            return json.load(handle)

    def test_task_contract_is_bounded(self):
        contract = self.load("ai-agent-task.schema.json")
        self.assertTrue(contract["additionalProperties"] is False)
        self.assertEqual(contract["properties"]["owner"]["const"], "mediahub-ai")
        self.assertIn("authorization", contract["required"])
        self.assertIn("constraints", contract["required"])

    def test_result_contract_is_advisory_and_fail_closed(self):
        contract = self.load("ai-agent-result.schema.json")
        self.assertTrue(contract["additionalProperties"] is False)
        self.assertEqual(contract["properties"]["owner"]["const"], "mediahub-ai")
        self.assertEqual(
            contract["properties"]["status"]["enum"],
            ["completed", "failed", "degraded", "blocked"],
        )
        self.assertIn("evidence", contract["required"])

    def test_task_and_result_are_distinct_from_inference_contracts(self):
        task = self.load("ai-agent-task.schema.json")
        result = self.load("ai-agent-result.schema.json")
        inference_request = self.load("ai-inference-request.schema.json")
        inference_response = self.load("ai-inference-response.schema.json")
        self.assertNotEqual(task["$id"], inference_request["$id"])
        self.assertNotEqual(result["$id"], inference_response["$id"])


if __name__ == "__main__":
    unittest.main()
