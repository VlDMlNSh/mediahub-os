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
| DEC-DEV-02 | Distributed AI Infrastructure §3; Passport v3 Section 13; Verifiable Architecture Contract 01 ARC-003 (source paths indexed by the map); existing placement matrix §5, NSP-SVC-02 and NSP-TR-04. | Jarvis is the umbrella orchestration concept and ASTRA a bounded engineering execution/queue/evidence subsystem; none of these sources proves a single accepted lifecycle owner for queue, lease, retry, cancellation and evidence promotion. | **OPEN — genuine owner/contract decision**, dependent on reconciliation of existing ASTRA lifecycle contracts. | Yes, but after independent source reconciliation identifies irreducible alternatives. |
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
