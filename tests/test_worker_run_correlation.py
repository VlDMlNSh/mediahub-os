import unittest

from runtime.mediahub_runtime.autonomous_queue import select_correlated_workflow_run


class CorrelatedWorkflowRunTests(unittest.TestCase):
    def setUp(self):
        self.dispatch_time = 1_800_000_000.0
        self.title = "Astra distributed worker / cmd-17 / task-4 / mh-dev-01 / claude"

    def row(self, database_id=41, title=None, created_at="2027-01-15T08:00:01Z"):
        return {
            "databaseId": database_id,
            "displayTitle": self.title if title is None else title,
            "createdAt": created_at,
        }

    def select(self, rows, **overrides):
        args = {
            "command_id": "cmd-17",
            "task_id": "task-4",
            "node_id": "mh-dev-01",
            "executor": "claude",
            "dispatched_after": self.dispatch_time,
        }
        args.update(overrides)
        return select_correlated_workflow_run(rows, **args)

    def test_exact_fresh_title_selects_single_run(self):
        row = self.row()
        self.assertEqual(self.select([row]), row)

    def test_empty_command_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid_command_id"):
            self.select([self.row()], command_id="")

    def test_substring_collision_does_not_match(self):
        row = self.row(title="Astra distributed worker / cmd-170 / task-4 / mh-dev-01 / claude")
        self.assertIsNone(self.select([row]))

    def test_stale_run_is_not_selected(self):
        row = self.row(created_at="2027-01-15T07:59:59Z")
        self.assertIsNone(self.select([row]))

    def test_duplicate_exact_runs_fail_closed(self):
        with self.assertRaisesRegex(RuntimeError, "ambiguous_remote_worker_run"):
            self.select([self.row(41), self.row(42)])

    def test_invalid_run_id_is_ignored(self):
        self.assertIsNone(self.select([self.row(database_id=0)]))

    def test_wrong_executor_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid_executor"):
            self.select([self.row()], executor="codex")


if __name__ == "__main__":
    unittest.main()
