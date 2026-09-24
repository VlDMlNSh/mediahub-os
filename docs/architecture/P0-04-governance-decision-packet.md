# P0-04 — Governance Decision Packet v1.1

## Decision target

P0-04 In-Memory State Authority acceptance.

## Governance decision

**ACCEPTED — P0-04 In-Memory State Authority v1.0**

Decision scope is limited to the deterministic in-memory implementation defined by P0-03 and implemented by P0-04.

## Decision boundary

This acceptance does not authorize persistence or any production/appliance integration.

The following remain explicitly NOT AUTHORIZED:

- SQLite/ZFS/filesystem persistence;
- cloud or hardware persistence;
- bootloader/systemd/appliance integration;
- installer/recovery media;
- update engine;
- durable checkpoint authenticity;
- durable personal-data protection.

No merge is authorized by this governance decision unless separately approved.

## Evidence basis

Accepted implementation state was verified on exact commit:

`7bda2c703c639103f309c03d9ba702a47df4a85e`

Execution evidence on that exact HEAD:

- targeted P0-04 regression: **16/16 PASS**;
- full repository regression: **126/126 PASS**;
- prohibited-capability scan: **0 matches**;
- exact `git rev-parse HEAD`: matched reviewed commit;
- working tree: clean and synchronized.

Observed execution evidence is authoritative.

## Security and privacy position

P0-04 is accepted with its demonstrated security properties: single State Authority, candidate isolation, atomic publication, failure preservation, stale/concurrent transaction controls, generation/version binding, independent integrity validation, default-deny authorization, restore isolation and self-test/fail-closed behavior, immutable read/checkpoint boundaries, structural resource bounds, sanitized diagnostics, and absence of prohibited execution/network/filesystem/unsafe-deserialization capabilities in the scanned runtime scope.

Personal-data protection remains bounded to the demonstrated in-memory and diagnostics boundaries. Durable personal-data protection is deferred and requires a separate architecture and governance decision before persistence authorization.

## Deferred items

- cryptographic/durable checkpoint authenticity;
- crash consistency and durable atomicity;
- retention/deletion of durable state;
- durable personal-data protection;
- bootloader/systemd/appliance integration;
- installer/recovery media;
- update engine;
- SQLite/ZFS/filesystem persistence;
- cloud or hardware persistence.

## Governance consequence

P0-04 is now **ACCEPTED/FROZEN in the approved scope**.

Acceptance does not retroactively authorize out-of-scope capabilities. Any expansion of the State Authority into persistence, durable recovery, production/appliance integration, or other deferred areas requires a new explicit architectural and governance gate.
