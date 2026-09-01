# P0-04 — State Authority Abuse-Case Register v1.0

## Status

**Prepared / pre-implementation security artifact**

This register supports P0-04 implementation and adversarial verification. It does not authorize implementation and does not change the formal P0-03 acceptance state.

## Security objective

Preserve the State Authority as the sole authoritative boundary for canonical runtime state while preventing unauthorized, stale, malformed, partial, externally mutated, or integrity-invalid state from becoming canonical.

## Abuse cases

| ID | Abuse case | Required invariant | Expected result |
|---|---|---|---|
| AC-01 | Caller attempts to mutate canonical state directly | SA-001, SA-011 | Mutation unavailable / rejected |
| AC-02 | Transaction candidate is modified after begin by another transaction | SA-002 | Other transaction cannot observe or alter candidate |
| AC-03 | Stale transaction commits over newer canonical state | SA-004, SA-006 | Commit rejected fail-closed |
| AC-04 | Caller supplies desired canonical revision/state version | SA-004, SA-005 | Caller-selected revision rejected |
| AC-05 | Compatible generation with invalid integrity is committed | SA-006, SA-007 | Integrity gate rejects commit |
| AC-06 | Valid integrity reference with incompatible generation is committed | SA-006, SA-007 | Compatibility gate rejects commit |
| AC-07 | Unauthorized restore is attempted | SA-010, SA-014 | Restore rejected without canonical mutation |
| AC-08 | Restore candidate fails validation/self-test | SA-008, SA-012 | Previous canonical state preserved |
| AC-09 | Accepted checkpoint identity is altered through restore | SA-009 | Checkpoint identity remains immutable |
| AC-10 | Malformed serialized state is treated as trusted | SA-013 | Input rejected before canonical publication |
| AC-11 | Hostile string resembles a command/path/expression | Security boundary | Treated strictly as data |
| AC-12 | Diagnostic payload contains nested sensitive data | Privacy-safe diagnostics | Sensitive values redacted recursively |
| AC-13 | Terminal transaction handle is reused | Transaction lifecycle | Operation rejected fail-closed |
| AC-14 | Failed commit partially publishes candidate data | SA-003, SA-012 | No partial canonical state visible |
| AC-15 | Concurrent readers observe mixed revisions | SA-003 | Reader sees one complete canonical revision |
| AC-16 | Oversized candidate attempts resource exhaustion | Resource bounds | Request rejected within defined bounds |
| AC-17 | AI/external actor attempts to become mutation authority | SA-011 | No executable mutation path exists |
| AC-18 | Error path exposes sensitive state | Privacy/security | Error remains typed and sanitized |

## Verification rule

Each abuse case must map to one or more deterministic tests or concrete implementation evidence before P0-04 can be accepted.

A passing unit test alone is insufficient where the property concerns capability absence, atomic publication, concurrency, resource limits, or diagnostic privacy; those require the appropriate execution/security evidence.

## Non-goals

This register does not introduce or authorize SQLite, ZFS, filesystem persistence, subprocesses, network transport, bootloader/systemd appliance behavior, installer/recovery media, update engine, cloud persistence, or hardware persistence.

## Governance

Formal P0-03 acceptance remains **PENDING**. P0-04 implementation remains **NOT AUTHORIZED** until an explicit governance decision grants that authorization.
