# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# MASTER HANDOFF PROMPT — MH-01…MH-23 ARCHITECTURE REDISTRIBUTION
# Date: 2026-09-05

## 0. PURPOSE

This prompt transfers the completed GitHub-side redistribution/reconciliation control point into the existing canonical MH-01…MH-23 architecture chats.

This is NOT a new MediaHub design and NOT a new forensic reconstruction. The purpose is to make each historical MH chat reconcile its historical architecture material against ONE canonical MediaHub Master Architecture while preserving provenance and preventing functional loss.

## 1. AUTHORITATIVE SOURCES

Repository: `VlDMlNSh/mediahub-os`
Branch: `recovery/full-functional-spec`

Mandatory sources:
- `recovery/forensic-control-point-2026-09-05.md`
- `recovery/MASTER-PROMPT-NEW-CHAT-MH01-23-REDISTRIBUTION-FINAL-2026-09-05.md`
- `recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml`
- `specification/capability-registry.yaml`
- `specification/contract-registry.yaml`
- `specification/invariant-registry.yaml`
- `specification/decision-registry.yaml`
- `specification/dependency-graph.yaml`
- `architecture/master-mediahub-architecture-reconstruction-2026-09-05.md`
- `development/implementation-map.yaml`
- this file

GitHub is the persistent source of truth. Chat history is evidence, not authority over canonical truth.

## 2. CONTROL POINT

Functional baseline: 58/58 capabilities preserved.
Canonical domains: 51.
Canonical ownership: 58/58.
Contract families: 36.
Protected invariants: 30.
Accepted decisions: DEC-001…DEC-012.
Architecture decisions DEC-A-001…DEC-A-004 remain DRAFT.
Master Architecture remains DRAFT / NOT ACCEPTED.
Production implementation remains BLOCKED.

The capability registry explicitly preserves CAP-001…CAP-058 and assigns each canonical capability an owner. fileciteturn18file0L2-L6

## 3. NON-NEGOTIABLE RULES

UNKNOWN ≠ LOST.
EVIDENCE_GAP ≠ LOST.
DEFERRED ≠ REJECTED.
NOT_IMPLEMENTED ≠ REMOVED.
NOT_FOUND ≠ NEVER_EXISTED.

No MH chat may delete, retire, replace or redefine a canonical capability without authoritative central reconciliation and evidence.

Canonical ownership is unique. Cross-domain references are allowed. Historical evidence must remain preserved.

Security semantics remain distinct:
Discovery ≠ Trust ≠ Authentication ≠ Authorization.
Presence, health, readiness and liveness never grant authorization.

Home Assistant is internal infrastructure; its UI is not the MediaHub user-facing model.

Local MediaHub is primary runtime. Cloud Development is privileged and separate.

System Storage, Surveillance Recording Storage and Personal Media Library Storage remain logically distinct.

Product variants preserve their explicit functional differences.

## 4. REQUIRED ACTION IN THE TARGET MH CHAT

The receiving MH chat MUST:

1. Read this prompt and the canonical sources above.
2. Preserve the current MH chat's historical context.
3. Determine its historical scope.
4. Extract every historical capability, requirement, contract, invariant, decision, dependency, architecture boundary, test and acceptance statement.
5. Map historical material to CAP/CTR/INV/DEC identifiers where evidence permits.
6. Classify each item:
   RETAIN / REMAP / RECONCILE / REPLACE / RETIRE / UNKNOWN.
7. Never infer RETIRE from absence.
8. Identify duplicates, ownership conflicts, contradictions, dangling references and stale references.
9. Identify technical decisions that remain OPEN / EVIDENCE-BLOCKED.
10. Perform an anti-loss audit against all 58 canonical capabilities.
11. Produce a Reverse Master Prompt for the MH contour.
12. Return proposed canonical registry changes only; do not apply them unilaterally.

## 5. REQUIRED REVERSE MASTER PROMPT FORMAT

The receiving MH chat must return:

- MH identifier
- historical scope
- source evidence and provenance
- CAP mapping
- requirement mapping
- contract mapping
- invariant mapping
- decision mapping
- architecture/boundary mapping
- classification of every historical item
- contradictions
- missing evidence
- dangling references
- stale references
- proposed technical decisions
- contract impacts
- invariant impacts
- dependency impacts
- verification requirements
- acceptance evidence
- acceptance authority
- OPEN items
- anti-loss confirmation
- proposed canonical registry changes
- explicit statement that the MH chat has no unilateral authority to apply those changes

## 6. CANONICAL PROJECTION OF ALL 23 MH CONTOURS

MH-01 — historical MH-01 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-02 — historical MH-02 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-03 — runtime/core lifecycle/startup/shutdown/commands/events/health/observability/recovery. Canonical domains: runtime_core, command_system, event_core, observability, recovery_core. STATUS: READY FOR RECONCILIATION.

MH-04 — historical MH-04 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-05 — historical MH-05 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-06 — core runtime/health/readiness/persistence/IPC/failure domains/recovery/resource governance/scheduling. Canonical domains: runtime_core, observability, recovery_core, resource_governance, scheduling_core. STATUS: READY FOR RECONCILIATION.

MH-07 — historical MH-07 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-08 — historical MH-08 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-09 — historical MH-09 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-10 — AI intelligence/AI authority. Canonical domains: assistant_core, knowledge_core, cloud_development, verification. STATUS: READY FOR RECONCILIATION.

MH-11 — historical MH-11 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-12 — identity/authentication/authorization/trust/PKI/crypto/secure remote/cloud security/incident response/supply chain. Canonical domains: security_core, privacy_security, network_core. STATUS: READY FOR RECONCILIATION.

MH-13 — privacy/data governance/provenance. Canonical domains: privacy_security, data_core, security_core. STATUS: READY FOR RECONCILIATION.

MH-14 — development interface/persistence. Canonical domains: cloud_development, data_core, ui_core. STATUS: READY FOR RECONCILIATION.

MH-15 — canonical OS appliance/product runtime. Canonical domains: product_core, runtime_core, installer_core, lifecycle_core. STATUS: READY FOR RECONCILIATION.

MH-16 — installer/recovery/update. Canonical domains: installer_core, recovery_core, lifecycle_core, migration_core. STATUS: READY FOR RECONCILIATION.

MH-17 — device/integration lifecycle/protocol selection/compatibility/firmware/offline/backpressure. Canonical domains: device_onboarding, device_management, integration_core, command_system. STATUS: READY FOR RECONCILIATION.

MH-18 — evidence provenance and historical media architecture. Canonical domains: data_core, media_core, surveillance_core, storage_core, personal_media_core. STATUS: READY FOR RECONCILIATION.

MH-19 — historical MH-19 contour; exact corpus to be recovered. STATUS: UNKNOWN / EVIDENCE_GAP.

MH-20 — automation governance. Canonical domains: automation_core, scheduling_core, command_system, event_core. STATUS: READY FOR RECONCILIATION.

MH-21 — distributed AI/security/cloud corpus. Canonical domains: cluster_core, cloud_development, assistant_core, security_core. STATUS: READY FOR RECONCILIATION.

MH-22 — production qualification/acceptance. Canonical domains: verification, lifecycle_core, recovery_core, security_core. STATUS: READY FOR RECONCILIATION.

MH-23 — historical migration contour; exact corpus to be recovered. Canonical domains: migration_core, recovery_core, data_core. STATUS: UNKNOWN / EVIDENCE_GAP.

The projection matrix defines these scopes and explicitly requires central-only final reconciliation. fileciteturn19file0L2-L6

## 7. CRITICAL FUNCTION PRESERVATION CHECK

During every MH reconciliation explicitly verify that no historical material causes loss of any of these canonical capability groups:

- direct surveillance recording and surveillance storage;
- Dahua, Hikvision, Ajax;
- KINCONY/KCS USB→firmware→network onboarding;
- KNX, DALI, RS-485, Centrsvet, Arlight, Maytoni;
- climate/ventilation/heating and energy infrastructure;
- UPS, solar, wind, generator, batteries;
- Ethernet/Wi-Fi/Keenetic/Ubiquiti;
- Local MediaHub Cluster/distributed compute;
- Cloud Development and Professional Engineering;
- Digital Twin and engineering/as-built documentation;
- Personal Media Library;
- iPhone/iPad/Android and phone camera/microphone/media endpoint;
- HDMI/4K, 3.5mm, Multiroom Audio and Hi-End audio concept;
- Xbox/PlayStation/gaming PC;
- HomeKit/Yandex Alice/Loxone and internal Loxone capability;
- Local Assistant and controlled AI/cloud escalation;
- content and website generation;
- contextual guidance;
- installer, self-recovery, update, backup, restore and migration;
- offline-first operation;
- Knowledge Graph, unified search, telemetry, health/readiness and diagnostics;
- cybersecurity, privacy, authorization and trust;
- automation, scheduling, events, notifications and history.

These are preservation checks, not permission to invent implementation details.

## 8. TRACEABILITY

Every material requirement should be traced:
FUNCTION → REQUIREMENT → CONTRACT → ARCHITECTURE → IMPLEMENTATION BOUNDARY → TEST → ACCEPTANCE.

Missing downstream artifacts are GAPs, never evidence of missing upstream capability.

## 9. TECHNICAL DECISIONS

No implementation technology may be declared canonical merely because it is conventional or popular.

Technical closure requires:
EVIDENCE → ALTERNATIVES → CONSTRAINTS → DECISION → CONTRACT UPDATE → INVARIANT IMPACT → VERIFICATION CRITERIA → ACCEPTANCE AUTHORITY.

Otherwise remain OPEN / EVIDENCE-BLOCKED.

## 10. CENTRAL RECONCILIATION GATE

The MH chat must not declare the Master Architecture accepted.

After all 23 Reverse Master Prompts are available, the central reconciliation must audit:
- duplicate ownership;
- ownership conflicts;
- contradictory requirements;
- contract conflicts;
- invariant conflicts;
- decision alternatives;
- dependency conflicts;
- security boundaries;
- product variants;
- verification gaps;
- acceptance gaps;
- historical evidence conflicts.

Only after this central audit may a Master Architecture Acceptance Request be prepared for explicit human acceptance.

## 11. PRODUCTION GATE

Until explicit human acceptance of the Master Architecture:

NO production implementation.
NO irreversible migrations.
NO implementation technology lock-in.
NO automatic conversion of MH projections into code.

The implementation map confirms that production implementation is not authorized until architecture acceptance and requires capability/requirement/contract/invariant/dependency/test/acceptance traceability. fileciteturn12file0L2-L6

## 12. REQUIRED OUTPUT FROM THIS CHAT

Return exactly two artifacts:

A. `MH-N REVERSE MASTER PROMPT`

B. `MH-N RECONCILIATION STATUS`

The status must state:
- historical evidence coverage;
- canonical mapping coverage;
- unresolved evidence gaps;
- contradictions;
- proposed changes;
- anti-loss result;
- verification state;
- acceptance state;
- whether anything remains OPEN.

Then wait for central reconciliation. Do not independently alter canonical truth.

## 13. FINAL PRINCIPLE

ONE MEDIAHUB.
ONE CANONICAL ARCHITECTURE.
23 HISTORICAL ARCHITECTURE PROJECTIONS.
ZERO FUNCTION LOSS.

Historical evidence is preserved.
Canonical truth is centrally governed.
Unknown remains unknown until evidence resolves it.
