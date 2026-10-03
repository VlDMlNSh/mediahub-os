import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).parents[1]


class TestAstraControllerReconciliation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("astra_github_agent", ROOT / "astra_github_agent.py")
        cls.agent = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.agent)

    @staticmethod
    def _result(stdout="", returncode=0):
        return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr="")

    def test_reconcile_controller_processes_terminates_duplicate(self):
        a = self.agent
        a.NODE_ID = "mh-dev-01"
        current = a.os.getpid()
        initial = f"{current} python astra_github_agent.py\n999 ASTRA_NODE_ID=mh-dev-01 python astra_github_agent.py\n"
        final = f"{current} python astra_github_agent.py\n"
        with mock.patch.object(a.subprocess, "run", side_effect=[
            self._result(initial),
            self._result(returncode=0),
            self._result(final),
        ]) as run_mock, mock.patch.object(a.time, "sleep"):
            result = a.execute({"operation": "reconcile_controller_processes"})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["remaining_duplicates"], [])
        self.assertEqual(result["terminated"], [{"pid": 999, "returncode": 0}])
        self.assertEqual(run_mock.call_count, 3)

    def test_reconcile_controller_processes_blocks_when_duplicate_survives(self):
        a = self.agent
        a.NODE_ID = "mh-dev-01"
        current = a.os.getpid()
        initial = f"{current} python astra_github_agent.py\n999 ASTRA_NODE_ID=mh-dev-01 python astra_github_agent.py\n"
        final = initial
        with mock.patch.object(a.subprocess, "run", side_effect=[
            self._result(initial),
            self._result(returncode=1),
            self._result(final),
        ]), mock.patch.object(a.time, "sleep"):
            result = a.execute({"operation": "reconcile_controller_processes"})
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["remaining_duplicates"], ["999"])


if __name__ == "__main__":
    unittest.main()
