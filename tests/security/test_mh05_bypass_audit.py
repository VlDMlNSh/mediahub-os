"""Adversarial MH-05 authority-boundary audit checks.

These checks are deliberately repository-local and fail closed when a new
runtime module introduces an unauthorized canonical mutation owner.
"""

import ast
import math
import pathlib
import unittest

from mediahub_runtime.consumer_boundary import ConsumerBoundary, ConsumerBoundaryError
from mediahub_runtime.state_authority import AuthorizationContext, AuthorityUnavailable, StateAuthority


ROOT = pathlib.Path(__file__).resolve().parents[2]
RUNTIME_PACKAGE = ROOT / "runtime" / "mediahub_runtime"
COMPOSITION_ROOT = RUNTIME_PACKAGE / "composition_root.py"


class MH05BypassAuditTests(unittest.TestCase):
    def setUp(self):
        self.authority = StateAuthority({"value": 1})
        self.boundary = ConsumerBoundary(self.authority)
        self.allowed = AuthorizationContext("runtime", True, frozenset({"state.write"}))

    def test_boundary_has_no_canonical_mutation_storage(self):
        source = (RUNTIME_PACKAGE / "consumer_boundary.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        forbidden = {"_state", "_events", "checkpoint", "_checkpoint", "_canonical_state"}
        assigned = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                assigned.add(node.id)
            if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
                assigned.add(node.attr)
        self.assertTrue(forbidden.isdisjoint(assigned), sorted(forbidden & assigned))

    def test_only_composition_root_constructs_canonical_authority(self):
        offenders = []
        constructors = []
        for path in RUNTIME_PACKAGE.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "StateAuthority":
                    constructors.append(path.relative_to(ROOT).as_posix())
                    if path != COMPOSITION_ROOT:
                        offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])
        self.assertEqual(constructors, [COMPOSITION_ROOT.relative_to(ROOT).as_posix()])

    def test_remote_like_identity_still_requires_explicit_authorization(self):
        request = self.boundary.request("remote-source", "corr-remote", AuthorizationContext("remote-source", True, frozenset()))
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            self.boundary.execute(request, "set", ("value",), 9, command_id="remote-1")
        self.assertEqual(ctx.exception.code, "authorization_denied")
        self.assertEqual(self.boundary.read()["value"], 1)

    def test_nonfinite_payload_is_rejected_before_authority(self):
        for payload in (math.nan, math.inf, -math.inf):
            with self.subTest(payload=payload):
                with self.assertRaises(ConsumerBoundaryError) as ctx:
                    self.boundary.execute(self.boundary.request("runtime", "corr-finite", self.allowed), "set", ("value",), payload, command_id=f"finite-{repr(payload)}")
                self.assertEqual(ctx.exception.code, "operation_rejected")
        self.assertEqual(self.authority.metadata()["event_sequence"], 0)

    def test_authority_unavailable_fails_closed_and_does_not_mutate(self):
        class UnavailableAuthority:
            def read(self):
                raise AuthorityUnavailable("offline")

            def execute(self, command):
                raise AuthorityUnavailable("offline")

            def restore(self, checkpoint, authorization=None):
                raise AuthorityUnavailable("offline")

        boundary = ConsumerBoundary(UnavailableAuthority())
        request = boundary.request("runtime", "corr-unavailable", self.allowed)
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            boundary.execute(request, "set", ("value",), 2, command_id="offline-1")
        self.assertEqual(ctx.exception.code, "authority_unavailable")
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            boundary.read()
        self.assertEqual(ctx.exception.code, "authority_unavailable")


if __name__ == "__main__":
    unittest.main()
