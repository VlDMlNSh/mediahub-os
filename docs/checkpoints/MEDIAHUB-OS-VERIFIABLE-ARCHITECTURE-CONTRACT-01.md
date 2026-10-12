# MediaHub OS — verifiable integrated architecture contract 01

- **Date:** 2026-10-12
- **Ref:** docs/mediahub-chat-tree-map-20261012
- **Status:** WORKING INTEGRATION CONTRACT / DRAFT — NOT A NEW CANONICAL BASELINE
- **Use:** operative review/checklist for documentation and architecture work on this branch, subject to the source precedence and gates below.
- **Not a grant of authority:** does not replace Baseline 2.0, alter Baseline 1.0, approve pending domain contracts, authorize implementation/deployment, or imply qualification/production acceptance.
- **Companion passport:** docs/checkpoints/MEDIAHUB-OS-SYSTEM-PASSPORT-V3.md.
- **Rule of evidence:** claim → source path → ref → blob SHA → exact scope/status → acceptance/evidence required → independent read-back.

## 1. Contract precedence and applicability

### 1.1 Source precedence

1. Product semantics: docs/checkpoints/mediahub-functional-baseline-2.0.md on main is the accepted current functional reference, blob SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f.
2. specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md on main, SHA 9df4892ed0734050ac79732603d15bb414717310, is the immutable literal/historical source for B1. B1 atoms require individually evidenced mapping; no implicit equivalence to B2.
3. Accepted/frozen domain contracts apply only inside their stated scope and dependency boundaries. A PROPOSED, FUTURE-GATED, CANDIDATE, branch-only or implementation-preparatory file does not override B2 merely by existing or being newer.
4. Explicit product-owner/governance decision records may resolve a decision only within their stated scope. Timestamp recency alone is not approval.
5. Matrices/checkpoints record traceability and state at the time of inspection; generated truth plus fresh exact-SHA evidence control current qualification claims.
6. This integrated contract is a synthesis and branch-level control artifact. It has no authority to silently amend or supersede sources above it.

### 1.2 Change rule

When two sources appear contradictory:
1. identify whether they discuss the same domain, lifecycle stage, deployment profile, version and normative force;
2. compare source refs/SHAs and decision provenance;
3. prefer the latest explicitly accepted decision only within its recorded authority, date, domain, dependency and rollout scope; newer unaccepted drafts never outrank an older accepted contract;
4. if the conflict cannot be resolved from accepted sources, record OPEN_CONFLICT, block the dependent claim/action and seek an owner/governance decision;
5. preserve historical source text and add a supersession/linkage note rather than rewriting history.

## 2. Normative architecture requirements

In this document, MUST means a condition for conformance to this working contract. It does not by itself authorize implementation or production.

### ARC-001 — one canonical product-state authority
**Rule:** MediaHub Product State Authority is the sole authority for canonical platform state. There must be no shadow canonical store or independent fallback authority.

**Acceptance:** Every canonical state mutation has one identified authority owner and a traceable command path. Failure of that authority does not transfer authority to an adapter, cloud, database leader, workflow engine, AI or queue coordinator. Critical state has explicit revision/generation semantics; unconditional critical-state LWW is not admitted.

**Evidence:** contract/source review; mutation-path and authority-boundary negative tests at implementation qualification stage.
**Primary source:** B2 §§3–4, 10, 13, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; B1 §3, SHA 9df4892ed0734050ac79732603d15bb414717310.
**Status:** architectural rule accepted; implementation/qualification status remains separately evidenced.

### ARC-002 — Smart Home authority is scoped to its domain
**Rule:** Home Assistant Core is the operational authority for Smart Home device/domain state. Product State Authority owns platform state, cross-domain policy/identity/lifecycle references. One authority does not silently subsume the other.

**Acceptance:** Every Smart Home integration documents the HA-owned state, MediaHub-owned platform metadata, command/event mapping, identity, and failure boundary; no UI/AI/external ecosystem bypasses HA Core or MediaHub policy.

**Evidence:** accepted domain contract, flow mapping, integration and bypass-negative verification.
**Primary source:** B2 §§3, 14, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; architecture/STATE-HA-INTEGRATION-CONTRACT.md, main, SHA aa68e876d06980ced3e6b6b3995ea6a117446423, status PROPOSED FUTURE EXTENSION — NOT CURRENT RUNTIME AUTHORITY.
**Status:** authority split accepted; proposed future HA/persistence architecture is not active runtime authority.

### ARC-003 — ASTRA's authority is engineering-only
**Rule:** A0-ASTRA coordinates engineering work and owns ASTRA's queue/claim/lease/evidence/gate state only. It is not MediaHub Product State Authority. No product object or domain mutation may treat A0 queue state as the canonical value of that product object. Human authorization remains final for launch/release actions requiring it.

**Acceptance:** ASTRA role contracts distinguish engineering workflow state from product state; no task, worker, executor, provider or verifier can self-promote or create product authority.

**Evidence:** schema/blueprint invariant checks and independent gate evidence for execution; human launch decision where required.
**Primary source:** architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml, branch SHA 0b86b07dfa916d4485ce1f8f54d19de136d98491; architecture/ASTRA-GOLD-QUALIFICATION-BLUEPRINT.yaml, branch SHA 9f199ba8e872d5ae188fcdac9635a53f16973534; docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md, branch SHA 9ad83781a8da53d1a8f540ede54eba95281f01c0.
**Status:** documentary ambiguity narrowed; no test run in this session and no operational promotion.

### ARC-004 — canonical mutation flow
**Rule:** A state-changing intent MUST enter the governed command path:

Command → Validation → Authorization/Policy → Consumer/Integration Contract → Owning Domain Authority → Canonical Mutation → Event/Fact → Observers.

Events, telemetry, logs and observations do not provide mutation rights.

**Acceptance:** command owner, authorization, freshness, schema, state preconditions, failure behavior and resulting authoritative revision are identifiable. Direct mutation bypasses are rejected.

**Primary source:** architecture/FUNCTIONAL-BASELINE-1.0-CONTRACT-RECONCILIATION.md, main, SHA 923d7accc2c0c67a5df4d76243ffb457c2d54ac5; docs/architecture/P0-06-core-runtime-services-contract.md, main, SHA ff21515e589b10fcbe2b167c3aadb3f66b32b4ae.
**Status:** path defined by primary contracts; do not infer a complete product-wide implementation from docs.

### ARC-005 — state semantics stay distinct
**Rule:** reported, observed, desired, policy-allowed, commanded, committed, applied, confirmed and predicted are distinct concepts.

**Acceptance:** contracts and APIs do not collapse request, commit and physical confirmation into one success state; revision/provenance and unknown-state behavior are explicit.
**Primary source:** B1 §§2–3, 45, SHA 9df4892ed0734050ac79732603d15bb414717310; current B2 authority and API/event model §§3,4,22, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; MH-06 health/readiness ADR main, SHA 7dda05379bd70007dc18acd62ed14fc83f0c9226.
**Status:** semantic invariant; runtime conformance evidence remains required.

### ARC-006 — fail-closed safety behavior
**Rule:** Unknown, malformed, stale, unauthorized, ambiguous or unqualified critical input cannot be optimistically admitted. UNKNOWN health/readiness does not become READY by default. State Authority failure creates no fallback authority.

**Acceptance:** rejection/deny/quarantine behavior and recovery conditions are explicit per contract; retries do not double-apply a mutation; no silent promotion from unknown to ready.
**Primary source:** B2 §4, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; docs/architecture/MH-06-ADR-001-health-readiness-semantic-contract.md, SHA 7dda05379bd70007dc18acd62ed14fc83f0c9226, status accepted semantics / implementation authorization NO; architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md, SHA 8d831c2a8fa333977dd86524099568bae2a8db0e, status proposed architecture.
**Status:** semantic rules accepted where source status says so; runtime verification pending.

### ARC-007 — the frozen MH-03 foundation is not silently upgraded
**Rule:** The current MH-03 foundation is single-node, in-memory State Authority, no HA and no physical persistence authorization. Future PostgreSQL/etcd/NATS-based HA is not active merely because a design exists.

**Acceptance:** any change to topology, persistence authority, HA/quorum, replication or consistency behavior has an explicit governance decision, dependency analysis, compatibility review, acceptance and freeze; until then the future extension is kept outside current implementation contract.

**Primary source:** architecture/MH-03-master-prompt.md, main, SHA e99035f596e236645bf8f2235fc4d375716ce476; architecture/STATE-HA-INTEGRATION-CONTRACT.md, SHA aa68e876d06980ced3e6b6b3995ea6a117446423.
**Status:** current foundation preserved; HA target remains proposed.

### ARC-008 — local-first and privacy/domain separation
**Rule:** Local capability survives cloud loss within its qualified profile. User data is not a default developer-cloud mirror or qualification fixture. External computation is a bounded request, not an authority grant.

**Acceptance:** classification, permitted data scope, destination/provider/model identity, privacy and retention controls, resource/cost/time limits, cancellation/failure semantics, and audit provenance are explicit. Developer compute does not create a raw-user-data mirror or personnel access.

**Primary source:** B2 §§2, 5–7, 11, 18, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; docs/architecture/MH-21-external-compute-contract.md, main, SHA b2127d6085cdbfcd98d2f819fa3ea5d12ffee68f, status proposed.
**Status:** architectural invariant; external-compute contract detail remains proposed.

### ARC-009 — runtime selection uses capability evidence
**Rule:** Hardware identity is not hardware qualification. Runtime/node/workload admission is based on a measured capability profile, explicit policy and workload requirements, not branding or GPU presence.

**Acceptance:** CPU/GPU/NPU and VRAM, RAM, storage I/O, network, thermal/power, reliability, OS/runtime support, isolation, privacy and available capacity are captured; capability drift downgrades or blocks admission until requalified.

**Primary source:** B2 §§8–11, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; docs/checkpoints/2026-09-29-compute-fabric-qualification-matrix.md, main, SHA 5ce43482e7bedb6d2e2a627485ecbc73b743d8e9.
**Status:** architecture rule accepted; Mac mini/Mac Pro/GPU expansion are planned target profiles, not qualified nodes.

### ARC-010 — network planes do not collapse into a flat network
**Rule:** User control/API, Media/Data, Smart Home/device, developer mesh, HIGH_SPEED developer interconnect, optional storage and bounded egress/qualification paths have explicit policy scopes.

**Acceptance:** ordinary user/media traffic does not traverse the developer HIGH_SPEED plane by default; CPRG remains API-registration-only, not a generic VPN/egress authority; no contributor receives general user-storage access.

**Primary source:** B2 §§5, 11–12, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; docs/checkpoints/2026-09-30-mediahub-hierarchical-cluster-architecture.md, main, SHA f49e2e38f131189147e6f9461ba82685e7924a52; network system passport extension SHA 43877c776889c58ae25a18d3ad60d2bb3a028578.
**Status:** architectural separation established; vendor/hardware interoperability and performance qualification open.

### ARC-011 — persistence, knowledge and object storage remain subordinate
**Rule:** PostgreSQL + pgvector + S3-compatible object storage describe the functional foundation, but implementation admission remains component- and target-gated. No cache/search/vector/graph/object store becomes Product State Authority implicitly.

**Acceptance:** clear ownership, authoritative records, projections, rebuildability, consistency and recovery/retention boundaries; measured need before adding a second durable indexing/relational subsystem.

**Primary source:** B2 §§13, 16, 23, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; docs/checkpoints/mediahub-github-component-final-manifest-2.0.md, main, SHA 45988bf9da202c9597d0ca2de50e92e5c2e6ed55.
**Status:** development component selection canonical; specific production admission not established.

### ARC-012 — component status is not execution status
**Rule:** SELECTED, CANDIDATE, TARGET-GATED, FUTURE-GATED, INSTALLED, IMPLEMENTED, VERIFIED, QUALIFIED, RELEASED, DEPLOYED and PRODUCTION ACCEPTED are not interchangeable.

**Acceptance:** each production dependency has identity, version/ref, license/provenance, security assessment, compatible runtime profile, integration/negative-path/recovery evidence and independent approval appropriate to the gate.
**Primary source:** Component Manifest 2.0 §§8, 12, SHA 45988bf9da202c9597d0ca2de50e92e5c2e6ed55; B2 §§20–21.
**Status:** mandatory rule. Component implementation/production qualification must be verified individually.

### ARC-013 — qualification truth is exact-SHA and evidence based
**Rule:** Current gate state is governed by the canonical machine contract plus fresh, attributable evidence. Historical evidence does not qualify a changed source SHA or changed deployment. Self-qualification/self-promotion is prohibited.

**Acceptance:** evidence binds node, executor, provider/model/transport, repository, exact SHA, clean worktree, command and timestamps; the required gate bundle is independently checked and missing evidence blocks progression. A 24-hour soak counts only when all prerequisite gates and current-SHA conditions pass.
**Primary source:** architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml, main, SHA 1d3ac25e7817f365807ad85d0d7c9007bd48bebf; ASTRA launch schema working branch SHA 0b86b07dfa916d4485ce1f8f54d19de136d98491; generated docs/qualification/CURRENT-TRUTH.generated.md, main, SHA 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731.
**Observed result:** NOT_PROVEN / BLOCKED in the inspected generated truth. No active GOLD or successful current 24h soak is claimed.

### ARC-014 — traceability is atom-level, source-anchored and non-inflated
**Rule:** Every normalized requirement atom is uniquely traceable to exact source lines, a status, an owning source/authority and an evidence plan. Child IDs are not minted until a full collision check.

**Acceptance:** preserve historical parent IDs; use only approved mapping statuses; distinguish literal, derived, split, cross-link-only and unresolved atoms; every row carries these 12 approved fields in order: Requirement ID; Owner; Source atom/classification; B2 mapping status; Canonical contract path/ref; Acceptance criteria; Required evidence; Lifecycle status; Reviewer/approval reference; Dependencies; Verification method; Change history; B1 source line anchors are real nonblank lines and B2 mapping claims point to actual clauses.
**Primary source:** Batch 04 owner decision record SHA 9117098e22c26708d48ca8ba5954669faa209d68; crosswalk draft SHA f9e66b7adde7afeaf6a7fb6ef1a867dee07c1b34; structural review SHA ea64aadc42244fe93a89735e7c0d8bce16b662d2.
**Observed result:** 48 historic parent IDs are present even though the older historical backlog text says “47”; do not rewrite that historical record to conceal the discrepancy. Current parent-level distribution is 4 MAPPED, 3 NO_DIRECT_COUNTERPART, 41 NOT_REVIEWED, 0 CONFLICT. This is not atom-level semantic approval. UI4-04 remains HOLD / CROSS-LINK-ONLY. No requirement atom or final child ID is created for UI4-04 until a cited literal source establishes unique residual behavior beyond the already mapped UI contract.

### ARC-015 — immutable baseline and history protection
**Rule:** Do not alter B1 or accepted B2 in order to reconcile derived matrices or draft architecture. Correct branch-level derived artifacts and record provenance. Do not merge main unless separately authorized.

**Acceptance:** each edit identifies base blob SHA, changed branch/ref, post-write blob SHA and read-back verification. Historical inconsistencies such as the older “47” count are not deleted; new docs may state a verified 48 unique IDs with provenance.
**Status:** enforced in the current work process; no edits made to B1, B2 or main.

### ARC-016 — lifecycle, release and production are separate gates
**Rule:** DESIGN, IMPLEMENTED, TESTED, VERIFIED, QUALIFIED, RELEASED, DEPLOYED, OBSERVED and PRODUCTION ACCEPTED require separate evidence and authorization. Architecture docs alone satisfy none of the later gates.

**Acceptance:** stage owner, required evidence, independent reviewer, target SHA/profile, rollback and acceptance decision are recorded. Any missing/contradictory evidence blocks promotion.
**Primary source:** B1 §§46, 48–49, 65–68, SHA 9df4892ed0734050ac79732603d15bb414717310; B2 §§0,20,24; generated ASTRA truth SHA 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731.

## 3. Cross-domain system contract

### 3.1 Public interfaces

Every component contract admitted to implementation MUST declare:
- stable/versioned request, result, event and error schemas;
- the owning domain and non-authorities;
- identity, authorization/policy and capability checks;
- idempotency/correlation IDs and freshness/revision rules;
- time/resource/cost/output limits where applicable;
- cancellation, timeout, retry, failure and degraded-mode semantics;
- data classification, residency, minimisation, retention and audit;
- observability outputs that contain no secrets or unrestricted personal payload;
- recovery/migration behaviour and backward-compatibility conditions;
- acceptance criteria and evidence to prove each criterion.

### 3.2 State transitions and events

- Commands express requests; events report facts that have happened.
- Result publication may be asynchronous but must be traceable to command/correlation ID and authoritative revision.
- Consumers must be idempotent where event delivery can repeat.
- Stale commands/results are rejected per version/generation/freshness contract.
- An event cannot stand in for authorization or mutate canonical state.
- Readiness/health is observational and operation-specific; a lifecycle READY state alone does not imply readiness for every operation.

### 3.3 Data and storage

- State authority and persistence technology are separate concepts.
- Every canonical, replicated, cached, indexed or derived data class has an owner, source of truth, retention and recovery story.
- Only an accepted domain contract may define the authoritative store for a domain; topology leadership or database availability alone never grants business authority.
- Backups, indexes, vector stores, graph stores and object storage do not supersede canonical authority.
- Restore validates provenance, integrity, version and authority before writes resume.

### 3.4 AI and external work

- AI outputs are advisory/proposals unless a specific bounded operation passes policy and domain authority.
- Model/provider identity, version, provenance, data class, allowed tools, destination, scope, timeout, resource/cost budget, retention, result limits, cancellation and failure behavior are part of an ExternalWorkload contract.
- Tool selection or model presence never creates capability authority.
- Any write requested by AI re-enters the exact same canonical command path as a human/API/device request.

## 4. Verification and acceptance matrix

| Check ID | Verifiable claim | Source/evidence required | Present status |
|---|---|---|---|
| V-01 | B2 accepted and current functional baseline pointer agrees | B2 SHA + MH-24 report + matrix | Documentary correction done on working branch; main matrix remains unchanged |
| V-02 | B1 source atoms individually reconciled | Atom-level crosswalk with nonblank line anchors and exact B2 mapping | OPEN; parent-level only |
| V-03 | Product/Smart Home authority boundaries are unambiguous | B2 + MH-03 + accepted HA integration contract and integration evidence | Functional split established; HA future extension still proposed |
| V-04 | ASTRA is not mistaken for Product State Authority | Scope annotation, executor matrix and architecture drift tests/readback | Wording clarified on branch; tests not run |
| V-05 | Target hardware profiles are admissible | Fresh component inventory, capability metrics, privacy/isolation/network profile and qualification | NOT PROVIDED / OPEN |
| V-06 | Component choices are qualified for production | Per-component identity/license/provenance/security/integration/recovery evidence | OPEN / component specific |
| V-07 | Live ASTRA transport and queue are qualified | Fresh per-node transport/runtime/scheduler/fencing/recovery/A3/24h evidence on one SHA | BLOCKED / NOT_PROVEN |
| V-08 | Local-first and privacy boundary is enforced | data-flow inventory, egress-negative tests, sanitized evidence, audit | Architectural requirement; implementation evidence not included here |
| V-09 | Recovery preserves single authority and provenance | restore/replay/fencing/rollback drills | OPEN |
| V-10 | System passport is fully accepted | independent review, owner approval and explicit baseline/change-control action | DRAFT / NOT ACCEPTED |

## 5. Definition of contract conformance

A document or subsystem is conformant only if:
1. every applicable ARC requirement has an explicit owner and source-backed scope;
2. each required interface/path, state owner, negative path, dependency and failure behavior is specified;
3. statuses and evidence are truthful and attributable to exact refs/SHA;
4. no open blocker is disguised as a pass;
5. any claim above documentary architecture has independent execution/evidence appropriate to its stage;
6. the exact reviewed version is re-read after each edit and the traceability/map indexes that read-back.

## 6. Non-conformance and stop rules

Set the dependent claim/action to BLOCKED (do not silently repair by assumption) when:
- the canonical source cannot be fetched or SHA/ref provenance is unknown;
- an authority boundary is ambiguous;
- a proposed/future contract would be promoted without approval;
- current runtime/gate evidence is stale, historical or for another SHA;
- sensitive data, credentials or production resources would be affected without authorization;
- a change would alter B1/B2, main, runtime semantics, infrastructure or production posture without explicit permission;
- child-ID uniqueness/source anchors/mapping cannot be demonstrated;
- the proposed correction contradicts a newer accepted owner decision.

## 7. Open decisions and blocked obligations

1. Complete Batch 04 atom-level mapping and independent semantic review. Keep UI4-04 HOLD; do not assign final child IDs yet.
2. Resolve remaining GOV-MH24 owner decisions, including shared-atom ownership, detailed HA/Core scope, automation literal-versus-derived distinctions, cloud gate, evidence details and any remaining domain sign-offs.
3. Resolve matrix/baseline traceability completely without editing immutable B1/B2.
4. Decide explicitly if/when the proposed State/HA persistence extension may replace or amend the current MH-03 foundation. No implied promotion.
5. Establish real hardware profile facts and qualification data for Mac mini, Mac Pro and any later GPU nodes.
6. Keep target-gated compute/network/storage/media/AI components behind individual measured/qualified gates.
7. Obtain fresh live ASTRA evidence; the current inspected truth remains NOT_PROVEN / BLOCKED.
8. Complete per-domain canonical path, master/reverse handoff, acceptance evidence and dependency map for MH-01…MH-25.
9. Obtain independent architecture review and owner acceptance before calling this the project-wide canonical contract or creating a new accepted system baseline.

## 8. Change history

- 2026-10-12 — initial integrated contract draft created from B1/B2, MH-24 report/matrix, domain contracts, component manifest and ASTRA gate sources.
- 2026-10-12 — matrix status corrected in branch; ASTRA internal state semantics clarified without changing authority field values.
- 2026-10-12 — pending 13-cycle audit/read-back.

**Final status:** a source-backed, verifiable working contract for branch review. It is not yet a globally accepted system contract and does not imply that all project documents, runtime functionality or qualifications have been fully verified.
