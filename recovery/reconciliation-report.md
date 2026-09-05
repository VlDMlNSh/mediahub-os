# MediaHub Forensic Reconciliation Report

Date: 2026-09-05
Status: IN PROGRESS — not an acceptance record

## Executive result

The accepted master passport establishes a substantially complete product-level functional baseline. The forensic pass confirms that the architecture must be reconstructed around capabilities and contracts rather than around historical P0-P8 boundaries or chat ownership.

## Reconciled principles

1. Functional requirements are primary.
2. Home Assistant remains internal and hidden behind MediaHub.
3. Surveillance recording is a native MediaHub capability; separate NVR is not mandatory.
4. Surveillance storage and Personal Media Library storage remain distinct logical domains.
5. Local-first/offline-first is a runtime property, not a cloud-hosted approximation.
6. Local Cluster and Cloud Development are separate trust/control contours.
7. Security, privacy, identity, trust and authorization are cross-cutting.
8. Product variants are capability-specific, not merely packaging variants.
9. Professional Engineering is a first-class product contour.
10. Deferred technical choices remain explicit open items.

## Historical recovery finding

The GitHub source inventory identifies a materially broader historical MH-18 media architecture than the current mainline. It must be reconciled into the master capability model rather than discarded. Because the full text of all MH-01…MH-23 chats is not exposed as one machine-readable corpus in this runtime, exhaustive historical reconciliation cannot yet be claimed.

## Duplicate policy

Canonical capabilities are unique by product meaning. A capability may have multiple supporting domains, contracts and UI surfaces without creating duplicate function records.

## Ownership policy

Each canonical capability receives one owner. Supporting domains do not become co-owners of authority. State authority, command authority and security authority are explicit boundaries.

## Semantic gaps still open

- Exact State Authority semantics and mutation model.
- Exact Home Assistant version/fork/adapter boundary.
- Vendor/protocol support matrix and device families.
- KINCONY firmware authenticity and safe flashing workflow.
- Surveillance transport, recording modes, retention and recovery details.
- Storage pool/filesystem/rebalance details.
- Network AP/mesh/controller replacement details.
- Local cluster coordination/scheduling/failover.
- Cloud compute contribution/privacy/metering.
- Mobile transport and iOS/Android platform limits.
- Gaming transport/capture/input topology.
- HomeKit/Yandex/Loxone technical bridge mechanisms.
- Exact security threat model, cryptographic algorithms and key lifecycle.

## Acceptance gate

MASTER ARCHITECTURE remains DRAFT until the historical corpus gap is closed to the required level, all material conflicts are reconciled or explicitly accepted as deferred, and the user performs acceptance.
