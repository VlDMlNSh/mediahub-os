# MH-06 — Lifecycle Model

Status: REQUIRES VERIFICATION against frozen P0-06 implementation/evidence.

P0-06 accepted lifecycle values are: PROVISIONING, INITIALIZING, SELF_TEST, READY, DEGRADED, SAFE_MODE, RECOVERY.

Allowed transitions:
PROVISIONING->INITIALIZING; INITIALIZING->SELF_TEST; SELF_TEST->READY|DEGRADED|SAFE_MODE; READY->DEGRADED|SAFE_MODE; DEGRADED->READY|SAFE_MODE; SAFE_MODE->RECOVERY; RECOVERY->INITIALIZING.

Lifecycle state is canonical only inside P0-04 State Authority under the accepted lifecycle field. Local LifecycleStateMachine state is a validator/compatibility primitive, not a canonical store.

Runtime service lifecycle and health lifecycle are separate concepts. STOPPING, STOPPED, FAILED and QUARANTINED must not be added to canonical P0-06 lifecycle without governance evidence.
