# MH-7 — Policy Evaluation

Status: CANDIDATE

Evaluation is deterministic, bounded and observational.

Pipeline: input → validation → normalization → exact applicable rules → conflict detection → decision → bounded diagnostics.

v1 decision semantics:
- malformed → DENY
- unsupported → DENY
- no match → DENY
- ambiguity/conflict → DENY
- explicit DENY → DENY
- explicit ALLOW without conflict → ALLOW

No implicit priority, wildcard, inheritance, hidden merge, LWW, retry, rebase, or hidden conflict resolution is permitted.
