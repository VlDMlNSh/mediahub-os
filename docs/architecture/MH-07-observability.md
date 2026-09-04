# MH-7 — Observability

Status: CANDIDATE / EVIDENCE REQUIRED

Observability must distinguish at minimum: candidate, validation result, policy decision, authorization result, publication attempt, commit result, application result and observed runtime state.

Diagnostics are bounded and must not expose credentials or sensitive payloads. Deny/conflict/stale outcomes must remain distinguishable for verification and auditability.

No observability mechanism may become a mutation or persistence authority. Concrete telemetry schema and retention semantics remain subject to evidence and governance.
