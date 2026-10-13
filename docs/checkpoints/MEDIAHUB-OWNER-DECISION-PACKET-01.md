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
