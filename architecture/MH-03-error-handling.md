# MH-03 Error Handling

**Status:** PROPOSED

Error classes:
- malformed input → reject;
- ambiguity → fail closed;
- missing authorization → deny;
- stale transaction → reject;
- unknown identity/device → deny or quarantine;
- critical dependency failure → not ready / controlled degraded;
- optional external dependency failure → isolate and degrade;
- service crash → supervised restart/isolation;
- State Authority failure → mutation unavailable; no fallback authority.

Errors must be observable without turning telemetry into mutation authority. Recovery actions are bounded by the same authority model as normal execution.
