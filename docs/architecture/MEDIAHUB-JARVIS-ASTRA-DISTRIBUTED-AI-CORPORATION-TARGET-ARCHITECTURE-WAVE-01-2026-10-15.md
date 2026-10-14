# MediaHub OS — Jarvis / ASTRA Distributed AI Corporation Target Architecture, Chat Synthesis Wave 01

- Date: 2026-10-15
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **CONSOLIDATED TARGET DESIGN / OWNER-DIRECTION RECORD / NOT A NORMATIVE CONTRACT / NOT IMPLEMENTATION EVIDENCE**
- Purpose: consolidate the architecture clarified in the owner conversation into one navigable scheme for roadmap planning and future contract work.
- Authority: explicit owner-approved decisions are distinguished from proposed design details and unresolved source reconciliation. Baseline 2.0 remains the canonical functional baseline. No product or runtime status is promoted by this document.

## 1. Executive architecture

The intended system is a **distributed AI corporation** with two cooperating but separate multi-agent systems:

1. **Internal MediaHub corporation** — Jarvis coordinates missions and routes work across admitted local, owned, provider-backed and future opt-in user-contributed executors. ASTRA remains a bounded engineering workflow/control subsystem, not the entire corporation. New specialist roles are added around Jarvis/ASTRA through explicit contracts rather than by turning ASTRA into a monolithic corporate agent system.
2. **External cloud executor/controller** — an external cloud-side executor may independently run its own ECC (Everything Claude Code) multi-agent controller and internal agents. MediaHub sees the external controller as one bounded executor and exchanges task requests/results through an approved interface. MediaHub does not manage its internal queue, credentials or agents; the external controller receives no authority over MediaHub canonical product state or ASTRA-owned workflow state.

Jarvis, ASTRA, Product State Authority, agents, executor nodes, gateways, providers and models are distinct identities and responsibilities. The architecture does not assume that every target component is already implemented or qualified.

## 2. Owner-approved decisions

### 2.1 DEC-DEV-02 — Option C: split lifecycle authority

The owner approved Option C.

- **Jarvis:** corporation-level mission coordination, planning, permitted route selection, executor selection and mission-result tracking.
- **ASTRA A0:** ASTRA-internal engineering workflow state under its accepted contract: queue, claims, leases, heartbeat/liveness, retry/cancellation, recovery and ASTRA evidence/gate transitions.
- **MediaHub Product State Authority:** sole canonical product-state mutation authority.
- Neither Jarvis, ASTRA, an LLM, a cloud executor, a user-contributed worker nor an adapter receives canonical product-state authority by implication.
- Jarvis must not create a competing ASTRA queue or mutate ASTRA-owned workflow state directly.

This owner decision resolves the choice; it does **not** by itself reconcile the broader “single MediaHub coordination and state authority” wording still present in primary ASTRA source documents. Controlled source reconciliation remains a tracked task.

### 2.2 Hybrid execution

The owner approved a hybrid execution model.

- Jarvis may directly dispatch bounded work to an eligible executor when that route is explicitly permitted and the task does not require ASTRA lifecycle controls.
- Engineering missions requiring ASTRA dependency tracking, queue/claim/lease/retry/cancellation, isolated workspaces, evidence gates or independent verification use the sourced ASTRA A0 interface.
- Direct dispatch is not a policy bypass. Authentication, capability scope, data classification, egress, audit, result validation and state-authority rules still apply.
- Video generation and other heavy specialized workloads are candidates for direct routing to a suitable local/cloud executor if capabilities, capacity and policy allow. This is not a claim that current hardware can execute a given video model.
- Local Mac Pro inference is preferred when suitable and permitted. `local-only` mode must fail closed; it must not silently fall back to cloud.

### 2.3 Corporation boundary and ECC

- ASTRA's current four-agent arrangement is a subsystem starting point, not the corporation-wide roster and not a proven maximum scale.
- Add future specialist roles outside ASTRA when a verified capability gap justifies them; do not duplicate ASTRA's controller/queue.
- ECC is intended, if later approved, to live on the external cloud executor's side as that executor's internal multi-agent controller. It is not proposed as a controller to install into the MediaHub core in this architecture.
- ECC status remains **NOT ASSESSED / NOT ADOPTED** until an authoritative upstream revision, license, provenance, security/side-effect profile, compatibility and overlap are reviewed. No installation/import is authorized by this document.

## 3. Logical topology

```text
User / client request
        |
        v
Jarvis — corporation mission coordinator
        |
        +-- Mission planner / task decomposition
        |       |
        |       +-- Dependency-aware task graph (proposed corporation contract)
        |       +-- Policy + capability + resource admission
        |       +-- Result tracking / integration requests
        |
        +-- Route A: bounded direct dispatch
        |       +-- Local executor adapter (Mac Pro / Alamo local model service)
        |       +-- Claude Code client -> compatible local backend route (Scenario B)
        |       +-- Other admitted executor adapters
        |       +-- Specialized workload executor (e.g. video), if qualified
        |
        +-- Route B: ASTRA A0 ingress
        |       +-- ASTRA-owned engineering queue / claims / leases / retries
        |       +-- isolated target-SHA workspaces
        |       +-- evidence gates / independent verification
        |
        +-- Route C: external cloud executor boundary
        |       +-- bounded mission/task request
        |       +-- cloud-side controller (ECC is a candidate, not adopted)
        |       +-- cloud-side internal agents / provider keys / own queue
        |       +-- bounded structured result + provenance
        |
        +-- Future Route D: opt-in user-contributed MediaHub workers
                +-- admission, isolation, limited capability, revocation
                +-- minimum necessary task payload; no central secrets
        |
        v
Result validation / integration / evidence
        |
        +-- ASTRA evidence/gate state where ASTRA owns the lifecycle
        +-- Product State Authority for canonical product-state mutations
        +-- Jarvis mission status (not a substitute for either authority)
```

This is a logical target topology, not a deployed network diagram. IP/port routing, service endpoints, authentication and protocol details must be sourced and qualified before implementation.

## 4. Executor and model roles

| Role | Target responsibility | Important boundary |
|---|---|---|
| Jarvis | Mission intake, planning, decomposition, policy-aware route selection, executor matching, result collection | Does not become ASTRA's queue owner or canonical product-state writer |
| ASTRA A0 | ASTRA engineering lifecycle and internal workflow state | Not the entire corporation; no duplicate authority beyond its accepted contract |
| Local Mac Pro / Alamo service | Preferred local inference executor when model/task/resources fit | Local inference is not itself proof of safe tool execution or autonomous mission control |
| Claude Code Scenario B | Client/tool surface configured to use a compatible local backend on Mac Pro | Does not mean the hosted Claude model runs locally; compatibility and route must be evidenced |
| Claude Code official-auth route | Separate supported configuration where owner chooses official Anthropic authorization | Must remain a distinct route and data-egress choice |
| Compatible corporate gateway route | Alternative Claude Code client path via compatible gateway | Must identify the actual upstream/backend; compatibility cannot be assumed |
| Other local LLM adapters | Direct local execution of approved models, e.g. Gemma/Qwen candidates | Model availability, license, runtime fit and quality are unverified until separately assessed |
| Provider-backed executors | Approved API-key-backed provider routes, quota/rate-limit-aware | Keys are managed as secrets; provider quotas and availability are not guaranteed |
| External cloud controller | Independent multi-agent system inside the cloud executor boundary; ECC is a candidate | One external executor boundary to MediaHub; no authority over internal MediaHub state |
| User-contributed MediaHub worker | Future opt-in remote compute for bounded tasks | Untrusted by default, isolated, revocable, policy-limited; no central secrets |

Model names such as Gemma 4 and Qwen are candidates, not locked choices. Provider/key aggregation must respect provider terms, quotas, rate limits, identity rules and data-egress policy. Do not assume an aggregate token volume is guaranteed. Never silently route restricted/local-only data to cloud.

## 5. Corporation mission lifecycle (target)

1. **Intake:** Jarvis receives a goal and creates a stable mission identity.
2. **Policy classification:** identify data class, egress constraints, permissions, budget, deadline and required verification.
3. **Decomposition:** break a large mission into bounded subtasks with explicit dependencies, expected artifacts and acceptance criteria. Do not split tasks that require shared mutable state or cannot be independently validated.
4. **Capability matching:** select eligible executors using supported task types, tool scope, model/backend identity, trust/admission, locality, capacity, health freshness, budget and policy.
5. **Route choice:** choose bounded direct dispatch for eligible work or ASTRA A0 for engineering work that requires ASTRA lifecycle controls. A cloud-side controller is one external executor, not a trusted authority.
6. **Admission and dispatch:** issue only a scoped task/capability, minimal payload, target revision, deadline and cancellation/retry policy.
7. **Execution:** workers produce artifacts and structured status; they do not self-approve their own work or change canonical product state.
8. **Result validation:** validate schema, provenance, digests, target revision, checks, limitations and policy. Remote results are untrusted data until validated.
9. **Integration:** combine only compatible outputs; detect conflicts and preserve blocked/partial/unverified/failed states. Engineering integration uses ASTRA gates when required.
10. **Authority-bound mutation:** only the authorized Product State Authority path may mutate canonical product state.
11. **Audit and recovery:** record non-secret routing and evidence, handle timeouts/cancellation/retry within bounded policy, and recover without assuming exactly-once execution.
12. **Mission closeout:** Jarvis reports outcome based on evidence, without promoting design to implementation, verification, qualification, release, deployment or acceptance.

## 6. Proposed task/result contract requirements

This section lists requirements for later schema work; it is not itself a wire schema.

### Mission envelope
- stable mission ID, idempotency key, schema revision;
- task objective and acceptance criteria;
- data classification / egress policy / permission scope;
- target repository/ref/SHA or other immutable input revision;
- budget, deadline, cancellation policy and retry ceiling;
- required evidence and verification profile.

### Task DAG node
- stable task ID, parent mission ID and dependency edges;
- explicit readiness and parallel-eligibility;
- executor capability constraints and allowed route classes;
- immutable inputs, output contract and artifact limits;
- scoped capability reference (never raw secret values);
- lease/timeout/retry/cancellation semantics where applicable;
- target revision/workspace isolation and integration gate.

### Executor profile
- stable executor ID and node identity;
- capabilities, protocol, supported operation/tool classes;
- locality, trust/admission state, permission scope and data classes;
- resource/capacity limits and health freshness;
- model/backend/provider identity where known;
- verification requirements, revocation state and audit metadata.

### Result envelope
- mission/task IDs, schema/policy revision, target SHA;
- executor/client/gateway/upstream/model identity as available;
- status: success, partial, blocked, failed, cancelled or unverified;
- artifact references, content digests and dependency inputs;
- checks performed and evidence references;
- limitations, warnings and provenance;
- start/end timestamps, retry/lease attempt identity and cancellation state;
- no embedded API keys, credentials or other secret values.

### Reliability semantics
- Use idempotency keys and replay detection where defined; do not promise global exactly-once execution.
- Bound retries, timeout, parallelism and output size.
- Lease expiry/recovery must not allow stale workers to mutate shared canonical state.
- Cancellation propagates where possible and records partial output.
- Failover is allowed only to an admitted route consistent with data policy; local-only work fails closed.
- Result integration is deterministic with explicit conflict handling and independent verification where required.

## 7. Security and trust model

- Reachability, IP address, port, VPN or mTLS alone do not grant operation authority.
- Authentication is distinct from authorization. Capabilities must be bound to issuer, principal, operation, resource/scope, lifetime and revocation.
- Model, agent, executor, worker node, gateway, upstream provider and authority must have separate identities.
- External/cloud and user-contributed workers receive only minimum necessary task data and scoped permissions; no central secrets or broad repository authority by default.
- Remote artifacts are untrusted until validated. An executor cannot approve its own unverified result when independent verification is required.
- Audit routing, selected executor/backend, policy decision, status, artifact digest and evidence references without logging secret values.
- No arbitrary provider fallback, public exposure of local model ports, or silent egress-policy downgrade.
- User-contributed MediaHub participation is future opt-in only and must be revocable.

## 8. Known source contracts to reuse, not duplicate

- ASTRA executor capability matrix: dependency readiness, claims/leases/heartbeat/recovery, bounded admission, target-SHA isolation and independent A3 verification within ASTRA scope.
- ASTRA governance contract: lease/heartbeat/timeout/retry/parallel-claim values are contractual parameters, not proof of runtime enforcement.
- MH-12: identity/capability/authorization/isolation and fail-closed semantics.
- MH-21: external compute is not external authority; egress must be explicitly permitted and remote results are data until validated.
- AI inference request schema: one inference request only; do not overload it as mission/DAG.
- Component evidence schema: component/gate evidence only; do not overload it as each task's result envelope.
- Jarvis adapter draft and corporation/DAG crosswalks: reuse candidate mission/task fields after checking accepted ingress and schema ownership.

## 9. Open reconciliation and blockers

1. Reconcile the primary ASTRA wording that calls A0 the “single MediaHub coordination and state authority” with the owner-approved lifecycle split and MH-12/MH-21. Preserve historical IDs, Baseline 2.0 and source lineage; do not silently edit.
2. Source the exact accepted A0 ingress/claim/lease/cancellation/replay interfaces and capability issuer lifecycle. Do not invent endpoints.
3. Reconcile existing agent registry, provider, executor, task and evidence schemas before proposing new IDs/schemas.
4. Trace non-secret route identity for Alamo/local model service, Claude Code variants, FCC/FreeLLMAPI or other router, Codex and cloud executors.
5. Assess ECC from an authoritative, revision-pinned upstream source, including license, provenance, security/side effects and overlap. Until then it is not adopted.
6. Keep Contour A deployment and independent acceptance as a gate before Contour B product development.
7. Validate actual Mac Pro model/runtime/video capacity separately; this document makes no hardware-performance claim.

## 10. Roadmap sequence

1. Source-crosswalk ASTRA authority wording, accepted A0 ingress and capability/security contracts.
2. Reconcile existing registries/schemas and preserve historical IDs.
3. Trace the route identity and policy matrix for local models, Claude Code modes, provider-backed adapters, Codex and external cloud executor.
4. Perform read-only ECC upstream assessment.
5. Draft versioned corporation mission/DAG/executor/result contracts with explicit lifecycle semantics.
6. Owner/governance review only for unresolved architecture/product decisions; routine technical details can be resolved by source evidence and policy.
7. Implement only after contracts and authority boundaries are reconciled; separately verify, qualify, release, deploy and accept each stage.

## 11. Evidence and status boundary

- This is a consolidated target-design document based on owner statements and repository source crosswalks.
- Owner-approved decisions: DEC-DEV-02 Option C; hybrid direct/A0 execution boundary; internal MediaHub corporation distinct from an external cloud-side ECC controller; local Mac Pro route preferred when suitable; Claude Code Scenario B as a compatible client-to-local-backend route; future user-contributed workers opt-in/untrusted-by-default.
- Proposed but not yet accepted as normative: corporation-wide mission/DAG/executor/result wire schemas and detailed selection/scoring policy.
- Unverified: runtime implementation, actual network endpoints, Claude Code compatibility, model performance, video generation capacity, ECC compatibility, provider quotas, and user-worker deployment.
- No installation, tests, model/provider calls, credentials, host/runtime inspection, qualification, infrastructure changes, deployment, merge, rebase or cherry-pick were performed in this documentation pass.
