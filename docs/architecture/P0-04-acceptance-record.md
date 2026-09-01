# P0-04 Acceptance Record

**Status:** ACCEPTED / FROZEN

## Governance decision

P0-04 In-Memory State Authority v1.0 is accepted within its explicitly bounded scope.

The governance decision explicitly does **not** authorize persistence.

## Evidence basis

Accepted implementation state:
- exact HEAD: `7bda2c703c639103f309c03d9ba702a47df4a85e`
- targeted P0-04 regression: 16/16 PASS
- full repository regression: 126/126 PASS
- prohibited-capability scan: 0 matches
- working tree: clean and synchronized with origin
- security exit: READY

## Accepted properties

The accepted implementation provides the P0-03 State Authority contract through a deterministic in-memory implementation, including:

- single authoritative state mutation boundary;
- isolated transactions and stale-writer rejection;
- atomic publication semantics within the in-memory scope;
- monotonic authority-owned state versions;
- generation binding;
- independent integrity validation;
- default-deny authorization;
- isolated restore with integrity and self-test gates;
- immutable read/checkpoint boundaries;
- checkpoint authority binding within the in-memory authority instance;
- structural and resource bounds;
- fail-closed security behavior and sanitized outward failures;
- no direct execution, network, filesystem mutation, unsafe deserialization, or AI mutation path.

## Explicitly excluded

The acceptance does not authorize or qualify:

- SQLite or any persistent state store;
- ZFS snapshots or rollback;
- durable/cryptographic checkpoint authenticity;
- crash-consistency or durable atomicity;
- retention/deletion policy for durable data;
- durable personal-data protection mechanisms;
- bootloader/systemd appliance integration;
- installer/recovery media;
- update engine;
- cloud persistence;
- hardware persistence;
- production topology or deployment qualification.

## Freeze rule

P0-04 semantics are frozen at this accepted state. Any change to the accepted contract, security properties, or implementation semantics requires a new controlled change with fresh execution evidence and governance review.

Persistence remains **NOT AUTHORIZED**.
