# MediaHub OS — verifiable integrated architecture contract 01

- **Date:** 2026-10-12
- **Ref:** docs/mediahub-chat-tree-map-20261012
- **Status:** WORKING INTEGRATION CONTRACT / DRAFT — NOT A NEW CANONICAL BASELINE
- **Use:** operative review/checklist for documentation and architecture work on this branch, subject to the source precedence and gates below.
- **Not a grant of authority:** does not replace Baseline 2.0, alter Baseline 1.0, approve pending domain contracts, authorize implementation/deployment, or imply qualification/production acceptance.
- **Companion passport:** docs/checkpoints/MEDIAHUB-OS-SYSTEM-PASSPORT-V3.md, current working blob SHA `d4b742ea5e55ae23472cb285bf39bc29cbbb359c`.
- **Current working inventory:** 34 ARC requirements / 27 verification checks; full architecture acceptance remains OPEN.
- **Rule of evidence:** claim → source path → ref → blob SHA → exact scope/status → acceptance/evidence required → independent read-back.

- **Current terminology:** the latest owner-provided umbrella name is **Jarvis**; an earlier same-day draft used “Astro”. Jarvis supersedes that draft label. The existing gap-report filename retains `ASTRO` for reference lineage; this does not rename ASTRA or assert deployed functionality.

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
**Status:** current foundation preserved: MH-03 remains single-node and in-memory, with no physical persistence or HA authorized in the current foundation; the HA target remains proposed and cannot become an implementation dependency without an explicit governance change.

### ARC-008 — local-first and privacy/domain separation
**Rule:** Local capability survives cloud loss within its qualified profile. User data is not a default developer-cloud mirror or qualification fixture. External computation is a bounded request, not an authority grant.

**Acceptance:** classification, permitted data scope, destination/provider/model identity, privacy and retention controls, resource/cost/time limits, cancellation/failure semantics, and audit provenance are explicit. Developer compute does not create a raw-user-data mirror or personnel access.

**Primary source:** B2 §§2, 5–7, 11, 18, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; docs/architecture/MH-21-external-compute-contract.md, main, SHA b2127d6085cdbfcd98d2f819fa3ea5d12ffee68f, status proposed.
**Status:** architectural invariant; external-compute contract detail remains proposed.

### ARC-009 — runtime selection uses capability evidence
**Rule:** Hardware identity is not hardware qualification. Runtime/node/workload admission is based on a measured capability profile, explicit policy and workload requirements, not branding or GPU presence.

**Acceptance:** CPU/GPU/NPU and VRAM, RAM, storage I/O, network, thermal/power, reliability, OS/runtime support, isolation, privacy and available capacity are captured; capability drift downgrades or blocks admission until requalified.

**Primary source:** B2 §§8–11, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; docs/checkpoints/2026-09-29-compute-fabric-qualification-matrix.md, main, SHA 5ce43482e7bedb6d2e2a627485ecbc73b743d8e9.
**Status:** architecture rule accepted; Mac mini/Mac Pro/later GPU expansion are planned target profiles, not confirmed installed nodes. No role is assigned before an inventory-bound capability profile and measured CPU/GPU/VRAM, RAM, storage, network, thermal/power, runtime compatibility, isolation and reliability evidence exist.

### ARC-010 — network planes do not collapse into a flat network
**Rule:** User control/API, Media/Data, Smart Home/device, developer mesh, HIGH_SPEED developer interconnect, optional storage and bounded egress/qualification paths have explicit policy scopes.

**Acceptance:** ordinary user/media traffic MUST NOT traverse the developer HIGH_SPEED plane by default; CPRG remains API-registration-only, not a generic VPN/egress authority; Media/Data, user control, developer mesh, high-speed compute/storage and qualification management retain separate admission/policy scopes; no contributor receives general user-storage access.

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
**Status:** mandatory rule. A selection manifest records an architecture/development decision only: it does not prove a component is installed, running, version-matched, secure, benchmarked or production-qualified. Component implementation/production qualification must be verified individually.

### ARC-013 — qualification truth is exact-SHA and evidence based
**Rule:** Current gate state is governed by the canonical machine contract plus fresh, attributable evidence. Historical evidence does not qualify a changed source SHA or changed deployment. Self-qualification/self-promotion is prohibited.

**Acceptance:** evidence binds node, executor, provider/model/transport, repository, exact SHA, clean worktree, command and timestamps; the required gate bundle is independently checked and missing evidence blocks progression. A 24-hour soak counts only when all prerequisite gates and current-SHA conditions pass.
**Primary source:** architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml, main, SHA 1d3ac25e7817f365807ad85d0d7c9007bd48bebf; ASTRA launch schema working branch SHA 0b86b07dfa916d4485ce1f8f54d19de136d98491; generated docs/qualification/CURRENT-TRUTH.generated.md, main, SHA 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731.
**Observed result:** CURRENT-TRUTH.generated.md on main (blob SHA 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731) reports NOT_PROVEN / BLOCKED with no gate having fresh PASS evidence. The Astra 24H runbook (main, blob SHA efb1c8af47578cbe14f8e788676d71ba4c665966) separately says live three-node transport is not qualified and identifies a legacy worker health-schema mismatch. A historical soak/run cannot override these current blockers; no active GOLD or successful current 24h soak is claimed.

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

### ARC-017 — Jarvis is the umbrella engineering architecture; Astra is a bounded subsystem

**Rule:** In the owner-provided target framing dated 2026-10-12, Jarvis is the umbrella for project context, source discovery, requirement decomposition, dependency planning, task-scoped execution, verification and release preparation. Astra/Astra Gold may supply queue/claim/worker/evidence capabilities as one subsystem. Neither Jarvis nor Astra may become MediaHub Product State Authority. This is a working-contract addition, not a claim of a deployed Jarvis runtime or a repository rename.

**Acceptance:** architecture diagrams, prompts and contracts explicitly distinguish Jarvis (umbrella), Astra (bounded engineering subsystem), MediaHub State Authority (product/platform state), and Home Assistant Core (Smart Home-domain authority). An ambiguity blocks the dependent task.

**Sources:** owner blueprint / branch gap reconciliation current blob SHA 39720b11e5e6777b86ffd71e0fec1214982e0d95; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; ASTRA launch schema SHA 0b86b07dfa916d4485ce1f8f54d19de136d98491.

### ARC-018 — one owner for engineering task lifecycle

**Rule:** Jarvis must not accidentally introduce a second independent queue, claim store, lease/fencing domain, retry engine or qualification-promotion store. Before implementation, select one lifecycle owner: an admitted Astra subsystem, a separately evaluated durable workflow service, or another explicitly selected implementation. Other candidates integrate through versioned adapters.

**Acceptance:** one task ID lineage and one authoritative engineering-task state transition path exist; retries are idempotent; exclusive tasks use fencing; all state changes are traceable. No product-state authority is inferred from this workflow state.

**Status:** design requirement; scheduler/framework choice OPEN.

### ARC-019 — source- and SHA-bound task envelope

**Rule:** Every dispatched Jarvis task MUST include task/parent ID, MH domain, requirement IDs, approved base ref/SHA, source refs and trust, dependencies, worker capability profile, workspace boundary, allowed tools/files/network/egress, timeout/lease/retry/idempotency rules, acceptance criteria, independent verifier, changed-path manifest, evidence digest, exit status and permitted next lifecycle state. Credential values and unrestricted personal payloads MUST NOT be included.

**Acceptance:** malformed/incomplete envelope is rejected; workspace/output and evidence refer to the same approved task/base; duplicate or stale result cannot silently advance state.

### ARC-020 — agent roles are capability profiles, not a fixed bot count

**Rule:** Collector, analyst, architect, builder, normalizer, documentation author, reviewer and specialist profiles are task-scoped capabilities. A library of 26 ECC/specialist roles, if adopted, is not a requirement for 26 always-running processes. Models and agents cannot self-assign authority or certify their own changes.

**Acceptance:** profile admission uses task fit, identity, permissions, resource budget and verification requirements; independent A3 review uses a distinct verifier role/identity and cannot be bypassed by role labels.

### ARC-021 — hardware roles and trust domains are explicit

**Rule:** Purchased Mac Pro, developer Mac mini 2011 (16 GB), customer-site Mac mini M2, current test servers and any future GPU/video server are separate inventory/profile records. The customer-site prototype MUST NOT silently join the developer compute pool or inherit developer credentials/data. Host names and model names do not qualify capabilities.

**Acceptance:** each admitted node has exact inventory, OS/security-support and dependency compatibility, capacity/thermal/network/isolation evidence, workload profile, node identity, recovery and privacy/egress policy. The 2011 node is not a mandatory dependency unless its required compatibility is demonstrated.

**Status:** owner-reported hardware intent recorded; device inventory and qualification OPEN.

### ARC-022 — deployment is a pinned, reproducible release, not a rebuild on target

**Rule:** A release candidate must be packaged before the target hardware is provisioned. Its manifest pins source/build SHA, supported CPU/OS range, dependency lock, checksums, license notices/SBOM/provenance, profile configuration, secret references, preflight, migration, health/readiness, backup/restore, rollback and post-deploy evidence. Containerization is not mandatory without compatibility evidence.

**Acceptance:** clean-profile preflight and install are repeatable on an admitted target; failed health or migration yields bounded rollback; final evidence names the exact package SHA and node profile.

**Status:** design requirement; package and install qualification not provided.

### ARC-023 — third-party reuse is evidence-gated

**Rule:** Before selecting a public repository/module, capture canonical identity, exact pin, license, maintenance/release history, security policy/advisories, dependency/SBOM provenance, platform/resource fit, offline/local behavior, egress and permission model, recovery/idempotency behavior, test evidence, integration cost and removal/rollback path. Stars, documentation claims or discovery alone are insufficient.

**Acceptance:** every candidate receives REJECT, REFERENCE ONLY, CANDIDATE, POC QUALIFIED, SELECTED FOR DEVELOPMENT or PRODUCTION QUALIFIED status with evidence and explicit decision authority. Candidate research does not permit installation or production admission.

### ARC-024 — MH context distribution must preserve primary-source lineage

**Rule:** Use one global Jarvis context packet plus domain-specific packets for MH-01…MH-23. Packets carry primary paths, refs/blob SHAs, accepted and superseded decisions, dependencies, invariants, change deltas and open conflicts; they link to primary documents rather than duplicating them as a second source of truth. MH-24/MH-25 remain reconciliation/control stages.

**Acceptance:** any packet can be traced to current primary files and has a generated/reviewed-at timestamp/ref; stale/missing inputs block its “current” designation; source changes are read back before dependent packets are refreshed.

### ARC-025 — repository coverage claims are measurable and bounded

**Rule:** Distinguish tree inventory, successfully fetched files, structurally classified files, semantically reviewed files, resolved conflicts and unreviewed files. An inventory of repository entries is not a semantic audit of every file. Do not claim “all defects fixed” without a source-by-source closure ledger.

**Acceptance:** every audit report states refs/tree snapshot, exact inspected set, exclusions, unresolved findings and review status; completion claims match that ledger.

### ARC-026 — every deployment profile pins its operating-system contract

**Rule:** A hardware name or role does not define its target operating system, boot mode, install method or lifecycle. B2 §9 states that clean Mac mini/Mini PC installations use Linux as the baseline implementation direction, while Apple platforms remain integrated adaptations where the base OS cannot be replaced. Each named target must therefore have an explicit, approved OS/build, architecture, boot/install/update/recovery and rollback profile; do not infer macOS/Linux from “Mac Pro” or “Mac mini”.

**Acceptance:** the release manifest identifies the exact node/profile OS and runtime constraints; model/architecture compatibility, support and security-update status, drivers, boot/install path, update/recovery image and rollback are source-backed and qualified for that profile. An unpinned profile blocks release packaging/admission.

### ARC-027 — physical asset identity and active role allocation is explicit

**Source conflict:** the owner blueprint assigns the purchased Mac Pro to the developer environment as the primary workstation and also describes a future production target based on Mac Pro + Mac mini. The current source does not establish whether the production Mac Pro is a separate physical asset or the same unit at a later point in time.

**Rule:** each physical node has a unique project inventory/profile identity (do not publish serial numbers in general project documents), exact model/configuration, trust domain, data/credential scope and active deployment role. Do not assign the same physical Mac Pro concurrently as both the primary developer workstation and a production/customer node by inference. If they are separate units, maintain separate profile records. If they are the same unit at different times, require an explicit owner-approved role transition, a replacement developer-workstation plan, developer credential revocation/rotation and data-boundary cleanup, an approved clean deployment profile, recovery/rollback path and exact release-manifest evidence before production admission.

**Acceptance:** the owner-confirmed inventory and deployment manifest resolve same asset versus separate asset; the role/trust domain is unambiguous; any transition has approval, replacement capacity, credential/data separation, restore/rollback and post-deploy evidence bound to the release SHA. Until then the affected production profile is BLOCKED / ASSET ALLOCATION REQUIRED.

**Sources:** owner-provided Jarvis blueprint (2026-10-12); gap reconciliation §17 / AG-20, current blob SHA 39720b11e5e6777b86ffd71e0fec1214982e0d95; Passport v3 / P-20, current blob SHA 306aca30d4757fa6ba835c30354ce7dd02705534.

**Sources:** B2 §9, `main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; Passport v3 current working SHA `306aca30d4757fa6ba835c30354ce7dd02705534`; Jarvis gap reconciliation current SHA `39720b11e5e6777b86ffd71e0fec1214982e0d95`.


### ARC-028 — B1↔B2 section pointers are semantically validated and historical audits remain immutable

**Rule:** Every crosswalk or architecture mapping must cite a real, nonblank source anchor and confirm that the referenced B2 section is semantically relevant to the requirement. A source-pointer defect is a traceability defect until a contradictory normative statement is independently established. Correct the current working crosswalk and record the correction with exact source refs/SHAs; preserve historical audit artefacts as history instead of silently rewriting them. A pointer correction alone does not justify promoting mapping, acceptance, implementation or qualification status.

**Acceptance:** the source SHA, exact B1 atom/line, B2 section heading and relevant content are read back; historical/derived and current/corrected refs are clearly distinguished; an independent structural review verifies pointer correctness; semantic owner acceptance remains a separate gate.

**Current finding:** Audit 01 row B1-15-13 links “Assist with documents” (B1 §15 line 246) to B2 §19. Pinned B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f defines §16 as Documents and Knowledge, §18 as AI architecture and §19 as Update / Recovery / Migration. Batch 06 working crosswalk SHA 9df96aca53d1004c33d45f038501dc6b7f52c0c9 correctly uses §§16/18 and preserves the historical Audit 01 mismatch. Review SHA 1edc976dd663ae16a1b61876a2dbbde9411be095 confirms the source headings. The mismatch is recorded as AG-21 / P-21; no B1/B2 semantic conflict is claimed.

**Sources:** B1 specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main, SHA 9df4892ed0734050ac79732603d15bb414717310; B2 docs/checkpoints/mediahub-functional-baseline-2.0.md@main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; historical Audit 01 SHA d0938f14ed4110545118f075175dee3be412097b; current Gap Reconciliation SHA 39720b11e5e6777b86ffd71e0fec1214982e0d95; current Passport v3 SHA 306aca30d4757fa6ba835c30354ce7dd02705534.

**Status:** pointer correction structurally verified in a working crosswalk; semantic acceptance and broader Audit 01 cleanup remain OPEN.

### ARC-029 — Trusted Sources scope and evidence semantics remain explicitly gated

**Source basis:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`, §18 lines 297–309; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §16 lines 358–366 and §18 lines 380–394; Product Owner Decision Record 01 D-06 SHA `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd`; Batch 09 crosswalk SHA `5e1b73c73c951638b549a30d569df2d1c7de8b31`; Review 03 SHA `184a99ef85143c2ad3048dca5c8d85b17f8651a3`.

**Rule:** Keep the named Trusted Sources Intelligence Engine and its lifecycle contract in an explicitly open disposition until the owner/governance scope decision and accepted contract exist. B2's general search, provenance, evidence and source-verification clauses do not by themselves prove that the full named subsystem, source lifecycle or four-category information taxonomy is accepted. Do not infer global repository absence from `NO_DIRECT_COUNTERPART`, or implementation/qualification from `MAPPED`. Preserve the distinction between verified evidence, external source, inferred information and AI-generated information; AI-generated information must not automatically become verified evidence. Knowledge stores and AI remain non-authoritative. D-06 remains controlling for the working traceability relationship: TSI-07 is primary provenance and TSI-12 remains a historical sub-aspect, not an independent sibling obligation.

**Acceptance:** record an explicit owner/governance decision to preserve, revise or defer the named TSI subsystem; if preserved, approve its owner, interfaces, allowed source scope, trust classification, retrieval/verification/provenance/comparison/change-detection/evidence workflows, information-state taxonomy, verified-knowledge lifecycle, failure/unknown handling and acceptance evidence. Independently review source anchors and each mapping. Do not mint final child IDs until lineage and collision checks are evidenced; do not promote the draft to the canonical backlog by this rule alone.

**Status:** OPEN — the bounded Review 03 finds the current documentary mapping internally consistent, but full semantic acceptance, owner/scope disposition, accepted contract, implementation and qualification remain open.

### ARC-030 — Local Cluster AI mapping and workload acceptance stay separate

**Sources:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`, §16 lines 253–267; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §10 lines 235–253, §18 lines 380–394 and §22 lines 438–455; Batch07 draft SHA `d6323442e3059dda091d0ad8b2a33fa91cad6ea0`; Batch07 Review02 SHA `0af17bf0db6f8b1c93d01aae3e8a8b5d8a0d9064`.

**Rule:** The working crosswalk may record B1-16-01 / CLAI4-01 as `MAPPED` for the bounded documentary capability because B2 §10 explicitly permits a qualified multi-node cluster to provide compute and AI with trust/admission, and B2 §18 explicitly names Local Cluster AI. This does not accept the complete Local Cluster AI contract, any individual workload-specific semantics, the named MediaHub AI Gateway, the derived control, runtime implementation or qualification. Keep B1-16-02…09 and B1-16-D01 `NOT_REVIEWED`; keep B1-16-10 `NO_DIRECT_COUNTERPART` narrowly scoped to the named gateway in the reviewed B2 clauses. B2 §22's compute protocol is relevant to distributed-task design but is not alone sufficient to accept retry/replay, task ownership, partition/rejoin or workload-specific semantics. Preserve all historical CLAI4/B1-16 identifiers, 12-field records and separate Review01 history.

**Acceptance:** an accepted Local Cluster AI contract must define owner, trust/admission and revocation boundaries, workload-specific contracts/resource profiles, named-gateway disposition and interface, and failure/unknown/retry behavior. Derived controls require explicit owner/governance acceptance. All implementation/verification/qualification gates remain separately evidenced. Do not mint final IDs until lineage/collision checks pass, and do not promote this draft into the canonical backlog from this clause alone.

**Status:** DOCUMENTARY MAPPING CORRECTION RECORDED; FULL SEMANTIC AND CONTRACT ACCEPTANCE OPEN.

### ARC-031 — AI Human Clone remains permission-scoped, traceable and non-authoritative

**Source basis:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`, §19 lines 315–328; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §§3–7, 15–18; Audit 01 SHA `d0938f14ed4110545118f075175dee3be412097b`, B1-17-05 / CDAI4-02; Batch 08 draft SHA `a978d6846b747f397b266dc0befa05fc22cdd7ab`; Batch 10 draft SHA `44b9369fea0be06e4e64f2052fd49f6d493f6603`; Batch 10 Review 01 SHA `36148379d7d1e39252bd918ad17772036cf0d972`; Batch 10 Review 02 SHA `612162b164b7d2585fa9646871839274cec5a343`.

**Rule:** Treat B1 §19 as a detailed source expansion of the named AI Human Clone subsystem already listed at B1 §17 line 278 / `PROVISIONAL/CDAI4-02/B1-17-05`. Preserve that lineage; AHC-19-01 is a cross-link-only traceability row and must not be counted as a new independent subsystem obligation. B2 provides only bounded generic controls for authorization, audit, revocation and non-authority. It does not by itself accept a clone-specific contract for consent, rights-holder authorization, identity/scope, voice/appearance permissions, model/asset provenance, real/synthetic separation, disclosure, revocation limits or representation policy.

**Acceptance:** an explicit owner/governance disposition identifies whether the subsystem is retained, its accountable owner, approved purposes and rights/permission model, identity/model/asset lineage, real/synthetic separation, audit/revocation behavior, authority exclusions and required evidence. Every acceptance claim is traceable to pinned source refs; any later implementation/qualification requires its own authorized evidence. No final child IDs before the project-wide lineage/collision check.

**Status:** OPEN — Batch 10 Review 01 confirms structure, source anchors and bounded status consistency only. The 19 labels remain provisional; semantic/owner acceptance, subsystem contract and implementation/qualification remain open.

### ARC-032 — Mobile Access roles remain distinct; detailed scope and packaging remain gated

**Source basis:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`, §20 lines 332–359; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §2.3 lines 63–72, §4 line 108, and §25 lines 508–509; working matrix rows 20–21, SHA `73377891072bac3c739c44055ceeb0874154f64c`; Batch 11 draft SHA `0c102e5071ed5a33cbc02b00872da78eebd5bf9c`; Review 01 SHA `2a11ae52c4401a51fc562df5c9ddbe07cb83b2ef`; Review 02 SHA `c143d1b349bcf2ba3a76ffdad03b1d4258a1ebe9`.

**Rule:** Preserve the distinct local Core and Remote Access roles. Core is defined as local full-minimal iOS/iPadOS MediaHub Core, not a remote client. Remote Access is a separate remote access/management role and is not Local Core. No mobile application is authority; actions remain inside the accepted MediaHub and domain authority/contract path. Do not resolve B1's literal “exactly two applications” scope by assumption: B2 identifies two user-facing functional roles and separately identifies Developer Mobile as a developer-only surface. Keep the distinction visible until owner/governance semantics are recorded. Generic B2 clauses do not prove the full local capability matrix, one-time payment model, every remote capability or a concrete Remote Access API contract.

**Acceptance:** source-anchored owner/governance disposition defines the application-count boundary; approved Core capability matrix by platform/profile and resource limit; product/entitlement policy for B1's one-time payment statement if retained; Remote Access capabilities, permitted service scope, API/version contract, authentication/authorization, failure/reconnect behavior and authority boundary. Implementation, verification and qualification require separate authorized evidence.

**Status:** OPEN — Batch 11 Reviews 01/02 verify structural/source anchors and bounded semantic consistency: nine provisional rows, 4 `MAPPED` / 5 `NOT_REVIEWED` / 0 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`. MA-20-05 is documentary contract/non-authority correspondence only. Matrix rows 20–21, B1 and B2 remain unchanged; app-count semantics, owner acceptance, concrete contracts, implementation and qualification remain OPEN.

### ARC-033 — Mobile invariants preserve authority, contract and security boundaries

**Source basis:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`, §21 lines 361–374; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §§2.3, 3–7, 14, 18, 22–23; matrix row 21 SHA `73377891072bac3c739c44055ceeb0874154f64c`; Batch 12 draft SHA `dcbc0a0e8a8186e926315ea318eff902e491f0e7`; Review 01 SHA `ece804af67ea66d0b0121b1e91c42451aa8143d8`; Review 02 SHA `f8d50509014f8c72476ab845476dcc40569c3357`.

**Rule:** Mobile apps are never canonical authorities, must not create alternative State Authority, and must use the accepted MediaHub contract model. Authentication, authorization, trust, privacy, audit and revocation are required. A mobile-specific command chain must not bypass MediaHub or the relevant domain authority; for Smart Home, HA Core retains its scoped operational authority. B1 §21 specifies the remote sequence `Remote Mobile Application → MediaHub API → MediaHub Core / State Authority / relevant subsystem`. Generic B2 authority/API/security clauses do not by themselves prove that the concrete mobile route exists or is enforced.

**Acceptance:** identify the concrete local/remote mobile command routes and versioned contracts; demonstrate that no direct physical-device bypass or shadow canonical authority exists; define identity/policy/privacy/audit/revocation behavior and negative cases; independently review exact source/evidence. Implementation/verification/qualification requires separate authorization and evidence.

**Status:** OPEN — Batch 12 Reviews 01/02 verify structure, source anchors and bounded semantic consistency: six provisional rows, 4 `MAPPED` / 2 `NOT_REVIEWED` / 0 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`. Review 02 corrects an uninformative change-history value in MAI-21-04 only; the direct-device bypass route and exact remote API/authority chain remain open. Working matrix row 21 remains unchanged.


### ARC-034 — iPhone Media / AirPlay support remains profile- and evidence-gated

**Source basis:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`, §22 lines 375–379; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §§8–9, 12, 15, 20; traceability matrix row 22 SHA `73377891072bac3c739c44055ceeb0874154f64c`; prior semantic finding `IPHONE-AIRPLAY-4K-01` in Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`; Batch 13 draft SHA `2f05bcf0b67200e44aaec7ba4e3a3164238270bf`, Review 01 SHA `abf9c5f669b59434c3a9bb52068b8f226efa129c`, and Review 02 SHA `36f171bf4ef6e9bec388cacc5ddc4ff8989d168e`.

**Rule:** Preserve the B1 §22 requirement as a candidate product capability: iPhone audio/video redirection to MediaHub using AirPlay, including 4K, subject to compatibility, network conditions, authorization, codec, latency, resolution and available bandwidth. B2 provides generic media endpoints, 4K media, capability profiles, network-plane and qualification principles, but the reviewed clauses do not explicitly accept an iPhone-to-MediaHub AirPlay contract. Do not convert generic phone-media or 4K terminology into a promise of AirPlay interoperability. Preserve the existing high-level `IPHONE-AIRPLAY-4K-01` and matrix row 22; Batch 13's provisional `IM-22-xx` records are subdivisions, not final child IDs.

**Acceptance:** an explicit product-owner/owner disposition and accepted media contract define the supported iPhone/iOS and MediaHub platform/device matrix, AirPlay behavior and directionality, 4K/codec constraints, rights/licensing, sender/receiver authorization, network and bandwidth admission, latency/resolution negotiation, unsupported-profile behavior, failure/degradation rules and exact evidence required per profile. Actual interoperability/performance evidence must be independently reviewed and bound to the precise hardware/software versions. MH-18 acceptance remains a separate gate.

**Current bounded mapping after Review 02:** Batch 13 has 9 provisional labels; **1 `MAPPED` / 7 `NOT_REVIEWED` / 1 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`**. Review 01's 0/8/1/0 distribution is retained as the pre-semantic-review snapshot. Only IM-22-06 is `MAPPED`, for generic media-codec handling expressly named in B2 §15; the AirPlay-specific codec profile remains OPEN. `NO_DIRECT_COUNTERPART` is only about the named AirPlay capability in the cited B2 clauses; it is not a claim that no related code or documents exist anywhere. No implementation or qualification is evidenced by this crosswalk.

**Status:** OPEN — Batch 13 Reviews 01/02 cover bounded structure/source anchors and semantic consistency. Review 02 recommends a single generic codec mapping only; AirPlay semantic/owner acceptance, the supported-profile contract, implementation, interoperability, performance and qualification remain OPEN. Do not promote row 22, alter B1/B2 or the canonical matrix, or mint final IDs based on this requirement alone.

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
| V-01 | B2 accepted and current functional baseline pointer agrees | B2 SHA + MH-24 report + matrix | Documentary correction done on working branch: blob SHA 73377891072bac3c739c44055ceeb0874154f64c (commit 2a1bc39bed1f0afe631c3587446af15837a5e980); main matrix remains unchanged |
| V-02 | B1↔B2 atom-level coverage and semantic acceptance are correctly recorded | Audit 01 plus Batch 01–08 union review; exact source anchors; owner decisions and accepted mapping evidence | STRUCTURAL UNION PASS: 153/153 labels across B1 §§3–6, 12, 15–17; 23 `MAPPED` / 119 `NOT_REVIEWED` / 11 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`. Semantic acceptance OPEN; not an all-68-section audit or canonical-backlog approval. |
| V-03 | Product/Smart Home authority boundaries are unambiguous | B2 + MH-03 + accepted HA integration contract and integration evidence | Functional split established; HA future extension still proposed |
| V-04 | ASTRA is not mistaken for Product State Authority | Scope annotation, executor matrix and architecture drift tests/readback | Wording clarified on branch; tests not run |
| V-05 | Target hardware profiles are admissible | Fresh component inventory, capability metrics, privacy/isolation/network profile and qualification | NOT PROVIDED / OPEN |
| V-06 | Component choices are qualified for production | Per-component identity/license/provenance/security/integration/recovery evidence | OPEN / component specific |
| V-07 | Live ASTRA transport and queue are qualified | Fresh per-node transport/runtime/scheduler/fencing/recovery/A3/24h evidence on one SHA | BLOCKED / NOT_PROVEN |
| V-08 | Local-first and privacy boundary is enforced | data-flow inventory, egress-negative tests, sanitized evidence, audit | Architectural requirement; implementation evidence not included here |
| V-09 | Recovery preserves single authority and provenance | restore/replay/fencing/rollback drills | OPEN |
| V-10 | System passport is fully accepted | independent review, owner approval and explicit baseline/change-control action | DRAFT / NOT ACCEPTED |
| V-11 | Jarvis and Astra roles do not cross the product-state boundary | owner blueprint + B2 + ARC-017 + architecture drift/readback evidence | Scope documented in branch; implementation conformance OPEN |
| V-12 | One owner controls task lifecycle and task state | selected scheduler/queue contract + collision/lease/retry/fencing/replay evidence | OPEN; Astra versus external scheduler/framework not selected |
| V-13 | Every agent task is source-, permission- and SHA-bound | valid/invalid envelope probes and evidence-manifest verification | Contract specified; tests not run |
| V-14 | Hardware profiles and customer/developer trust domains are separated | exact node inventory, security/network/egress profile, capability benchmarks and recovery evidence | Owner-reported roles documented; measured admission OPEN |
| V-15 | Target deployment is reproducible and rollbackable | pinned release bundle, SBOM/licenses, clean-profile preflight/install, health and rollback evidence | Design requirement; artifact not provided |
| V-16 | Reused public components are reviewed and pinned | repository scorecards, exact versions, license/security/provenance and bounded PoC evidence | Public desk review completed for shortlist only; no candidate qualified |
| V-17 | MH-01…MH-23 context packets remain traceable to primary sources | global/domain packet inventory with current refs/SHA and read-back status | Design requirement; packet mechanism not implemented |
| V-18 | Audit coverage is accurately represented | exact tree/source set, per-file review state and open findings | Bounded review only; whole-repository semantic completion not claimed |
| V-19 | Every target node has an explicit and compatible OS/boot/install/update/recovery profile | B2 §9 + per-node hardware manifest + supported-platform and rollback evidence | OPEN — profile decision and qualification not provided |
| V-20 | Developer and production Mac Pro asset allocation is explicit | Owner-confirmed inventory + release/deployment manifest or approved role-transfer record; trust/credential, replacement, recovery and rollback evidence | OPEN — source text does not identify same vs separate physical unit |
| V-21 | Crosswalk B1↔B2 section pointers are correct and historical traceability is preserved | Pinned B1/B2 SHAs, exact section headings and content, corrected working crosswalk, Audit 01 provenance, independent read-back | Structural/source-pointer review PASS for B1-15-13; semantic acceptance and broader Audit 01 cleanup OPEN |
| V-22 | TSI subsystem scope, source lifecycle, information categories and no-automatic-verification rule are correctly dispositioned | Pinned B1 §18 lines 297–309; B2 §§16/18; D-06; Batch 09 draft and Review 03; explicit owner/governance decision and accepted TSI contract | Bounded documentary consistency PASS; 17 provisional labels; 3 `MAPPED` / 13 `NOT_REVIEWED` / 1 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`; full semantic and owner/contract acceptance OPEN; no final IDs or canonical promotion |
| V-23 | Batch 07 B1 §16 mapping is accurately bounded and traceable | Pinned B1 §16 and B2 §§8–11/17–18/22/25; Audit 01/02; Batch07 draft; Review02; 12-field schema and historical IDs | One bounded `MAPPED` (B1-16-01), 9 `NOT_REVIEWED`, 1 `NO_DIRECT_COUNTERPART`, 0 `CONFLICT`; full Local Cluster AI workload/owner/gateway contract and implementation/qualification remain OPEN |
| V-24 | Batch 10 B1 §19 AI Human Clone mapping is source-anchored and does not double-count the named subsystem | Pinned B1 §19 lines 315–328; B2 §§3–7,15–18; Audit 01 / Batch 08 B1-17-05 lineage; Batch 10 draft and Reviews 01/02; 12-field schema | 19 provisional traceability labels; 5 `MAPPED` / 13 `NOT_REVIEWED` / 1 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`; structural/source-anchor and bounded semantic consistency checks PASS; owner/contract acceptance OPEN; AHC-19-01 cross-link only |
| V-25 | Batch 11 B1 §20 Mobile Access roles/claims are source-anchored, distinct and status-bounded | Pinned B1 §20 lines 332–359; B2 §2.3 lines 63–72, §22 lines 438–455, §4 line 108, §25 lines 508–509; working matrix rows 20–21; Batch 11 draft and Reviews 01/02 | 9 provisional labels; 4 `MAPPED` / 5 `NOT_REVIEWED` / 0 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`; structural/source-anchor and bounded semantic review PASS; app-count scope, price, full capability matrix, remote feature/API contracts and owner acceptance OPEN |
| V-26 | Batch 12 B1 §21 mobile invariants preserve authority and security boundaries | Pinned B1 §21 lines 361–374; B2 §§2.3, 3–7, 14, 18, 22–23; matrix row 21; Batch 12 draft and Reviews 01/02 | 6 provisional labels; 4 `MAPPED` / 2 `NOT_REVIEWED` / 0 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`; bounded semantic consistency PASS; concrete device-bypass route and remote API/authority chain OPEN; MAI-21-04 history field quality correction; no implementation/qualification inferred |
| V-27 | B1 §22 iPhone Media / AirPlay is source-anchored and its support claims are not inferred from generic B2 media capabilities | Pinned B1 §22 lines 375–379; B2 §§8–9, 12, 15, 20; matrix row 22; Audit Batch 03; Batch 13 draft and Reviews 01/02; MH-17/MH-18 acceptance/evidence | 9 provisional labels; current 1 `MAPPED` / 7 `NOT_REVIEWED` / 1 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT` (Review01 pre-review 0/8/1/0); bounded semantic consistency PASS; codec mapping is generic only; AirPlay contract, owner acceptance, compatibility/performance profile and qualification OPEN |

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

1. Complete independent semantic review and owner dispositions for atom-level Batches 01–08 (153 labels across B1 §§3–6, 12, 15–17), and continue uncovered B1 sections. Resolve the SH4 lineage issue and preserve UI4-04 HOLD. Final child IDs and canonical-backlog promotion remain gated by full collision review, source-anchor verification, semantic acceptance and explicit owner/governance approval.
2. Resolve remaining GOV-MH24 owner decisions, including shared-atom ownership, detailed HA/Core scope, automation literal-versus-derived distinctions, cloud gate, evidence details and any remaining domain sign-offs.
3. Resolve matrix/baseline traceability completely without editing immutable B1/B2.
4. Decide explicitly if/when the proposed State/HA persistence extension may replace or amend the current MH-03 foundation. No implied promotion.
5. Establish real hardware profile facts and qualification data for Mac mini, Mac Pro and any later GPU nodes.
6. Keep target-gated compute/network/storage/media/AI components behind individual measured/qualified gates.
7. Obtain fresh live ASTRA evidence; the current inspected truth remains NOT_PROVEN / BLOCKED.
8. Complete per-domain canonical path, master/reverse handoff, acceptance evidence and dependency map for MH-01…MH-25.
9. Obtain independent architecture review and owner acceptance before calling this the project-wide canonical contract or creating a new accepted system baseline.
10. Define the Jarvis public interface and choose the single owner for task lifecycle, claims, leases, retry, evidence and promotion; explicitly compare Astra against other durable execution candidates.
11. Record exact hardware identity for the Mac Pro, developer Mac mini 2011 and client-site Mac mini M2; qualify a future GPU/video server only when acquired.
12. Define and review the global Jarvis context packet and the MH-01…MH-23 domain-packet generation/update procedure.
13. Evaluate pinned component candidates using ARC-023 before any install or PoC; retain the no-install/no-qualification gate until separate authorization.
14. Define the immutable, reproducible deployment bundle, per-profile preflight, health, backup/restore and rollback acceptance evidence.
15. Reconcile the owner’s late-October planning window with real gate evidence; do not transform the calendar intent into a release commitment.
16. Pin per-node OS/build/boot/install/update/recovery profiles under ARC-026; the named Apple hardware does not settle the OS choice.
17. Resolve AG-20/P-20 and ARC-027/V-20: explicitly distinguish the developer Mac Pro from the future production Mac Pro, or approve and evidence a safe role transition.
18. Resolve AG-21/P-21 and ARC-028/V-21 through a source-pointer closure register; preserve historical Audit 01, correct current derivative pointers, and do not promote semantic mapping without owner review.
19. Resolve P-22 / ARC-029 / V-22: record the owner's disposition for the named Trusted Sources Intelligence Engine and approve its scope/owner/contract only if retained. Keep all Batch 09 mappings documentary/open, preserve D-06, and verify any future TSI implementation/qualification separately.
20. Resolve P-23 / ARC-030 / V-23: complete the Local Cluster AI owner/contract disposition, including workload-specific profiles, named MediaHub AI Gateway interface/disposition, failure/retry/revocation behavior and independent acceptance evidence. Preserve the single task-lifecycle-owner rule; do not infer implementation or qualification from the one bounded `MAPPED` row.
21. Resolve P-24 / ARC-031 / V-24: obtain the AI Human Clone owner/scope decision and, if retained, approve clone-specific consent, rights-holder authorization, scope, identity/voice/appearance permission, model/asset provenance, audit/revocation, real/synthetic separation and representation policy. Preserve B1 §17 row B1-17-05 / CDAI4-02 lineage; AHC-19-01 is cross-link-only, and no child ID or canonical promotion is authorized.
22. Resolve P-25 / ARC-032 / V-25: define the B1 two-application boundary against separate Developer Mobile; approve the local Core platform capability matrix, payment/entitlement disposition, Remote Access capability/API/authorization contract and independent acceptance evidence. Preserve working matrix rows 20–21; do not infer implementation or qualification from the four bounded documentary `MAPPED` rows.
23. Resolve P-26 / ARC-033 / V-26: specify and accept the concrete mobile command paths that prevent direct physical-device bypass, preserve the single State Authority and HA Core's scoped authority, use defined MediaHub contracts, and apply authentication/authorization/trust/privacy/audit/revocation. Define the exact Remote Mobile → MediaHub API → Core/State Authority/subsystem chain and its negative/error cases; do not infer conformance from the generic B2 text or four documentary `MAPPED` labels.
24. Resolve P-27 / ARC-034 / V-27: obtain an explicit owner disposition and accepted iPhone Media/AirPlay contract covering supported device/OS profiles, 4K/codec behavior, rights/authorization, network/bandwidth admission, latency/resolution negotiation, degradation/failure behavior and qualification evidence. Review02 adds only bounded generic codec correspondence; do not treat this as acceptance of the AirPlay codec matrix. Preserve `IPHONE-AIRPLAY-4K-01` and matrix row 22; keep Batch 13 provisional and do not promote the matrix/backlog or mint final child IDs.

## 8. Change history

- 2026-10-12 — initial integrated contract draft created from B1/B2, MH-24 report/matrix, domain contracts, component manifest and ASTRA gate sources.
- 2026-10-12 — matrix status corrected in branch; ASTRA internal state semantics clarified without changing authority field values.
- 2026-10-12 — 13-cycle source/contract review performed with separate read-back checks; audit ledger is recorded in MEDIAHUB-OS-13-CYCLE-ARCHITECTURE-AUDIT-01.md after its creation and verification.
- 2026-10-12 — repository tests/qualification/deployment were not run; main was not changed and no merge was performed.
- 2026-10-12 — incorporated the owner-provided Jarvis umbrella direction, single-task-lifecycle rule, hardware trust/profile split, reproducible deployment requirements, public-repository scorecard and MH-01…MH-23 context-packet contract; companion gap report blob SHA b65ddaa2c91b18265cffd7be55fdefc7a0877db5.

**Review coverage limitation:** an initial API tree snapshot at commit `58305d5a9a5b1593f15d2dfb0ff79838c1bddaec` contained 826 entries / 445 Markdown files. A later pre-update branch snapshot at commit `572dfade59961e2e58c9bcaac16d09d996b997b6` contained 846 entries (465 Markdown, 193 Python, 47 YAML and 54 JSON; `truncated=false`). These counts are dated inventory snapshots, not a current-head inventory. The reviewed set includes the governing baselines, key state/security/HA contracts, component-selection artifacts, selected traceability batches, and ASTRA qualification sources. The Batch 01–08 union review verified the structural completeness of 153/153 labels for B1 §§3–6, 12, 15–17; semantic acceptance remains OPEN. Batch 09 Review 03 covers B1 §18 lines 297–309 (17 provisional labels; 3 MAPPED / 13 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT); full TSI acceptance remains OPEN. Batch 10 Reviews 01/02 cover B1 §19 lines 315–328 (19 provisional traceability labels; 5 MAPPED / 13 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT), cross-links the repeated subsystem identity to B1-17-05 / CDAI4-02, and keeps AI Human Clone semantic/owner acceptance OPEN. Batch 11 Reviews 01/02 cover B1 §20 lines 332–359 (9 provisional labels; 4 MAPPED / 5 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT). Review 02 justifies MA-20-05 only as bounded documentary shared-contract/non-authority correspondence; exact two-app scope, one-time purchase model, full capability matrix and Remote Access API remain open. Batch 12 Reviews 01/02 cover B1 §21 lines 361–374 (6 provisional labels; 4 MAPPED / 2 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT). Review 02 confirms mapping distribution unchanged and records the MAI-21-04 change-history correction; the concrete mobile physical-device bypass route and Remote Mobile → API → authority/subsystem chain remain open. Batch 13 Reviews 01/02 cover B1 §22 lines 375–379 (9 provisional labels; current 1 MAPPED / 7 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT; Review01 pre-review 0/8/1/0). Review02 maps only the generic codec/transcoding constraint in B2 §15. The named AirPlay/4K path remains distinct from generic B2 media and capability statements; protocol/profile, rights/authorization, network/performance criteria, owner acceptance and qualification remain OPEN. These scoped reviews are not an all-68-section semantic audit. This was not a line-by-line semantic review of every file or branch, so whole-repository semantic completeness is not claimed.

**Final status:** a source-backed, verifiable working contract for branch review. It is not yet a globally accepted system contract and does not imply that all project documents, runtime functionality or qualifications have been fully verified.

- 2026-10-12 — Normalized the current owner-provided umbrella name to Jarvis (superseding the prior working label Astro), refreshed the gap-report blob reference and pinned the latest read-back passport blob. The legacy gap-report path remains unchanged for provenance.

- 2026-10-12 — Added ARC-026 / V-19 for target OS and install/recovery profile pinning based on B2 §9; updated the current Passport v3 and gap-report blob references. This is an additional source finding after the recorded 13 cycles, not a runtime test or qualification.
- 2026-10-12 — refreshed current source pointers after the read-only GitHub metadata snapshot in the Jarvis gap report (§16): Passport v3 `b25931bf6b88936c110dff6a3217d5edea2fed35`; gap report `406e33a480d195915f7ab8963836066988ee2fd0`. Earlier change-history entries retain the SHA used at their time; no baseline or runtime changed.

- 2026-10-12 — added ARC-027 / V-20 for the unresolved physical-asset identity and role allocation between the developer Mac Pro and the future production Mac Pro. This is a documentary follow-up after the recorded 13 cycles; release admission remains blocked until evidence resolves same-vs-separate asset.

- 2026-10-12 — added ARC-028 / V-21 for a confirmed B1-15-13 → B2 §19 cross-reference error in historical Audit 01; the current working crosswalk points to B2 §§16/18 while preserving audit history. Updated active Gap Reconciliation and Passport v3 source pointers to current read-back SHAs. This post-cycle correction does not amend the 13-cycle ledger and is not a runtime test or qualification.


- 2026-10-12 — refreshed four active Passport v3 source pointers to the read-back SHA `5125a721210c4c1a058fecf534a6a6773a17d569` after correcting P-19's stale Gap Reconciliation reference. Gap Reconciliation remains `fee9977fee0a5efa79ec48c652544d2c4a0d665f`; historical change records are preserved. No baseline or runtime changed.

- 2026-10-12 — refreshed active Gap Reconciliation references to SHA `39720b11e5e6777b86ffd71e0fec1214982e0d95` after reconciling its current finding count to 21, and Passport v3 references to SHA `327089a0780e85a053c3d56c185c22d2e76857ae`. Older source-pointer values in dated history are retained. No B1/B2/main/runtime changes.

- 2026-10-12 — refreshed active Passport v3 refs to current read-back SHA `b504a2e2065bf864578dccd79830c2a58b9099bf` after the P-13 source-pointer correction; historical pointer values are retained in dated entries.

- 2026-10-12 — integrated the bounded TSI semantic result (Batch 09 Review 03 SHA `184a99ef85143c2ad3048dca5c8d85b17f8651a3`) as ARC-029 / V-22, refreshed active Passport pointers, and kept the full TSI contract and semantic acceptance OPEN. B1/B2, matrix, canonical backlog and `main` remain unchanged; no runtime test or qualification was run.

- 2026-10-12 — added ARC-030 / V-23 after Batch07 Review02. B1-16-01 is a bounded documentary mapping only; workload semantics and named-gateway contract remain open. Refreshed active Passport references to current blob `8ec8ed05e3a4f303fb8a93a63c2d77c7defd3fd6`; the immediately preceding active pointer `c844b42f5b98a29ff3d883857fdaf4b0b6873768` remains historical provenance for the prior Passport revision. B1/B2/main, matrix and canonical backlog remain unchanged.

- 2026-10-12 — added ARC-031 / V-24 for the B1 §19 AI Human Clone supplemental crosswalk. Batch 10 Review 01 verified structural/source-anchor consistency (19 provisional labels; 5/13/1/0); clone-specific owner/semantic contract acceptance remains OPEN. Updated active Passport pointers to `040437cbbb9440c30cb7f6dd4f3e451251e1dff6`; B1/B2/main/matrix/canonical backlog unchanged.
- 2026-10-12 — corrected the working inventory after re-reading the current Batch 10 additions: ARC-031 / V-24 are already present, so the count is 31 ARC requirements / 24 verification checks, not 30/23. This is a counter/index correction only; Batch 10 semantic and owner acceptance remain OPEN. Current Passport pointer `040437cbbb9440c30cb7f6dd4f3e451251e1dff6`; the live project map must index the current Passport/Contract/Batch10 state. B1/B2/main/matrix and canonical backlog remain unchanged.
- 2026-10-12 — added Batch 10 Review 02 (`612162b164b7d2585fa9646871839274cec5a343`) to ARC-031 / V-24 evidence pointers. Review 02 confirms the current 5/13/1/0 mapping distribution remains internally consistent, with clone-specific semantic and owner acceptance OPEN. Refreshed active Passport pointer to `97b92bdfe08fecb8b99e96c2b8ff8aa421b44bf3`; preserved `040437cbbb9440c30cb7f6dd4f3e451251e1dff6` in prior dated pointer history. Inventory remains 31 ARC / 24 checks. No baseline, matrix, main or runtime change.

- 2026-10-12 — added ARC-032 / V-25 for B1 §20 Mobile Access after Batch 11 Review 01. The review records 9 provisional labels, 3 MAPPED / 6 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT; exact app-count scope, one-time payment model, complete capabilities and Remote Access API remain OPEN. Current Passport pointer refreshed to `8c905852e5efac71d421653ba1075647807a5de5`. B1/B2/matrix/canonical backlog/main unchanged.

- 2026-10-12 — added ARC-033 / V-26 for B1 §21 Mobile Access Invariants after Batch 12 Review 01. Six provisional rows, 4 MAPPED / 2 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT; concrete physical-device bypass and Remote Mobile API/authority chain remain OPEN. Current Passport pointer refreshed to `306aca30d4757fa6ba835c30354ce7dd02705534`. B1/B2/matrix/canonical backlog/main unchanged.

- 2026-10-12 — integrated Batch 11 semantic Review 02 SHA `c143d1b349bcf2ba3a76ffdad03b1d4258a1ebe9` and working draft SHA `0c102e5071ed5a33cbc02b00872da78eebd5bf9c` into ARC-032/V-25. MA-20-05 is mapped at the abstract documentary level using B2 §2.3 line 72 and §22 lines 438–455; the nine-row distribution is 4/5/0/0. Full Mobile Access scope/owner/contract/implementation/qualification remain OPEN. Companion Passport refreshed to `d190c022a51e4d3129bd33112dbff4e5c7080d97`; Batch 12 / ARC-033 / V-26 remains preserved. No B1/B2/matrix/main/canonical backlog change.

- 2026-10-12 — corrected Markdown punctuation/backtick delimiting in the ARC-033 / V-26 source manifest only. Source paths, SHAs, requirement semantics, mapping statuses and lifecycle states are unchanged; no acceptance or qualification is implied.

- 2026-10-12 — integrated Batch 12 semantic Review 02 SHA `f8d50509014f8c72476ab845476dcc40569c3357` and corrected draft SHA `dcbc0a0e8a8186e926315ea318eff902e491f0e7` into ARC-033/V-26. Mapping remains 4/2/0/0. Review 02 keeps direct-device bypass and exact mobile API/authority chain OPEN and records MAI-21-04 field-value correction only. Companion Passport refreshed to `3cabf4d68d19423ac4bf21b09f3483783155cf20`. Batch 11, B1/B2/matrix/canonical backlog/main unchanged.

- 2026-10-12 — added ARC-034 / V-27 for B1 §22 iPhone Media / AirPlay after Batch 13 Review 01. Nine provisional labels have distribution 0/8/1/0; generic B2 media/phone/4K language is not treated as AirPlay acceptance. Refreshed the active Passport pointer to `a4337a2f4ae68c36b01ed3420d15929f83fa6483`; owner/contract, interoperability and qualification gates remain OPEN. B1/B2, matrix, canonical backlog and `main` unchanged.

- 2026-10-12 — integrated Batch 13 Review02 SHA `36f171bf4ef6e9bec388cacc5ddc4ff8989d168e` and current draft SHA `2f05bcf0b67200e44aaec7ba4e3a3164238270bf` into ARC-034 / V-27. Current distribution is 1/7/1/0; the earlier Review01 0/8/1/0 snapshot is preserved. Only generic codec handling is mapped; AT-15 remains OPEN—OWNER DECISION, and AirPlay/4K interoperability, supported profile, rights/authorization, network/performance, implementation and qualification remain OPEN. Companion Passport refreshed to `d4b742ea5e55ae23472cb285bf39bc29cbbb359c`; B1/B2/matrix/canonical backlog/main unchanged.
