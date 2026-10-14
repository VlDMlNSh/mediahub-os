# MediaHub — owner decision packet: developer-fabric architecture closure 01

- Date: 2026-10-13
- Repository: `VlDMlNSh/mediahub-os`
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **OWNER DECISION PACKET / PROPOSED / NOT ACCEPTED / NOT FROZEN**
- Scope: Contour A only. This packet consolidates existing DEC-DEV-01…DEC-DEV-08; it does not create new decision IDs, alter Baseline 2.0, authorize implementation, or qualify any runtime.
- Sequence authority: [Master Development Roadmap 1.0](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md).
- Supporting crosswalk: [Node/service placement matrix and decision register 01](MEDIAHUB-NODE-SERVICE-PLACEMENT-AND-DECISION-REGISTER-01.md).

## 1. Source evidence read for this packet

| Source | Ref | Live blob SHA | Relevant finding / limit |
|---|---|---|---|
| `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` | `main` | `e549692f207fbc91d9b9b9b92b8e665404f07290` | Accepted target topology; Mac Pro central node; Alamo local inference endpoint; runtime/protocol/model are deployment facts to discover; local-only mode must fail closed. |
| `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` | `main` | `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Component selection closed, implementation open, production admission qualification-gated; ONNX Runtime and llama.cpp are target-gated candidates. |
| `docs/architecture/MH-15-os-appliance-architecture.md` | `main` | `f817925c69ce4484713f952e47aacad283af8eeb` | MH-15 work in progress; acceptance/freeze not authorized and implementation authorization absent; exact legacy hardware profile remains unknown. |
| `docs/architecture/MH-15-acceptance-criteria.md` | `main` | `082642e67dc66cb359a5566773c143854cafaa00` | Hardware, OS, network, security, recovery, resources and evidence gates remain mandatory. |
| `docs/architecture/MH-16-installer-recovery-update-architecture.md` | `main` | `f3ad2401f00a4062b39eed640e0c5c5f70064312` | Proposed/not frozen/not authorized; installer/update/migration/recovery do not become State Authority. |
| `docs/architecture/MH-16-master-prompt.md` | `main` | `62924d4686aa3f55fce442a3c4bab66c82ae19e5` | Governance handoff preserves lifecycle/security boundaries; implementation not authorized. |
| `docs/architecture/MH-12-security-architecture.md` | `main` | `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Explicit identity/authentication/trust/capability/authorization/policy path; reachability is not authorization. |
| `docs/architecture/MH-12-security-invariants.md` | `main` | `0609be9c3420070434014dad4529e4ccd46b0996` | Proposed invariants include sole State Authority, fail-closed ambiguity, revocation and no trust-by-network. |
| `docs/architecture/MH-21-hybrid-cloud-distributed-ai.md` | `main` | `a76f6b35ec31d6b8fff2b0a3e8a1fd22bdbec71c` | Architecture work authorized but not accepted/frozen; external compute is not authority; placement is policy-driven. |
| `docs/architecture/MH-21-acceptance-criteria.md` | `main` | `582f898fe4be332b6a7fef3e8cca2e27c7328ac2` | MH-21 acceptance criteria not satisfied; trust, egress, provider/model, privacy, isolation and qualification evidence remain required. |
| `docs/architecture/MH-21-provider-contract.md` | `main` | `d2bf7e29eee9ff2e07f4e25bf58229df11ff3cda` | Provider contract source exists; this pass does not assert provider admission or compatibility. |
| `docs/architecture/MH-21-external-compute-contract.md` | `main` | `b2127d6085cdbfcd98d2f819fa3ea5d12ffee68f` | External compute is bounded and subordinate; admission and evidence remain required. |
| `docs/checkpoints/mediahub-unified-architecture-and-deployment-contract-v0.1.md` | `docs/mediahub-chat-tree-map-20261012` | `1057776ca9192b307a4e6de72db5d12cdbcc1a39` | Proposed draft records a local Ollama direction; not accepted/frozen and not evidence of deployment. |
| `docs/checkpoints/MEDIAHUB-NODE-SERVICE-PLACEMENT-AND-DECISION-REGISTER-01.md` | `docs/mediahub-chat-tree-map-20261012` | `39e9ec183988c9caee5eb7ab0128bf4c71ffaa39` | Existing source-anchored placement baseline and DEC-DEV-01…08 conflict register; do not repeat it as a new artifact. |
| `docs/checkpoints/mediahub-unified-system-traceability-matrix-v0.1.md` | `docs/mediahub-chat-tree-map-20261012` | `9af75da0b1383a51bb95cb3cd5dd62bf22b571f7` | Large working cross-domain traceability draft; not accepted/frozen. |
| `docs/checkpoints/MEDIAHUB-OS-SYSTEM-PASSPORT-V3.md` | `docs/mediahub-chat-tree-map-20261012` | `467aedfc655db966597f564f4bf3074185aca6e9` | Working integrated passport; not canonical replacement for Baseline 2.0. |

Blob SHA values are live read-time provenance snapshots, not immutable aliases for future reads. Refresh them on the next pass.

## 2. Decision summary for the owner

| ID | Decision needed | Options | Recommendation (not a decision) | Consequence if deferred |
|---|---|---|---|---|
| DEC-DEV-01 | Define whether Alamo is an endpoint/service label or a specific runtime, and how Ollama, ONNX Runtime and llama.cpp compose. | A. Alamo endpoint with one or more explicitly selected runtime adapters. B. Select one runtime as endpoint implementation. C. Defer composition until host/model constraints are known. | Keep Alamo as the target endpoint/service label; defer runtime composition until the owner approves a diagram and compatibility evidence exists. Do not install or invoke anything. | Local inference implementation cannot be specified or admitted; this is not a blocker to documentary crosswalk work. |
| DEC-DEV-02 | Assign one authoritative owner for engineering queue/claim/lease/retry/cancel/evidence-promotion lifecycle across Jarvis and ASTRA. | A. Jarvis owns lifecycle, ASTRA is execution/qualification adapter. B. ASTRA owns a bounded lifecycle delegated by Jarvis. C. Split only into explicitly disjoint lifecycle domains. | Prefer one owner with a typed delegation/adapter boundary; decide only after existing ASTRA contracts are reconciled. | Duplicate lease/retry/promotion authority risks inconsistent state; runtime implementation remains blocked. |
| DEC-DEV-03 | Decide whether a future production Mac Pro is the same physical asset as the developer Mac Pro. | A. Controlled role transition of same asset. B. Separate production asset. | Keep asset identities separate in all contracts until an explicit decision. | No production placement or role transition may be assumed. |
| DEC-DEV-04 | Define allowed workload for Mac mini Server 2011. | A. Optional documentation/low-risk worker after compatibility evidence. B. Exclude from critical path. C. Retire if unsupported. | Keep optional and out of critical dependencies until exact hardware, OS support, security lifecycle and workload evidence exist. | No critical service can be assigned based only on the 16 GB report or model year. |
| DEC-DEV-05 | Define provider/data-class routing and fallback policy. | A. Local-only for restricted data. B. Explicit per-task route policy. C. Deny external providers for specified classes. | Default-deny external egress; make provider, data class, purpose, retention, authorization and fallback explicit and auditable. | MH-21 remains unaccepted/not production-ready; no silent fallback. |
| DEC-DEV-06 | Define Developer Mobile identity, API scopes, operation authorization, revocation and lost-device behavior. | A. Narrow authenticated operation APIs. B. Separate privileged workflow with explicit approvals. | Start with per-device identity, narrowly scoped APIs, immediate revocation and audit; no generic shell/admin surface by default. | Mobile acceptance remains blocked; mesh reachability is not authorization. |
| DEC-DEV-07 | Define future owned GPU/video server workload and capability envelope. | A. Workload/profile first, then hardware. B. Hardware first, then constrain workload. | Specify privacy, capacity, performance, availability, network, isolation and recovery requirements before selecting hardware. | Hardware choice risks mismatch; server remains optional and unselected. |
| DEC-DEV-08 | Define the exact evidence and approval package required to unlock Contour B. | A. Independent Contour A qualification + explicit owner acceptance. B. Begin product implementation earlier. | Preserve the gate: only begin Contour B after Contour A is deployed, independently qualified and explicitly accepted with exact-SHA evidence. | Contour B remains blocked by the project invariant. |

## 3. Dependency order and closure protocol

1. **Documentary closure first:** reconcile exact source clauses, live refs/SHA and contradictions; update traceability only where the sources support it.
2. **Owner decisions:** DEC-DEV-01 and DEC-DEV-02 define runtime/lifecycle composition; DEC-DEV-03/04/07 constrain physical placement; DEC-DEV-05/06 constrain provider/mobile security; DEC-DEV-08 preserves the Contour A → Contour B gate.
3. **Evidence design:** turn accepted owner decisions into ADRs/contracts, measurable acceptance criteria and evidence schemas. A decision is not implementation evidence.
4. **Implementation authorization:** separately gated by the applicable MH-15/MH-16/MH-21 governance and the owner's explicit permission.
5. **Verification/qualification/release/deployment/acceptance:** remain distinct stages and require their own evidence. This packet itself executes none of them.

## 4. Stable invariants

- Baseline 2.0 remains the canonical accepted functional reference; Baseline 1.0 remains historical provenance.
- Product State Authority is separate from Jarvis/ASTRA engineering workflow state.
- Home Assistant Core remains the Smart Home authority within its accepted scope.
- AI, cloud, provider, tools, adapters, queues, persistence, graph/search and observability do not become product State Authority.
- Network reachability, VPN/mesh membership, authentication, capability, authorization and trust are distinct.
- Local-only mode fails closed; no implicit local/cloud/provider fallback.
- Contour B is not started before Contour A deployment and independent acceptance.
- No implementation, test, qualification, provider/model call, credential use, host/runtime inspection, deployment or infrastructure change is authorized by this packet.

## 5. Next executable documentary step

Use this packet as the owner-decision interface. Before asking for a decision, continue independent documentary work by verifying each DEC-DEV row against its exact primary clauses and source status, and identify any decision that can be eliminated by existing accepted evidence. Then present only the irreducible owner choices. Do not re-create the placement inventory or promote any draft to canonical status.


## 6. Crosswalk validation and owner-question triage (2026-10-13)

**Purpose:** remove questions already answered by accepted source or binding owner instruction, without silently closing unresolved decisions. This section supersedes the broad wording in §2 where the status below is more precise. Historical IDs remain unchanged.

### 6.1 Decision disposition

| ID | Exact source anchor | Finding established by source | Current disposition | Ask owner now? |
|---|---|---|---|---|
| DEC-DEV-01 | Distributed AI Infrastructure `main` blob `e549692f207fbc91d9b9b9b92b8e665404f07290`, §1 item 5 and §2; Component Manifest 2.0 `main` blob `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`, §4; proposed Unified Architecture/Deployment Contract on docs ref blob `1057776ca9192b307a4e6de72db5d12cdbcc1a39`, §4.1. | Alamo is already defined as a **local inference endpoint**; its runtime, protocol, model and exact endpoint are deployment facts to discover. Manifest lists ONNX Runtime and llama.cpp as target-gated candidates; a proposed draft points to Ollama but is not accepted. | The endpoint label is **answered**. Runtime/adapter composition remains **OPEN / TARGET-GATED**. Preserve DEC-DEV-01 for the unresolved composition only. | Not until documentary compatibility/source review narrows the actual options; do not ask whether Alamo is an endpoint again. |
| DEC-DEV-02 | ASTRA GOLD Unified System `main` blob `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` §§3, 6–7; Complete Component Scheme `main` blob `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1` §§1–3; Governance Contract `main` blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`; Jarvis Verifiable Architecture Contract `docs/mediahub-chat-tree-map-20261012` blob `c248956417cc61d66c968a4c58a56e799f653354` ARC-003/017/018; independent review blob `022f1bd881906d4ab837b2f46c091c43546fce14` §3 item 9; current truth `main` blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`. | ASTRA sources assign A0 queue/claim/lease/scheduling/control state; Jarvis ARC-018 says one lifecycle owner must be selected and the independent review still marks it OPEN. More critically, the Complete Component Scheme says “A0-ASTRA = ... MediaHub State Authority”, conflicting with ARC-003 and the product authority invariant. ASTRA Current Truth is NOT_PROVEN / BLOCKED, with G0–G11 BLOCKED. | **OPEN_CONFLICT — owner/governance reconciliation required.** Distinguish ASTRA engineering workflow state from MediaHub Product State Authority; do not silently amend either primary source or infer that Jarvis already owns/has implemented the lifecycle. | Not yet: evidence is sufficient to identify the contradiction. Present the exact conflicting clauses and proposed bounded reconciliation when a governance decision is needed; continue independent P0-07 documentary work. |
| DEC-DEV-03 | Master Roadmap §2 and §5; Passport v3 asset allocation gap; Verifiable Architecture Contract 01 ARC-009 (indexed in map). | Existing sources do not establish that the developer Mac Pro and future production Mac Pro are the same physical asset. | **OPEN — genuine owner decision**, but not needed to close current documentary crosswalk; keep identities separate meanwhile. | Defer until production asset/role transition becomes an active dependency. |
| DEC-DEV-04 | Distributed AI Infrastructure scope/§2; MH-15 architecture `main` blob `f817925c69ce4484713f952e47aacad283af8eeb`; MH-15 criteria `main` blob `082642e67dc66cb359a5566773c143854cafaa00`. | MH-15 is work in progress; acceptance/freeze/implementation authorization are absent; exact hardware, OS lifecycle, thermal/resource envelope and compatibility evidence are not established. | **EVIDENCE-GATED / OWNER CHOICE DEFERRED**. No workload can be made critical from model year or reported RAM alone. | Not yet; source/compatibility evidence first, then decide allowed workload. |
| DEC-DEV-05 | Distributed AI Infrastructure §§1, 4, 6 and §8; MH-21 `main` blob `a76f6b35ec31d6b8fff2b0a3e8a1fd22bdbec71c`; MH-21 criteria `main` blob `582f898fe4be332b6a7fef3e8cca2e27c7328ac2`. | Local-only must not silently fall back to cloud; MH-21 requires explicit policy-driven placement and evidence-backed egress/classification/provider/retention/security. MH-21 is not accepted/frozen/production ready. | **INVARIANT ESTABLISHED; ROUTING POLICY OPEN**. Do not ask whether silent fallback is allowed; it is not. Provider/data-class matrix and route-specific evidence remain open. | Not for the invariant; later only for irreducible data-class/provider policy choices. |
| DEC-DEV-06 | MH-12 Security Architecture `main` blob `cf4ebfd5bf471ca676f075c51d3a24906504e490`, §7 Trust and §§13–14; Distributed AI Infrastructure §6; MH-12 Security Invariants `main` blob `0609be9c3420070434014dad4529e4ccd46b0996`. | Reachability/VPN/mesh does not automatically establish trust or authorization; authentication, identity, capability and authorization are distinct. | **INVARIANT ESTABLISHED; MOBILE CONTRACT OPEN**. Device identity, API scopes, revocation/lost-device behavior and audit still need a specific contract. | Not for the invariant; ask only after an API/operation inventory is mapped. |
| DEC-DEV-07 | Distributed AI Infrastructure §§2, 5–8; MH-21 placement/acceptance; Master Roadmap Phase 02/04/06. | Future owned GPU server is a target capacity extension; no hardware model or admitted workload profile is selected. Component admission requires qualification and reproducible evidence. | **PROFILE-FIRST RECOMMENDATION; OWNER HARDWARE CHOICE DEFERRED**. Define capacity/privacy/performance/isolation/recovery envelope before choosing hardware. | Not yet; derive workload envelope and acceptance measures first. |
| DEC-DEV-08 | Binding project Bootstrap instruction, architecture gate rule; Master Roadmap Phase 09–10. | The project instruction already forbids starting Contour B before Contour A is deployed and independently accepted. Roadmap Phase 10 likewise requires deployment and acceptance to be explicitly evidenced. | **GATE ESTABLISHED — NOT AN OPEN DISCRETIONARY DECISION**. Preserve historical ID as a gate/evidence tracker. The evidence bundle, independent result and explicit acceptance record remain unproven and required. | No. Do not re-ask whether the gate should apply. Ask only if a concrete evidence/acceptance record is ambiguous. |

### 6.2 Minimum unresolved decision set

After this source crosswalk, do not present eight equal-weight questions to the owner. The irreducible architecture decisions are currently:

1. **DEC-DEV-02 — Jarvis/ASTRA lifecycle authority**, after exact existing lifecycle contracts and failure semantics are reconciled.
2. **DEC-DEV-01 — runtime/adapter composition**, after documentary compatibility and target-gated status review.
3. **DEC-DEV-05 — provider/data-class routing**, only for specific policy choices not already settled by fail-closed/no-silent-fallback invariants.
4. **DEC-DEV-06 — Developer Mobile operation/API scopes**, only after an operation inventory and threat boundary are mapped.
5. **DEC-DEV-03 / DEC-DEV-04 / DEC-DEV-07** are deferred decisions gated by asset, hardware/OS or workload evidence; do not interrupt current documentary work to ask them prematurely.
6. **DEC-DEV-08** is no longer an owner choice. The Contour A → Contour B gate is binding; its evidence and acceptance remain outstanding.

### 6.3 Closure semantics

- “Answered” closes only the sub-question directly established by the source; it does not close the historical ID if a distinct sub-question remains.
- “Invariant established” does not imply runtime implementation or qualification.
- “Deferred” is not “accepted”; it means evidence/dependencies should be completed before asking the owner.
- No DEC-DEV identifier is deleted or reused.
- No implementation, tests, qualification, provider/model invocation, credential use, host/runtime inspection, infrastructure change or deployment is authorized by this crosswalk.


### 6.4 DEC-DEV-02 — exact ASTRA/Jarvis lifecycle and authority conflict

The source review narrows the conflict; it does not close it:

1. `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` (`main`, blob `e2067dc41b52983fc4e0b2549fb6af3c099cbc60`, status **CANONICAL / QUALIFICATION-READY DESIGN**) identifies A0 ASTRA as the coordination/state controller and describes queue → claim → lease → dispatch → result → recovery lifecycle (§§2, 3, 6–7).
2. `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md` (`main`, blob `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`, status **CANONICAL ARCHITECTURAL RECONCILIATION / QUALIFICATION INVENTORY**) explicitly states “A0-ASTRA = single coordination and MediaHub State Authority” (§1), while its component table assigns A0 decomposition, claims, scheduling, integration, reconciliation and state (§3).
3. `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` (`main`, blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`, status `CANONICAL_GOVERNANCE_SOURCE`) defines qualification gates and requires missing evidence to remain blocked; it does not make the ASTRA engineering queue a product-state authority.
4. `MEDIAHUB-OS-VERIFIABLE-ARCHITECTURE-CONTRACT-01.md` (`docs/mediahub-chat-tree-map-20261012`, blob `c248956417cc61d66c968a4c58a56e799f653354`) ARC-003 says A0-ASTRA owns ASTRA queue/claim/lease/evidence/gate state only, never MediaHub Product State Authority; ARC-017 frames Jarvis as umbrella and ASTRA as bounded subsystem; ARC-018 requires one engineering lifecycle owner to be selected before implementation.
5. `MEDIAHUB-JARVIS-BUNDLE-INDEPENDENT-REVIEW-01.md` (blob `022f1bd881906d4ab837b2f46c091c43546fce14`) confirms the lifecycle owner remains open; `docs/qualification/CURRENT-TRUTH.generated.md` (`main`, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`) says overall `NOT_PROVEN / BLOCKED`, all G0–G11 blocked.

**Bounded conclusion:** the ASTRA design describes A0 as owner of ASTRA's internal engineering queue/control lifecycle, but the repository also contains a direct product-authority wording conflict and the Jarvis integration contract says lifecycle-owner selection remains open. The safe invariant is that ASTRA may own its engineering workflow state only; it cannot be MediaHub Product State Authority. Whether the existing A0 lifecycle is the admitted single engineering-task owner under Jarvis, and what adapter/delegation boundary Jarvis uses, remains an explicit governance/architecture reconciliation.

**Do not** edit the ASTRA primary documents, rename A0, select a second queue, or claim runtime readiness during this pass. Keep ASTRA Current Truth `NOT_PROVEN / BLOCKED`. The next independent documentary track is the existing P0-07 → P0-05 context/authorization bridge, using the canonical-read trace and existing D1/D2/D4 directions; return to the lifecycle decision with an exact clause-level conflict sheet if it blocks a later implementation authorization.


### 6.5 Minimal owner question — DEC-DEV-02 (2026-10-13)

**Only immediate owner/governance question from the DEC-DEV crosswalk validation.** The other existing IDs are either partially answered, constrained by an established invariant, or deferred until evidence prerequisites are available. No ID is created, deleted or renumbered.

> For existing DEC-DEV-02, which engineering lifecycle model do you approve?
>
> - **A — Jarvis owns the cross-system task lifecycle; ASTRA is a bounded execution/qualification adapter.**
> - **B — ASTRA owns a bounded engineering lifecycle explicitly delegated by Jarvis, with a typed delegation/adapter contract.**
> - **C — Jarvis and ASTRA retain strictly disjoint lifecycle domains, with no duplicate queue/claim/lease/retry/evidence-promotion authority.**
>
> Separately, confirm the scope of the Complete Component Scheme's phrase “MediaHub State Authority” for A0-ASTRA. The non-negotiable product boundary is that ASTRA engineering workflow state is **not** MediaHub Product State Authority. If the phrase was intended to grant A0 product-state authority, provide the explicit governed scope; do not infer it.

**Recommendation (not an owner decision):** retain A0 as owner of ASTRA-internal workflow state only; select the single cross-system lifecycle owner only after the phrase conflict is resolved and a typed lifecycle/delegation contract is reviewed. No implementation begins until the decision and contract are accepted through the applicable governance process.

**Deferred—not asked now:** DEC-DEV-01 runtime composition until documentary compatibility narrows options; DEC-DEV-03 until a concrete asset/role-transition plan; DEC-DEV-04 until exact hardware/OS/security/workload evidence; DEC-DEV-05 until route/data-class inventory yields irreducible provider policy choices; DEC-DEV-06 until Developer Mobile operation/API inventory exists; DEC-DEV-07 until a quantified workload envelope exists. DEC-DEV-08 remains a binding Contour A → Contour B gate, not an optional owner decision.

## 7. Supplemental project-wide integrity sweep and administrative response block (2026-10-14)

- Broad audit: [MediaHub OS — project-wide architecture integrity sweep wave 06](MEDIAHUB-PROJECT-WIDE-ARCHITECTURE-INTEGRITY-WAVE-06-2026-10-14.md), latest reviewed report blob `62a2715db8dd4555946fa05b26f15ece734def79`.
- The existing DEC-DEV-02 owner question in §6.5 remains the authoritative question in this packet; wave 06 does not replace the prior owner-recorded directions or create a new DEC-DEV ID.
- For ready-to-answer options and evidence anchors, see report §9. ADMIN-01 elaborates DEC-DEV-02; ADMIN-02 concerns commissioning an actual qualified independent P0-07 D2 reviewer; ADMIN-03 asks for governed clarification of ASTRA design-status/version semantics; ADMIN-04 requests the change-control route for main-vs-documentation branch wording.
- The report's P0-07 review/status question is cross-cutting and does not extend this packet's Contour A scope or imply permission to start Contour B.
- Recommendations in the report are **not** recorded owner decisions. Existing P0-05 D1–D7 directions, including D6 defer-for-evidence, remain in force. No contract status, implementation, qualification, or deployment was accepted or authorized by this addendum.
