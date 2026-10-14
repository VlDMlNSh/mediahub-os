# External Controller Ecosystem — Canonical Manifest Crosswalk and Reusable Work Package

- Date: 2026-10-14
- Status: **DOCUMENTARY CROSSWALK / PROPOSED / NOT ACCEPTED / NOT FROZEN**
- Scope: Contour A — Jarvis, ASTRA/Astra Gold, Alamo/local inference, model routing, durable task lifecycle and tool integration.
- Sequence authority: `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md`
- Canonical component selection authority: `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md@main`
- Accepted target topology: `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md@main`
- Prior bounded research: `docs/checkpoints/mediahub-autonomous-controller-ecosystem-review-2026-10-14.md`
- This document turns the prior candidate list into a source-anchored decision crosswalk. It does not admit dependencies or authorize implementation.

## 1. Live source evidence

| Source | Ref | Blob SHA | Result |
|---|---|---|---|
| Canonical Component Manifest 2.0 | `main` | `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Selection closed; implementation open; production admission qualification-gated. Explicitly includes llama.cpp as target-gated, Temporal as future-gated only after a demonstrated gap, NATS JetStream/etcd under the same gap rule, and prohibits duplicate brokers/databases/AI runtimes without evidence. |
| Distributed AI Infrastructure | `main` | `e549692f207fbc91d9b9b9b92b8e665404f07290` | Accepted target, not runtime-qualified. Mac Pro central; Alamo is a local inference endpoint label whose runtime/API/model remain deployment facts to discover; local-only must fail closed; Jarvis remains control plane; FCC is a required Claude Code path integration layer. |
| Functional Baseline 2.0 | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Accepted canonical functional reference; architecture is not implementation evidence. |
| Node/service placement matrix | `docs/mediahub-chat-tree-map-20261012` | `59107fd6d7b8a73d671098adcf2824c310642907` | Proposed crosswalk; not accepted/frozen. |
| Owner decision packet | `docs/mediahub-chat-tree-map-20261012` | `a9f7929f9ac910c3fff1f1fb59f4ee68abf67e42` | DEC-DEV-01…08 remain existing decision IDs. DEC-DEV-02 exposes a serious ASTRA/Jarvis lifecycle-authority conflict and an ASTRA/Product State Authority wording conflict; this crosswalk does not resolve it. |

## 2. Candidate-to-manifest disposition

| External project/pattern | Upstream | Existing project overlap | Disposition now | Why / next evidence |
|---|---|---|---|---|
| llama.cpp | https://github.com/ggml-org/llama.cpp | Explicit target-gated candidate in Manifest §4; Alamo is accepted target endpoint, runtime unspecified | **REUSE EXISTING SELECTION; DO NOT ADD A SECOND LLM RUNTIME** | First document the Alamo API/runtime decision and host/model envelope. Then verify exact upstream release/license, supported build, model provenance, resource benchmark, adapter boundary and all §8 qualification gates. |
| Ollama | https://github.com/ollama/ollama | Named as target direction in a proposed unified deployment draft; not listed as selected runtime in the canonical manifest | **OWNER DECISION / NOT ADMITTED BY THIS CROSSWALK** | Compare Ollama and llama.cpp against the single Alamo endpoint contract. Do not install, invoke or assume compatibility. Resolve DEC-DEV-01 with hardware and API evidence. |
| Temporal | https://github.com/temporalio/temporal | Explicit future-gated reference in Manifest §5 | **DEFER; NO DEPENDENCY ADDITION** | Existing source says only after a demonstrated durable-workflow gap. First inspect current Jarvis/ASTRA task, lease, retry, cancellation and evidence-promotion contracts; resolve DEC-DEV-02 lifecycle owner. A new workflow engine cannot become a competing lifecycle authority. |
| NATS JetStream | https://github.com/nats-io/nats-server | Explicit future-gated reference in Manifest §5 | **DEFER** | Manifest excludes a second message broker without a proven gap. Establish whether existing transport/queue contracts lack a required capability before considering. |
| etcd | https://github.com/etcd-io/etcd | Explicit future-gated reference in Manifest §5 | **DEFER** | No distributed coordination store without an evidenced gap; never let it own product state or duplicate an existing coordination authority. |
| LangGraph | https://github.com/langchain-ai/langgraph | Not selected in Manifest 2.0; overlaps orchestration/stateful graph execution | **DO NOT ADD AT THIS STAGE** | No evidence of a capability gap that justifies a second orchestration/state model. Revisit only with a bounded use case, comparison, license/security review and owner decision. |
| Microsoft AutoGen | https://github.com/microsoft/autogen | Not selected; multi-agent orchestration overlaps Jarvis/ASTRA role model | **DO NOT ADD AT THIS STAGE** | The project already has controller roles and an unresolved lifecycle-authority conflict. Adding a framework now compounds ambiguity. |
| CrewAI | https://github.com/crewAIInc/crewAI | Not selected; role/task orchestration overlaps existing control plane | **DO NOT ADD AT THIS STAGE** | No documented unique capability gap; framework maturity/popularity alone is not admission evidence. |
| OpenHands | https://github.com/All-Hands-AI/OpenHands | Not selected; autonomous coding worker pattern | **RESEARCH ONLY / NOT ADMITTED** | Could be assessed as a sandboxed worker, not a controller. Requires task-scoped capabilities, sandbox/effect controls, egress policy, provider/data handling, provenance and resource review. |
| LiteLLM | https://github.com/BerriAI/litellm | Not selected; overlaps model/provider routing target | **RESEARCH ONLY / NOT ADMITTED** | Existing target architecture already requires a MediaHub-owned policy router. A provider proxy is acceptable only as a subordinate adapter that cannot change data-class policy or silently fallback from local-only to cloud. |
| MCP | https://github.com/modelcontextprotocol | Protocol ecosystem, not a canonical runtime component or authorization system | **PROTOCOL REFERENCE ONLY** | May be evaluated for typed tool interoperability after defining tool schemas, identity, capability allowlists, confirmation, audit, revocation and egress boundaries. MCP connectivity does not grant permission. |
| Home Assistant Core | https://github.com/home-assistant/core | Manifest §3 includes whole-product sidecars, while Bootstrap and roadmap preserve Home Assistant as Smart Home authority | **PRESERVE DOMAIN AUTHORITY; NO DUPLICATE CONTROL PLANE** | AI may use approved adapters only. Jarvis/ASTRA must not bypass Home Assistant authorization or become Smart Home authority. |

## 3. Ready-to-use architectural work products

The following are design-level artifacts ready to be carried into implementation planning once their gates are satisfied. They are not code that has been built or tested.

### WP-A — Alamo endpoint contract

Minimum contract fields:
- stable endpoint/service ID and owner;
- supported request/response schema and protocol version;
- authentication and network trust boundary;
- model identity, immutable model artifact digest, license/provenance and quantization;
- capability envelope (context length, modality, structured output/tool support);
- resource limits and overload behavior;
- health/readiness/liveness semantics;
- timeout, cancellation and idempotency behavior;
- privacy/data-class labels and local-only routing enforcement;
- no implicit cloud fallback; route denial is an explicit result;
- structured usage/performance evidence and audit correlation ID;
- version pin, upgrade/rollback and removal procedure.

**Gate:** DEC-DEV-01 and host/model evidence; no runtime selection implied here.

### WP-B — One engineering task envelope for Jarvis ↔ ASTRA

Minimum fields:
- stable task ID and idempotency key;
- requesting controller and authoritative lifecycle owner;
- task type, priority, deadline and cancellation token;
- declared inputs, data classification and provenance;
- allowed capability/tool set and policy decision reference;
- execution target and worker identity;
- lease/heartbeat, retry budget and terminal-state rules;
- expected output schema and artifact digests;
- evidence bundle, independent reviewer and promotion status;
- audit correlation ID and failure/degraded-mode reason.

**Invariant:** exactly one lifecycle authority owns claim/lease/retry/cancel/terminal state/evidence promotion. Product State Authority remains separate and owns canonical product-state mutation. The current authority conflict must be reconciled before implementation.

### WP-C — Provider/model route decision contract

Each route decision must carry:
- task and data-class identity;
- allowed providers/runtimes for the data class;
- explicit local-only flag and policy version;
- model capability constraints;
- cost/quota/latency budget and availability;
- route chosen plus reason;
- explicit denial/failure result when no compliant route exists;
- proof that local-only mode did not transition to cloud;
- provenance for provider/model/runtime version and result.

**Invariant:** local-only fails closed. Network reachability, a provider proxy or model response is not authorization.

### WP-D — Tool capability contract (MCP or non-MCP adapter)

Every tool declaration must define:
- stable tool ID, version and owner;
- typed input/output schema;
- read/write/effect classification;
- minimum capability and target resource scope;
- authorization/policy check and required user confirmation;
- network/data-egress behavior;
- timeout, cancellation, idempotency and retry behavior;
- audit event and result provenance;
- sandbox boundary, revocation and disable procedure.

**Invariant:** MCP is an interface protocol, not a permission grant.

### WP-E — External dependency admission record

For every proposed dependency, attach:
1. specific capability gap and source evidence;
2. official upstream URL and immutable release/commit;
3. license and redistribution review;
4. provenance, signature verification and SBOM;
5. vulnerability/security review;
6. supported OS/architecture and dependency/resource footprint;
7. adapter boundary and data-flow/egress map;
8. positive, negative, degraded-mode and recovery tests;
9. independent qualification evidence;
10. rollback/removal/replacement procedure.

This list operationalizes the existing Canonical Component Manifest §8; it does not weaken or replace that gate.

## 4. Prioritized action register

| Priority | Action | Status | Dependency / exit evidence |
|---|---|---|---|
| P0 | Reconcile DEC-DEV-02: one engineering lifecycle owner and explicit separation from Product State Authority | **BLOCKED ON OWNER/GOVERNANCE DECISION** | Exact contradictory clauses already documented in Owner Decision Packet. No implementation before decision. |
| P0 | Close DEC-DEV-01: define Alamo as endpoint contract and decide how local runtime candidates are evaluated | **OPEN / EVIDENCE-GATED** | Host/model facts and explicit route/adapter diagram; no installation or provider/model invocation in this pass. |
| P0 | Produce the existing canonical manifest crosswalk and avoid duplicate runtime/broker/workflow engine | **THIS DOCUMENT CREATED; PROPOSED, NOT ACCEPTED** | Owner/governance review and source-level upstream admission review. |
| P1 | Complete Jarvis/ASTRA task envelope and evidence-promotion state machine | **DESIGN INPUT READY; NOT IMPLEMENTED** | Lifecycle owner decision, canonical task-state contract, negative/failure semantics. |
| P1 | Complete model/provider route contract and local-only failure matrix | **DESIGN INPUT READY; NOT IMPLEMENTED** | DEC-DEV-05 and MH-21 data-egress/provider decisions and acceptance evidence. |
| P1 | Define tool capability contract and audit requirements | **DESIGN INPUT READY; NOT IMPLEMENTED** | MH-12 security invariants and tool-specific policy approval. |
| P2 | Source-level review of only the remaining non-admitted candidates | **NOT STARTED** | Begin only where a specific gap/use case exists; inspect upstream license, security, release, dependencies and supported platforms. |

## 5. Explicit non-actions and limitations

- No software installed or code integrated.
- No model/provider called; no credentials used.
- No tests or qualification run.
- No host/runtime inspection or hardware facts inferred.
- No infrastructure, deployment, migration, merge, rebase or cherry-pick.
- No owner decision made; DEC-DEV-01…08 IDs preserved.
- This is a focused candidate-to-manifest crosswalk, not a complete audit of all GitHub repositories or a claim that any candidate is globally best.
- The document is **PROPOSED / NOT ACCEPTED / NOT FROZEN** until the project’s governance process says otherwise.
