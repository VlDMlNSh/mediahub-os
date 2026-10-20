"""Regression tests for the host worker's generic gateway fallback boundary."""

import builtins
import unittest
from unittest.mock import patch

import astra_github_agent as agent


class GenericGatewayRouteAdmissionTests(unittest.TestCase):
    def test_generic_language_operations_fail_closed_before_gateway_import(self):
        expected = {
            "research",
            "architecture",
            "review",
            "documents",
            "coding",
            "coding_v2",
        }
        self.assertEqual(agent.UNADMITTED_GENERIC_GATEWAY_OPERATIONS, frozenset(expected))

        original_import = builtins.__import__

        def reject_gateway_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "mediahub_runtime.astra_gateway":
                raise AssertionError("unadmitted host-side gateway must never be imported")
            return original_import(name, globals, locals, fromlist, level)

        for operation in sorted(expected):
            with self.subTest(operation=operation):
                with patch("builtins.__import__", side_effect=reject_gateway_import):
                    with self.assertRaisesRegex(RuntimeError, "^gateway_route_not_admitted$"):
                        agent.execute({"operation": operation, "command_id": "test-command"})

    def test_health_operation_keeps_its_concrete_handler(self):
        original_import = builtins.__import__

        def reject_gateway_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "mediahub_runtime.astra_gateway":
                raise AssertionError("health must not import the generic gateway")
            return original_import(name, globals, locals, fromlist, level)

        with patch("builtins.__import__", side_effect=reject_gateway_import):
            result = agent.execute({"operation": "health"})

        self.assertEqual(result["status"], "ready")
        self.assertIn("node_id", result)

    def test_generic_gateway_fallback_is_removed_from_source(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn('raise RuntimeError("gateway_route_not_admitted")', source)
        self.assertIn('raise RuntimeError("operation_handler_not_implemented")', source)
        self.assertNotIn("AstraGatewayRuntime().run_bounded(", source)


if __name__ == "__main__":
    unittest.main()
