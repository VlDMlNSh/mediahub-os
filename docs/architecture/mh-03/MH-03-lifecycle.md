# MH-03 Lifecycle

State machine:
`ABSENT → INITIALIZING → STARTING → READY ↔ DEGRADED/RECOVERING → STOPPING → STOPPED`.

Invalid transitions are rejected without partial transition.

READY requires critical dependencies and State Authority readiness. Optional dependency failure may produce DEGRADED when deterministic operation remains safe.

Recovery is bounded by approved policy; repeated failure must not create authority escalation.
