# MH-13 — Privacy / Data Governance

**Status:** ACCEPTED RECONSTRUCTION / ETALON BASELINE / RECONCILED  
**Acceptance:** ACCEPTED RECONSTRUCTION; QUALIFICATION QUEUED  
**Frozen:** NO  
**Production implementation:** NOT AUTHORIZED

## Provenance

**Original historical MH-13 artifact:** NOT RECOVERED.

This document is a governance-authorized reconstruction derived from:
- Git-backed downstream evidence;
- MH architecture chat history;
- the master architecture index;
- forensic reconciliation findings.

It MUST NOT be interpreted as the recovered historical original.

**Reconstruction:** AUTHORIZED  
**Reconstruction basis:** DOWNSTREAM GIT-BACKED EVIDENCE + MH ARCHITECTURE CHAT HISTORY + MASTER ARCHITECTURE INDEX + FORENSIC RECONCILIATION  
**Historical fidelity:** PARTIAL / REQUIRES VERIFICATION

The reconstruction does not rewrite or imply recovery of the historical Git lineage.

## 1. Domain and authority boundary

MH-13 is the Privacy / Data Governance architectural domain.

MH-13 is not State Authority, canonical mutation authority, Persistence authority, Media authority, AI authority, or Cloud authority. P0 State Authority remains the sole canonical mutation authority. Privacy governance is enforced through the existing Boundary → Authorization → State Authority path and MUST NOT introduce a shadow mutation path.

MH-13 does not replace MH-12 Security, P0-03/P0-04/P0-05/P0-06, or downstream domain ownership.

## 2. Reconstructed minimum architecture

The following directions are supported by recovered evidence. Where exact historical semantics are unavailable, this document intentionally avoids inventing them.

### 2.1 Data classification

Privacy-aware classification is required before applicable downstream operations, especially external egress. Exact historical classification levels are UNKNOWN / REQUIRES VERIFICATION.

### 2.2 Purpose limitation

Data use is purpose-bound to an authorized purpose. Exact historical purpose vocabulary and policy representation are UNKNOWN / REQUIRES VERIFICATION.

### 2.3 Data minimization

Collection, processing, retention and transfer are minimized relative to the authorized purpose. Minimization and redaction are required controls for sensitive/private data.

### 2.4 Access and privacy constraints

Privacy restrictions interact with authentication, authorization, capability and trust controls. Privacy does not weaken Security; MH-12 remains responsible for security/trust/authentication/authorization concerns.

### 2.5 Retention

Retention is part of the data lifecycle and must be explicitly defined where applicable. Exact historical retention periods are UNKNOWN / REQUIRES VERIFICATION.

### 2.6 Deletion / erasure

Deletion/erasure requires defined semantics and coordination with Persistence governance. Exact historical deletion guarantees, backup deletion semantics and implementation mechanisms are UNKNOWN / REQUIRES VERIFICATION.

### 2.7 Redaction and protected channels

Protected/private data must not enter unauthorized telemetry, diagnostics, audit or external-transfer channels. Audit evidence must not expose protected payload unnecessarily.

### 2.8 External transfer

External AI/cloud/provider processing follows the reconstructed control sequence:

**classified → purpose-bound → minimized → authorized → bounded → observable**

No provider is implicitly trusted by this reconstruction. Exact provider contracts, regions, deletion guarantees, training-use terms and residency rules remain UNKNOWN / REQUIRES VERIFICATION.

### 2.9 Auditability

Privacy-relevant operations require verifiable/auditable evidence, while audit metadata must avoid unnecessary disclosure of protected payload.

### 2.10 AI boundary

AI has no privacy authority. AI routing MUST NOT weaken MH-13 restrictions. AI processing is subject to classification, purpose, minimization, authorization and external-transfer controls.

### 2.11 Media privacy

Media may contain faces, voices, locations, conversations, documents, behavioral information and personal information. MH-18 applies MH-13 privacy principles to media/content-specific behavior and verification.

### 2.12 Device privacy

Device telemetry, identifiers, topology, occupancy-like signals, logs and command history may be privacy-relevant. MH-17 applies the privacy boundary to device-specific behavior and delegates retention/deletion governance to MH-13 plus Persistence.

## 3. Responsibility reconciliation

| Domain | Responsibility boundary |
|---|---|
| MH-12 | Security, trust, authentication, authorization |
| MH-13 | Privacy and data governance |
| MH-14 | Persistence implementation and durable lifecycle |
| MH-17 | Device/protocol behavior and device-specific privacy application |
| MH-18 | Media/content-specific privacy application |
| MH-21 | Hybrid-cloud/distributed-AI-specific privacy application |
| MH-23 | Long-term compatibility, migration and evolution |

Domain-specific ownership is not transferred into MH-13.

## 4. Downstream governance relationships

MH-17, MH-18 and MH-21 contain privacy requirements that apply MH-13 principles within their domains. Their presence does not create a competing privacy authority.

MH-21 explicitly identifies its privacy material as governed by MH-13. MH-18 applies privacy controls to media/content. MH-17 applies privacy controls to device telemetry and related data. These are downstream applications of the reconstructed MH-13 domain.

## 5. Core invariants

1. Privacy governance does not become State Authority.
2. Data presence does not imply mutation authority.
3. Ownership does not imply unrestricted access.
4. Privacy does not weaken Security.
5. Purpose is required for governed data use.
6. Minimization applies to collection, processing and transfer.
7. Sensitive/private data requires applicable classification before external egress.
8. Retention and deletion are lifecycle concerns and must coordinate with Persistence.
9. Derived data is not automatically less sensitive.
10. Metadata may itself be sensitive.
11. Audit is distinct from ordinary logs/telemetry.
12. Observability does not authorize collection.
13. AI does not receive implicit all-data access or privacy authority.
14. RAG/knowledge systems do not become privacy authority.
15. Plugin integration is bounded and does not create privacy authority.
16. Cloud/external processing is not the default trusted path.
17. External transfer must be explicit and governed.
18. Secrets/credentials are not ordinary data.
19. Unknown classification must not authorize external transfer.
20. Backup/restore remains part of the lifecycle and does not erase privacy obligations.
21. Temporary data must not silently become permanent retention.
22. Privacy governance does not replace the State Authority.
23. Privacy controls must remain compatible with offline-first/local-first operation where applicable.

## 6. Unknown register

The following remain UNKNOWN / REQUIRES VERIFICATION and are intentionally not invented here:

- original MH-13 branch;
- original MH-13 commit;
- original canonical historical path;
- exact historical taxonomy;
- exact classification levels;
- exact ownership/stewardship model;
- exact consent model;
- exact data-subject model;
- exact residency model;
- exact retention periods/semantics;
- exact deletion and backup-deletion semantics;
- exact provider contracts and guarantees;
- exact AI-provider rules;
- exact plugin privacy contract;
- exact telemetry privacy contract;
- exact provenance/lineage model;
- exact forensic privacy model;
- jurisdiction-specific legal/compliance mappings.

Future proposals must be marked PROPOSED / DERIVED until independently verified and accepted.

## 7. Contradiction / reconciliation register

### C-13-01 — Repository lineage
The architecture dependency graph confirms MH-13, while the original canonical historical artifact was not recovered.

**Classification:** REPOSITORY LINEAGE CONTRADICTION / REQUIRES VERIFICATION.  
This is not treated as a contradiction in the reconstructed architecture itself.

### C-13-02 — MH-21 privacy material
MH-21 contains privacy requirements and explicitly identifies them as governed by MH-13.

**Classification:** DOWNSTREAM INHERITED + DOMAIN-SPECIFIC APPLICATION.

### C-13-03 — MH-18 privacy material
MH-18 contains media-specific privacy architecture and applies MH-13 principles.

**Classification:** CROSS-DOMAIN GOVERNANCE + DOMAIN-SPECIFIC IMPLEMENTATION.

## 8. Evidence register

| ID | Evidence | Classification |
|---|---|---|
| E-13-01 | `docs/architecture/MEDIAHUB-MASTER-ARCHITECTURE-INDEX.md` on `architecture/mh-23-long-term-evolution`; confirms MH-12 → MH-13 → MH-14 and notes historical linkage may require verification | GIT-BACKED |
| E-13-02 | Commit `8c37efd5305bc2e5b954fb3c17c60ffef5fdbb12`, `docs/architecture/MH-21-privacy.md`; states governed by MH-13 | GIT-BACKED |
| E-13-03 | Commit `f470b1fe957a3eb68ce84f7251c53ef69f377297`, `docs/architecture/MH-21-privacy-invariants.md` | GIT-BACKED |
| E-13-04 | Commit `ec6fb020953b00497eb55bd0cf397ecbb7761995`, `docs/architecture/MH-21-data-retention.md` | GIT-BACKED |
| E-13-05 | Commit `5450b5c1bf2b374e4d657ec3bc6f2b7245cb3885`, `docs/architecture/MH-17-privacy.md` | GIT-BACKED |
| E-13-06 | `docs/architecture/MH-18-privacy.md`; media privacy application | GIT-BACKED |
| E-13-07 | `docs/architecture/MH-18-privacy-testing.md`; privacy verification/testing requirements | GIT-BACKED |
| E-13-08 | `docs/architecture/MH-18-chat-sync.md`; separate development/architecture synchronization discipline | GIT-BACKED |
| E-13-09 | MH-23 master index warning on historical repository linkage | GIT-BACKED |
| E-13-10 | Direct MH-13 artifact search did not recover canonical artifact | OBSERVED |
| E-13-11 | MH-13 commit search did not recover historical canonical commit | OBSERVED |

## 9. Dependency map

**Upstream / interacting:** MH-04…MH-12 as applicable, with MH-12 Security providing security/trust/authentication/authorization controls.

**Core boundary:** P0-03 State Authority, P0-04 in-memory State Authority, P0-05 Consumer/Integration Boundary, P0-06 Core Runtime Services.

**Downstream:** MH-14 Persistence, MH-17 Devices/Protocols, MH-18 Media, MH-21 Hybrid Cloud/Distributed AI, MH-23 Long-Term Evolution/Compatibility/Migration.

The dependency relation does not grant MH-13 mutation or persistence authority.

## 10. Acceptance criteria

Acceptance MUST NOT be inferred from creation of this file. Before governance acceptance, verify:

- provenance remains explicit and historical original remains NOT RECOVERED;
- all evidence references resolve to the cited Git artifacts;
- responsibility boundaries do not duplicate MH-12/MH-14/MH-17/MH-18/MH-21/MH-23 authority;
- no State Authority duplication exists;
- no hidden mutation path exists;
- no undocumented provider trust is asserted;
- no AI authority is introduced;
- no unauthorized external-transfer path is introduced;
- unknowns and contradictions remain visible;
- no frozen P0 contract is modified by this artifact;
- downstream privacy requirements remain compatible;
- verification evidence is recorded before acceptance.

## 11. Git / governance state

This document is intended for a dedicated reconstruction branch and subsequent normal Git review. It does not authorize production implementation, deployment, provider integration, deletion-engine implementation, consent-engine implementation, media capture implementation, telemetry implementation, or AI/cloud routing implementation.

**Current state:** ACCEPTED RECONSTRUCTION / ETALON BASELINE / RECONCILED  
**Historical original:** NOT RECOVERED  
**Acceptance:** NOT YET VERIFIED  
**Frozen:** NO  
**Production implementation:** NOT AUTHORIZED

## 12. Governance handoff

This artifact is the accepted reconstruction and etalon privacy baseline for autonomous qualification. Historical original remains NOT RECOVERED. Qualification is independently queued in GitHub Issue #128 and must not be inferred from architecture text. Frozen and production authorization remain separate states.


## 13. Etalon privacy baseline

The following policy surface is the canonical MH-13 qualification target. It extends the reconstructed minimum architecture without creating a new authority.

### 13.1 Data domains and ownership
Privacy governance covers User, System, Security, Smart Home, Media, Documents, Engineering, Digital Twin, Network, Identity, Credential/Secret, AI Context, AI Memory, AI Output, Telemetry, Audit, Recovery, Backup, Integration, Plugin, Developer, Corporate, Model and Qualification data.

For each class, qualification must identify authoritative owner, operational owner, processor, readers, writers, retention authority, deletion authority, export authority, backup and recovery policy. Ownership never implies authorization.

### 13.2 Classification, purpose and minimization
Supported policy classes are Public, Internal, User, Sensitive, Highly Sensitive, Security, Secret, Restricted Developer and Corporate. Classification may be deterministic, automatic, AI-assisted or user-confirmed; AI classification is not authoritative by itself.

Sensitive operations require an explicit purpose. Purpose is bounded and cannot become an indefinite permission. Every consumer request is reduced to Minimum Necessary Data.

### 13.3 Context, RAG and Knowledge Graph
AI Context Assembly must evaluate identity, authorization, policy, purpose, sensitivity, residency and retention. AI must not receive full user context by default.

Retrieval follows Identity -> Authorization -> Classification -> Purpose -> Retrieval Scope -> Provenance. Embeddings, vector indexes, OCR/index copies and Knowledge Graph projections inherit source-data authorization. Graph controls apply to entity, relation, property and collection/domain; traversal cannot use one permitted entity to disclose unrelated protected entities.

### 13.4 Data-flow and residency
Governed data flow is Source -> Classification -> Purpose -> Destination -> Authorization -> Policy -> Transport -> Processing -> Storage -> Retention -> Deletion. External transfer additionally requires Egress Decision -> Destination Verification -> Audit.

Local node and local cluster are the default residency boundary. Mobile, integrations, cloud and backup are separate residency decisions. Developer Domain is not a User Data residency destination.

### 13.5 Local First and cloud
Without Internet, local AI/search/Documents/Media/Smart Home/diagnostics remain available where locally implemented; cloud-dependent functions degrade without weakening privacy.

Cloud processing requires classification, purpose, authorization, policy, egress decision, provider/destination verification and audit. Implicit upload, bulk synchronization, hidden telemetry and silent training transfer are prohibited.

### 13.6 Developer, support and telemetry boundaries
Developer Domain may use source code, corporate data, synthetic data, approved test data, OSS research and qualification artifacts, but not User Documents, Media, Smart Home state, Digital Twin, Identity data, private telemetry, backups or AI Memory.

Support follows Issue -> Local Diagnosis -> Sanitized Evidence -> User/Policy Authorization -> Controlled Export. Export is scoped, time-limited where appropriate, classified and auditable.

Telemetry and logs require classification, redaction, secret filtering, PII minimization and configurable retention. Credentials, private keys, passwords and private content must not enter ordinary telemetry or diagnostic paths.

### 13.7 AI Memory and outputs
AI Memory is separated into session, user preference, task, domain, engineering and system categories. Each category requires explicit persistence, visibility, retention, deletion, export and model-access semantics.

AI outputs receive classification and policy treatment. An output does not automatically cross a trust-domain boundary or become authoritative.

### 13.8 Domain applications
Documents, Media, Smart Home/camera, Digital Twin, Engineering and Network data remain under their existing domain authorities while inheriting MH-13 privacy constraints. Media AI organization does not imply cloud upload. Camera processing is local-first by default. Digital Twin export is scoped; full Twin export is not implicit. Network metadata is not presumed non-sensitive.

### 13.9 Identity, credentials and secrets
Identity, authentication/session state, device identity and authorization state have dedicated protection policies. Credentials, keys and secrets are not ordinary User Data and are not automatically included in exports or ordinary backups/telemetry.

### 13.10 Backup, recovery, deletion and retention
Backup inherits source privacy properties and does not create a new permission model. Restore preserves data, permissions, classification, provenance and applicable retention metadata. Recovery requires purpose, scope, authorization, audit and controlled credentials.

Deletion evaluates primary data, replicas, indexes, embeddings, caches, derived artifacts and backups. Logical deletion, inaccessible state, scheduled physical deletion and retained security/audit evidence are distinct outcomes. Unlimited retention is not the default.

### 13.11 Export, portability, sharing and consent
Export is explicit, scoped, authenticated, policy-checked and auditable. Portability preserves schema/version/provenance/relationships/permissions where applicable but does not require export of secrets or internal security mechanisms.

Sharing is identity-aware, scope-limited, purpose-limited and time-limited where appropriate. Consent, authentication, authorization and policy remain distinct controls. Family/child restrictions are inherited from existing identity/policy architecture and do not create a second identity authority.

### 13.12 Integrations, plugins and mobile
Third-party integrations receive only declared data, approved scope, required purpose and permitted duration. Plugin manifests must declare data classes, purpose, network, storage, retention, external destinations, AI access and secrets; undeclared access is denied.

Mobile applications use local minimization, secure storage, session controls, remote revoke, notification privacy, API scoping and bounded offline cache. Wall Panel receives minimum necessary context and does not expose secrets, full network topology or sensitive content without need.

### 13.13 Privacy UI, observability and audit
Material privacy behavior should expose source, sensitivity where useful, local/cloud processing state and sharing/AI status without unnecessary technical overload.

Privacy observability covers data access, export, sharing, cloud transfer, AI context access, policy decisions, retention, deletion, plugin access and support export. Audit records who, what, when, purpose, policy, destination, scope and result while minimizing protected payload.

### 13.14 Threat model and incident response
Qualification covers unauthorized access, overcollection, hidden collection, secondary use, cross-domain leakage, cloud/developer/plugin/AI leakage, inference, backup, telemetry, retention, deletion, export and correlation risks.

Incident response is Detect -> Contain -> Scope -> Classify -> Revoke -> Investigate -> Recover -> Verify -> Audit. Controls may include egress block, integration/plugin quarantine, credential revocation, cache invalidation, node isolation and cloud/AI processing disablement.

### 13.15 Availability, observability, migration
Privacy controls preserve Local First availability where safe. Critical security controls remain enforced; cloud functions may become unavailable while safe local functions continue.

Observability never justifies unrestricted collection. Migration preserves ownership, permissions, classification, provenance, retention and deletion semantics and does not silently move sensitive data into a new trust domain.

## 14. Etalon closure invariant

**Local First + Data Minimization + Purpose Limitation + Explicit Trust Boundaries + Identity-Aware + Policy-Driven + Classification-Aware + Egress-Controlled + Residency-Aware + AI-Context-Minimized + Developer-Isolated + Cloud-Controlled + Observable + Auditable + Deletable Where Permitted + Recoverable + Portable Where Permitted.**

No subsystem, integration, plugin, AI component, cloud service, telemetry path or developer workflow receives User Data merely because it is technically capable of reading it.

## 15. Qualification control

GitHub Issue #128 is the autonomous qualification queue entry. Qualification must use fresh exact-revision evidence and independently test the 23 waves recorded there. Architecture acceptance does not equal implementation qualification, release authorization or production authorization.
