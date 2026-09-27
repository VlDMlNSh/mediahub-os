"""Characterize the GitHub transport to Astra runtime boundary without contacting nodes."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import astra_github_agent as agent


class AstraTransportContractTests(unittest.TestCase):
    def test_health_does_not_import_runtime(self):
        with patch.dict(agent.sys.modules, {"mediahub_runtime": None}):
            result = agent.execute({"operation": "health"})
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["node_id"], agent.NODE_ID)

    def test_non_health_task_uses_runtime_request_contract(self):
        from runtime.mediahub_runtime.astra_gateway import AstraTaskRequest

        with TemporaryDirectory() as directory:
            root = Path(directory)
            gateway = root / "runtime" / "mediahub_runtime" / "astra_gateway.py"
            gateway.parent.mkdir(parents=True)
            gateway.touch()
            command = {
                "command_id": "transport-contract-1",
                "node_id": agent.NODE_ID,
                "operation": "architecture",
                "title": "Inspect isolation",
                "description": "Review worker isolation",
            }
            captured = []

            def bounded(self, task):
                captured.append(task)
                return "bounded-result"

            with patch.object(agent, "ROOT", root), patch.dict(agent.os.environ, {"ASTRA_RUNTIME_ROOT": ""}), patch(
                "runtime.mediahub_runtime.astra_gateway.AstraGatewayRuntime.run_bounded", bounded
            ):
                result = agent.execute(command)

        self.assertEqual(result, "bounded-result")
        self.assertEqual(len(captured), 1)
        self.assertIsInstance(captured[0], AstraTaskRequest)
        self.assertEqual(captured[0].request_id, command["command_id"])
        self.assertEqual(captured[0].user_command, command["description"])

    def test_missing_runtime_fails_closed(self):
        with TemporaryDirectory() as directory, patch.object(agent, "ROOT", Path(directory)), patch.dict(
            agent.os.environ, {"ASTRA_RUNTIME_ROOT": ""}
        ):
            with self.assertRaisesRegex(ModuleNotFoundError, "runtime root not found"):
                agent.execute({"operation": "review", "command_id": "missing-runtime"})


if __name__ == "__main__":
    unittest.main()
