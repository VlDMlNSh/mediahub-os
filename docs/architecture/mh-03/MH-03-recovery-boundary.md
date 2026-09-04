# MH-03 Recovery Boundary

Recovery is bounded runtime coordination, not authority escalation.

Allowed classes: service restart, dependency reinitialization, transition to degraded mode, controlled stop, and re-readiness checks when explicitly covered by policy.

Forbidden: creating a replacement canonical state store, bypassing authorization, promoting cache/persistence/cloud/AI to authority, widening capabilities after failure, or arbitrary shell/filesystem/network execution.

Recovery loops must be bounded and observable. Repeated failure leads to controlled DEGRADED or STOPPED state according to approved policy.
