# MediaHub OS — Contour A WB-14C: Existing ASTRA Queue vs Direct-Local Route B

- Date: 2026-10-15
- Status: **BOUNDED READ-ONLY QUEUE SOURCE COMPARISON / ROUTE B NOT IMPLEMENTED OR QUALIFIED**
- Parent: WB-14 source reconciliation; WB-14B ingress trace.
- Scope: compare the tracked ASTRA autonomous queue and claim store to the owner-directed Route B requirement (Jarvis → separate local executor queue → local executor). This is documentary source analysis only.

## 1. Result

The existing `runtime/mediahub_runtime/autonomous_queue.py` is an ASTRA-oriented distributed development queue, not evidence of a ready-made independent Alamo queue. Its permanent executor pool is hard-coded to three named lanes (`mh-dev-01`, `mh-dev-02`, `Voktors-Mac-mini.local`), and task selection requires `node_id` and `executor` to match that pool. Alamo is not a listed lane.

The queue delegates claim persistence and conflict checks to `ClaimStore` in `runtime/mediahub_runtime/agent_fabric.py`. Source defines claims with expiry, acquisition, heartbeat and release. The inspected code does not establish that this lifecycle can be independently owned by Jarvis/Alamo without conflicting with ASTRA's authority boundary, nor does it prove a Route B service, durable queue, or media workload adapter exists.

**Conclusion:** current source can inform a contract, but it does not satisfy Route B admission evidence. Do not fork or repurpose it by inference.

## 2. Source pins and direct observations

| Source | Ref / blob SHA | Observed | Does not establish |
|---|---|---|---|
| `runtime/mediahub_runtime/autonomous_queue.py` | `main` / `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | `PERMANENT_EXECUTOR_POOL` is a fixed three-entry mapping; `select_distributed_tasks` rejects nodes/executors outside it; `claim_for` creates an A2-BUILDER claim with bounded expiry; task processing uses `ClaimStore`, heartbeat, result files and completion/evidence records. | No Alamo entry, independent Route B owner, Jarvis ingress, cross-route fencing, explicit cancellation API, or accepted video executor contract is proven by this file. |
| `runtime/mediahub_runtime/agent_fabric.py` | `main` / `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | `ClaimStore` lists claims, checks path conflicts, acquires claims, rejects expired/conflicting claims, heartbeats active claims and releases claims. | A claim store is not itself a full mission queue or proof of process-death recovery, cancellation propagation, or cross-route idempotency. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | `main` / `9ad83781a8da53d1a8f540ede54eba95281f01c0` | Assigns ASTRA queue/claim/lease/heartbeat/recovery and evidence/gate transitions to A0 within its engineering scope. | Static role assignment is not runtime qualification or authority to make A0 the corporation-wide mission authority. |
| WB-10 direct route matrix | docs branch / `62101df270acd1f4e551a8fcaf69f1fe741a8b51` | Route B is a separately bounded owner-directed architecture option and requires its own queue lifecycle owner, policy and result adapter. | Does not prove Route B implementation. |
| WB-12 topology decision matrix | docs branch / `87ce2d51c81d3e5c8dfe2517f61878d91a0e069a` | Compares topology options and calls out cross-domain identity, fencing and result/evidence contracts. | Does not select or qualify a specific Alamo topology. |

## 3. Route B capability comparison

| Control | Existing ASTRA queue evidence | Route B status |
|---|---|---|
| Node/executor admission | Fixed allow-list of three node/executor pairs | **BLOCKED** — Alamo absent; admission contract absent |
| Queue/lifecycle owner | ASTRA queue plus ASTRA claim store | **OPEN OWNER DECISION** for a separate local queue |
| Stable task identity | Task IDs and request IDs exist in different seams | **PARTIAL** — common corporation mission identity and cross-route uniqueness not demonstrated |
| Claim/lease | Claim expiry and heartbeat primitives exist | **PARTIAL** — semantics cannot be presumed reusable; fencing/token ownership and restart behavior need explicit contract |
| Duplicate suppression | Duplicate request IDs rejected within one FileTaskIngress batch; queue has task completion checks | **PARTIAL** — not cross-route idempotency or atomic route fencing |
| Retry | Queue worker logic includes bounded processing behavior, but reviewed surface does not establish a Route B retry contract | **OPEN** — attempt budget, backoff, terminal states and safe replay need definition |
| Cancellation | No explicit Route B cancellation protocol established in reviewed queue/claim interface | **OPEN** |
| Restart/recovery | ASTRA has claim expiry and recovery-related queue behavior | **PARTIAL** — not evidence for independent Alamo process recovery or orphan reconciliation |
| Result/evidence | ASTRA queue writes result/completion/evidence artifacts | **PARTIAL** — no accepted Jarvis common result envelope/adapter for Route B |
| Provider/egress/data locality | Queue lane label `claude` does not prove inference locality | **OPEN** — provider, endpoint, model and egress policy must be explicit |
| Media workload/resource gate | No qualified Alamo video backend or resource envelope established | **BLOCKED** |
| Product state authority | Queue claims are engineering coordination state, not product authority | **INVARIANT** — Product State Authority remains separate |

## 4. Contract gaps before any implementation proposal

1. Name the Route B lifecycle owner and define the exact state machine, durable storage boundary and restart-reconciliation behavior.
2. Define a corporation-wide mission ID plus attempt ID, route ID, executor identity and input/source revision; specify idempotency scope across A0 and Route B.
3. Define atomic claim/lease/fencing semantics, including stale-worker rejection and ownership of cancellation/retry transitions.
4. Define retry budget, backoff, terminal failure classification, cancellation acknowledgement and orphan handling.
5. Define a versioned result/evidence envelope binding mission, attempt, route, executor, provider/model mode, inputs, artifact digests, logs and verifier disposition.
6. Admit Alamo only after host identity, actual provider/inference mode, workload backend, resource envelope, data-egress constraints and required isolation are specified and independently qualified.
7. Preserve the owner’s topology choice as open: WB-12 options remain a decision matrix, not an accepted selection for Alamo.

These are contract requirements/gaps, not implementation instructions. No architecture decision is made here.

## 5. Verification boundaries

- Read-only source/document review; no code or normative contract modified.
- No tests, qualification, model/provider calls, credentials, host/runtime inspection, installation, infrastructure changes, deployment or branch integration.
- Source claims are limited to the pinned files; no claim of repository-wide absence or exploitability is made.
- Route B remains **NOT IMPLEMENTED / NOT QUALIFIED / NOT ACCEPTED**.

## 6. Next bounded sub-request

**WB-14D — Cross-route lifecycle controls:** reconcile stable mission identity, idempotency, owner/lease/fencing, cancellation, retry, restart recovery and result provenance across Jarvis, ASTRA A0 and the proposed direct-local route. Keep unresolved semantics explicitly open.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
