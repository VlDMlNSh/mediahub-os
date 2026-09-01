# P0-04 — Governance Decision Packet v1.0

Status: SECURITY REVIEW COMPLETE WITH CONDITIONS; GOVERNANCE ACCEPTANCE PENDING.

## Decision scope

This packet covers only P0-04: deterministic in-memory State Authority implementation.

Persistence remains NOT AUTHORIZED. SQLite, ZFS/filesystem persistence, network transport, subprocess/arbitrary command execution, bootloader/systemd appliance integration, installer/recovery media, update engine, cloud persistence, and hardware persistence remain outside scope.

## Authorization baseline

P0-03 State Authority Contract v1.0 was explicitly accepted before P0-04 implementation authorization.

P0-04 implementation was authorized strictly as an in-memory implementation. Authorization to implement is not acceptance of the implementation.

## Executed implementation evidence

Exact implementation commit executed on validation host:

`456deb9aadd3cae7d8978a7d89f540e1a029b7f4`

Environment:

- host: `mh-dev-01`
- Python: 3.12.3
- Linux kernel: 6.8.0-138-generic
- architecture: x86_64

Evidence:

- full repository regression: 123/123 PASS, 0 failures, 0 errors
- targeted P0-04 regression: 13/13 PASS, 0 failures, 0 errors
- prohibited-capability read-only grep: no matches

The later documentation commit does not replace the exact implementation identity of the execution evidence.

## Security verification assessment

### Demonstrated by execution

- single-authority mutation path within the implementation
- candidate isolation from canonical state
- serialized commit behavior and stale-writer rejection
- authority-owned monotonic revisions
- generation compatibility checks
- independent integrity validation gate
- operation-specific default-deny authorization
- authority-bound checkpoint validation
- checkpoint immutability at the dataclass boundary
- malformed and oversized state rejection
- hostile strings remain data
- terminal transaction enforcement

### Security conditions still required before acceptance

1. **Restore self-test gate** — P0-03 semantics require candidate restore validation followed by self-test before publication. The current implementation validates structure, generation, and integrity but exposes no explicit restore self-test stage. This must be resolved or formally bounded by an approved contract clarification before acceptance.

2. **Broader negative-path evidence** — targeted tests cover important adversarial paths but do not yet independently demonstrate every SEC-SA-01..18 item. In particular, explicit tests/evidence are still desirable for unauthorized commit/abort/restore, restore failure preservation, generation mismatch preservation, and mutation attempts against returned state/checkpoint data.

3. **Checkpoint authenticity limitation** — in-memory authority-token binding is intentionally non-cryptographic and non-durable. Cryptographic checkpoint authenticity is deferred by scope and therefore remains a known residual risk, not a claim of durable trust.

4. **Read-boundary immutability clarification** — `CanonicalState` is frozen, while its returned payload is a detached mutable copy. This preserves authority state isolation, but the contract phrase “immutable-at-read-boundary logical revision” should be explicitly reconciled with this representation before a future persistent implementation.

5. **Evidence integrity** — final acceptance must retain exact executed commit, environment, commands, and outputs as the authoritative evidence tuple.

## Privacy assessment

No secrets or personal-data-bearing fixtures are required for the demonstrated P0-04 tests. Failure classes exposed by the implementation are intentionally generic and do not serialize candidate state or authorization context.

The hostile-input test confirms that command-like text is treated as ordinary data. This is defensive validation only and introduces no execution primitive.

Privacy review remains bounded to the in-memory state layer; persistence, retention, deletion, export, and durable personal-data handling are not assessed because they are not authorized in P0-04.

## Governance disposition

**P0-04 ACCEPTANCE: NOT GRANTED.**

The implementation has strong execution evidence and passes the declared regression slice, but acceptance is blocked until the restore self-test requirement and the remaining security/evidence conditions above are resolved or explicitly dispositioned by governance.

PR #12 must remain open/draft and must not be merged as a consequence of this packet.

Persistence remains NOT AUTHORIZED.
