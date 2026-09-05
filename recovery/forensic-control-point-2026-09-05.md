# MediaHub Forensic Reconstruction Control Point

Date: 2026-09-05
Branch: recovery/full-functional-spec
Status: IN PROGRESS — MASTER ARCHITECTURE NOT ACCEPTED

## Completed in this consolidated pass

- Source inventory established from currently accessible GitHub recovery corpus and accepted functional baseline references.
- 51 product domains registered.
- 58 canonical capabilities registered; cross-domain support does not create duplicate canonical functions.
- Loss audit performed against currently accessible evidence.
- Duplicate policy established and applied.
- Conflict registry established with explicit reconciliations and open technical questions.
- Ownership model established: one canonical owner per capability; supporting systems are not authority co-owners.
- Capability registry established.
- Contract registry established with 36 contract families.
- Invariant registry established with 30 system invariants.
- Master domain audit matrix established.
- Master architecture reconstruction drafted around control planes, capability planes and contracts.
- Development baseline and implementation boundaries are preserved as planning artifacts only; production implementation is not authorized.

## Confirmed preservation rules

- No function is removed because historical architecture cannot currently express it.
- DEFERRED means preserved/open, not rejected.
- Missing historical chat evidence is UNKNOWN, not LOSS.
- Surveillance recording is a native MediaHub capability and does not require a separate NVR where MediaHub can provide it.
- Surveillance storage and Personal Media Library storage remain separate logical domains.
- Home Assistant remains internal; MediaHub remains the user-facing Smart Home model.
- Health, readiness, liveness, trust, authentication and authorization remain semantically distinct.
- Local MediaHub Cluster and Cloud Development Cluster remain separate trust/control domains.
- Product variants retain explicit capability differences.
- Professional Engineering is a first-class contour distinct from ordinary UX.

## Material historical recovery finding

Currently accessible GitHub evidence identifies an expanded historical MH-18 media architecture. Its capabilities are preserved as recovery evidence and must be reconciled into the canonical model. This includes broader ingestion, metadata/provenance, indexing/search, duplicate detection, playback/streaming/live media, transcoding, subtitles/thumbnails/playlists, lifecycle, backup/recovery, migration, offline-first, export, privacy/security, AI analysis, API and observability concerns.

## Remaining gate blockers

1. Full machine-readable historical bodies for MH-01…MH-23 are not currently exposed in this runtime; exhaustive historical reconciliation therefore cannot truthfully be marked complete.
2. Material technical contracts remain deferred: exact HA boundary/version, vendor/device matrix, KINCONY firmware trust workflow, surveillance transports/modes, storage pool/filesystem semantics, cluster coordination/failover, cloud contribution controls, mobile transport, gaming topology, ecosystem bridge mechanisms, and exact cryptographic/key lifecycle choices.
3. User acceptance of the reconstructed master architecture has not occurred.

## Acceptance state

FUNCTIONAL BASELINE: CONFIRMED_ACCEPTED (upstream baseline)
FORENSIC RECONSTRUCTION: IN PROGRESS
MASTER ARCHITECTURE: DRAFT — NOT ACCEPTED
DISTRIBUTION TO MH-01…MH-23: BLOCKED UNTIL MASTER ARCHITECTURE ACCEPTANCE
PRODUCTION DEVELOPMENT: BLOCKED UNTIL REQUIRED ACCEPTANCE GATES

## Control rule

This document is a recovery checkpoint. Future chats must treat it as evidence of the current state and must not convert IN PROGRESS/DRAFT into COMPLETE/ACCEPTED without the missing evidence and explicit user acceptance.