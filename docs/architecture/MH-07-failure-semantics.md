# MH-07 — Failure Semantics

Status: CANDIDATE.

Malformed configuration/policy → reject / NO APPLY. Unsupported schema/semantics → DENY or reject. Conflicting policy → DENY. Missing capability → DENY. Unauthorized update → DENY. Stale revision → fail closed. Policy-engine failure → NO APPLY unless a separately accepted hard-safety rule mandates otherwise.

Runtime incompatibility → NO APPLY. Partial application must not be treated as authoritative without an explicit runtime contract; absent that contract, publication is not considered applied.

Rollback is an explicit authorized operation, not hidden retry/rebase. P0-07 does not invent persistence for restart/recovery.
