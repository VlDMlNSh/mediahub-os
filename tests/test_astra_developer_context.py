import unittest

from runtime.mediahub_runtime.astra_developer_context import (
    DeveloperContextContract,
    DeveloperContextContractError,
)


class DeveloperContextContractTests(unittest.TestCase):
    def test_parses_project_session_and_references(self):
        request = DeveloperContextContract.parse({
            "request_id": "r1",
            "session_id": "s1",
            "project_id": "p1",
            "message": "continue MediaHub",
            "context_refs": ["m1", "m2"],
            "task_id": "t1",
        })
        self.assertEqual(request.project_id, "p1")
        self.assertEqual(request.context_refs, ("m1", "m2"))

    def test_rejects_missing_required_fields(self):
        with self.assertRaises(DeveloperContextContractError):
            DeveloperContextContract.parse({"session_id": "s1", "message": "x"})

    def test_rejects_malformed_context_refs(self):
        with self.assertRaisesRegex(DeveloperContextContractError, "context_refs"):
            DeveloperContextContract.parse({
                "request_id": "r1", "session_id": "s1", "message": "x",
                "context_refs": ["m1", ""],
            })

    def test_rejects_oversized_message(self):
        with self.assertRaisesRegex(DeveloperContextContractError, "message_limit"):
            DeveloperContextContract.parse({
                "request_id": "r1", "session_id": "s1", "message": "x" * 65_537,
            })

    def test_maps_without_auth_or_secret_fields(self):
        request = DeveloperContextContract.parse({
            "request_id": "r1", "session_id": "s1", "project_id": "p1", "message": "x",
        })
        task = DeveloperContextContract.to_gateway_task(request)
        self.assertEqual(task.project_id, "p1")
        self.assertEqual(task.session_id, "s1")
        self.assertFalse(hasattr(task, "api_key"))

    def test_preserves_task_scope_in_gateway_mapping(self):
        request = DeveloperContextContract.parse({
            "request_id": "r1", "session_id": "s1", "project_id": "p1",
            "task_id": "t1", "message": "x",
        })
        task = DeveloperContextContract.to_gateway_task(request)
        self.assertEqual(task.task_id, "t1")

    def test_rejects_blank_task_id(self):
        with self.assertRaisesRegex(DeveloperContextContractError, "task_id"):
            DeveloperContextContract.parse({
                "request_id": "r1", "session_id": "s1", "message": "x",
                "task_id": "   ",
            })


if __name__ == "__main__":
    unittest.main()
