# MH-17 — Device Failure Model

**Status:** PROPOSED / CANDIDATE

Failure states distinguish transport failure, protocol failure, authentication/authorization failure, device rejection, device offline, stale observation, timeout, partial application, and unknown outcome.

`Timeout ≠ Physical Failure`; `Sent ≠ Applied`; `Applied ≠ Confirmed`. For ambiguous non-idempotent commands, retry is forbidden unless an explicit recovery policy establishes safety.

Repeated or security-significant failures may transition the integration into Degraded or Quarantined state. Failure handling MUST preserve evidence and MUST NOT bypass State Authority.
