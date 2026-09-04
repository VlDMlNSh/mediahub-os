# MH-7 — Failure Semantics

Status: CANDIDATE

Malformed configuration/policy, unsupported schema, policy conflict, stale revision, unauthorized operation, missing capability, policy-engine failure and runtime incompatibility fail closed: DENY, NO APPLY, or transaction abort as applicable.

Application failure must never be represented as successful publication.

No hidden retry, recovery, merge, rebase or fallback is permitted. Partial application, rollback and restart recovery remain UNKNOWN until explicitly contracted and evidenced.
