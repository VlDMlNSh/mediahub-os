# P0-04 Implementation Scope Lock v1.0

## Status

Prepared. This lock is a governance constraint, not implementation authorization.

## Authorized scope after explicit governance approval

P0-04 may implement only the deterministic in-memory State Authority contract:

- canonical state representation;
- isolated candidate transactions;
- begin/commit/abort lifecycle;
- authority-owned monotonic revision sequencing;
- generation compatibility validation;
- independent integrity validation seam;
- operation-specific default-deny authorization;
- immutable checkpoint identity;
- restore through candidate validation and new canonical revision;
- bounded inputs and safe diagnostics;
- functional, adversarial, security, and privacy verification.

## Explicitly outside the scope lock

The following are prohibited from being introduced under P0-04:

- SQLite or any other persistence implementation;
- ZFS, filesystem persistence, or storage orchestration;
- subprocesses or arbitrary command execution;
- network sockets, HTTP clients, telemetry, or mTLS transport;
- bootloader/systemd appliance integration;
- installer or recovery media;
- update/rollback engine;
- cloud persistence or remote state authority;
- hardware-backed persistence or hardware security integration;
- production deployment topology;
- real user/private data in fixtures or evidence.

## Scope-change rule

If a proposed change requires an excluded capability, stop P0-04 work and open a separate architecture/security scope decision. Do not reinterpret the change as an implementation detail.

## Authority rule

No branch, issue, PR, workplan, test plan, or source change itself grants authorization. P0-03 formal acceptance must explicitly precede implementation.

## Verification rule

Every in-scope security invariant must be demonstrable by tests or inspection on an exact immutable implementation commit. Missing evidence is a gate blocker, not an implicit PASS.

## Historical boundary

This scope lock does not infer historical MH-02…MH-16 responsibilities.
