# P0-05 — Implementation Workplan v1.0

## Status

IMPLEMENTATION AUTHORIZED — controlled scope

## Objective

Implement the P0-05 consumer integration boundary around the frozen P0-04 State Authority without changing State Authority semantics or introducing persistence.

## Work packages

### WP-01 — Consumer facade

Provide a narrow integration facade for canonical reads and explicit operation requests. No direct mutable canonical-state reference is exposed.

### WP-02 — Authorization hand-off

Require explicit authorization context at operation entry. Preserve default-deny behavior and operation-specific capability scope.

### WP-03 — Transaction adapter

Expose only controlled transaction lifecycle operations: begin, candidate update, commit, abort. Preserve generation/state-version freshness and failure preservation.

### WP-04 — UI/request boundary

Represent UI intent as inert request data. UI has no direct mutation capability and cannot select canonical revisions.

### WP-05 — Plugin capability boundary

Define capability-scoped requests. Reject undeclared or unauthorized operations before state mutation.

### WP-06 — AI proposal boundary

Accept proposal data only. No proposal API may execute commands, mutate canonical state, choose revisions, bypass authorization, or initiate network/filesystem activity.

### WP-07 — Diagnostics boundary

Allow observation without mutation. Preserve sanitized errors and diagnostic privacy guarantees.

### WP-08 — Security/privacy verification

Implement negative-path tests for bypass, aliasing, privilege escalation, stale transactions, hostile proposals, malformed input, leakage, and prohibited capabilities.

## Explicit non-goals

No SQLite/ZFS/filesystem persistence, durable checkpoint storage, network transport, subprocess execution, cloud/hardware persistence, bootloader/systemd integration, installer/recovery media, update engine, or production qualification.

## Stop conditions

Stop implementation on any authority bypass, mutable canonical alias, implicit authorization, executable AI path, unscoped plugin capability, new durable path, prohibited side effect, privacy boundary violation, or divergence from approved architecture.

## Evidence

Acceptance requires exact-commit execution evidence on `mh-dev-01`, targeted and full regression, security/privacy negative-path verification, prohibited-capability scan, and governance disposition.
