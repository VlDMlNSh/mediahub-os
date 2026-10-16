import hashlib
import os
import unittest

from runtime.mediahub_runtime.astra_gateway import AstraGatewayRuntime, AstraTaskRequest


class ApprovalBoundaryTests(unittest.TestCase):
    def test_untrusted_approval_state_does_not_authorize(self):
        task = AstraTaskRequest("r1", "s1", "credential_change", approval_state="approved")
        with self.assertRaises(Exception):
            AstraGatewayRuntime._validate_task(task)

    def test_approval_requires_bound_proof(self):
        token = "test-token"
        old = os.environ.get("ASTRA_APPROVAL_TOKEN")
        os.environ["ASTRA_APPROVAL_TOKEN"] = token
        try:
            task = AstraTaskRequest("r1", "s1", "credential_change", approval_state="approved")
            task = task.__class__(**{**task.__dict__, "approval_token": hashlib.sha256(f"r1:credential_change:{token}".encode()).hexdigest()})
            self.assertTrue(AstraGatewayRuntime._approval_is_trusted(task, "credential_change"))
        finally:
            if old is None:
                os.environ.pop("ASTRA_APPROVAL_TOKEN", None)
            else:
                os.environ["ASTRA_APPROVAL_TOKEN"] = old


if __name__ == "__main__":
    unittest.main()
