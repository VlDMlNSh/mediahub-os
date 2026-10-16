import unittest

from runtime.astra_cloud import AstraCloudService, TaskState


BASE = {
    "schema_id": "mediahub.ai.astra-task", "schema_version": "1.0.0", "owner": "mediahub-ai",
    "request_id": "req-1", "session_id": "sess-1", "user_command": "inspect repository",
    "approval_state": "not_required",
}


class AstraCloudTests(unittest.TestCase):
    def test_unconfigured_provider_blocks(self):
        record = AstraCloudService().submit(BASE)
        self.assertEqual(record.state, TaskState.BLOCKED)
        self.assertEqual(record.error_code, "provider_unconfigured")
        self.assertIsNone(record.output)

    def test_provider_output_succeeds(self):
        record = AstraCloudService(lambda command: "ok:" + command).submit(BASE)
        self.assertEqual(record.state, TaskState.SUCCEEDED)
        self.assertEqual(record.output, "ok:inspect repository")

    def test_rejected_task_never_executes(self):
        with self.assertRaisesRegex(ValueError, "task_rejected"):
            AstraCloudService(lambda _: "must-not-run").submit(dict(BASE, approval_state="rejected"))

    def test_invalid_schema_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid_task"):
            AstraCloudService(lambda _: "must-not-run").submit(dict(BASE, schema_id="other"))


if __name__ == "__main__":
    unittest.main()
