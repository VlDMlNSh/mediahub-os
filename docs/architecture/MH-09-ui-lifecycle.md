# MH-09 — UI Lifecycle

**Status:** PROPOSED / REQUIRES VERIFICATION

Presentation lifecycle states: launch, initialization, authentication, authorization-context acquisition, loading, ready, degraded, offline, reconnecting, background, foreground, suspended, termination and recovery.

UI lifecycle is independent of runtime lifecycle. Re-entry, restoration and background/foreground transitions must not imply a canonical commit or re-authorize an operation. Pending operations require explicit outcome reconciliation.
