# MH-13 — Privacy / Data Governance

**Status:** RECONSTRUCTED / PROPOSED  
**Acceptance:** NOT YET VERIFIED  
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

**Current state:** RECONSTRUCTED / PROPOSED  
**Historical original:** NOT RECOVERED  
**Acceptance:** NOT YET VERIFIED  
**Frozen:** NO  
**Production implementation:** NOT AUTHORIZED

## 12. Governance handoff

This artifact is a reconstruction candidate for independent verification and governance acceptance. It MUST NOT be marked ACCEPTED or FROZEN automatically.
