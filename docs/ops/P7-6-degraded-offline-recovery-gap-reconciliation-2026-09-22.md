# P7.6 — Degraded/offline behavior and recovery evidence

Status: DISCOVERY_RECONCILIATION / P7.6 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for existing degraded/offline and recovery requirements relevant to the Cloud Development AI boundary. It does not infer provider outage, network outage, cloud availability, credentials, provider guarantees, provider recovery or external execution results.

## Deterministic classification

- Existing local-first/offline and generic degraded/recovery declarations: PRESENT where recorded below.
- Existing generic resilience implementation/tests: PRESENT in the inspected repository surfaces.
- Cloud Development AI-specific degraded/offline acceptance and externally observable recovery: NOT ESTABLISHED by this reconciliation alone.
- Overall P7.6 status: PARTIAL — repository-level requirements and generic resilience evidence exist, but subsystem-specific acceptance is not demonstrated here.

## Acceptance boundary

The following remain separate until domain-specific deterministic evidence exists: provider/network outage, cloud availability, credential readiness, provider recovery, external execution, and end-to-end Cloud Development AI recovery. No such external fact is asserted by this artifact.

## Source evidence

### specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md
SHA256: 9cab7f0518208ecaeae8f605785a9e25eb9ed1ae9db420b19898fe83059dc18a
- 31: → Mobile Access Layer / Cloud Development AI → controlled development infrastructure.
- 115: **Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI**.
- 124: Cloud Development AI — корпоративная облачная вычислительная среда MediaHub. Обычные пользователи
- 134: Trusted Sources Intelligence Engine — first-class Cloud Development AI subsystem:
- 143: AI Human Clone — отдельная Cloud Development AI subsystem для авторизованного media content:
- 173: ## 12. CLOUD DEVELOPMENT AI И DEVELOPMENT ENVIRONMENT
- 175: Cloud Development AI включает Website, Trusted Sources Intelligence, AI Human Clone,
- 199: ## 14. UPDATE / BACKUP / RECOVERY

### specification/invariant-registry.yaml
SHA256: a73fc89921980839622d586f19c5b5499a03c14036fcb670daff015b102ac4fc
- 12: - INV-009: Offline-first operation where technically possible
- 26: - INV-023: Readiness is operation-scoped
- 27: - INV-024: Health, Readiness, Liveness, Trust and Authorization remain distinct
- 49: - INV-045: AI escalation order is Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI

### specification/decision-registry.yaml
SHA256: b668cba90558f93f6889a346a079e7040f2b81bd1da6e96f38edcd43715d5827
- 13: decision: "Local-first/offline-first is mandatory product direction where technically possible."
- 19: decision: "Health is observation-only; Readiness is operation-scoped."
- 42: decision: "Adopt MediaHub AI escalation as Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI; Mobile Access Layer is not an AI compute tier, routed by a deterministic AI Gateway."

### docs/architecture/MH-06-recovery-model.md
SHA256: ae656807154400ecc0b6f4a422a2b432db156b183252d737115d90ede7ef3bd4
- 1: # MH-06 — Recovery Model
- 5: Low-risk candidates: service restart, reconnect, cache rebuild, queue cleanup, stale-session expiration, certificate renewal, bounded retry, degraded mode.
- 11: Every recovery action requires trigger, risk/confidence assessment where applicable, authorization, audit context, rate/attempt bounds and quarantine condition. Recovery never becomes a second mutation authority.

### docs/architecture/MH-06-health-readiness.md
SHA256: d694ad35ad0366e44d843d7823e46a50081c4d00b63011101b3cbf44c34efa41
- 1: # MH-06 — Health / Readiness
- 4: ADR: `docs/architecture/MH-06-ADR-001-health-readiness-semantic-contract.md`
- 9: Liveness is the ability of a process/service to perform its basic runtime loop. Health is observation. Readiness is an operation-scoped derived verdict. Neither health nor readiness implies trust, authorization, capability or mutation authority.
- 11: `P0-06 LifecycleState.READY != MH-06 Readiness.READY`.
- 17: - DEGRADED
- 23: ## Readiness results
- 28: - DEGRADED
- 31: Readiness is evaluated as `Readiness(operation, observations) -> verdict`. UNKNOWN never becomes READY automatically. READY requires all mandatory prerequisites for the specified operation. DEGRADED is valid only where the operation contract explicitly permits degraded execution. QUARANTINED blocks normal-operation readiness.

### ops/mediahub_resilience.py
SHA256: e2473f5382c56aea1d41a2b61c96e9066cf10884060fc3dc31c8e1afa81f0831
- 1: """Native bounded retry and circuit-resilience primitives.
- 49: class ResilienceDecision:
- 58: class ResilienceEngine:
- 65: def first(self, *, now: float | None = None) -> ResilienceDecision:
- 67: return ResilienceDecision(decision.provider, None, False, 1, 0.0, decision.reason)
- 78: ) -> ResilienceDecision:
- 82: return ResilienceDecision(None, failure, False, attempt, 0.0, "retry budget exhausted")
- 85: return ResilienceDecision(None, decision.failure, False, attempt, 0.0, decision.reason)

### tests/test_mediahub_resilience.py
SHA256: 97869fd0b857bd23a7704b7cc9be8407cf031c67fd5d9d5de0fc1614bc9e1975
- 4: from ops.mediahub_resilience import ResilienceEngine, RetryPolicy
- 22: engine = ResilienceEngine(gateway(), RetryPolicy(max_attempts=3))
- 30: engine = ResilienceEngine(gateway(), RetryPolicy(max_attempts=3))
- 38: engine = ResilienceEngine(gateway(), RetryPolicy(max_attempts=2, base_delay_seconds=0.5))
- 47: engine = ResilienceEngine(gateway(), RetryPolicy(max_attempts=1))
