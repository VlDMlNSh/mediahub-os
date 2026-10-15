# MediaHub OS — Contour A WB-10: Jarvis Direct Local-Executor Route and Contract Evidence Matrix

- Date: 2026-10-15
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **OWNER-DIRECTED ARCHITECTURE OPTION RECORDED / SOURCE TRACE PARTIAL / NOT IMPLEMENTED / NOT QUALIFIED / NOT ACCEPTED**
- Scope: record the owner's explicit direction that Jarvis may send autonomous queues directly to a local executor, bypassing ASTRA A0 for that route; map this route against current source contracts and identify required controls/evidence. This document does not authorize runtime implementation, deployment or qualification.
- This is a working architecture/evidence artifact. It does not replace Baseline 2.0 or silently amend accepted primary contracts.

## 1. Owner direction and route distinction

Owner direction (2026-10-15): Jarvis may create/coordinate missions and may submit autonomous work to a local executor directly, without passing through ASTRA A0.

Record this as a **separate, explicitly bounded route**, not as a universal replacement for the ASTRA A0 route:

- Route A — **Jarvis → ASTRA A0 → ASTRA-owned executor lane(s)**. A0 owns ASTRA-internal queue admission, claim/lease, scheduling, retries, cancellation, recovery and ASTRA evidence/gate transitions under its accepted scope.
- Route B — **Jarvis → local executor queue → local executor**. This route bypasses A0 coordination for tasks explicitly eligible for direct local execution. The local executor/queue must have one declared lifecycle owner and cannot implicitly claim A0's state or product authority.
- Both routes remain subordinate to the owner-defined mission scope, accepted authorization policy, task/result schemas, audit/evidence requirements and the Contour A → Contour B gate.
- Route B bypasses A0 **coordination**, not authentication, authorization, sensitive-operation approval, isolation, evidence provenance, or failure controls.
- A task must not be dispatched simultaneously into both routes unless a defined cross-route idempotency/fencing contract explicitly permits it. Otherwise duplicate execution is denied.
- If a task needs A0-owned ASTRA state, A0-specific gates/evidence, or an executor only reachable through A0, it is not eligible for Route B unless an accepted adapter contract establishes equivalence.
- A0 and the local executor must not be treated as competing global mission authorities. Jarvis coordinates corporation-level missions; each execution domain owns only its explicitly scoped internal lifecycle; MediaHub Product State Authority remains separate.

This is an owner-directed target architecture option. The existing source set does not prove Route B is implemented or that any current local executor is admitted for it.

## 2. Source-pinned observations

| Source | Live ref / blob SHA | Direct observation | What it does not prove |
|---|---|---|---|
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` | `main` / `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | Describes ASTRA's queue → claim → lease → dispatch → heartbeat → result/recovery lifecycle and a bounded set of executor lanes. | Does not establish an accepted Jarvis-to-independent-local-executor queue contract or show that Route B can bypass A0 safely. |
| `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md` | `main` / `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1` | Assigns queue/scheduling/claims and state to A0; includes recovery, duplicate suppression and replay-idempotency expectations. Its phrase “MediaHub State Authority” is already in a documented scope conflict. | Does not authorize A0 as Product State Authority or prove that its wording covers Route B. |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `main` / `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Defines bounded operational controls, human approval semantics and queue-related invariants. | Static contract presence is not runtime qualification; no new direct-route semantics are inferred from it. |
| `runtime/mediahub_runtime/task_ingress.py` | `main` / `59e1254aa61cc8f55f53bd1e179631e81c441393` | `FileTaskIngress` reads JSON Task Contracts, checks selected schema/shape fields and forwards `approval_state` into the gateway request. | Does not prove a trusted Jarvis producer, direct executor ingress, cryptographically verified approval or a production caller. |
| `runtime/mediahub_runtime/astra_gateway.py` | `main` / `10985e4ad8f682313d08e7492ecc1856a8bce20f` | Gateway uses task fields, applies a sensitive-action check against `approval_state`, derives routing capability labels and executes through its own registry/orchestrator. | Does not establish Route B's local queue/lease/recovery contract; routing labels are not security grants. |
| `runtime/mediahub_runtime/authorization.py` | `main` / `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | Typed in-process `AuthorizationContext` holds principal/capability strings and policy checks a configured tuple. | Does not prove trusted context issuance, wire transport, issuer/audience/freshness/revocation or connection to either queue route. |
| `ops/control/sign_command.py` | `main` / `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Signs a node-bound operational command schema using per-node HMAC environment-variable names and timestamp freshness bounds. | Does not establish this as the task/mission ingress contract or bind a sensitive-operation approval attestation. |
| `astra_github_agent.py` | `main` / `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Verifies the corresponding `mediahub.astra.control-command.v1` envelope, freshness and command ID/execution markers. | Source alignment is not runtime proof and does not authorize direct local task dispatch. |
| `tools/sign_astra_command.py` | `main` / `a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8` | Emits a different `schema: 1` envelope with generic `ASTRA_COMMAND_HMAC_KEY`. | Canonical/active status and any relationship to Route B remain unknown. |
| WB-03 ingress gap packet | docs branch / `e2f13fe8250fedef02b27bb221072b582db1f3d1` | Enumerates ingress identity, trust, replay and schema gaps for Jarvis→A0. | Must not be reinterpreted as already covering direct-to-executor ingress. |
| WB-06 AuthorizationContext inventory | docs branch / `9bd850e869dbd19db9bde2ce08768aaf502c95a2` | Confirms a local typed authorization seam and separate HMAC command path. | Does not connect those seams into an end-to-end Jarvis→executor trust chain. |
| WB-07 ingress/command seam trace | docs branch / `89fab594f9a9ae9a729d63ecb14dad2543edc9af` | Distinguishes Task Contract ingress, P0 authorization and signed operational command paths. | Does not establish a direct local-executor producer or caller. |
| WB-09 owner/hardware integrity review | docs branch / `b8d6b71d4cdf3a860bca9bc955543fa412221264` | Records owner-reported hardware and the previously directed Jarvis→A0 route. | Is superseded only to the extent WB-10 adds a second owner-directed route; all unknown hardware facts remain unknown. |

## 3. Dual-route architecture contract — requirements, not implementation claims

| ID | Requirement | Route A: via A0 | Route B: direct local executor | Failure behavior / required evidence |
|---|---|---|---|---|
| RTE-01 Mission identity | Stable mission/task/request IDs, creator, parent mission, creation time and schema version. | Required | Required | Reject missing/conflicting identity; audit the rejection. |
| RTE-02 Route eligibility | Explicit policy decides route based on task scope, data class, required authority and executor profile. | A0 route selected | Direct route explicitly allowed | Unknown route eligibility fails closed; no implicit fallback. |
| RTE-03 Authenticated caller | Verify Jarvis workload identity and its allowed task-submission scope. | Verify at accepted A0 ingress | Verify at direct local ingress | Network reachability alone is not identity or trust. |
| RTE-04 Approval attestation | Sensitive approval binds approver, mission/task, action/resource, audience, expiry and revocation state. | Verified before sensitive action | Verified before sensitive action | Caller-supplied `approval_state` alone is insufficient. |
| RTE-05 Queue ownership | One lifecycle authority per queue; explicit boundary between mission coordination and execution lifecycle. | A0 owns A0 queue | Named local-queue owner must be decided and recorded | Reject split-brain/duplicate owner; no silent queue-state mirroring. |
| RTE-06 Claim/lease/fencing | Atomic claim, bounded lease, unique claim generation/fencing token and stale-worker rejection. | Required by A0 contract | Required by direct local queue contract | Stale claims cannot commit results or mutate queue state. |
| RTE-07 Idempotency/replay | Bind idempotency key to request payload digest, route and execution domain; define duplicate/conflict behavior. | Required | Required | Same ID/different payload is rejected; cross-route duplicate dispatch is denied absent explicit protocol. |
| RTE-08 Capability scope | Capability is issued by an authorized issuer, bound to subject/action/resource/audience and attenuated at delegation. | Verified by accepted chain | Verified by accepted chain for direct ingress | Missing issuer/provenance/scope/expiry/revocation state fails closed. |
| RTE-09 Execution isolation | Executor receives only scoped workspace, tools, network/egress and secrets required for the task. | Required | Required | Policy violation denies execution; secrets are not copied into task payloads/logs. |
| RTE-10 Cancellation/timeouts | Cancellation token and deadline propagate; executor acknowledges stop or records bounded inability to stop. | A0-owned semantics | Local queue owner semantics | Late results from cancelled/stale attempts are quarantined. |
| RTE-11 Retry/recovery | Explicit retryable error classes, attempt budget, backoff, worker-loss detection and restart recovery. | A0 owns A0 lifecycle | Local queue owner owns direct lifecycle | No unbounded retry or duplicate side-effect execution. |
| RTE-12 Result contract | Result binds mission/task/attempt/route/executor, source SHA, status, artifacts and evidence digest. | Publish through A0's accepted result path | Publish through a defined Jarvis/local-executor result adapter | Missing/mismatched provenance cannot be promoted as verified evidence. |
| RTE-13 Audit/observability | Correlation IDs and append-only decision events for route selection, auth, approval, claims, retries, execution and result. | Required | Required | Sensitive values redacted; clock uncertainty handled explicitly. |
| RTE-14 Authority separation | Neither route may mutate canonical Product State Authority except through its accepted consumer boundary. | Required | Required | Product state mutation outside the approved boundary is denied. |
| RTE-15 Resource policy | Per-route concurrency, CPU/RAM, disk, execution time and queue-depth limits are explicit. | A0 limits | Local executor limits | Saturation causes bounded backpressure, not silent task loss. |
| RTE-16 Route failure/fallback | Route failure semantics and any failover are explicitly approved and observable. | No implicit direct fallback | No implicit A0 fallback | No silent route switching; fail closed or enqueue a separately authorized retry. |
| RTE-17 Evidence promotion | Execution output is a candidate until the required independent checks pass. | Existing qualification gates remain | Same promotion policy; direct route cannot self-qualify | No executor self-promotion; preserve exact-SHA evidence. |

## 4. Queue lifecycle and authority model

The owner-directed architecture should keep three scopes separate:

1. **Mission coordination (Jarvis):** mission decomposition, dependency graph, global priorities, task creation, route eligibility request, result aggregation and mission-level status.
2. **Execution queue lifecycle (domain-specific):**
   - A0 owns queue/claim/lease/retry/cancel/recovery for Route A.
   - A separately named and accepted local queue controller owns the equivalent lifecycle for Route B.
   - The owner of the direct local queue is **NOT YET IDENTIFIED AS AN ACCEPTED CONTRACT**. Jarvis may request work, but must not become an implicit queue authority unless that role is explicitly designed and accepted.
3. **Canonical product state (MediaHub Product State Authority):** remains a separate authority; neither Jarvis, A0 nor a local executor gets product-state authority by implication.

This is a recommendation for contract closure, not a claim that the local queue controller already exists. The direct route should not be launched as an autonomous queue until its lifecycle owner, persistent state, atomic claims, fencing, recovery and audit contract are defined.

## 5. Required source/documentary closure

1. Identify candidate local executor(s) from tracked source and determine whether each is an execution backend, a queue controller, or both. Do not infer from filenames or capability labels.
2. Trace Jarvis task producer → route decision → direct ingress → local queue persistence → claim/lease → executor → result publication. Pin each edge to live refs and blob SHA.
3. Compare direct-route semantics with ASTRA queue contracts, qualification requirements, security invariants and the accepted owner direction (DEC-DEV-02 Option C). Preserve existing decision IDs; do not create a conflicting lifecycle authority.
4. Close issuer, verifier, audience, freshness, revocation, replay/idempotency, approval attestation, cancellation, retry and result provenance contracts.
5. Establish a hardware resource profile for the Mac mini 2018 before assigning direct local workloads. Keep the 2011 machine non-critical and unqualified until its OS/security/workload evidence is complete.
6. Draft the minimal normative contract change set only after explicit authorization. This artifact alone does not authorize source-code or normative-contract changes.
7. Define verification and qualification evidence separately from design review. No claim of successful execution until permitted tests and independent evidence exist.

## 6. Open blockers

- **B-01:** No accepted Jarvis → direct-local-executor ingress contract or tracked end-to-end caller trace established.
- **B-02:** Direct local queue lifecycle owner is not yet identified in an accepted contract.
- **B-03:** Existing ASTRA primary-source wording about “MediaHub State Authority” conflicts with established product-state separation; governance reconciliation remains required.
- **B-04:** Sensitive-operation approval provenance remains unresolved; current file-based `approval_state` is not itself attestation.
- **B-05:** The typed `AuthorizationContext` path and HMAC operational command path are not shown to compose into the direct route.
- **B-06:** Alternate signer helper schema/canonicality remains unknown.
- **B-07:** Exact OS, storage, network, resource envelope and target workload on Mac mini 2018 remain unknown; the 2011 machine is not qualified.
- **B-08:** No execution, test, qualification, deployment or independent acceptance evidence is claimed.

## 7. Explicit non-claims and safety boundary

- No code/runtime was changed; no tests, security scans, model/provider calls, credential use, host/runtime inspection, installation, infrastructure changes or deployment occurred.
- No branch merge/integration was performed.
- Source evidence is static and bounded; absence of a tracked caller in this trace is not proof of absence in external/generated/deployment contexts.
- Route B is owner-directed as an architecture requirement, but is not implemented, qualified or accepted.
- Baseline 2.0, product-state authority boundaries, historical decision IDs and Contour A → Contour B gate remain unchanged.

## 8. Next bounded step

WB-11: trace the concrete local executor and queue-controller candidates from the repository tree, then create a source-pinned Route B producer/consumer/lifecycle trace. Determine whether an existing component can satisfy the direct-route contract or whether the architecture must specify a new bounded adapter; keep implementation and qualification gated.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)


## Follow-up owner proposal clarification — WB-11 (2026-10-15)

The owner subsequently clarified that the particular workload topology is **a proposal, not the final structure**: ASTRA is intended for engineering work such as coding, while heavy local jobs such as video generation may be routed directly to Claude running on the local host called “Alamo”. This is not yet a selected or accepted topology.

See [WB-11 Proposed Alamo/Claude Heavy-Local-Workload Routing and Executor Source Trace](MEDIAHUB-CONTOUR-A-WB-11-PROPOSED-ALAMO-CLAUDE-HEAVY-LOCAL-WORKLOAD-ROUTING-AND-EXECUTOR-SOURCE-TRACE-2026-10-15.md), creation commit `8a8b3b037239bceb95668ff1e5dc757e8c706ef2`.

Important distinction: a Claude/Claude Code client running on Alamo does not by itself prove that model inference is local; repository sources contain both an external Anthropic credential path and a Claude-compatible local endpoint backed by Ollama. Actual Alamo identity, provider/model mode, media-generation backend and direct queue lifecycle owner remain UNKNOWN. The WB-10 direct route remains a general contract matrix, not acceptance of the specific Alamo proposal.
