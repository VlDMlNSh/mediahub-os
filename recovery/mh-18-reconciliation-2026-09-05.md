# MH-18 RECONCILIATION — 2026-09-05

Status: RECONCILED WITH AVAILABLE EVIDENCE / NOT ACCEPTED / NOT FROZEN
Repository: VlDMlNSh/mediahub-os
Branch: recovery/full-functional-spec

## 1. Historical scope
MH-18 historical contour is Media / Content Architecture. The available current architecture-chat evidence covered media/content ingestion, content identity, lifecycle, validation, metadata/provenance, AI analysis, privacy, cloud media, storage, indexing/search, transcoding, thumbnails/previews, playback/media sessions, streaming, playlists, subtitles, rights/DRM, device interaction/live media, security/sandboxing, cache, offline-first, backup/recovery, migration, observability/resource governance, plugins, APIs/export, supply chain and testing/technology evaluation.

## 2. Source evidence and provenance
Primary canonical sources read from recovery/full-functional-spec:
- recovery/forensic-control-point-2026-09-05.md
- recovery/MASTER-PROMPT-NEW-CHAT-MH01-23-REDISTRIBUTION-FINAL-2026-09-05.md
- recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml
- specification/capability-registry.yaml
- specification/contract-registry.yaml
- specification/invariant-registry.yaml
- specification/decision-registry.yaml
- specification/dependency-graph.yaml
- architecture/master-mediahub-architecture-reconstruction-2026-09-05.md
- development/implementation-map.yaml
- development/baseline.yaml

Historical MH-18 architecture artifact inspected from branch mh-18-media-content-architecture:
- docs/architecture/MH-18-media-content-architecture.md
- blob SHA: 6fd226c08c9d915f73c3adf160858cf1137d8c05

Repository-side targeted search on the default GitHub search surface did not expose additional MH-18 implementation files. This is a search-surface limitation, not evidence of historical absence or capability loss.

## 3. CAP mapping
Directly mapped/protected:
- CAP-008 direct surveillance recording/live/archive/playback/export — MH-18 references surveillance integration and explicitly preserves recording boundary.
- CAP-009 dedicated logical surveillance storage — preserved as separate logical storage.
- CAP-010 multi-source media ingestion — direct match.
- CAP-011 Personal Media Library — direct match.
- CAP-012 iPhone/Android bidirectional media sync — direct architectural match through mobile media/sync.
- CAP-013 unified photo/video/audio playback — direct match.
- CAP-014 live media streaming/routing/transcoding — direct match.
- CAP-015 multiroom audio/3.5mm — direct match.
- CAP-016 phone camera/microphone/media endpoint — direct match.
- CAP-017 HDMI/4K — direct match.
- CAP-018 gaming integration — direct architectural boundary.
- CAP-023 network integration — dependency for streaming/media routing.
- CAP-024 local cluster/media storage/failover — dependency.
- CAP-025 distributed compute/AI processing — dependency.
- CAP-026/027 cloud development and content generation — controlled boundary.
- CAP-031/032 telemetry and health/readiness — observability dependency.
- CAP-035 offline-first — direct architectural requirement.
- CAP-036 metadata/provenance — direct match.
- CAP-037 unified search/indexing — direct match.
- CAP-039 privacy — direct match.
- CAP-040 security/trust/authentication/authorization — direct boundary.
- CAP-041 logical system/surveillance/personal media storage — direct match.
- CAP-042 backup/restore — direct match.
- CAP-043 migration — direct match.
- CAP-048 resource governance — direct match.
- CAP-049 extensibility/plugins/providers — direct match.
- CAP-050 simulation/verification/acceptance — direct testing requirement.
- CAP-051 media lifecycle — direct match.
- CAP-056 authorized export — direct match.
- CAP-058 security/safety system invariant — cross-cutting dependency.

CAP-001…CAP-058 remain canonical baseline; MH-18 does not request deletion or retirement of any capability. Cross-domain capabilities are references/dependencies, not duplicate ownership.

## 4. Contract mapping
Primary:
- CTR-001 State Authority: media never becomes canonical mutation authority.
- CTR-011 Media: identity, ingestion, processing, playback/routing, lifecycle, authorization and recovery.
- CTR-012 Surveillance: camera/live/direct recording/archive/playback/search/export.
- CTR-013 Surveillance Storage: logical isolation, retention, capacity, integrity, recovery.
- CTR-014 Personal Media Storage: library storage/lifecycle/privacy/backup/migration.
- CTR-015 Storage Management: logical storage domains, quotas, capacity, repair/rebalance/failure.
- CTR-019 Assistant Escalation: AI/media analysis and cloud boundary.
- CTR-025 Migration: media/storage/config migration.
- CTR-026 Privacy: minimization, processing, disclosure/egress.
- CTR-028 Mobile Endpoint: phone/tablet identity, permissions, media/IO routing.
- CTR-032 Export: authorization, classification, provenance, integrity and audit.
- CTR-033 Telemetry: media observability without payload logging by default.
- CTR-034 Search-Knowledge: indexing/search authorization and rebuildability.
- CTR-035 Resource Governance: media processing/streaming quotas and priority.
- CTR-036 Verification-Acceptance: evidence and acceptance traceability.

## 5. Invariant mapping
Relevant protected invariants include INV-001, INV-002, INV-008, INV-009, INV-010, INV-011, INV-013, INV-017, INV-021, INV-022, INV-023, INV-024, INV-025, INV-026, INV-027, INV-029 and INV-030. The decisive MH-18 semantics are unified media identity, direct surveillance recording preservation, logical storage separation, local/offline operation, security as cross-cutting and preservation of historical evidence.

## 6. Decision mapping
Accepted decisions materially applicable:
- DEC-001 functional baseline is primary truth.
- DEC-003 MediaHub can directly record supported cameras.
- DEC-004 surveillance and personal media library are separate logical storage domains.
- DEC-005 local/offline-first direction.
- DEC-006 privileged cloud-development boundary.
- DEC-007 local cluster as one coordinated system.
- DEC-009 security as system invariant.
- DEC-010 product variants preserve functional differences.
- DEC-012 deferred technical detail is preserved, not rejected.

No DEC-A-001…DEC-A-004 proposal is promoted by MH-18.

## 7. Architecture and boundary mapping
Canonical projection: data_core, media_core, surveillance_core, storage_core, personal_media_core.

Boundary rules:
- State Authority remains sole canonical mutation authority.
- Content, Asset, Object/File, Storage Locator, External ID, Digest/Fingerprint and Version remain distinct.
- Index/search/thumbnails/previews/waveforms/transcodes are derived and rebuildable.
- AI output is candidate metadata until validation/policy/authorization.
- External providers/media/codecs/parsers/imported metadata are untrusted by default.
- Playback reads through authorized read model/media session/resolver; session state is not global canonical state.
- Surveillance Recording Storage and Personal Media Library Storage remain logically separate.
- Device/protocol authority belongs to MH-17 boundary; media does not become device authority.

## 8. Classification
RETAIN:
- media/content domain and unified media model;
- multi-source ingestion;
- content identity separation;
- media lifecycle;
- metadata/provenance;
- Personal Media Library;
- surveillance recording boundary;
- playback/streaming/live media/transcoding;
- audio/display/mobile/gaming relationships;
- search/index/derived artifacts;
- privacy/security/AI boundaries;
- storage separation;
- backup/recovery/migration;
- export/plugin/API boundaries;
- testing and technology-neutral evaluation.

REMAP:
- direct media/device interactions are remapped through MH-17 device/integration boundary and canonical authorization contracts;
- persistence/storage mutation is remapped through State Authority and storage contracts;
- AI/media enrichment is remapped through candidate metadata → validation → policy → authorization;
- observability is remapped through MH-11/observability contracts;
- privacy is remapped through MH-13;
- mobile/device endpoint concerns cross-reference MH-17 and mobile contracts.

RECONCILE:
- exact technical media stack and codec/container support;
- exact storage substrate and filesystem/pool semantics;
- exact streaming transports and remote exposure;
- exact camera transport/discovery/recording semantics;
- exact DRM/provider integration;
- exact AI provider/model qualification;
- exact sandbox/process isolation technology;
- exact mobile transport/permission implementation;
- exact cluster workload placement for media processing.

REPLACE:
- any historical implication that a media subsystem, indexer, transcoder, AI processor, plugin or storage backend can become canonical authority is replaced by the canonical State Authority boundary.

RETIRE:
- none evidenced.

UNKNOWN:
- full historical MH-18 corpus beyond material available in the current architecture-chat context;
- exact historical implementation evidence, because repository audit did not establish production media implementation.

## 9. Contradictions
No direct contradiction was found between the available MH-18 architecture baseline and the canonical registries.
Potential reconciliation surfaces are technical-detail gaps rather than accepted architectural conflicts: codec support, transports, storage implementation, DRM, AI qualification, sandbox technology and exact device/media protocol behavior.

## 10. Missing evidence / search scope
Search included repository architecture/specification/development surfaces and targeted media terms. GitHub search is documented by the connector as operating on the default branch, so failure to surface ref-specific historical MH-18 files is not treated as absence. The known MH-18 branch artifact was directly fetched by its exact path/ref.

Missing evidence remains required for implementation closure, compatibility qualification, security qualification and terminal verification.

## 11. Dangling/stale references
No canonical registry endpoint was changed. No material dangling reference was introduced by this reconciliation.
Historical references to P0-03…P0-07 are retained as historical decomposition; they do not override the current canonical State Authority boundary.

## 12. Proposed technical decisions
No technical decision is closed.

Open/evidence-blocked decisions:
- codec/container/parser baseline;
- media processing sandbox/isolation mechanism;
- storage backend/filesystem/pool design;
- indexing/search implementation;
- streaming transport/ABR mechanism;
- camera recording transport/timestamp/integrity model;
- DRM/provider integration model;
- AI model/provider qualification and quarantine;
- mobile media transport and platform permission details;
- cluster scheduling/resource placement for media workloads.

Closure requires evidence → alternatives → constraints → decision → contract update → invariant impact → verification criteria → acceptance authority.

## 13. Contract/invariant/dependency impacts
No canonical registry mutation proposed as an immediate action. If later evidence changes a contract, the likely affected families are CTR-011…CTR-015, CTR-025, CTR-026, CTR-028, CTR-032…CTR-036, with invariant review at minimum against INV-001/002/008/009/010/011/013/021/024/026/027/029/030.

Dependency relationships remain compatible with dependency-graph entries media_core→storage_core/personal_media_core/mobile_media/audio_core/gaming_core/network_core/cluster_core, surveillance_core→storage_core, export_core→media_core, assistant_core→media_core, recovery_core→storage_core and privacy_security→security_core.

## 14. Verification requirements
Required before acceptance:
- content identity and lifecycle contract tests;
- ingestion idempotency, cancellation, timeout and retry tests;
- malformed/untrusted media corpus and parser/security tests;
- metadata provenance/conflict tests;
- AI candidate metadata authorization-negative tests;
- storage isolation and failure/recovery tests;
- index rebuild correctness tests;
- playback/session authorization tests;
- streaming quota/authentication/degraded-network tests;
- transcoding resource/sandbox/cancellation tests;
- subtitle/artwork trust-boundary tests;
- export authorization/privacy/audit tests;
- backup/restore/migration tests;
- mobile/offline tests;
- compatibility matrix tests for supported media/device variants;
- performance/resource-pressure tests;
- terminal evidence with exact versions/platform/configuration/timestamps.

## 15. Acceptance evidence and authority
Acceptance authority is central governance / explicit human acceptance, not MH-18.
Current terminal verification for the overall reconstructed baseline is partial; the control point records VERIFIED=0 and ACCEPTED=0. MH-18 itself therefore remains NOT ACCEPTED / NOT FROZEN.

## 16. OPEN items
All exact implementation-specific decisions listed above remain OPEN / EVIDENCE-BLOCKED. No production implementation authorization is implied.

## 17. Anti-loss confirmation
PASS at architectural preservation level: no canonical capability is proposed for removal, retirement or replacement as a function. Where MH-18 touches capabilities owned by other domains, those are preserved as cross-domain dependencies. UNKNOWN/EVIDENCE_GAP is retained where historical corpus is incomplete.

This is preservation/reconciliation, not proof of implementation.

## 18. Suggested canonical registry changes
None required immediately.

Potential future registry clarifications may be proposed after central reconciliation for media-specific subcontracts and verification criteria, but MH-18 has no unilateral authority to apply them.

## 19. Final authority statement
MH-18 has NO unilateral authority to modify capability, contract, invariant or decision registries. This document records a scoped reconciliation result for central reconciliation only.
