# MediaHub OS — Jarvis Corporation Architecture Proposal Crosswalk, Wave 01

- Date: 2026-10-15
- Status: OWNER-SUPPLIED PROPOSAL RECONCILIATION / PARTIAL COVERAGE / NOT ACCEPTED AS NEW NORMATIVE CONTRACT / NOT IMPLEMENTED / NOT QUALIFIED
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Functional authority: accepted Functional Baseline 2.0 on `main`; Baseline 1.0 remains historical.
- Purpose: reconcile the two owner-supplied architecture messages with current repository sources, record overlaps/gaps/conflicts and preserve the proposals as proposals. This document does not approve a new architecture, select implementations, grant permissions, or qualify runtime behavior.
- **Wave 364 identity correction (2026-10-22): Alamo is hosted on `Voktors-Mini.Dlink` (Mac mini 2018, macOS), which the owner identifies as the central-infrastructure host as well. Runtime/API/provider qualification remains open; this is a host-identity correction only.**

## 1. Executive finding

The proposals are **partially synchronized already**. The repository already contains a target distributed AI architecture, a Claude Code/FCC/local-Alamo and cloud-provider routing design, separate Codex cloud path, Jarvis/ASTRA authority boundaries, local-only fail-closed behavior, component identity constraints, and a proposed Jarvis Control Plane/GitHub Adapter contract.

The supplied messages add a broader corporation framing: six logical planes; formal agent profiles; a policy-based task router selecting an executor rather than just a model; task-graph/DAG decomposition; structured task results; independent verification; a multi-node Claude Code presence goal; Everything Claude Code (ECC) as a candidate reuse source; and future user-contributed compute. These ideas are not all present as one accepted, complete, machine-verifiable contract. They should be reconciled with existing contracts before normative edits or implementation.

## 2. Proposal-to-source crosswalk

| Proposed element | Existing evidence | Status | Gap / guardrail |
|---|---|---|---|
| Jarvis is corporation-level controller, not the sole executor | Current map §20.256 and §20.262; owner direction D-03 in roadmap; Jarvis adapter draft §§1–3 | OWNER-DIRECTED TARGET / unified contract still draft | Define interfaces and lifecycle ownership without giving Jarvis direct write authority over ASTRA queue/claim/lease/gate internals or Product State Authority. |
| Local LLM performs bounded autonomous decisions | Distributed AI architecture and provider/egress crosswalk support local Alamo route and policy-controlled selection | TARGET DIRECTION / actual runtime/model not pinned | Specify allowed decision classes, data policy, capability checks, fallback rules and evidence; local model output never grants authority. |
| Claude Code is an engineering executor under local controller | Distributed architecture §§1–4; map §20.256; inventory confirms CLI presence on two observed nodes, but not route execution | TARGET DESIGN / CLI PRESENCE ONLY | Distinguish Claude Code client/tool from Claude model/provider. Route and authentication must be evidenced per task. |
| Claude Code available on Mac mini 2018, Mac mini/Linux and MacBook | Inventory Wave 02 reports CLI versions on two online nodes; distributed architecture identifies Mac mini 2018, Mac mini worker and MacBook clients | PARTIAL INVENTORY / MacBook NOT VERIFIED HERE | No installation or host inspection in this pass. Presence on each named device remains a deployment fact, not an assumption. |
| Claude official cloud route and local model backend route are separate configurations | Distributed architecture and crosswalk separate Claude Code → FCC → Alamo and/or FreeLLMAPI, with Codex on a separate cloud path; local-only is fail-closed | TARGET ROUTE SEPARATION / exact FCC mapping open | Preserve distinct modes: (A) official Anthropic-backed route; (B) compatible gateway to a local backend; (C) native local LLM executor; (D) other admitted providers. Do not imply local backend is Claude. Verify compatibility against pinned versions before claiming support. |
| One dispatcher chooses the executor per task | Jarvis draft §5–6 requires per-task immutable routing record and eligible executor route | DRAFT PARTIAL COVERAGE | Formalize route eligibility by capabilities, data class/egress, availability, resources, cost/quota, latency, permissions, verification policy and user approval. No eligible route => hold/fail, not false success. |
| Agent Registry with stable IDs, capabilities, location, permissions, resource requirements, availability and verification policy | Existing agent/provider registries and component inventory; crosswalk notes identities are distinct | PARTIAL / schema alignment gap | Separate configured, observed-present, available, tested and qualified statuses. Define schema and evidence freshness; registration is not proof of availability. |
| Six planes: control, registry, router, execution, verification, policy/security | Existing architecture distributes these responsibilities across documents; no single accepted six-plane contract found in checked sources | PROPOSAL / NOT ACCEPTED | Treat as logical planes, not a mandatory count of services. Map each responsibility to existing authority and avoid duplicate controllers. |
| Task decomposition into DAG, parallel execution and dependency tracking | Existing queue/dispatch/qualification mechanisms are documented; the checked Jarvis adapter draft does not define a full corporation-wide task DAG contract | GAP / PROPOSAL | Define task identity, dependency edges, idempotency, cancellation, leases, retry bounds, conflict handling and integration gates before scaling parallelism. Existing concurrency conflicts elsewhere in the map remain governed by their own source contracts. |
| Structured task results and provenance | Jarvis draft requires immutable per-task route and evidence; component evidence record schema exists | PARTIAL COVERAGE | Standardize result envelope: task ID, input/contract revision, executor and route, artifacts/digests, dependencies, checks, limitations, terminal status and verifier. Never embed secrets. |
| Independent verification and lifecycle distinctions | Baseline/governance and Jarvis draft require evidence and distinct lifecycle gates | EXISTING PRINCIPLE / end-to-end implementation unproven | Keep prepared, executed, verified, passed, accepted, implemented, qualified, released and deployed distinct. Executor cannot self-approve. |
| ECC / Everything Claude Code reuse | No ECC-specific assessment or accepted dependency was found in the checked map, roadmap, distributed architecture, inventory, crosswalk or Jarvis draft | NOT ASSESSED / NOT ADOPTED | Source-only review of upstream repository, pinned version, license, provenance, agents/skills/hooks/rules/MCP configs, side effects, permissions and overlap with existing MediaHub contracts before recommendation. Do not install or import components in this pass. |
| Provider Gateway and multiple legitimate provider credentials | Existing provider registry, route evidence and egress crosswalk | PARTIAL / provider identity conflict open | Model logical provider/model/resource availability, quota, policy and credential references; do not read secrets or implement account/key rotation to bypass provider limits. |
| User-contributed MediaHub compute | Distributed architecture identifies future user-contributed compute as a possible pool subject to explicit trust boundary; prior map synthesis treats it as future opt-in only | FUTURE DESIGN / NOT IMPLEMENTED OR APPROVED | Requires explicit opt-in, least privilege, isolation, data minimization, caps, revocation, provenance and result verification. Treat nodes as untrusted; no default connection or access to internal infrastructure. |
| Secure network APIs for control/model/execution | Distributed architecture includes authenticated private API and separate permission boundaries | TARGET DESIGN / endpoint and implementation not qualified | Control API, Model Gateway and Execution API may be logical interfaces, not necessarily three servers. Define client auth, per-operation authorization, replay/idempotency, revocation, rate/resource limits and secret-free audit. IP:port is transport, not authentication. |
| Local-first routing | Distributed architecture and crosswalk require local-only fail-closed; cloud route only when approved | ACCEPTED TARGET INVARIANT / runtime enforcement not proven | Do not require every task to call local model first; choose an eligible route by policy. No silent cloud fallback in local-only mode. |
| Contour A before Contour B | Master roadmap §0 and map explicitly preserve sequential gating | OWNER-DIRECTED MASTER PLAN | No product Contour B development before Contour A deployment and independent acceptance. Installing Claude Code or having multiple agents does not satisfy that gate. |

## 3. Key reconciliation notes

### 3.1 Claude Code is not the model

The architecture must keep separate identities for:
- Claude Code client/tooling and its local execution environment;
- the model/provider serving a request;
- FCC and any gateway/router;
- Alamo as the intended local inference endpoint;
- Ollama or another runtime, whose relationship to Alamo remains unproven;
- Codex and its separate cloud-authenticated path.

A Claude Code CLI on a node does not prove which backend serves it, whether its route is local, or whether the route is qualified. A compatible local backend would be a local model accessed through a supported or compatible interface, not “Claude running locally.”

### 3.2 Node placement is a target, not observed deployment

The proposal names Mac mini 2018, Mac mini 2011/Linux, MacBook and mobile clients. Existing distributed architecture describes the Mac mini 2018 as central target, Mac mini as worker and MacBook as client; the owner has clarified that Alamo itself is hosted on Voktors-Mini.Dlink. Wave 02 inventory only reports two online nodes in that bounded inventory and CLI observations for two nodes; it does not establish the proposed complete three-computer deployment. The MacBook presence/configuration is not verified by this pass.

### 3.3 No architectural authority is added by this crosswalk

This document does not resolve the open Jarvis-vs-ASTRA lifecycle ownership question, FreeLLMAPI local-gateway/cloud-upstream conflict, FCC implementation mapping, Alamo runtime/API identity, or route/provider provenance. Alamo's host identity is now owner-confirmed as Voktors-Mini.Dlink; runtime qualification and route/provider provenance remain open and governed by their source contracts and owner/governance decisions.

## 4. Source anchors reviewed

1. `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md@main`, blob `e549692f207fbc91d9b9b9b92b8e665404f07290` — target topology, Alamo endpoint, FCC, Codex separate cloud path, local-only semantics, node roles and future compute pools.
2. `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md@docs/mediahub-chat-tree-map-20261012`, blob `084691d73a814c8da520a4648ba27a65e3739c54` — §20.256 Claude Code/FCC/FreeLLMAPI/local Ollama correction; §§20.262–20.263 current chat-to-repository sync records; prior Contour and authority reconciliations.
3. `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md@docs/mediahub-chat-tree-map-20261012`, blob `e112cc73178eef5f71b8a814296e4902c2e80390` — authority boundaries, route records, fail-closed behavior, open G3/G4 gates.
4. `docs/checkpoints/MEDIAHUB-PROVIDER-IDENTITY-AND-EGRESS-CONTRACT-CROSSWALK-WAVE-05-2026-10-14.md@docs/mediahub-chat-tree-map-20261012`, blob `01b22130e8b5de49782a7241ec14331016259de0` — FreeLLMAPI conflict, FCC mapping and provider identity/evidence requirements.
5. `docs/checkpoints/MEDIAHUB-UNIFIED-LOCAL-INVENTORY-AND-VERIFIABLE-COMPONENT-MATRIX-WAVE-02-2026-10-14.md@docs/mediahub-chat-tree-map-20261012`, blob `4d239780af2367fdecd00e7156521934ef2f8114` — bounded node observations, CLI presence, model tags and identity gaps.
6. `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md@docs/mediahub-chat-tree-map-20261012`, blob `d70a6654d4ce1850369b0431c4e35de2aa0af36a` — master sequencing and Contour A/B gate.

## 5. Restrictions and evidence boundary

This pass was documentary/source-only. No models or external providers were invoked; no credentials were accessed; no host/runtime inspection, installation, tests, qualification, configuration or infrastructure changes, deployment, merge, rebase or cherry-pick occurred. No ECC component is installed, integrated, approved or qualified by this report.

## 6. Next bounded work

1. Reconcile the existing Jarvis draft, distributed architecture and agent/provider registries into a responsibility/interface matrix without rewriting normative contracts.
2. Identify whether an existing schema/contract already covers agent profiles, task DAG/dependencies, structured results and independent verification; record exact file/section/SHA before proposing new schema.
3. Perform source-only upstream review of ECC and compare its candidate components against identified gaps; do not install.
4. Continue resolving existing route identity evidence (FCC, FreeLLMAPI, Alamo/runtime, Claude Code backend and Codex path).
5. Present owner decisions only where source contracts cannot resolve a genuine architectural choice.
