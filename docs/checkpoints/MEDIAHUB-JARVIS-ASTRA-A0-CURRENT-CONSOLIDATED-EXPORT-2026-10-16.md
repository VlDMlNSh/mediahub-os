# Jarvis + ASTRA A0 — consolidated current-state export

- Date: 2026-10-16
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **DOCUMENTARY CONSOLIDATION / SOURCE-BOUND SNAPSHOT / NOT A NEW ARCHITECTURE ACCEPTANCE**
- Purpose: collect the currently evidenced Jarvis, ASTRA/A0, and autonomous engineering-controller decisions, boundaries, proposals, blockers, and next steps in one navigable artifact.
- Evidence boundary: this document consolidates the current project map, continuation checkpoint, master roadmap, and recent conversation context available at creation time. It is not a claim that every historical chat message or every repository branch has been exhaustively recovered.

## 1. Executive summary

MediaHub is being designed as a new, clean developer fabric (Contour A) that will host Jarvis, ASTRA GOLD/A0 and autonomous engineering workflows. The product itself (Contour B) remains gated until Contour A is deployed and independently accepted. The old attempted deployment is not a source of current runtime truth: legacy hostnames such as `mh-dev-01`, `mh-dev-02`, and `Voktors-Mac-mini.local` must not be used as current target identities or assumed to exist. No live host/runtime state has been inspected in this pass.

The current architectural direction separates three kinds of authority:

1. **Jarvis** — corporation-level mission coordination: interpret the developer's goal, coordinate work across engineering capabilities, and present/track the mission at the top level.
2. **ASTRA GOLD / A0** — ASTRA-internal engineering workflow coordination and control state, including internal queue/claim/gate/lifecycle responsibilities within its accepted scope. A0 is not a global product-state authority.
3. **MediaHub Product State Authority** — the only authority allowed to mutate canonical MediaHub product state. Jarvis and ASTRA must not bypass it. Home Assistant Core remains the authority for Smart Home state within approved boundaries.

The authority split is owner-approved as **DEC-DEV-02, Option C (2026-10-15)**. This settles the semantic division of responsibility; it does not itself prove that every primary document has matching wording, that a Jarvis-to-A0 ingress has been implemented, or that the system has been qualified.

## 2. Canonical navigation and source hierarchy

- [Project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap 1.0](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Bootstrap instruction](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Unified architecture and deployment contract draft](mediahub-unified-architecture-and-deployment-contract-v0.1.md)

Source precedence: explicit owner decisions and governance records within scope; accepted Baseline 2.0 and accepted domain contracts; accepted component/target architecture within declared scope; domain evidence; working matrices/drafts; chat history and inference. Baseline 2.0 remains the canonical functional baseline. Baseline 1.0 is historical provenance and must not be silently merged into Baseline 2.0.

## 3. Contours and sequencing

### Contour A — Developer Fabric
The autonomous development environment: Jarvis, ASTRA/A0, engineering task routing, approved model/provider/tool adapters, evidence and qualification workflows, GitHub integration, engineering memory/provenance, developer client access, and eventual reproducible installation/update/recovery.

### Contour B — MediaHub OS product
Product implementation is not to be mixed into the developer fabric. Do not begin product development in Contour B until Contour A is deployed and independently accepted against explicit readiness gates.

### Deployment status
This export is design/documentation only. It does not establish deployment, installation, runtime operation, test success, qualification, release, or acceptance. The clean target inventory and hardware/software compatibility remain to be evidenced under the appropriate authorization. Do not revive old deployment identities as defaults.

## 4. Responsibilities and non-negotiable authority boundaries

| Actor / subsystem | Responsibility | Explicitly not responsible for |
|---|---|---|
| Jarvis | Corporation-level mission planning and coordination; choose among approved engineering capabilities; maintain top-level mission visibility and delegation | Canonical MediaHub product-state mutation; overriding A0 internal policy; bypassing identity, authorization, egress, evidence, or qualification gates |
| ASTRA GOLD / A0 | ASTRA-internal engineering queue/workflow/control state, claims, gates, bounded execution coordination, provenance/evidence and internal lifecycle rules within accepted contracts | Global corporation/product state; MediaHub Product State Authority; unrestricted host control; treating a proposed ingress draft as an accepted API |
| Product State Authority | Canonical product-state mutation under approved product contracts | Engineering task coordination or replacing ASTRA's internal workflow authority |
| Home Assistant Core | Smart Home state authority within approved boundaries | General cross-domain authority |
| Models, cloud services, workflow engines, plugins, adapters, knowledge graph, persistence, observability | Bounded supporting capabilities under explicit policy | Becoming an independent canonical State Authority |
| Independent A3/verifier role | Independent verification where required by ASTRA qualification/evidence contracts | Self-approval or replacing owner/governance acceptance |

Use status distinctions precisely: IDEA → DESIGN → IMPLEMENTED → TESTED → VERIFIED → QUALIFICATION CANDIDATE → QUALIFIED → RELEASED → DEPLOYED → OBSERVED → PRODUCTION ACCEPTED. A document or selected component does not prove implementation or runtime qualification.

## 5. Jarvis mission and engineering workflow — current direction

The intended top-level flow is:

1. Receive a developer mission and clarify scope/constraints when necessary.
2. Classify task, sensitivity, required capabilities, data-egress constraints, risk, and acceptance evidence.
3. Build a bounded plan and decompose work into traceable tasks.
4. Delegate engineering tasks to approved ASTRA/A0 or other authorized capabilities through an accepted, authenticated interface.
5. Track mission/task progress using evidence-backed states rather than inferred success.
6. Collect outputs, provenance, target/source identity, validation evidence, and unresolved decisions.
7. Request independent verification/qualification where required.
8. Return a result with changed artifacts, source refs/SHA, evidence, limitations, and next action.

This is a target workflow, not proof that a full autonomous loop currently runs. A0's internal queue/task contract and any separate signed operational-command path must not be represented as an already-integrated, authenticated Jarvis producer-to-A0 chain.

## 6. ASTRA A0 ingress — latest documented state

### Status
The transport-neutral ingress contract candidate **WB-14AA** is **PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED**. Its proposal-local labels `A0-ING-01…09` have only had a bounded collision scan; they are not canonical registry IDs and must not be promoted without a wider collision check and governance acceptance.

### Logical operations in the proposal
The draft describes logical operations such as:
- `SubmitMission`
- `GetMissionStatus`
- `GetMissionResult`
- `RequestCancellation`
- optional `ProbeA0`
- optional `ReconcileAdmission`

These are conceptual operation names, not approved endpoint names, wire messages, or a frozen API.

### Required contract areas still open
- accepted request/ACK/status/result/cancellation contract and versioning;
- trusted service principal, caller edge, issuer/attester/verifier and lifecycle;
- authentication and authorization binding to the intended operation and resource;
- durable admission and idempotency semantics;
- freshness/replay handling, with external policy kept distinct from internal lease/retry values;
- fencing, cancellation, restart/recovery and terminal-result semantics;
- correlated health challenge/response and mapping into the accepted health vocabulary;
- ownership, delegated authority, governance approval path, and acceptance evidence;
- qualification criteria and independent verification of the ingress contract.

No endpoint, transport, schema ID, issuer, cryptographic profile, persistence technology, external TTL, status enum, or exactly-once guarantee has been selected. Do not infer these from internal retry/lease numbers.

### Decision register
D-ING-01…04, D-ING-05a, D-ING-05b, and D-ING-06 remain OPEN. WB-14AD is a governance request, not evidence that owners were appointed or the request accepted. Role-level ownership suggestions are not actual assignments.

### Route separation
- **Jarvis → ASTRA A0 engineering ingress** is one route and remains design-only pending accepted contracts and evidence.
- **P0-07 → P0-05 → P0-04 product mutation** is a separate route with its own contract/caller-edge gates. A product-mutation blocker does not automatically block every engineering task submitted to A0; equally, A0 cannot bypass product-state authority or mutate canonical product state itself.

## 7. Model and tool direction

A recorded owner direction favors Claude-centered reasoning/engineering workflows together with local Ollama inference capability. The technical distinction is important: Claude is an external model/service interface; Ollama is a separate local model runtime. Claude models are not served by Ollama. Compatibility of any particular Claude tool with an Ollama endpoint must be independently evidenced.

Two design shapes remain options, not accepted decisions:
- **A. External engineering operator + local inference/tool endpoint:** Jarvis/engineering workflow uses an approved Claude interface for suitable work and separately uses local Ollama for tasks assigned to local inference.
- **B. Policy-based per-task router:** Jarvis selects between separately defined Claude and Ollama adapters according to task classification, capability, privacy/egress policy, availability, and owner-approved routing rules.

Open choices include exact Claude access mode, routing authority, local model and host profile, licensing/provenance, capacity and performance, fallback behavior, data retention, sandbox/tool permissions, auditability, and reconciliation with relevant MH domains. No provider invocation, credentials use, component installation, or model benchmark is evidenced by this export.

Non-negotiable routing safeguards:
- explicit task/data classification and egress policy;
- no silent cloud fallback for a local-only task;
- least privilege and bounded worktree/tool/host permissions;
- treat model outputs as untrusted inputs;
- provenance and evidence for consequential actions;
- no change to MediaHub Product State Authority.

## 8. Clean deployment and hardware identity

The target is a newly verified, reproducible deployment, not a continuation of failed legacy installation attempts. No old hostnames or stale node identities may be used as proof of the current design or runtime.

The roadmap contains owner-directed hardware role concepts (developer workstation, low-resource auxiliary server, optional future owned GPU/video server, developer clients, restricted API-key workflow host). These are target-role concepts, not evidence that a specific machine is currently provisioned, compatible, clean, reachable, or accepted. The user's latest clean-deployment direction takes precedence over assumptions based on old deployment history; any discrepancy between this direction and legacy target tables must be reconciled explicitly before installation planning.

No installation, software setup, host/runtime inspection, test, qualification, credential use, provider call, infrastructure change, deployment, migration, merge, rebase, or cherry-pick is authorized by this export.

## 9. Security, reliability, evidence, and failure behavior

- Local-first where required; fail closed on unknown authorization or unresolved authority.
- Distinguish reported, observed, desired, policy-allowed, commanded, committed, applied, confirmed, and predicted state.
- Preserve target SHA and source provenance for evidence; evidence must be fresh for the relevant target and immutable where the accepted ASTRA qualification contract requires it.
- Independent verification cannot be replaced by self-review.
- Do not claim “exactly once” without a contract and evidence; use explicit idempotency/admission semantics.
- Keep cancellation, fencing, retries, recovery, health probes, token freshness, and evidence freshness as separate concepts unless an accepted contract explicitly relates them.
- A selected component, draft document, static schema, or successful documentation update does not prove runtime compatibility or qualification.
- Production remains NO-GO until the relevant gates have fresh evidence and authorized acceptance.

## 10. Known source/status discrepancies

1. **A0 authority wording drift:** the documentation-branch executor capability matrix scopes A0 to ASTRA workflow/control state; the `main` copy retains broader “Global coordination/state” wording. DEC-DEV-02 Option C settles the intended authority split, but source-text drift remains and branch integration is not authorized.
2. **A0 ingress absent as accepted contract:** internal ASTRA workflow/security/evidence rules exist, but the accepted Jarvis-facing wire/API, caller/issuer chain, admission/idempotency, lifecycle/result and health-probe contracts are not established.
3. **Health vocabulary scope/mapping:** generic domain-health schema and accepted MH-06 health semantics differ; no accepted mapping/scope decision was evidenced. Do not choose an enum or silently edit either contract.
4. **Owner and acceptance path:** the governance request does not establish named accountable owners or formal acceptance workflow for D-ING items.
5. **Runtime and clean target inventory:** deployment, host identity, exact OS/hardware/software compatibility, network/security posture, and recovery evidence remain unverified in this documentary pass.
6. **Branch divergence:** the documentation branch and `main` have historically diverged materially. Do not merge/rebase/cherry-pick to resolve this without explicit authorization; always refresh live refs before follow-up work.

## 11. Current evidence register (selected)

| Evidence | Ref/status | What it establishes |
|---|---|---|
| Project map §20.294–20.302 | `docs/mediahub-chat-tree-map-20261012`, read during this consolidation | Latest ingress ownership, route boundary, source-contract census, candidate, ID crosswalk, evidence boundary, governance request, and executor authority drift |
| WB-14AA A0 ingress candidate | `docs/mediahub-chat-tree-map-20261012`, commit `d05462b3c39ad5d08fad0ebde07e76158df361ba`, blob `030273bfe9fd6d44e78b611c011af95d08c88a45` | Non-normative logical ingress candidate; unresolved decisions preserved |
| WB-14AB ID/owner crosswalk | `docs/mediahub-chat-tree-map-20261012`, commit `fee7c7b732bb1974e453fc0d023b1ec739eed2e1`, blob `2c87f5549609dc5298e0a5117ec46a2331972ba8` | Bounded proposal-ID collision scan and D-ING crosswalk; no canonical registration |
| WB-14AC evidence/qualification crosswalk | `docs/mediahub-chat-tree-map-20261012`, commit `8b92df9305869f93e4691ea948413c4418a6d2a7` | Internal ASTRA evidence/qualification boundaries; not the external ingress API |
| WB-14AD governance request | `docs/mediahub-chat-tree-map-20261012`, commit `d32e0dce23bfb577836b4ef861bf33be0361fbf8`, blob `a2367eff5ca2092fa12bda0be4cab75bf4e2ba9d` | Request for owner/approval-path confirmation, not an accepted appointment/decision |
| WB-14AE executor matrix drift | `docs/mediahub-chat-tree-map-20261012`, commit `01aeaf874dba72a55940f718cc1b74e50a17f448`, blob `ba655f1af358f97634cfc5d1402ac60c25d7b0d5` | Exact docs/main wording discrepancy; no branch integration |
| Owner decision | DEC-DEV-02 Option C, owner-approved 2026-10-15 | Jarvis/A0/Product State Authority responsibility split |
| Master roadmap | `docs/mediahub-chat-tree-map-20261012`, blob at consolidation: to be read back in map/checkpoint as applicable | Contour A/B sequencing, source precedence, authorization limits |

## 12. Immediate next actions

1. Continue source-only inspection of the exact A0-facing contract references in the ASTRA lifecycle trace and Jarvis adapter draft.
2. Record accountable owners and formal acceptance workflow only when supported by explicit owner/governance evidence; keep D-ING decisions OPEN until then.
3. Reconcile the executor capability matrix wording drift through owner-approved change control; do not integrate branches unilaterally.
4. Resolve health vocabulary scope/mapping through a separate accepted decision, not by guessing an enum.
5. Keep the proposed A0 ingress transport-neutral and non-normative until the required owners accept the contract and its security/lifecycle decisions.
6. Reconcile the clean target hardware/software inventory without resurrecting old deployment hostnames; perform no host inspection or installation without explicit authorization.
7. Only after contract decisions and authorization, define implementation work, test/qualification evidence, and independent acceptance gates.

## 13. What this export does not claim

It does not claim that Jarvis or ASTRA A0 is running, that a complete autonomous engineering loop exists, that the ingress candidate is accepted, that any code is implemented, that any tests passed, that models/providers were called, that credentials were used, that a clean deployment is installed, or that Contour A has been qualified/accepted. Those claims require separate current evidence.

## 14. Primary links

- [WB-14Z A0 ingress source-contract census](MEDIAHUB-CONTOUR-A-WB-14Z-A0-INGRESS-SOURCE-CONTRACT-CENSUS-2026-10-16.md)
- [WB-14AA A0 ingress contract candidate](MEDIAHUB-CONTOUR-A-WB-14AA-ASTRA-A0-INGRESS-CONTRACT-CANDIDATE-2026-10-16.md)
- [WB-14AB A0 ingress ID/owner crosswalk](MEDIAHUB-CONTOUR-A-WB-14AB-A0-INGRESS-ID-COLLISION-AND-DECISION-OWNER-CROSSWALK-2026-10-16.md)
- [WB-14AC evidence/qualification crosswalk](MEDIAHUB-CONTOUR-A-WB-14AC-A0-INGRESS-EVIDENCE-AND-QUALIFICATION-BOUNDARY-CROSSWALK-2026-10-16.md)
- [WB-14AD governance request](MEDIAHUB-CONTOUR-A-WB-14AD-A0-INGRESS-GOVERNANCE-REQUEST-2026-10-16.md)
- [WB-14AE executor matrix authority-drift reconciliation](MEDIAHUB-CONTOUR-A-WB-14AE-EXECUTOR-CAPABILITY-MATRIX-AUTHORITY-DRIFT-RECONCILIATION-2026-10-16.md)
- [Unified architecture/deployment contract draft](mediahub-unified-architecture-and-deployment-contract-v0.1.md)

