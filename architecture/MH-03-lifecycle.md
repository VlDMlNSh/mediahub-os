# MH-03 Lifecycle

**Status:** PROPOSED

State machine:

`ABSENT → INITIALIZING → STARTING → READY ↔ DEGRADED/RECOVERING → STOPPING → STOPPED`

Rules:
- READY requires critical dependencies and State Authority readiness.
- Optional dependency failure may yield DEGRADED rather than total failure.
- Recovery must remain inside existing authority boundaries.
- State Authority failure does not permit a shadow state store or fallback mutation authority.
- Shutdown is ordered and controlled; new work is stopped before dependent services are terminated.
