# MediaHub OS — Distributed Task DAG / Executor / Result Contract Crosswalk, Wave 01

- Date: 2026-10-15
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-ONLY CROSSWALK / DESIGN GAP RECORD / NOT AN ACCEPTED CORPORATION-WIDE CONTRACT**
- Scope: determine which existing MediaHub/ASTRA artifacts can be reused for Jarvis multi-agent task decomposition, parallel dispatch, worker leases, idempotency/cancellation, and result aggregation.
- Owner direction being reconciled: local Mac Pro models are the preferred route when suitable; Claude Code Scenario B targets a compatible client-to-local-backend route; Jarvis may decompose a large mission into dependency-aware subtasks and dispatch them concurrently to eligible local, approved provider, operator-owned, and future opt-in user-contributed executors. This records target direction, not deployed behavior.

## 1. Sources checked

| Source | Ref / blob SHA | Finding | Boundary |
|---|---|---|---|
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | documentation ref / `9ad83781a8da53d1a8f540ede54eba95281f01c0` | Canonical ASTRA executor-workflow policy explicitly covers task dependencies/readiness, claim/lease/heartbeat/recovery, bounded executor/model admission, target-SHA isolation, resource qualification, and independent A3 verification. | Applies to ASTRA's engineering workflow/control state. It does not by itself define a corporation-wide wire protocol or authorize Jarvis to write ASTRA internals. |
| `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md` | documentation ref / `e112cc73178eef5f71b8a814296e4902c2e80390` | Draft mission envelope already calls for stable mission ID, idempotency key, schema revision, target SHA, policy/data class, resource budget, cancellation/deadline, workspace lease, acceptance criteria and evidence schema revision. | Draft only; not an accepted wire schema and does not establish the exact ASTRA ingress API or capability issuer. |
| `schemas/ai/ai-inference-request.schema.json` | `main` / `e59c72b4a2a62b2372da57c6699ab12ebe25122f` | Existing v1.0.0 schema describes one AI inference request: request ID, provider/model, bounded operation, input, parameters and metadata. | It is not a mission/task DAG, executor profile, worker lease, cancellation contract, or structured result envelope. |
| `schemas/mediahub-component-evidence-record.schema.json` | documentation ref / `2e62a9d0174e2c72e23ac88edc3094d13b4e336a` | Draft v0.1 component/gate evidence record supports revision-bound component status, provider/model identity, source SHA, node, egress policy, qualification state and evidence references. | Component/gate evidence is not the per-task result envelope; status schema is draft and does not qualify components. |
| `architecture/MH-21-CHAT-MASTER-PROMPT.md` | `main` / `61d552db4d1a1abefa2cef9f44eebcf634d11111` | External compute may compute; MediaHub decides. Remote results are data, distributed compute creates no distributed State Authority, egress must be classified/authorized, arbitrary fallback/destinations are forbidden. | Governance invariants, not an execution protocol or implementation evidence. |
| `docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-RESPONSIBILITY-INTERFACE-MATRIX-WAVE-01-2026-10-15.md` | documentation ref / `d5934af98552ddee99ac5658dfffc8a3049f5cad` | Enumerates logical request→mission, mission→DAG, task→executor, worker admission, result envelope, integration/verifier and evidence interfaces. | Design reconciliation only; not an accepted normative contract. |

## 2. Reuse decision

1. **Reuse, within scope:** ASTRA's existing dependency-aware dispatch, lease/heartbeat/recovery, target-SHA isolation, bounded model admission and independent A3 verification rules for ASTRA-internal workflow.
2. **Reuse as a component contract:** the AI inference request schema for a single inference operation; do not overload it to represent a mission or multi-task job.
3. **Reuse as evidence substrate:** the component evidence record where its component/gate semantics fit; do not treat it as the structured output of each subtask.
4. **Do not duplicate or bypass ASTRA queue state:** Jarvis submits missions through a sourced, authorized A0 interface and consumes returned status/evidence. A0 remains the single writer for ASTRA-internal queue, claim, lease, retry/cancellation and gate state.
5. **Do not declare a corporation-wide DAG/result protocol already exists:** the checked artifacts provide useful partial fields and policy but do not form one accepted end-to-end schema covering heterogeneous executors and user-contributed nodes.

## 3. Gaps requiring a versioned proposal

- Agent/executor profile: stable identity, capability set, trust/admission class, locality, supported tools/protocols, resource profile, permission scope, health freshness, and verification requirements.
- Task DAG node and edges: stable task ID, immutable input/contract/base SHA, explicit dependencies, parallel eligibility, output contract, budget/deadline, retry ceiling, cancellation propagation, and integration gate.
- Idempotency and delivery semantics: per-operation idempotency key, replay behavior, lease expiry/recovery, duplicate execution handling, and explicit avoidance of a global exactly-once guarantee.
- Worker protocol: opt-in/admission, short-lived scoped capability, isolated workspace, minimal payload, resource caps, lease/heartbeat, result provenance, revocation, and no access to central secrets.
- Structured result envelope: mission/task IDs; target SHA and schema/policy revisions; executor/client/gateway/upstream/model identity where known; status; artifact references and digests; dependency inputs; checks; limitations; cancellation/partial-output state; verifier evidence; timestamps; and no secret values.
- Aggregation/integration contract: deterministic input set, conflict detection, version/contract compatibility, independent validation, and explicit blocked/unverified outputs.
- Failure policy: bounded retries, timeout, cancellation, provider/worker failover only when permitted, and fail-closed behavior for local-only or restricted-data tasks.

## 4. Required invariants

- Local Mac Pro inference is the preferred primary route when suitable and permitted; no silent cloud fallback in `local-only` mode.
- Claude Code is a client/tool surface, not proof that the Claude hosted model is running locally. Scenario B requires a compatible client-to-local-backend route and separate compatibility evidence.
- Model, agent, executor, dispatcher, gateway, upstream provider, worker node and authority are separate identities.
- User-contributed MediaHub nodes are future opt-in, untrusted-by-default workers; they receive only bounded, policy-approved tasks and minimum necessary data.
- Parallelism is conditional on dependencies, capacity, isolation, permissions and integration boundaries; no promise that every task can be split or that more agents always improve throughput.
- Remote results are untrusted data until validated. Neither a model nor a worker gains canonical product-state authority.
- Design, implementation, verification, qualification, release, deployment and acceptance remain distinct.
- No new schema is created in this pass. No tests, model/provider calls, credentials, installation, host/runtime inspection, qualification, infrastructure changes, deployment or branch integration occurred.

## 5. Next plan

1. Read the accepted ASTRA A0 queue/lease/claim/cancellation contracts and relevant security/identity contracts to pin the permitted mission-ingress boundary.
2. Reconcile existing agent registry/provider fabric schemas and ASTRA task schema fields against the gaps above; preserve existing IDs and avoid duplicate schemas.
3. Perform a read-only ECC (Everything Claude Code) upstream assessment only against confirmed gaps: exact source/version, license, provenance, security/side effects, compatibility and overlap with ASTRA's canonical capability matrix.
4. Prepare a **proposed** versioned corporation task/result contract and owner/governance review packet only after the source crosswalk is complete.
5. Do not install ECC, change runtime configuration, run tests/qualification, call providers, inspect hosts, merge/rebase/cherry-pick or begin Contour B product development under this pass.


## 6. Source-bound interface / field disposition — Wave 02 (2026-10-15)

- Status: **READ-ONLY TECHNICAL RECONCILIATION / SOURCE-BOUND / NOT A NORMATIVE CONTRACT**.
- Live refs at review: `main` HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`; documentation branch HEAD `bafe0fe4159e5117f2227bb83f676e4a9eaac64b`; compare `DIVERGED`, docs branch 1188 ahead / 3 behind main, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No branch integration is authorized or attempted.

### 6.1 Field-group disposition

| Field group | Existing source / revision | Established semantics | Authority owner | Status / disposition |
|---|---|---|---|---|
| Single inference request | `schemas/ai/ai-inference-request.schema.json@main`, blob `e59c72b4a2a62b2372da57c6699ab12ebe25122f` | One bounded inference operation with request ID, provider/model, operation, input, parameters and metadata | Authorized inference adapter under policy | Existing contract; reuse only for one inference call, not a mission or DAG |
| Component / gate evidence | `schemas/mediahub-component-evidence-record.schema.json@docs`, blob `2e62a9d0174e2c72e23ac88edc3094d13b4e336a` | Draft, revision-bound component/gate evidence and qualification references | Evidence producer plus independent gate/reviewer roles; no authority transfer | DRAFT v0.1; not a task-result envelope and not qualification evidence by itself |
| ASTRA task readiness / claim / lease / heartbeat / recovery | `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md@main`, blob `da26185254d9954fcee204f81ecca129bf052e7c`; documentation branch same path, blob `9ad83781a8da53d1a8f540ede54eba95281f01c0` | Dependency readiness, executor binding, claim conflict, capacity gate, lease/heartbeat/recovery, target-SHA isolation and independent A3 verification | ASTRA A0 within ASTRA engineering workflow | Reuse within ASTRA only; not a corporation-wide wire protocol |
| Mission envelope | `MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md@docs`, blob `e112cc73178eef5f71b8a814296e4902c2e80390` | Proposed mission ID/idempotency/schema revision, target SHA, policy/data class, budgets, cancellation/deadline, workspace lease, acceptance criteria and evidence revision | Jarvis proposes/submits; accepted ingress owner controls admission | DRAFT; do not serialize as accepted production traffic |
| Corporation task DAG | Wave 01 crosswalk and Wave 09 technical baseline, blobs `3669fb53d33d68e00186d40f3b4eaa6f9f5f0666` and `6ab5f244cb0d4e74ac2b26013c02502832170365` | Recommended immutable task nodes/edges, explicit dependencies, bounded attempts, declared outputs and validation | Jarvis plans; ASTRA A0 owns lifecycle for tasks admitted to ASTRA | No accepted corporation-wide schema found in checked sources; proposed only |
| Executor profile / worker admission | ASTRA capability matrix + Jarvis responsibility matrix blob `d5934af98552ddee99ac5658dfffc8a3049f5cad` | Capability/trust/admission class, locality, tool/resource limits, scoped authority, isolation and provenance are required design dimensions | Admission policy / capability issuer; executor cannot self-authorize | No accepted cross-corporation profile schema or issuer lifecycle found in checked sources |
| Task result / aggregation | Wave 01 crosswalk + Wave 09 technical baseline | Status, task/attempt/target SHA, output digests, dependency inputs, route identity, partial/cancel state, limitations and verifier evidence should be bound together | Executor emits untrusted result; coordinator validates; A0 resolves A0-managed terminal lifecycle; Product State Authority alone mutates canonical product state | No accepted corporation-wide result envelope found in checked sources |
| Capability / authorization | `docs/architecture/MH-12-security-architecture.md@main`, blob `cf4ebfd5bf471ca676f075c51d3a24906504e490`; `docs/architecture/MH-12-security-invariants.md@main`, blob `0609be9c3420070434014dad4529e4ccd46b0996` | Principal, issuer, operation, target, scope, constraints, provenance, lifetime and revocation context; authentication is not authorization; ambiguity fails closed | Governed security/capability issuer; not Jarvis itself by implication | Security design anchors exist; concrete issuer/delegation/revocation lifecycle remains unresolved |
| A0 ingress / fencing / cancellation race | Wave 07 source trace blob `52dcd76e1ceaf66ccee560a34eb17b5be4f73bbf`; owner direction blob `70376a2709e055972ceddc4a280d26992977213c` | Jarvis must use a sourced accepted ingress; A0 is sole writer of ASTRA internal queue/claim/lease/retry/cancellation/gate state | ASTRA A0 | No accepted Jarvis-facing ingress operation, capability issuer lifecycle, fencing primitive or cancellation/completion race contract was identified. A0-managed engineering submissions remain BLOCKED; no endpoint or token defaults invented |

### 6.2 Confirmed source conflict

The same capability-matrix path has different semantics by ref:
- `main@da26185254d9954fcee204f81ecca129bf052e7c` still labels A0 as “Global coordination/state” and “autonomous queue + claim/evidence state”.
- `docs/mediahub-chat-tree-map-20261012@9ad83781a8da53d1a8f540ede54eba95281f01c0` contains a scope clarification that “state” means ASTRA's engineering workflow/control state, not MediaHub canonical product state.

The narrower documentation-branch wording aligns with owner-approved DEC-DEV-02 Option C and the Product State Authority invariant. The conflict is **partially reconciled on the documentation branch, not reconciled on main**. Because refs are diverged and main changes/integration are not authorized, do not overwrite or merge either branch in this pass.

### 6.3 Technical defaults safely closed without owner escalation

1. Reuse each existing artifact only within its established semantic scope; do not overload the inference schema or component-evidence schema.
2. Keep mission, DAG/task, executor profile, task result and evidence reference as separate proposed schema concerns; no global exactly-once claim.
3. A0-required engineering work fails closed until the accepted ingress and issuer lifecycle are source-backed.
4. Until an accepted fencing/publication primitive exists, do not claim stale-worker publication is prevented or treat concurrent reassignment as safe.
5. Treat worker/model/provider outputs as untrusted data until schema, provenance, target SHA and independent validation are checked.
6. Keep route identity, upstream provider and fallback behavior UNKNOWN unless source evidence establishes them; `LOCAL_ONLY` must not silently fall back to cloud.
7. Keep all proposed wire schemas non-normative and implementation blocked pending existing governance/change-control gates.

These defaults are technical recommendations consistent with the checked contracts and owner-approved boundaries. They are not evidence of runtime enforcement or acceptance.

### 6.4 Next bounded step

Inventory existing schema files and stable IDs/version conventions across the relevant refs, identify producers/consumers and collision risks, and crosswalk any existing ASTRA task/agent/provider-fabric schema before drafting a new versioned proposal. Preserve the branch split and do not run tests, installs, provider/model calls, host inspection, qualification or infrastructure operations.
