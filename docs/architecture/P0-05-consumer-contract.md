# P0-05 — State Authority Consumer Contract v1.0

## Status

DRAFT — GOVERNANCE REVIEW REQUIRED

## Contract purpose

Define the normative interface boundary between consumers and the accepted/frozen P0-04 State Authority.

## Normative rules

1. State Authority is the sole authority for canonical state mutation.
2. `read` returns one consistent immutable canonical revision; consumers receive no mutable alias to authority-owned state.
3. `begin` requires an explicit authorization context and creates an isolated transaction bound to the observed generation and state version.
4. Candidate mutation occurs only inside the transaction boundary.
5. `commit` is the only consumer-visible publication path and revalidates authorization, transaction freshness, generation, structural bounds, and integrity before publication.
6. `abort` invalidates the candidate without modifying canonical state.
7. `snapshot` exposes only an authority-created checkpoint; consumers cannot construct an authoritative checkpoint accepted by the authority.
8. `restore` is a separately authorized operation and must preserve integrity, generation, self-test, isolation, and failure-preservation gates.
9. Stale transactions fail closed; last-writer-wins is prohibited.
10. AI/external proposals are inert data and have no execution or mutation capability.

## Consumer-specific boundary

| Consumer | Read | Request operation | Direct mutation | External execution |
|---|---|---|---|---|
| Runtime service | Yes | Authorized | No | No |
| UI/presentation | Yes | User/system request | No | No |
| Plugin/extension | Scoped | Capability-scoped | No | No |
| AI/proposal | Proposal inspection only | Via explicit authority outside proposal | No | No |
| Diagnostics/telemetry | Observation only | No | No | No |
| Future persistence adapter | Not implemented | Not implemented | No | No |

## Authorization hand-off

Authorization must be evaluated before a state operation is started. Consumer identity, requested operation, and applicable capability scope are inputs to authorization; consumers cannot self-grant authority.

## Error contract

Externally visible errors are stable, minimal, and sanitized. They must not expose secrets, authorization internals, sensitive state, local filesystem paths, network details, or implementation-private material.

## Resource contract

Consumer-provided state is subject to structural and size limits before expensive validation or publication. Rejection is fail-closed.

## Privacy contract

Consumers must minimize personal-data-bearing input. P0-05 provides no durable personal-data storage mechanism. Any future durable boundary requires a separate data-classification, minimization, retention, deletion, recovery, and governance decision.

## Compatibility

Consumers are bound to the P0-03/P0-04 contract and generation/version semantics. Contract changes require controlled architecture, security review, fresh execution evidence, and governance acceptance.

## Explicit exclusions

No persistence, network transport, filesystem mutation, subprocess execution, unsafe deserialization, bootloader/systemd integration, installer/recovery media, update engine, cloud persistence, hardware persistence, or production qualification is part of this contract.
