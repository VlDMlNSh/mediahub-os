# MH-7 — Runtime Interaction

Status: CANDIDATE

Canonical application path:
Configuration Candidate → validation → policy → authorization → P0-05 → P0-04 transaction → atomic commit → runtime application → observed state.

Configuration and policy never directly mutate runtime state. Runtime consumes only validated and authorized representations.

Publication success and runtime application success are distinct facts. Application failure cannot be reported as successful publication.

Partial application and rollback semantics are UNKNOWN until an explicit runtime contract supplies evidence. Restart recovery remains UNKNOWN while physical persistence is unauthorized.
