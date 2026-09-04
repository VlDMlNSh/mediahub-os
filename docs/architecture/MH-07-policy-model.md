# MH-7 — Policy Model

Status: CANDIDATE

Policy defines admissibility under declared conditions. It is not authorization, runtime state, persistence, or mutation authority.

## Canonical shape
- identity
- namespace
- version/revision
- device-local scope in v1
- bounded declarative rules

Rules are deterministic, declarative, non-executable and bounded. v1 does not authorize wildcard matching, priority ordering, inheritance, hidden merging, LWW, or executable policy DSLs.

Policy cannot grant itself or another principal capabilities. Policy-engine failure is fail-closed.
