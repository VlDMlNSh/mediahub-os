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
