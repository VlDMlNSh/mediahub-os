import unittest
from datetime import datetime, timedelta, timezone

from runtime.mediahub_runtime.authorization import (
    AuthorizationContext,
    AuthorizationPolicy,
)
from runtime.mediahub_runtime.diagnostics import make_event
from runtime.mediahub_runtime.errors import (
    AuthorizationDenied,
    ExpiredProposal,
    GenerationMismatch,
    InvalidStateTransition,
)
from runtime.mediahub_runtime.generation import Generation, validate_generation_compatibility
from runtime.mediahub_runtime.lifecycle import LifecycleState, LifecycleStateMachine
from runtime.mediahub_runtime.proposals import Proposal, ProposalAuthority
from runtime.mediahub_runtime.state import StateAuthority


class LifecycleTests(unittest.TestCase):
    def test_valid_lifecycle(self):
        machine = LifecycleStateMachine()
        machine.transition(LifecycleState.INITIALIZING)
        machine.transition(LifecycleState.SELF_TEST)
        self.assertEqual(machine.transition(LifecycleState.READY), LifecycleState.READY)

    def test_invalid_transition_rejected(self):
        machine = LifecycleStateMachine()
        with self.assertRaises(InvalidStateTransition):
            machine.transition(LifecycleState.READY)

    def test_failures_can_enter_safe_mode(self):
        machine = LifecycleStateMachine(LifecycleState.SELF_TEST)
        self.assertEqual(machine.enter_safe_mode(), LifecycleState.SAFE_MODE)


class GenerationTests(unittest.TestCase):
    def generation(self, generation_id="g1", schema="s1", state="t1"):
        return Generation(generation_id, "b1", schema, state, "hash")

    def test_matching_generation_is_compatible(self):
        value = self.generation()
        self.assertTrue(validate_generation_compatibility(value, value, value))

    def test_mismatch_is_rejected(self):
        with self.assertRaises(GenerationMismatch):
            validate_generation_compatibility(self.generation(), self.generation("g2"), self.generation())


class AuthorizationTests(unittest.TestCase):
    def test_default_is_deny(self):
        policy = AuthorizationPolicy()
        context = AuthorizationContext("service-a", "state.write")
        with self.assertRaises(AuthorizationDenied):
            policy.require(context, "commit")

    def test_explicit_grant(self):
        context = AuthorizationContext("service-a", "state.write")
        policy = AuthorizationPolicy({("service-a", "state.write", "commit")})
        self.assertTrue(policy.require(context, "commit").allowed)


class ProposalTests(unittest.TestCase):
    def proposal(self, expires_at):
        return Proposal("p1", "change", "target", 0.8, "g1", expires_at)

    def test_proposal_has_no_execution_primitive(self):
        proposal = self.proposal(datetime.now(timezone.utc) + timedelta(minutes=5))
        self.assertFalse(hasattr(proposal, "execute"))
        self.assertEqual(ProposalAuthority().validate(proposal), proposal)

    def test_expired_proposal_is_rejected(self):
        proposal = self.proposal(datetime.now(timezone.utc) - timedelta(seconds=1))
        with self.assertRaises(ExpiredProposal):
            ProposalAuthority().validate(proposal)


class StateAuthorityTests(unittest.TestCase):
    def test_state_authority_is_an_interface(self):
        self.assertTrue(issubclass(StateAuthority, object))
        with self.assertRaises(TypeError):
            StateAuthority()


class DiagnosticsTests(unittest.TestCase):
    def test_sensitive_fields_are_redacted(self):
        event = make_event("test", {"token": "secret", "voice": "raw", "safe": "value"})
        self.assertEqual(event.fields["token"], "[REDACTED]")
        self.assertEqual(event.fields["voice"], "[REDACTED]")
        self.assertEqual(event.fields["safe"], "value")


if __name__ == "__main__":
    unittest.main()
