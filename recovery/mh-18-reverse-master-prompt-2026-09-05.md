# MH-18 REVERSE MASTER PROMPT — 2026-09-05

MH: MH-18
Scope: Media / Content Architecture
Repository: VlDMlNSh/mediahub-os
Branch: recovery/full-functional-spec
Status: RECONCILED WITH AVAILABLE EVIDENCE / NOT ACCEPTED / NOT FROZEN

## 1. Historical scope
Available MH-18 architecture context covered media/content ingestion, identity, lifecycle, metadata/provenance, storage, indexing/search, playback, streaming, transcoding, thumbnails/previews, playlists, subtitles, rights/DRM, live media, AI analysis, privacy, security/sandboxing, cache, offline-first, backup/recovery, migration, observability, resource governance, plugins, API/export, supply chain and testing/technology evaluation.

## 2. Evidence inventory / provenance
Canonical recovery baseline and registries were fetched from `recovery/full-functional-spec`. The historical MH-18 architecture artifact was fetched from branch `mh-18-media-content-architecture`, path `docs/architecture/MH-18-media-content-architecture.md`, blob SHA `6fd226c08c9d915f73c3adf160858cf1137d8c05`.

Repository search did not expose additional ref-specific MH-18 implementation material on the available search surface. This is recorded as an evidence gap, not absence.

## 3. CAP mapping
Primary direct mappings: CAP-010, CAP-011, CAP-013, CAP-014, CAP-015, CAP-016, CAP-017, CAP-036, CAP-037, CAP-041, CAP-042, CAP-043, CAP-048, CAP-049, CAP-050, CAP-051, CAP-056.
Cross-domain protected mappings/dependencies: CAP-008, CAP-009, CAP-012, CAP-018, CAP-023, CAP-024, CAP-025, CAP-026, CAP-027, CAP-031, CAP-032, CAP-035, CAP-039, CAP-040, CAP-058.
No CAP-001…CAP-058 is proposed for removal, retirement or semantic loss.

## 4. Requirement mapping
The MH-18 requirements are preserved as contracts for:
- safe multi-source media ingestion;
- stable content/asset/object/storage identity separation;
- validation/integrity/security/policy gates;
- metadata normalization and provenance;
- Personal Media Library;
- surveillance recording/media boundary;
- indexing/search as derived systems;
- playback and media sessions;
- streaming/live media;
- transcoding and derivative generation;
- playlists/subtitles/artwork;
- rights/DRM boundary;
- AI candidate metadata;
- storage/lifecycle/deletion;
- privacy and export controls;
- backup/recovery/migration;
- observability/resource governance;
- plugin/API extensibility;
- compatibility/security/privacy/performance/recovery verification.

## 5. Contract mapping
Primary: CTR-001, CTR-011, CTR-012, CTR-013, CTR-014, CTR-015, CTR-025, CTR-026, CTR-028, CTR-032, CTR-033, CTR-034, CTR-035, CTR-036.
Cross-domain: CTR-003, CTR-004, CTR-016, CTR-017, CTR-019, CTR-023, CTR-024, CTR-029 where applicable.

## 6. Invariant mapping
Primary: INV-001, INV-002, INV-008, INV-009, INV-010, INV-011, INV-013, INV-021, INV-024, INV-025, INV-026, INV-027, INV-029, INV-030.
Product/cluster/device references additionally preserve INV-017 and INV-018 where applicable.

## 7. Decision mapping
Applicable accepted decisions: DEC-001, DEC-003, DEC-004, DEC-005, DEC-006, DEC-007, DEC-009, DEC-010, DEC-012.
Applicable draft proposals: DEC-A-001…DEC-A-004, but MH-18 does not promote any proposal to accepted status.

## 8. Architecture / boundary mapping
Canonical owner domains: data_core, media_core, surveillance_core, storage_core, personal_media_core.
Supporting domains: mobile_media, audio_core, gaming_core, network_core, cluster_core, assistant_core, recovery_core, migration_core, search_core, observability, privacy_security, export_core, integration_core and verification.

Critical boundaries:
- State Authority remains the sole canonical mutation authority.
- Storage is not authority.
- Index/search/cache/thumbnails/previews/transcodes are derived and rebuildable.
- AI output is candidate data until validation/policy/authorization.
- External media/providers/parsers/codecs/imported metadata are untrusted by default.
- Playback is authorized read-path activity; media-session state is distinct from global runtime state.
- Surveillance recording storage remains distinct from Personal Media Library storage.

## 9. Historical classification
RETAIN: core media architecture, ingestion, identity, lifecycle, metadata/provenance, personal library, playback, streaming, live media, transcoding, storage separation, derived indexing/search, AI/privacy/security boundaries, backup/recovery/migration, APIs/export/plugins, testing and technology neutrality.

REMAP: storage/persistence through canonical state/storage contracts; device/protocol interactions through MH-17; privacy through MH-13; observability through MH-11; mobile/device endpoint concerns through mobile/device contracts; AI mutation through candidate→validation→policy→authorization.

RECONCILE: exact codecs/containers, storage implementation, camera transport/timestamp semantics, streaming transports, DRM/provider integration, AI model/provider qualification, sandboxing technology, mobile transport/permissions, cluster workload placement.

REPLACE: any historical implication that a media file, indexer, transcoder, AI subsystem, plugin or storage backend can become canonical State Authority.

RETIRE: none evidenced.

UNKNOWN: complete historical MH-18 corpus outside the currently available chat context and exact production implementation evidence.

## 10. Contradictions / gaps
No direct accepted-architecture contradiction was identified. Remaining issues are evidence/technical closure gaps, not reasons to remove functionality.

Known evidence gaps: exact historical implementation corpus; exact media technology matrix; terminal media test evidence; production qualification evidence.

No dangling canonical registry references were introduced. Historical P0 references remain historical decomposition only.

## 11. Technical decisions requiring evidence
Keep OPEN / EVIDENCE-BLOCKED:
- codec/parser/container baseline;
- processing isolation/sandbox;
- storage/filesystem/pool semantics;
- search/index implementation;
- streaming/ABR transport;
- camera recording/discovery/timestamp/integrity semantics;
- DRM/provider integration;
- AI provider/model qualification;
- mobile transport and platform permission details;
- cluster scheduling and resource placement.

Required closure sequence: EVIDENCE → ALTERNATIVES → CONSTRAINTS → DECISION → CONTRACT UPDATE → INVARIANT IMPACT → VERIFICATION CRITERIA → ACCEPTANCE AUTHORITY.

## 12. Contract impacts
No immediate canonical registry changes proposed. Future evidence may refine CTR-011…CTR-015, CTR-025, CTR-026, CTR-028, CTR-032…CTR-036 and associated verification semantics.

## 13. Invariant impacts
No invariant change proposed. Any technical closure must explicitly re-check storage separation, function preservation, security, local/offline operation, direct surveillance recording and evidence preservation.

## 14. Dependency / authority impacts
MH-18 depends on and cross-references State Authority, security, privacy, storage, device, network, cluster, mobile, audio, gaming, assistant, recovery, migration, observability and verification boundaries. It does not claim their ownership.

## 15. Verification requirements
Contract tests, malformed-media/security corpus, ingestion idempotency/retry/cancel/timeout, metadata provenance/conflict, AI authorization-negative tests, storage isolation/recovery, index rebuild, playback authorization/session, streaming quotas/degraded network, transcoding resource isolation, subtitle/artwork trust boundary, export privacy/audit, backup/restore/migration, mobile/offline, compatibility, performance and terminal evidence are required before acceptance.

## 16. Acceptance evidence / authority
Acceptance evidence is not yet terminal. Overall control point records terminal capability verification VERIFIED=0 and ACCEPTED=0 with partial evidence. Acceptance authority is central governance plus explicit human acceptance. MH-18 has no acceptance authority.

## 17. OPEN items
All implementation-specific items above remain OPEN / EVIDENCE-BLOCKED. Production implementation remains BLOCKED.

## 18. Anti-loss confirmation
ANTI-LOSS: PASS at preservation/reconciliation level. No canonical capability is removed or retired by this MH-18 result. Missing historical evidence remains UNKNOWN/EVIDENCE_GAP. Cross-domain capabilities remain preserved through dependency mapping.

## 19. Suggested registry changes
None immediately. If central reconciliation later identifies a necessary registry refinement, proposal must include reason, evidence, affected CAP/CTR/INV/DEC, dependency impact, verification impact and acceptance authority.

## 20. Authority statement
This Reverse Master Prompt is an input to central reconciliation. MH-18 has no unilateral authority to modify canonical registries, accepted decisions, protected invariants or Master Architecture status.
