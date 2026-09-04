# MH-7 — Configuration Model

Status: CANDIDATE

Configuration represents desired behavior, never effective runtime state and never mutation authority.

## Canonical shape
- identity
- namespace
- schema version
- device-local scope in v1
- bounded metadata
- desired declarative value
- revision/publication metadata when governed

Configuration objects are immutable, bounded, structured, declarative, non-executable, and transient in v1. Opaque references are inert and are not dereferenced.

## Authority
A candidate is non-authoritative until it passes validation, policy admissibility, principal authorization, the controlled P0-05 ingress, and P0-04 atomic publication.

No configuration object may contain credentials, executable instructions, hidden policy, capability grants, or persistence semantics.
