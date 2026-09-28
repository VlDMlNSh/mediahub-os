import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from runtime.mediahub_runtime.cloud_orchestrator import CloudFirstOrchestrator, ProviderRoute


class CloudAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.cloud = (
            ProviderRoute(
                "test-cloud",
                "cloud",
                frozenset({"coding"}),
                "TEST_CLOUD_KEY",
                "TEST_CLOUD_MODEL",
                1,
            ),
        )
        self.local = (
            ProviderRoute(
                "test-local",
                "local",
                frozenset({"coding"}),
                None,
                None,
                100,
            ),
        )

    def _orchestrator(self, evidence, *, commit="abc123"):
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(evidence, temp)
        temp.close()
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))
        return CloudFirstOrchestrator(
            cloud_routes=self.cloud,
            local_routes=self.local,
            credential_env={
                "TEST_CLOUD_KEY": "present",
                "TEST_CLOUD_MODEL": "model",
                "MEDIAHUB_PROVIDER_EVIDENCE_FILE": temp.name,
                "MEDIAHUB_RELEASE_COMMIT": commit,
            },
            executors={"test-cloud": lambda prompt: "qualified-output"},
        )

    def _evidence(self, *, commit="abc123", qualification="QUALIFIED", age_hours=0):
        timestamp = datetime.now(timezone.utc) - timedelta(hours=age_hours)
        return {
            "schema": "mediahub.provider-model.v1",
            "commit": commit,
            "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
            "providers": {
                "test-cloud": {
                    "catalog_status": "PASS",
                    "inference_status": "PASS",
                    "qualification_status": qualification,
                }
            },
        }

    def test_fresh_qualified_provider_is_admitted(self):
        orchestrator = self._orchestrator(self._evidence())
        self.assertEqual(orchestrator.admitted_cloud_providers(), ("test-cloud",))
        decision = orchestrator.decide("coding", allow_local_extension=False)
        self.assertEqual(decision.provider_id, "test-cloud")
        self.assertEqual(decision.reason, "cloud_provider_configured")

    def test_partial_provider_is_fail_closed_to_local(self):
        orchestrator = self._orchestrator(self._evidence(qualification="PARTIAL"))
        self.assertEqual(orchestrator.admitted_cloud_providers(), ())
        decision = orchestrator.decide("coding")
        self.assertEqual(decision.provider_id, "test-local")

    def test_stale_provider_is_fail_closed_to_local(self):
        orchestrator = self._orchestrator(self._evidence(age_hours=7))
        self.assertEqual(orchestrator.admitted_cloud_providers(), ())
        decision = orchestrator.decide("coding")
        self.assertEqual(decision.provider_id, "test-local")

    def test_commit_mismatch_is_fail_closed_to_local(self):
        orchestrator = self._orchestrator(self._evidence(commit="old-commit"))
        self.assertEqual(orchestrator.admitted_cloud_providers(), ())
        decision = orchestrator.decide("coding")
        self.assertEqual(decision.provider_id, "test-local")


if __name__ == "__main__":
    unittest.main()
