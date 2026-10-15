# MediaHub OS — Contour A WB-13: Option C Route-Adapter Requirement, Failure and Verification Matrix

- Date: 2026-10-15
- Status: **DOCUMENTARY TRACE / PROPOSED SEAM ONLY / OWNER TOPOLOGY DECISION OPEN / NOT IMPLEMENTED / NOT TESTED / NOT QUALIFIED / NOT ACCEPTED**
- Inputs: WB-10 direct local-executor control matrix; WB-11 Alamo/Claude source trace; WB-12 topology options matrix; canonical ASTRA executor policy and current source tree on `main`.
- Scope: translate the proposed common Jarvis route adapter (Option C) into traceable requirements, component boundaries, failure controls and future verification evidence. Preserve Option A (Jarvis → A0) as the current governed baseline. Option B (direct Jarvis → Alamo) remains a candidate route, not an accepted exception.
- No normative contract, runtime code, workflow, infrastructure or branch integration is changed by this document.

## 1. Decision state

WB-12 compares:
- **A — ASTRA-only governed execution:** Jarvis submits execution tasks through A0.
- **B — ASTRA engineering + direct Alamo heavy-workload route:** Jarvis may directly submit eligible work to an Alamo-local queue.
- **C — ASTRA engineering + Alamo behind a common Jarvis route adapter:** a common dispatch contract routes work to execution domains while each domain retains its accepted lifecycle ownership.

**Recommendation for design exploration only:** develop Option C as the interface seam; retain Option A as the current governed baseline; keep Alamo as an optional execution domain. This is not an owner-accepted topology decision.

## 2. Source baseline and evidence limits

Source paths were read from `main` at HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`. Documentation WB-10/11/12 was read from `docs/mediahub-chat-tree-map-20261012`. These are source inspections only; no workflow/test/runtime behavior is asserted.

| Component / contract | Blob SHA | Source-backed fact | Gap relevant to Option C |
|---|---|---|---|
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | `da26185254d9954fcee204f81ecca129bf052e7c` | Canonical policy assigns global coordination/state, model/executor admission, leases/recovery, security/resource qualification and evidence ledger to A0/A3. | A shared adapter must not silently replace A0 authority for ASTRA-governed tasks; any boundary change needs governed reconciliation. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Reference queue has permanent pool `mh-dev-01`, `mh-dev-02`, `Voktors-Mac-mini.local`; queue state defaults under `/var/lib/mediahub-astra/queue`. | Alamo is not listed in this source-pinned pool; source alone does not establish current target placement or persistent-store safety. |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` | `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` | Routing schema is qualification-gated and declares executor-only clients/transports, including Claude-related routes. | Provider/transport labels do not establish Alamo identity, local model inference or media-generation capability. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Workflow inputs bind command, target SHA, task ID, node ID, executor and task payload. | Workflow presence does not prove live dispatch, authorization end-to-end, or a common route-adapter contract. |
| `.github/workflows/astra-local-claude-qualification.yml` | `7f7dc2d65481e2cc80a1db94b41a1e60ed117ffd` | Has a self-hosted qualification path and local Claude-compatible endpoint backed by Ollama/Qwen coder model. | Does not prove it runs on Alamo or qualifies a video-generation backend. |
| `.github/workflows/mediahub-claude-worker.yml` | `e1260cfef88ac02bcc9d0cce67bb497820f5f63c` | Uses an explicit metered-provider gate and `ANTHROPIC_API_KEY` for an external Anthropic worker path. | Not evidence of local model inference; provider egress differs materially from a local model runtime. |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Canonical governance contract defines ordered qualification gates and failure states. | Any new execution domain must map to applicable gates/evidence rather than claiming qualification by route selection. |
| WB-10 | `7dfe9fa64a688cb8b16b5782dc48fa87d7027474` | Defines direct-route controls: identity, approval, queue owner, fencing, idempotency, isolation, recovery and evidence. | General route matrix, not an implementation or Alamo acceptance. |
| WB-11 | `b34b50dc749cade5b32e6ed369fe5b430d1a788e` | Distinguishes external Claude client/provider from local Claude-compatible model-runtime possibility; actual media backend unknown. | Alamo host and inference/provider mode are not confirmed. |
| WB-12 | `87ce2d51c81d3e5c8dfe2517f61878d91a0e069a` | Compares three topologies and leaves owner decisions open. | Does not constitute owner selection of Option C. |

## 3. Proposed Option C logical boundary

The adapter is proposed as a **routing/contract boundary**, not a new global authority or execution queue:

1. **Jarvis mission coordinator** creates a mission, derives bounded tasks and requests a route under accepted policy.
2. **Common route adapter** validates envelope shape, stable identity, allowed route class and dispatch policy; records route decision/correlation; forwards to the selected domain. It must not mint capabilities, approve sensitive operations, mutate canonical product state or independently promote evidence.
3. **ASTRA A0 domain** remains the admitted queue/lifecycle authority for ASTRA engineering tasks and any task whose governance contract requires A0.
4. **Alamo domain (candidate)** may expose a bounded local queue/adapter for explicitly eligible heavy local workloads only after host identity, backend, owner, resources, security and recovery are defined and qualified.
5. **Execution workers** run within domain-specific scope; worker outputs are untrusted candidates until result validation and required independent verification.
6. **Result/evidence adapter** normalizes result metadata without erasing route, executor, model/provider, host, input/source revision or output digests. ASTRA-specific qualification evidence remains under its accepted evidence authority.
7. **MediaHub Product State Authority** remains separate. Neither Jarvis, the adapter, A0 nor a local executor obtains product-state mutation authority by implication.

### Invariants

- One authoritative lifecycle owner per queue/domain.
- Route selection does not itself authorize execution.
- No silent A0 bypass for tasks whose accepted contract requires A0.
- No silent external-provider fallback from a requested local-only task.
- No dispatch to two domains for the same task unless a reviewed cross-domain idempotency/fencing protocol explicitly permits it.
- A task/result preserves a stable identity and provenance across route changes.
- An executor cannot approve its own sensitive operation, qualify its own result or promote its own evidence.
- Unknown host, provider, capability, approval or route eligibility fails closed.

## 4. Requirement → contract → component → failure control → verification evidence

Verification entries below are **future evidence requirements**, not checks performed in WB-13.

| ID | Requirement / contract | Component boundary | Failure mode | Required control | Future verification evidence |
|---|---|---|---|---|---|
| C13-01 | Versioned mission/task/result envelope with stable IDs, parent mission, creator, payload digest and source revision | Jarvis ↔ adapter | Missing/colliding IDs or schema drift | Strict version/schema validation; reject unknown incompatible versions | Contract fixtures and compatibility matrix; recorded schema-version tests |
| C13-02 | Route eligibility is explicit, policy-based and auditable | Jarvis → adapter | Ineligible task sent to direct route | Allow-list by workload class, data class, authority requirement and executor profile; default deny | Decision-table tests for allow/deny and unknown values |
| C13-03 | ASTRA-governed tasks retain A0 admission | Adapter → A0 | Silent bypass of A0 gate | Route policy marks A0-required classes; adapter rejects direct override | Negative tests plus audit events proving rejected bypass |
| C13-04 | Direct Alamo route is unavailable until explicitly enabled and qualified | Adapter → Alamo candidate | Unqualified or wrong host receives tasks | Feature/policy gate tied to immutable host/executor profile and qualification evidence | Host identity mismatch and unqualified-node rejection evidence |
| C13-05 | Jarvis identity and task-submission scope are authenticated | Jarvis → adapter/domain ingress | Forged caller or network-reachability-as-trust | Accepted workload identity, audience binding, scoped authorization and revocation | Forged/expired/wrong-audience credential denial evidence; no secrets in logs |
| C13-06 | Sensitive approvals are independently verifiable and bound to action/resource/task | Approval authority → adapter/domain | Caller-supplied approval state or stale approval reused | Signed/otherwise verifiable attestation; scope, expiry, audience and revocation checks | Valid/invalid/replayed/expired/mismatched attestation cases |
| C13-07 | Capabilities are issued by a known authority and attenuated on delegation | Issuer → adapter → executor | Adapter or Jarvis self-grants rights | Separate authentication, authorization and capability checks; fail closed on unknown issuer | Issuer-to-verifier trace, scope-attenuation cases and revocation evidence |
| C13-08 | Exactly one queue lifecycle owner per execution domain | Adapter → A0 / Alamo queue | Split-brain queue ownership or duplicate state authorities | Adapter forwards commands; it does not shadow-author queue state; domain declares owner | Architecture contract and fault-injection evidence for concurrent claims |
| C13-09 | Atomic claims use leases/fencing and reject stale workers | Queue → worker → result store | Worker resumes after lease expiry and overwrites newer result | Monotonic claim generation/fencing token; conditional result commit | Stale-claim rejection and worker-loss/reclaim evidence |
| C13-10 | Idempotency is stable across retries and route decisions | Adapter/queue | Duplicate side effects after retry or reroute | Idempotency key bound to payload digest and execution domain; same key/different payload rejected | Duplicate delivery, conflict, timeout-after-commit and cross-route tests |
| C13-11 | Local-only data and model/provider egress are explicit | Adapter → Alamo backend | Sensitive data sent to external provider without approval | Per-route egress/data-class policy; no silent provider fallback; provider identity in audit | Network/egress policy evidence and forced-provider-unavailable behavior |
| C13-12 | Workload-specific capability and resource budgets are admitted before dispatch | Admission policy → executor | Video job starves coding workers or exhausts RAM/disk | Separate concurrency/queue-depth/CPU/GPU-memory/disk/deadline budgets and backpressure | Load/resource saturation tests; no cross-class starvation within declared SLO |
| C13-13 | Cancellation and deadlines propagate end-to-end | Jarvis → adapter → queue → worker | Cancelled/expired task continues or late result is promoted | Deadline/cancel token, bounded stop acknowledgement, stale-result quarantine | Cancel-before-start, cancel-in-flight, timeout and late-result cases |
| C13-14 | Retry and recovery behavior is bounded and documented | Domain queue owner | Infinite retries, lost task or duplicate side effect after restart | Retryable error taxonomy, attempt budget, backoff, durable state and restart recovery | Crash/restart, disk error, worker disappearance and retry exhaustion evidence |
| C13-15 | Results bind to task, route, host, executor/provider/model and artifacts | Worker → result adapter/evidence ledger | Unattributed or substituted output | Signed/hashed result envelope, output digests, input/source pin and status semantics | Tamper/mismatch tests and reproducible evidence verification |
| C13-16 | Engineering verification remains independent of implementation | ASTRA A2 → A3/evidence authority | Implementer self-accepts output | Separate verifier identity/process; exact target SHA; acceptance authority distinct from worker | Independence check, target-SHA binding and negative promotion tests |
| C13-17 | Canonical product-state writes remain behind the accepted consumer boundary | Any route → product-state consumer | Jarvis/adapter/worker writes authoritative state directly | Explicit authorized consumer and scoped mutation contract | Unauthorized-writer denial and audit trail |
| C13-18 | Logs and evidence are correlatable without leaking secrets | All components | Untraceable execution or credential/prompt leakage | Correlation IDs, redaction, retention/access policy, clock uncertainty handling | Redaction fixtures, audit completeness and incident reconstruction exercise |
| C13-19 | Route failover is explicit and observable | Adapter/domain queues | Silent external fallback or duplicate cross-domain dispatch | Policy-controlled failover with new authorized attempt identity and fencing | Provider/node outage tests and evidence of no silent fallback |
| C13-20 | Qualification/acceptance gates remain separate from design and implementation | Qualification authority | Design artifact or worker assertion treated as acceptance | Gate registry, immutable evidence bundle, independent reviewer and owner acceptance | Gate-by-gate dossier bound to exact SHA and recorded acceptance authority |

## 5. Failure scenarios that must be covered before qualification

- Adapter process restarts after recording route decision but before dispatch.
- Dispatch succeeds but acknowledgement is lost; retry arrives with same idempotency key.
- Same task ID arrives with a different payload digest.
- A0 or Alamo queue is unavailable; policy prohibits silent route substitution.
- Alamo hostname resolves to an unexpected node or node identity no longer matches the admitted profile.
- Local model runtime is unavailable; no implicit call to an external provider occurs for local-only tasks.
- Heavy media task saturates disk/memory and would starve engineering queue.
- Worker loses connectivity, lease expires, and old worker later returns with a result.
- Cancellation arrives after dispatch or after output creation.
- Approval is expired, revoked, wrong-audience, or bound to a different task/resource.
- Result is returned without host/provider/model identity or output digest.
- Adapter or worker attempts canonical product-state mutation outside the accepted boundary.
- Logs include credential material or sensitive task payload.
- Qualification evidence refers to a different source SHA, host profile or model/backend than the dispatched task.

For each case, the future verification plan must specify expected state transition, audit event, bounded time, retry/fallback rule and retained evidence. WB-13 does not execute these cases.

## 6. Owner decisions still open

| Decision | Options / facts needed | Current status |
|---|---|---|
| TD-01 Final topology | A, B or C; may be staged in phases | OPEN — no final choice |
| TD-02 “Alamo” identity | Exact physical host/profile and whether it is one of the two Mac minis | OPEN |
| TD-03 Claude execution mode | External Anthropic service via local client vs local model runtime | OPEN; materially different data/compute/security behavior |
| TD-04 Heavy-workload backend | Actual video-generation engine/model, version, accelerator and licensing | OPEN |
| TD-05 Direct queue owner | Named local lifecycle controller and durable state authority | OPEN |
| TD-06 Eligible task classes | Workload/data/authority classes allowed to bypass A0 coordination | OPEN |
| TD-07 Failover authority | Whether and when direct route can fall back to A0 or external service | OPEN; default recommendation: no silent fallback |
| TD-08 Adapter authority | Pure routing/validation boundary vs any additional orchestration; must not become a second global queue | OPEN; recommendation: bounded adapter only |

The user explicitly described the Alamo/Claude route as a proposal. These choices must remain PROPOSED/OPEN until explicitly accepted. Continue independent source review without treating silence as approval.

## 7. Verification and qualification status

- Documentary source pins: recorded above.
- Static contract/architecture matrix: drafted in WB-13.
- Cross-file normative contradiction reconciliation: **NOT COMPLETE**.
- Code implementation: **NOT STARTED / NOT AUTHORIZED BY THIS ARTIFACT**.
- Tests, failure injection, security scans, runtime checks: **NOT RUN**.
- Hardware and backend qualification: **NOT RUN / FACTS UNKNOWN**.
- Deployment: **NOT PERFORMED**.
- Independent acceptance: **NOT PERFORMED**.

No tests, provider/model calls, credential use, host/runtime inspection, installation, infrastructure changes, deployment, migration, merge, rebase or cherry-pick were performed.

## 8. Next bounded step

WB-14: build a source-pinned contradiction and ownership matrix across the canonical ASTRA executor policy, ASTRA reference architecture, unified system model, governance contract and existing queue/ingress implementations. Capture exact conflicting clauses and SHA; recommend minimal reconciliation options without editing normative sources. In parallel, preserve hardware/backend decisions as OPEN and the Option A baseline as current governed behavior.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
