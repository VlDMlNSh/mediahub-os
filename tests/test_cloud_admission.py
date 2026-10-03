import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from runtime.mediahub_runtime.cloud_orchestrator import (
    CloudFirstOrchestrator,
    CloudOrchestratorError,
    ProviderRoute,
)


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
            executors={
                "test-cloud": lambda prompt: "qualified-output",
                "test-local": lambda prompt: "local-output",
            },
        )

    def _evidence(self, *, commit="abc123", qualification="QUALIFIED", age_hours=0, providers=None):
        timestamp = datetime.now(timezone.utc) - timedelta(hours=age_hours)
        return {
            "schema": "mediahub.provider-model.v1",
            "commit": commit,
            "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
            "providers": providers or {
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
        self.assertEqual(decision.reason, "cloud_provider_admitted")

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

    def test_execution_fails_over_to_next_admitted_provider(self):
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(
            {
                "schema": "mediahub.provider-model.v1",
                "commit": "abc123",
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "providers": {
                    "first-cloud": {
                        "catalog_status": "PASS",
                        "inference_status": "PASS",
                        "qualification_status": "QUALIFIED",
                    },
                    "second-cloud": {
                        "catalog_status": "PASS",
                        "inference_status": "PASS",
                        "qualification_status": "QUALIFIED",
                    },
                },
            },
            temp,
        )
        temp.close()
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))

        routes = (
            ProviderRoute("first-cloud", "cloud", frozenset({"coding"}), "FIRST_KEY", "FIRST_MODEL", 1),
            ProviderRoute("second-cloud", "cloud", frozenset({"coding"}), "SECOND_KEY", "SECOND_MODEL", 2),
        )
        calls = []

        def first(prompt):
            calls.append("first-cloud")
            raise CloudOrchestratorError("provider_auth_failed")

        def second(prompt):
            calls.append("second-cloud")
            return "second-output"

        orchestrator = CloudFirstOrchestrator(
            cloud_routes=routes,
            local_routes=(),
            credential_env={
                "FIRST_KEY": "present",
                "FIRST_MODEL": "model-1",
                "SECOND_KEY": "present",
                "SECOND_MODEL": "model-2",
                "MEDIAHUB_PROVIDER_EVIDENCE_FILE": temp.name,
                "MEDIAHUB_RELEASE_COMMIT": "abc123",
            },
            executors={"first-cloud": first, "second-cloud": second},
        )

        decision, output = orchestrator.execute("coding", "bounded prompt", allow_local_extension=False)
        self.assertEqual(decision.provider_id, "second-cloud")
        self.assertEqual(output, "second-output")
        self.assertEqual(calls, ["first-cloud", "second-cloud"])

    def test_failover_tries_credentials_and_models_before_next_provider(self):
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(
            {
                "schema": "mediahub.provider-model.v1",
                "commit": "abc123",
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "providers": {
                    "slot-cloud": {
                        "catalog_status": "PASS",
                        "inference_status": "PASS",
                        "qualification_status": "QUALIFIED",
                    },
                    "next-cloud": {
                        "catalog_status": "PASS",
                        "inference_status": "PASS",
                        "qualification_status": "QUALIFIED",
                    },
                },
            },
            temp,
        )
        temp.close()
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))

        routes = (
            ProviderRoute("slot-cloud", "cloud", frozenset({"coding"}), "SLOT_KEY", "SLOT_MODEL", 1),
            ProviderRoute("next-cloud", "cloud", frozenset({"coding"}), "NEXT_KEY", "NEXT_MODEL", 2),
        )
        calls = []

        def slot_executor(prompt):
            calls.append(("slot", prompt))
            raise CloudOrchestratorError("provider_auth_failed")

        def next_executor(prompt):
            calls.append(("next", prompt))
            return "next-output"

        orchestrator = CloudFirstOrchestrator(
            cloud_routes=routes,
            local_routes=(),
            credential_env={
                "SLOT_KEY": "primary",
                "SLOT_KEY_1": "backup",
                "SLOT_MODEL": "model-a",
                "SLOT_MODELS": "model-b,model-c",
                "NEXT_KEY": "next-key",
                "NEXT_MODEL": "next-model",
                "MEDIAHUB_PROVIDER_EVIDENCE_FILE": temp.name,
                "MEDIAHUB_RELEASE_COMMIT": "abc123",
            },
            executors={"slot-cloud": slot_executor, "next-cloud": next_executor},
        )

        decision, output = orchestrator.execute("coding", "bounded prompt", allow_local_extension=False)
        self.assertEqual(decision.provider_id, "next-cloud")
        self.assertEqual(output, "next-output")
        self.assertEqual(calls, [("slot", "bounded prompt")] * 6 + [("next", "bounded prompt")])

    def test_no_admitted_cloud_uses_local_only_after_cloud_filter(self):
        orchestrator = self._orchestrator(self._evidence(qualification="PARTIAL"))
        decision, output = orchestrator.execute("coding", "bounded prompt")
        self.assertEqual(decision.provider_id, "test-local")
        self.assertEqual(output, "local-output")

    def test_without_local_extension_fail_closed_when_no_admitted_provider(self):
        orchestrator = self._orchestrator(self._evidence(qualification="PARTIAL"))
        with self.assertRaisesRegex(CloudOrchestratorError, "no_provider_available"):
            orchestrator.execute("coding", "bounded prompt", allow_local_extension=False)

    def test_gateway_route_preserves_provider_identity(self):
        providers = {
            "openrouter": {
                "catalog_status": "PASS",
                "inference_status": "PASS",
                "qualification_status": "QUALIFIED",
            }
        }
        evidence = self._evidence(providers=providers)
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(evidence, temp)
        temp.close()
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))

        route = ProviderRoute(
            "openrouter",
            "cloud",
            frozenset({"coding"}),
            "OPENROUTER_API_KEY",
            "MEDIAHUB_OPENROUTER_MODEL",
            1,
        )
        observed = []

        def gateway(prompt):
            observed.append(prompt)
            return "gateway-output"

        orchestrator = CloudFirstOrchestrator(
            cloud_routes=(route,),
            local_routes=(),
            credential_env={
                "OPENROUTER_API_KEY": "present",
                "MEDIAHUB_OPENROUTER_MODEL": "provider/model-x",
                "MEDIAHUB_PROVIDER_EVIDENCE_FILE": temp.name,
                "MEDIAHUB_RELEASE_COMMIT": "abc123",
            },
        )

        with patch(
            "runtime.mediahub_runtime.cloud_orchestrator.OpenAICompatibleExecutor",
            return_value=gateway,
        ):
            decision, output = orchestrator.execute("coding", "bounded prompt", allow_local_extension=False)
        self.assertEqual(decision.provider_id, "openrouter")
        self.assertEqual(decision.model, "provider/model-x")
        self.assertEqual(decision.tier, "cloud")
        self.assertEqual(output, "gateway-output")
        self.assertEqual(observed, ["bounded prompt"])


if __name__ == "__main__":
    unittest.main()
