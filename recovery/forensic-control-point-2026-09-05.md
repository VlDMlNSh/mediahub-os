# MediaHub Forensic Reconstruction Control Point

Date: 2026-09-05
Branch: recovery/full-functional-spec
Status: IN PROGRESS — MASTER ARCHITECTURE NOT ACCEPTED

## Consolidated pass status

PASS 0 Source Inventory: IN PROGRESS — accessible GitHub corpus inventoried; full MH-01…MH-23 historical bodies are not exposed as one machine-readable corpus.
PASS 1 Function Inventory: COMPLETE against currently accessible accepted baseline/evidence — 51 canonical domains, 58 canonical capabilities.
PASS 2 Loss Audit: IN PROGRESS — no accessible-evidence item is silently classified as loss; historical gaps remain UNKNOWN.
PASS 3 Duplicate Audit: COMPLETE for current registries — one canonical capability ID; cross-domain support may reference the same capability without creating a new canonical function.
PASS 4 Conflict Audit: IN PROGRESS — known semantic conflicts reconciled; technical questions remain explicitly open.
PASS 5 Ownership Audit: COMPLETE at current boundary level — all 58 canonical capability owners have explicit implementation boundaries; further historical reconciliation remains separate.
PASS 6 Capability Reconstruction: COMPLETE at current canonical level — 58 capabilities registered; full source/contract/test/acceptance trace still being completed.
PASS 7 Contract Audit: IN PROGRESS — 36 contract families registered; material technical details remain deferred/open.
PASS 8 Invariant Audit: COMPLETE against accepted baseline — 30 invariants registered.
PASS 9 Verification/Acceptance Coverage: IN PROGRESS — acceptance evidence is materially present but only partially covers the canonical capability set.
Cross-reference consistency pass: COMPLETED for current dependency graph and capability-to-domain mapping.

## Repairs made in this recovery cycle

1. Dependency graph schema upgraded to 1.1. Every dependency edge endpoint is now explicitly declared as a node; undefined endpoints `health_readiness`, `notification`, and `all_components` were resolved by declaring semantic nodes and removing the non-semantic `all_components` dependency edge.
2. Capability-to-domain mapping normalized to exactly 51 unique domain IDs. CAP-054..CAP-058 are mapped into existing canonical domains instead of creating duplicate domain IDs.
3. Supporting cross-domain relationships remain allowed; canonical capability ownership remains singular.
4. Product/runtime implementation-boundary gaps for `product_core` and `runtime_core` were corrected.
5. Verification/acceptance coverage audit was added as `recovery/verification-acceptance-coverage-audit-2026-09-05.md` (commit `b2e73fdc76163a831db11f62861866c322599e42`).

## Verification / acceptance evidence finding

The accessible `recovery/accepted/` tree contains F-006 presence/people/context and F-007 users/identity/access/authorization.

The accessible `recovery/acceptance/` tree contains F-007 security/trust/safety through F-015 HDMI/display, covering security, energy, remote/mobile/cloud escalation, personal media, surveillance, media, audio, phone I/O and HDMI/display.

Direct repository code searches for F-001…F-005 returned no matching results. This is an evidence gap only and is not evidence that the corresponding functionality never existed.

Historical commit search independently confirms acceptance-criteria/governance records for MH-03, MH-06, MH-10, MH-12, MH-13, MH-14, MH-15, MH-21 and MH-22. Other MH contours without matching accessible commits remain UNKNOWN.

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
- Acceptance coverage and architectural acceptance are separate gates.

## Material historical recovery finding

Currently accessible GitHub evidence identifies an expanded historical MH-18 media architecture. Its capabilities are preserved as recovery evidence and must be reconciled into the canonical model. This includes broader ingestion, metadata/provenance, indexing/search, duplicate detection, playback/streaming/live media, transcoding, subtitles/thumbnails/playlists, lifecycle, backup/recovery, migration, offline-first, export, privacy/security, AI analysis, API and observability concerns.

## Remaining gate blockers

1. Full machine-readable historical bodies for MH-01…MH-23 are not currently exposed in this runtime; exhaustive historical reconciliation therefore cannot truthfully be marked complete.
2. Material technical contracts remain deferred: exact HA boundary/version, vendor/device matrix, KINCONY firmware trust workflow, surveillance transports/modes, storage pool/filesystem semantics, cluster coordination/failover, cloud contribution controls, mobile transport, gaming topology, ecosystem bridge mechanisms, and exact cryptographic/key lifecycle choices.
3. Full CAP-001…CAP-058 verification and acceptance evidence matrix is not yet proven.
4. User acceptance of the reconstructed master architecture has not occurred.

## Acceptance state

FUNCTIONAL BASELINE: CONFIRMED_ACCEPTED (upstream baseline)
FORENSIC RECONSTRUCTION: IN PROGRESS
MASTER ARCHITECTURE: DRAFT — NOT ACCEPTED
DISTRIBUTION TO MH-01…MH-23: BLOCKED UNTIL MASTER ARCHITECTURE ACCEPTANCE
PRODUCTION DEVELOPMENT: BLOCKED UNTIL REQUIRED ACCEPTANCE GATES

## Latest checkpoint commits

- Verification/acceptance coverage audit: `b2e73fdc76163a831db11f62861866c322599e42`
- Implementation-map correction: `d9adc5b979adaa24d365cd0e76c9a8c0c0d040ae`
- Full semantic traceability: `b54294d1af6d39c3926a5bfd2bec4964f6fa3a98`
- Forensic closure matrix update: `ce0e280ce2158e437b6b1ca2904ccbd593ae4a3c`

## Control rule

This document is a recovery checkpoint. Future chats must treat it as evidence of the current state and must not convert IN PROGRESS/DRAFT into COMPLETE/ACCEPTED without the missing evidence and explicit user acceptance.
