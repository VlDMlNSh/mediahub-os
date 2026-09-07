import unittest

from mediahub_runtime.composition_root import build_runtime
from mediahub_runtime.state_authority import AuthorizationContext, AuthorizationDenied, Command


class TestMH05HealthNotAuthorization(unittest.TestCase):
    def test_available_authority_still_requires_authorization(self):
        authority = build_runtime({"x": 1})["state_authority"]
        self.assertTrue(authority.metadata()["available"])
        command = Command(
            command_id="health-no-auth",
            correlation_id="health-corr",
            operation="set",
            path=("x",),
            value=2,
            authorization=AuthorizationContext("probe", False, frozenset()),
            source_identity="health-probe",
        )
        before = (authority.read(), authority.metadata(), authority.events())
        with self.assertRaises(AuthorizationDenied):
            authority.execute(command)
        self.assertEqual((authority.read(), authority.metadata(), authority.events()), before)

    def test_unavailable_is_distinct_from_authorization(self):
        authority = build_runtime({"x": 1})["state_authority"]
        authority.set_available(False)
        command = Command(
            command_id="unavailable",
            correlation_id="unavailable-corr",
            operation="set",
            path=("x",),
            value=2,
            authorization=AuthorizationContext("probe", True, frozenset({"state.write"})),
            source_identity="health-probe",
        )
        before = (authority.metadata(), authority.events())
        with self.assertRaises(Exception) as ctx:
            authority.execute(command)
        self.assertNotIsInstance(ctx.exception, AuthorizationDenied)
        self.assertEqual((authority.metadata(), authority.events()), before)


if __name__ == "__main__":
    unittest.main()
