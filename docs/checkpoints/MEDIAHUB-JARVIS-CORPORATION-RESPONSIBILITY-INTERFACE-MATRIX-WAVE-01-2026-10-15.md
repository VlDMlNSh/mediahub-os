# MediaHub OS — Jarvis Corporation Responsibility / Interface Matrix, Wave 01

- Date: 2026-10-15
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-ANCHORED DESIGN RECONCILIATION / OWNER-DIRECTED TARGET CLARIFICATION / NOT A NEW ACCEPTED NORMATIVE CONTRACT / NOT IMPLEMENTED / NOT QUALIFIED**
- Purpose: translate the owner’s distributed AI-corporation direction into a traceable responsibility/interface matrix using existing repository contracts. This document supplements; it does not replace; accepted Baseline 2.0, primary domain contracts, ASTRA governance, or the accepted distributed AI target architecture.
- Owner direction captured from project conversation: prefer local models on Mac Pro as the primary execution route; select Scenario B as a target in which Claude Code is configured to use a compatible local model backend through a gateway. Keep official Anthropic authorization, compatible gateway routing, native local LLM execution, and other admitted executor adapters as distinct configurations. Actual compatibility and routing remain unverified.
- Related prior record: [Jarvis Corporation Proposal Crosswalk, Wave 01](MEDIAHUB-JARVIS-CORPORATION-ARCHITECTURE-PROPOSAL-CROSSWALK-WAVE-01-2026-10-15.md) on `main`. That file’s presence on `main` does not mean this documentation branch is merged.

## 1. Source anchors and evidence status

| Source | Ref / blob SHA | What it establishes | What it does not establish |
|---|---|---|---|
| `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` | `main` / `e549692f207fbc91d9b9b9b92b8e665404f07290` | Accepted target topology: Mac Pro central node; Jarvis; Alamo local inference endpoint; FCC integration layer; FreeLLMAPI cloud route; separate Codex path; owned and user-contributed compute pools; local-only fail-closed | Runtime deployment, exact FCC implementation, Alamo-to-Ollama identity, compatibility, qualification |
| `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md` | documentation ref / `e112cc73178eef5f71b8a814296e4902c2e80390` | Draft mission envelope, authority boundaries, least-privilege GitHub capabilities, immutable per-task route record, isolated workspace and evidence gates | Accepted wire schema, actual A0 API, issuer lifecycle, implementation |
| `docs/checkpoints/MEDIAHUB-PROVIDER-IDENTITY-AND-EGRESS-CONTRACT-CROSSWALK-WAVE-05-2026-10-14.md` | documentation ref / `01b22130e8b5de49782a7241ec14331016259de0` | FreeLLMAPI identity conflict; separate FCC, OmniRoute, UnoRouter, Alamo, Ollama and Claude Code identities; required per-hop egress evidence | Which unresolved gateway/provider topology is actually deployed |
| `docs/checkpoints/MEDIAHUB-UNIFIED-LOCAL-INVENTORY-AND-VERIFIABLE-COMPONENT-MATRIX-WAVE-02-2026-10-14.md` | documentation ref / `4d239780af2367fdecd00e7156521934ef2f8114` | Bounded observations from two online nodes and declared-vs-observed gaps | Complete inventory of Mac Pro, Mac mini and MacBook; successful route execution |
| `docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-ARCHITECTURE-PROPOSAL-CROSSWALK-WAVE-01-2026-10-15.md` | `main` / `721e4c994d4800df4605af52630ea75339971a27` | Prior proposal reconciliation and remaining design gaps | New normative acceptance or deployment |
| `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md` | documentation ref / `d70a6654d4ce1850369b0431c4e35de2aa0af36a` before this update | Working development sequence and existing D-03/local-first/Contour A-B gates | Permission to install, run tests, call providers, inspect hosts, deploy or integrate branches |

## 2. Responsibility and authority matrix

| Logical role | Responsibility | Authority boundary / must not do | Interface or evidence required | Status |
|---|---|---|---|---|
| **Jarvis Control Plane** | Accept request, form bounded mission, coordinate decomposition, dispatch, monitor progress, collect results, request validation and report disposition | Must not write ASTRA queue internals, mutate canonical product state, bypass policy or self-approve | Versioned mission envelope; ASTRA mission-ingress contract; task graph; audit correlation ID | Owner-accepted top-level direction; implementation unproven |
| **ASTRA A0 / queue authority** | Sole writer for ASTRA-internal queue, claim, lease, heartbeat, retry/cancellation and gate state under its accepted contract | Must not become Product State Authority or a second queue writer | Existing accepted ASTRA contract; authenticated, capability-scoped mission ingress; lease/state evidence | Authority invariant established; exact ingress API open |
| **Product State Authority** | Sole canonical product-state mutation authority | Must not delegate canonical mutation implicitly to Jarvis, agents, model/provider, GitHub adapter or workers | Existing primary state contract and its own authorization/evidence | Existing invariant; unchanged |
| **Task Planner / DAG Coordinator** | Split a large task into bounded subtasks; encode dependencies, critical path, resource needs and merge/integration gates | Must not schedule dependent tasks as independent or reinterpret accepted contracts | Proposed task graph: stable task IDs, dependency edges, idempotency, deadlines, cancellation and retry rules | Gap to formalize; do not assume deployed service |
| **Agent Registry** | Describe agent role, capabilities, allowed tools, trust class, location, resource needs, permissions, availability and verification requirements | Registration is not proof of current availability or qualification; an agent cannot grant itself permissions | Stable IDs; schema revision; observed health/availability timestamp; capability provenance | Partial registry coverage; schema alignment gap |
| **Dispatcher / Executor Selector** | Choose an eligible executor per task from local, approved cloud and admitted worker pools | Must not bypass egress policy, provider terms, budgets, user consent or required verification | Revision-bound route decision; eligibility reasons; denied alternatives; budget/quota; selected identity | Draft partial coverage; formal selection matrix needed |
| **Claude Code client/tool** | Engineering interaction and tool orchestration on an authorized node | Its presence does not identify the model serving the request; it must not silently bypass local-only routing | Explicit backend configuration; request-to-backend evidence; tool/API compatibility record | Target configuration selected; actual route unverified |
| **Local model runtime / Alamo endpoint** | Serve admitted local models on Mac Pro as the preferred route when suitable and policy permits | Must not be treated as “Claude running locally”; no cloud fallback in local-only mode; Alamo/Ollama identity must not be assumed | Exact endpoint, runtime, model tag/digest, provenance/license, API/tool-call compatibility, health and route evidence | Accepted target role; runtime identity/qualification open |
| **FCC integration/control layer** | Provide the required Claude Code integration/control boundary as supported by its pinned implementation | Must not become Jarvis, product authority or an assumed generic API proxy | Exact source/package/release, supported config, request route and lifecycle evidence | Required in target architecture; implementation mapping unresolved |
| **Provider / Model Gateway** | Adapt admitted upstream APIs, enforce routing policy, track provider/model identity, quotas, errors, fallback and secret references | Must not conflate gateway location with upstream location or evade provider restrictions | Per-hop locality/egress; upstream provider/model identity; capability reference (never secret); quotas and fallback evidence | Partial contracts; FreeLLMAPI classification conflict open |
| **External API executor** | Perform tasks where cloud use is allowed and appropriate | Must not receive private data without policy permission or be treated as guaranteed free/available | Provider terms, model capability, quota, budget, route authorization and provenance | Candidate capability only; provider routes unqualified |
| **Codex cloud path** | Separate cloud-authenticated development workflow | Must not be silently substituted for Claude Code/local route or treated as an interchangeable generic endpoint | Its own supported auth and workflow contract; separate route evidence | Explicitly separate target path |
| **Owned GPU worker pool** | Execute bounded tasks on operator-managed hardware | Remote RAM/VRAM is not automatically shared with Mac Pro; worker does not become control authority | Authenticated worker API, resource telemetry, lease, task/result provenance | Future/target pool; qualification open |
| **User-contributed MediaHub worker** | Voluntarily execute eligible, bounded tasks and return results | Untrusted by default; no central secrets, unrestricted host access or sensitive data without explicit policy; no self-qualification | Explicit opt-in/consent, isolation, least privilege, data minimization, resource caps, revocation, provenance and result verification | Future target only; not admitted |
| **Independent verifier / quality layer** | Verify output against mission, source SHA, contract, checks and evidence | Executor cannot be sole independent reviewer when independence is required | Structured result envelope, immutable artifact digests, verifier identity and lifecycle disposition | Principles exist; corporation-wide envelope/contract gap |
| **Resource Manager** | Track capacity, latency, memory/VRAM, queue pressure, budgets, provider quotas and node availability | Must not claim capacity from stale registry entries or promise free quotas | Fresh resource observations, budgets, per-node limits, admission decision | Logical role; no separate deployed service asserted |
| **Policy / Egress Engine** | Enforce data class, privacy mode, allowed destinations, local-only and permission boundaries | Must fail closed on unknown route identity or missing authorization | Versioned policy decision and per-hop egress record; local-only fallback = none | Invariants established; runtime enforcement unverified |
| **GitHub Adapter** | Read and write only authorized refs/paths/operations for bounded missions | No implicit merge, release, deployment, workflow-secret administration, protected governance changes or bypass of review | Capability-scoped operation; before/after SHA; actor, mission and evidence record | Draft contract only; no broader permissions granted |
| **Client interfaces (MacBook/iPhone)** | Submit requests and display task/result state | Network reachability/IP:port is not authorization; no implicit shell/admin access | Authenticated private API; per-operation authorization; revocation and audit | Target architecture; endpoint not qualified |

## 3. Logical interface contracts to define or reconcile

These are logical boundaries; they do not require one physical service per row.

1. **Request → Mission:** request identity, objective, scope, data class, expected artifacts, constraints, deadline and approval requirements.
2. **Mission → Task DAG:** stable task IDs, dependencies, parallel eligibility, contract/input revisions, idempotency keys, cancellation propagation, retry ceilings and integration gates.
3. **Task → Executor selection:** capabilities, permission set, locality/egress, privacy, model/tool compatibility, resource needs, availability freshness, cost/quota, latency and verifier requirements.
4. **Jarvis → ASTRA A0:** bounded mission submission and status/evidence retrieval through the actual accepted ASTRA API; Jarvis must not write ASTRA-internal queue/lease/gate state directly.
5. **Claude Code → FCC → backend:** distinct client, control adapter, gateway, runtime, model and upstream identities; local model route is primary by owner direction when suitable; local-only must fail closed.
6. **Gateway → provider/model:** per-hop route identity, API compatibility, auth principal/capability reference, quota/budget, timeout/retry/circuit-breaker and fallback policy.
7. **Task → worker node:** explicit worker admission, lease, isolation, resource/deadline bounds, cancellation and minimal task payload.
8. **Executor → Result envelope:** task/mission IDs, target SHA, contract/policy revision, executor and route identity, artifacts/digests, dependency outputs, checks, limitations, status and verifier evidence; no secrets.
9. **Result → Integrator/verifier:** deterministic input set, conflict detection, independent review, accepted artifact list and blocked/unverified items.
10. **Client → Control API:** authenticated principal, capability-scoped operation, replay/idempotency behavior, rate limits and revocation.
11. **Lifecycle transition → Evidence:** distinct design/implementation/test/verification/qualification/release/deployment/observation/acceptance states, each with explicit evidence and authority.

## 4. Distributed task lifecycle (proposal, not accepted protocol)

Request intake → mission normalization → data/policy classification → decomposition and dependency DAG → eligible-executor admission → bounded dispatch → execution → structured result return → artifact/provenance validation → independent verification → integration → lifecycle gate → completion or explicit hold/fail/escalation.

Parallelism is allowed only where dependencies, isolation, capacity, authorization and integration boundaries permit. More agents do not automatically imply higher useful throughput. If no eligible executor exists, the task is held/rejected/failed explicitly; the system must not report success.

Retries require idempotency and lease/state reconciliation. Cancellation must propagate to workers where supported and record partial outputs. Conflicting or untrusted results require revalidation or duplicate execution on an independently admitted worker.

## 5. Owner-directed routing and node model

- **Primary route:** local models on Mac Pro through the intended Alamo/local-runtime interface, when suitable and permitted.
- **Claude Code Scenario B:** Claude Code uses a compatible local model backend through the configured gateway. This is not the Claude model running locally. Compatibility and local-only network behavior are not yet proven.
- **Distinct route modes:** (A) official Anthropic authorization; (B) compatible gateway to a local backend; (C) native local LLM executor; (D) other explicitly admitted provider/worker adapters. Keep their authentication and evidence separate.
- **Mac Pro:** intended central Jarvis/control and local inference node.
- **Mac mini/Linux:** intended independent Contour A development/worker node. It must not be used to bypass Contour A gates.
- **MacBook:** intended client and optional engineering-client node.
- **Provider pool:** multiple legitimate providers and supported credentials may be registered, subject to terms/quotas; do not implement artificial account multiplication or key rotation to evade limits.
- **Future user MediaHub pool:** opt-in, untrusted-by-default and separately admitted. No access to central secrets or unrestricted internal services.

The placement statements above are target architecture and owner direction, not evidence that each machine is configured or qualified.

## 6. Unresolved conflicts and required follow-up

| ID | Conflict / gap | Safe disposition | Next evidence needed |
|---|---|---|---|
| C-01 | FreeLLMAPI is described as a cloud-model route in architecture but registry metadata says `local_gateway` / `PENDING` | Keep conflict open; do not rewrite registry | Non-secret source/config/deployment evidence identifying gateway location and upstreams |
| C-02 | FCC exact implementation and compatibility mapping unknown | Treat as required logical boundary, not proven component | Pinned upstream/package identity, supported configuration and request path |
| C-03 | Alamo-to-Ollama/runtime and exact model identity unbound | Keep logical endpoint separate from runtime | Non-secret configuration/source evidence, model provenance/digest/license and API compatibility |
| C-04 | Existing Ollama executor hard-codes `qwen2.5-coder:3b` while route/evidence may name another model or `unspecified` | Preserve as a static identity/provenance defect; do not claim runtime impact | Source-level trace of model selection from admission through invocation and evidence |
| C-05 | Corporation-wide task DAG, cancellation/idempotency and result envelope not found as one accepted contract | Design draft only; inspect existing schemas before inventing duplicates | Crosswalk existing queue, lease, evidence and schema contracts |
| C-06 | User-contributed workers need a separate trust/admission boundary | Future target only | Threat model, consent, sandbox, resource/data policy, revocation and verifier contract |
| C-07 | ECC reuse has not been assessed | Do not install/import | Read-only upstream source, version, license, provenance, security, side-effect and overlap review |
| C-08 | ASTRA mission-ingress API and capability issuer lifecycle remain open | Jarvis must not directly mutate A0 internals | Accepted ASTRA interface and security/identity source contracts |
| C-09 | Current branch topology is diverged from main | Do not merge/rebase/cherry-pick | Separate governance/branch integration authorization and source comparison |

## 7. Status invariants

- This matrix is a source-anchored design aid, not a new accepted normative contract.
- Existing owner-accepted D-03 and accepted distributed AI target architecture remain the authority for their stated scope.
- Product State Authority remains the only canonical product-state writer; ASTRA A0 remains the ASTRA-internal queue/lease/gate state writer.
- Local-only mode must fail closed; no silent cloud fallback.
- Model, client, agent, executor, gateway, upstream provider and worker are separate identities.
- Architecture, implementation, verification, qualification, release, deployment and acceptance are separate states.
- No component is declared installed, integrated, qualified or accepted based on this matrix.
- No credentials, providers/models, host/runtime, tests, installation, configuration, infrastructure, deployment or branch integration were used or changed in this documentary pass.

## 8. Next work

1. Inspect existing schema and primary contracts for task DAG, agent profiles, leases, cancellation/idempotency and result envelope before designing a new schema.
2. Resolve C-01/C-02/C-03 from non-secret source/config/deployment evidence without calling providers or reading credentials.
3. Perform read-only ECC upstream review against the concrete gaps above; produce a candidate-only recommendation and license/security/overlap table.
4. Only after source reconciliation, prepare a proposed versioned corporation contract and owner/governance review packet. Keep Baseline 2.0 and accepted domain contracts unchanged unless approved through change control.
5. Keep Contour A deployment and independent acceptance ahead of Contour B product development.
