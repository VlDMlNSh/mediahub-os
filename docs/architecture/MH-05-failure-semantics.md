# MH-5 — Failure Semantics

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

Boundary failures are fail-closed unless an operation has an explicitly governed recovery behavior.

| Condition | Required disposition |
|---|---|
| invalid/malformed input | reject; no publication |
| unauthorized caller | deny |
| missing/unknown capability | deny |
| stale transaction | reject; do not rebase implicitly |
| invalid/forged handle | reject |
| policy denial/ambiguity | deny |
| timeout | terminate/return bounded failure; no hidden mutation |
| cancellation | stop at safe boundary; no implicit commit |
| dependency failure | fail without authority escalation |
| unknown device | remain untrusted; deny protected operation |
| unavailable external service | bounded failure; no implicit trust change |
| network partition | no implicit merge/LWW/recovery publication |
| duplicate command | operation-specific idempotency only |
| replay | reject or handle only under explicit command/replay semantics |
| conflicting request | deterministic conflict rejection unless governed otherwise |

Exactly-once delivery is not claimed. At-most-once, at-least-once, or effectively-once semantics must be specified per operation when required.
