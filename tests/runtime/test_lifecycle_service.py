from unittest import TestCase

from mediahub_runtime import (
    AuthorizationContext,
    AuthorizationPolicy,
    ConsumerBoundary,
    ConsumerBoundaryError,
    Generation,
    InMemoryStateAuthority,
    LifecycleService,
    LifecycleState,
    LifecycleStateMachine,
)


class LifecycleContractTests(TestCase):
    def test_transition_graph_matches_contract(self):
        allowed = {
            LifecycleState.PROVISIONING: {LifecycleState.INITIALIZING},
            LifecycleState.INITIALIZING: {LifecycleState.SELF_TEST},
            LifecycleState.SELF_TEST: {
                LifecycleState.READY,
                LifecycleState.DEGRADED,
                LifecycleState.SAFE_MODE,
            },
            LifecycleState.READY: {LifecycleState.DEGRADED, LifecycleState.SAFE_MODE},
            LifecycleState.DEGRADED: {LifecycleState.READY, LifecycleState.SAFE_MODE},
            LifecycleState.SAFE_MODE: {LifecycleState.RECOVERY},
            LifecycleState.RECOVERY: {LifecycleState.INITIALIZING},
        }
        for source, targets in allowed.items():
            for target in targets:
                self.assertEqual(LifecycleStateMachine(source).transition(target), target)
        for source in LifecycleState:
            for target in LifecycleState:
                if target not in allowed.get(source, set()):
                    with self.assertRaises(Exception):
                        LifecycleStateMachine(source).transition(target)

    def test_service_publishes_only_through_authority(self):
        context = AuthorizationContext("runtime", LifecycleService.CAPABILITY)
        policy = AuthorizationPolicy(
            {
                ("runtime", LifecycleService.CAPABILITY, "begin"),
                ("runtime", LifecycleService.CAPABILITY, "commit"),
                ("runtime", LifecycleService.CAPABILITY, "abort"),
            }
        )
        generation = Generation("gen-1", "bin-1", "schema-1", "0", "int-1")
        authority = InMemoryStateAuthority(
            generation,
            {"lifecycle": {"state": LifecycleState.PROVISIONING.value}},
            authorization_policy=policy,
        )
        service = LifecycleService(ConsumerBoundary(authority))

        result = service.transition(service.request(LifecycleState.INITIALIZING, context))

        self.assertEqual(result.payload["lifecycle"]["state"], LifecycleState.INITIALIZING.value)
        self.assertEqual(authority.read().payload["lifecycle"]["state"], LifecycleState.INITIALIZING.value)

    def test_invalid_transition_does_not_mutate(self):
        context = AuthorizationContext("runtime", LifecycleService.CAPABILITY)
        policy = AuthorizationPolicy(
            {
                ("runtime", LifecycleService.CAPABILITY, "begin"),
                ("runtime", LifecycleService.CAPABILITY, "commit"),
                ("runtime", LifecycleService.CAPABILITY, "abort"),
            }
        )
        generation = Generation("gen-1", "bin-1", "schema-1", "0", "int-1")
        authority = InMemoryStateAuthority(
            generation,
            {"lifecycle": {"state": LifecycleState.READY.value}},
            authorization_policy=policy,
        )
        service = LifecycleService(ConsumerBoundary(authority))

        with self.assertRaises(ConsumerBoundaryError):
            service.transition(service.request(LifecycleState.RECOVERY, context))

        self.assertEqual(authority.read().payload["lifecycle"]["state"], LifecycleState.READY.value)

    def test_wrong_capability_is_rejected_before_mutation(self):
        context = AuthorizationContext("runtime", "runtime.other")
        generation = Generation("gen-1", "bin-1", "schema-1", "0", "int-1")
        authority = InMemoryStateAuthority(
            generation,
            {"lifecycle": {"state": LifecycleState.PROVISIONING.value}},
            authorization_policy=AuthorizationPolicy(),
        )
        service = LifecycleService(ConsumerBoundary(authority))

        with self.assertRaises(ConsumerBoundaryError) as raised:
            service.request(LifecycleState.INITIALIZING, context)

        self.assertEqual(raised.exception.code, "authorization_denied")
        self.assertEqual(authority.read().payload["lifecycle"]["state"], LifecycleState.PROVISIONING.value)

    def test_validate_transition_is_observation_only(self):
        context = AuthorizationContext("runtime", LifecycleService.CAPABILITY)
        generation = Generation("gen-1", "bin-1", "schema-1", "0", "int-1")
        authority = InMemoryStateAuthority(
            generation,
            {"lifecycle": {"state": LifecycleState.READY.value}},
            authorization_policy=AuthorizationPolicy(),
        )
        service = LifecycleService(ConsumerBoundary(authority))

        result = service.validate_transition(
            service.request(LifecycleState.DEGRADED, context),
            LifecycleState.READY,
        )

        self.assertEqual(result, LifecycleState.DEGRADED)
        self.assertEqual(
            authority.read().payload["lifecycle"]["state"],
            LifecycleState.READY.value,
        )
        self.assertEqual(authority.read().state_version, 0)

    def test_malformed_authoritative_lifecycle_fails_closed(self):
        context = AuthorizationContext("runtime", LifecycleService.CAPABILITY)
        generation = Generation("gen-1", "bin-1", "schema-1", "0", "int-1")
        authority = InMemoryStateAuthority(
            generation,
            {"runtime": {"value": "unchanged"}},
            authorization_policy=AuthorizationPolicy(),
        )
        service = LifecycleService(ConsumerBoundary(authority))

        with self.assertRaises(ConsumerBoundaryError) as raised:
            service.transition(
                service.request(LifecycleState.INITIALIZING, context)
            )

        self.assertEqual(raised.exception.code, "operation_rejected")
        self.assertEqual(authority.read().payload["runtime"]["value"], "unchanged")
        self.assertEqual(authority.read().state_version, 0)

    def test_failure_during_update_preserves_canonical_state(self):
        context = AuthorizationContext("runtime", LifecycleService.CAPABILITY)
        policy = AuthorizationPolicy(
            {
                ("runtime", LifecycleService.CAPABILITY, "begin"),
                ("runtime", LifecycleService.CAPABILITY, "commit"),
                ("runtime", LifecycleService.CAPABILITY, "abort"),
            }
        )
        generation = Generation("gen-1", "bin-1", "schema-1", "0", "int-1")
        authority = InMemoryStateAuthority(
            generation,
            {"lifecycle": {"state": LifecycleState.PROVISIONING.value}},
            authorization_policy=policy,
        )

        class FailingConsumerBoundary(ConsumerBoundary):
            def update(self, transaction, payload):
                raise ConsumerBoundaryError("operation_rejected")

        service = LifecycleService(FailingConsumerBoundary(authority))

        with self.assertRaises(ConsumerBoundaryError) as raised:
            service.transition(
                service.request(LifecycleState.INITIALIZING, context)
            )

        self.assertEqual(raised.exception.code, "operation_rejected")
        self.assertEqual(
            authority.read().payload["lifecycle"]["state"],
            LifecycleState.PROVISIONING.value,
        )
        self.assertEqual(authority.read().state_version, 0)

    def test_toctou_revision_change_fails_closed(self):
        context = AuthorizationContext("runtime", LifecycleService.CAPABILITY)
        policy = AuthorizationPolicy(
            {
                ("runtime", LifecycleService.CAPABILITY, "begin"),
                ("runtime", LifecycleService.CAPABILITY, "commit"),
                ("runtime", LifecycleService.CAPABILITY, "abort"),
            }
        )
        generation = Generation("gen-1", "bin-1", "schema-1", "0", "int-1")
        authority = InMemoryStateAuthority(
            generation,
            {"lifecycle": {"state": LifecycleState.PROVISIONING.value}},
            authorization_policy=policy,
        )

        class RacingConsumerBoundary(ConsumerBoundary):
            def __init__(self, authority):
                super().__init__(authority)
                self._authority_for_test = authority
                self._raced = False

            def begin(self, request, payload=None):
                transaction = super().begin(request, payload)
                if not self._raced:
                    self._raced = True
                    race_tx = self._authority_for_test.begin(request.context)
                    race_tx.set_payload(
                        {"lifecycle": {"state": LifecycleState.INITIALIZING.value}}
                    )
                    self._authority_for_test.commit(race_tx)
                return transaction

        service = LifecycleService(RacingConsumerBoundary(authority))

        with self.assertRaises(ConsumerBoundaryError) as raised:
            service.transition(
                service.request(LifecycleState.INITIALIZING, context)
            )

        self.assertEqual(raised.exception.code, "stale_transaction")
        self.assertEqual(
            authority.read().payload["lifecycle"]["state"],
            LifecycleState.INITIALIZING.value,
        )
        self.assertEqual(authority.read().state_version, 1)

    def test_service_result_does_not_expose_mutable_canonical_alias(self):
        context = AuthorizationContext("runtime", LifecycleService.CAPABILITY)
        policy = AuthorizationPolicy(
            {
                ("runtime", LifecycleService.CAPABILITY, "begin"),
                ("runtime", LifecycleService.CAPABILITY, "commit"),
                ("runtime", LifecycleService.CAPABILITY, "abort"),
            }
        )
        generation = Generation("gen-1", "bin-1", "schema-1", "0", "int-1")
        authority = InMemoryStateAuthority(
            generation,
            {
                "lifecycle": {"state": LifecycleState.PROVISIONING.value},
                "runtime": {"mode": "normal"},
            },
            authorization_policy=policy,
        )
        service = LifecycleService(ConsumerBoundary(authority))

        result = service.transition(
            service.request(LifecycleState.INITIALIZING, context)
        )

        with self.assertRaises(TypeError):
            result.payload["runtime"]["mode"] = "tampered"

        self.assertEqual(
            authority.read().payload["lifecycle"]["state"],
            LifecycleState.INITIALIZING.value,
        )
        self.assertEqual(
            authority.read().payload["runtime"]["mode"],
            "normal",
        )

    def test_wrong_capability_transition_object_cannot_reach_authority(self):
        context = AuthorizationContext("runtime", "runtime.other")
        valid_generation = Generation(
            "gen-1", "bin-1", "schema-1", "0", "int-1"
        )
        authority = InMemoryStateAuthority(
            valid_generation,
            {"lifecycle": {"state": LifecycleState.PROVISIONING.value}},
            authorization_policy=AuthorizationPolicy(),
        )
        service = LifecycleService(ConsumerBoundary(authority))

        forged_request = type(
            "ForgedRequest",
            (),
            {
                "target": LifecycleState.INITIALIZING,
                "context": context,
            },
        )()

        with self.assertRaises(ConsumerBoundaryError) as raised:
            service.transition(forged_request)

        self.assertEqual(raised.exception.code, "invalid_request")
        self.assertEqual(
            authority.read().payload["lifecycle"]["state"],
            LifecycleState.PROVISIONING.value,
        )
        self.assertEqual(authority.read().state_version, 0)
