# MediaHub OS — Contour A WB-12: Execution Topology Options and Decision Matrix

- Date: 2026-10-15
- Status: **OPTIONS ANALYZED / OWNER DECISION NOT REQUESTED YET / NO TOPOLOGY ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED**
- Inputs: owner direction recorded in WB-09; direct local executor route matrix in WB-10; Alamo/Claude proposal and source trace in WB-11.
- Scope: compare three plausible execution topologies without choosing the final architecture on the owner's behalf. This is a documentary architecture pass only.

## 1. Decision boundary

The owner has said that ASTRA should be used for engineering tasks such as code writing and related work, while heavy local jobs such as video generation might be sent directly to Claude running on a machine called “Alamo”. The owner explicitly characterized this as a proposal, not a final structure.

Therefore, **no topology is accepted by WB-12**. In particular:
- “Alamo” has not yet been tied to an exact host identity/profile.
- “Claude on Alamo” could mean a local Claude Code client using an external Anthropic service or a local Claude-compatible endpoint/model runtime; these have different egress, privacy, compute and reliability properties.
- The actual video-generation backend is unknown. Claude may be a coordinating client rather than the media-generation engine.
- The canonical ASTRA executor policy currently assigns A0 global coordination/state and executor/model admission responsibilities. A direct route needs explicit reconciliation with that contract, not a silent bypass.
- No implementation, test, qualification, deployment or acceptance is implied.

## 2. Options

### Option A — ASTRA-only governed execution
Jarvis submits all autonomous execution work through ASTRA A0. A0 performs admission and queue lifecycle, selects a qualified executor/model, and routes engineering and eligible media jobs through accepted executor lanes.

**Advantages**
- One established governance/admission boundary and one principal queue lifecycle for autonomous work.
- Simpler audit, idempotency, recovery and result-evidence path than multiple independent queues.
- Fits the current canonical ASTRA executor matrix with the least topology divergence.

**Costs/risks**
- May couple heavy media workloads to engineering queue capacity unless strong resource partitioning and scheduling are added.
- A0 becomes a bottleneck if its throughput or executor integrations do not match the workload.
- Does not by itself prove a video-generation engine is available or qualified.

**Required closure**
- Show that the selected media backend is supported and qualified; define per-class resource quotas and starvation prevention; verify A0 admission, recovery and result contracts.

**Status:** viable baseline/reference option; not accepted as the final topology.

### Option B — ASTRA engineering + direct Alamo heavy-workload route
Jarvis uses ASTRA A0 for engineering tasks, while eligible heavy local jobs go directly to a queue/executor on Alamo without A0 queue coordination.

**Advantages**
- Can isolate heavy local media workloads from engineering queue capacity.
- May reduce transfer of large media inputs/outputs if data and backend are truly local to Alamo.
- Allows a specialized media execution lifecycle without requiring every workload to use ASTRA's executor lanes.

**Costs/risks**
- Creates a second execution-queue lifecycle and requires a separately owned admission, claim/lease/fencing, retry/cancel/recovery, audit and result-evidence contract.
- Current ASTRA source pins do not show Alamo in the permanent executor pool or establish an end-to-end Jarvis→Alamo caller.
- Easy to confuse a local Claude client with a locally hosted model; an external Anthropic path may send task content outside the machine.
- Highest risk of duplicated task execution, split-brain state, inconsistent approval enforcement or bypassed ASTRA qualification if boundaries remain implicit.

**Required closure**
- Identify Alamo and its actual local/cloud execution mode; name the local queue lifecycle owner; establish direct ingress identity and approval/capability provenance; define route idempotency/fencing and result adapter; reconcile A0 authority wording and qualify the actual media backend.

**Status:** explicitly owner-proposed candidate; not accepted, implemented or qualified.

### Option C — ASTRA engineering + Alamo through a common Jarvis route adapter
Jarvis expresses mission intent and a routing request. A small governed dispatcher/adapter chooses either the A0 engineering route or the Alamo media route. Each execution domain keeps its own internal queue lifecycle, but both use common mission identity, admission-policy inputs, approval envelope, result schema, audit correlation and evidence-promotion rules.

**Advantages**
- Separates mission coordination from execution-domain mechanics.
- Supports resource-based routing and prevents a silent route switch or provider fallback.
- Can provide consistent audit and result/evidence semantics across execution domains while preserving Alamo's independent media queue if needed.
- Can evolve as the final topology becomes clearer.

**Costs/risks**
- Adds an adapter and another contract boundary that must be secured and maintained.
- Does not remove the need for a local queue owner or A0 governance reconciliation.
- If the adapter is allowed to mutate canonical product state or issue privileges, it becomes an unsafe new authority; scope must remain narrow.
- Requires explicit policy for who makes the final route decision (Jarvis request, policy decision point, or owner-approved configuration).

**Required closure**
- Define adapter's non-authoritative role, route policy and deny/fail-closed semantics; maintain one queue owner per execution domain; define shared task/result/audit envelopes; independently qualify each backend.

**Status:** recommended architecture option for further design because it preserves optionality while keeping execution-domain boundaries explicit; still only a recommendation, not an owner decision.

## 3. Comparison matrix

Ratings are qualitative design assessment, not measured performance. “Lower” means less complexity/risk under the currently known evidence, not zero risk.

| Criterion | A: ASTRA-only | B: direct Alamo route | C: shared Jarvis route adapter |
|---|---|---|---|
| Authority clarity | High alignment with current ASTRA policy | Low until local queue owner and A0 exception are governed | Potentially high if adapter is non-authoritative and contracts are explicit |
| Queue/recovery complexity | Lower: one main lifecycle | Highest: independent A0 and local queue lifecycles | Medium-high: separate domain queues, common envelope/policy |
| Engineering workload isolation | Depends on A0 resource quotas | High potential isolation | High potential isolation with policy-managed route |
| Heavy media workload suitability | Unknown until backend admitted to ASTRA | Potentially strong if Alamo/backend are capable | Potentially strong, with explicit resource admission |
| Data locality | Depends on selected executor/provider | Best only if input, model/backend and outputs are genuinely local; otherwise unknown | Policy can select based on data class and egress constraints |
| External provider/egress clarity | Existing executor/provider policy can govern, but must preserve actual provider identity | Most ambiguous until “Claude local” semantics are resolved | Strong potential with explicit per-route provider/data-flow declarations |
| Duplicate/replay control | One primary queue boundary, still needs idempotency | More difficult across two domains | Shared mission IDs and route fencing can improve control, but require implementation |
| Result/evidence consistency | Existing ASTRA gates are the reference | Requires a direct-route result adapter and same promotion bar | Common result/evidence contract can normalize both routes |
| Migration cost | Lowest topology change | Medium-high: new direct route and queue controls | Highest initial design/integration cost; may lower future topology migration cost |
| Fit with current source evidence | Best fit | Weakest: Alamo direct route not found in permanent pool | Moderate: adapter itself is not established but can preserve existing A0 path |
| Main blocker | Media backend admission and resource isolation | Direct ingress, queue ownership, local/cloud mode, policy reconciliation | Adapter authority/scope, route policy, queue-domain contracts |
| Overall current assessment | Safe reference baseline | Possible specialized option but evidence gaps are material | **Recommended option to design next**, not accepted final structure |

## 4. Recommendation — preserve options with Option C as the design target

Recommendation for further architecture work: **design Option C as the integration seam**, while preserving Option A as the initial governed baseline and Option B as a possible execution-domain behavior behind explicit route policy.

Rationale:
1. It does not force heavy media tasks through ASTRA's engineering queue if the evidence later supports an Alamo-local execution domain.
2. It avoids making Jarvis itself an implicit second queue/state authority.
3. It preserves A0's current ASTRA governance for engineering tasks.
4. It makes local-versus-external model/provider/data flow an explicit routing property.
5. It requires each domain to have one lifecycle owner and a common mission/result/audit envelope, reducing accidental divergence.

This is not a request to implement the adapter now and is not a final owner decision. If the owner later chooses Option A or B, the design can be updated before implementation.

## 5. Hard gates common to all options

- **Identity:** authenticated caller and executor/node identity; network reachability is not identity.
- **Approval:** sensitive actions require a verifiable attestation bound to task/action/resource/audience/expiry; a task-supplied boolean/string alone is insufficient.
- **Capabilities:** explicit issuer, scope, attenuation, expiry/revocation and consumer enforcement.
- **Queue:** durable state semantics, atomic claims, leases/fencing, idempotency, bounded retries, cancellation, duplicate handling and restart recovery.
- **Resource admission:** CPU/GPU/memory/disk, concurrency, deadlines, backpressure and workload-class isolation.
- **Data and provider flow:** record actual model/provider, endpoint and egress; “client runs locally” does not imply “model inference is local”.
- **Evidence:** results bind to task, route, executor/node, model/provider, source/input revision and artifact digests; executor cannot self-qualify or self-accept.
- **Authority separation:** no route or adapter acquires MediaHub Product State Authority by implication.
- **Rollout:** no Contour B product development before Contour A deployment and independent acceptance gates are satisfied.

## 6. Owner-decision register (not yet resolved)

| Decision ID | Decision needed | Options | Recommendation | Current state |
|---|---|---|---|---|
| TD-01 | Which topology is the target design? | A / B / C | C for design, retain A as baseline and B as optional domain route | PROPOSED; owner has not selected |
| TD-02 | What is Alamo? | 2018 Mac mini / 2011 Mac mini Server / another host | Do not infer; identify exact host and profile | UNKNOWN |
| TD-03 | What does “Claude on Alamo” mean? | External Claude/Anthropic service via local client / local Claude-compatible model runtime / other | Record exact runtime/provider/egress; avoid “fully local” label without proof | UNKNOWN |
| TD-04 | What engine generates video? | Existing media backend / new backend / external service | Identify actual engine/model and qualification requirements | UNKNOWN |
| TD-05 | Who owns Alamo queue lifecycle? | Dedicated local queue controller / another explicitly named owner | One explicit owner, with Jarvis only requesting dispatch unless separately authorized | OPEN |
| TD-06 | What jobs can use direct route? | Media-only / wider resource-based classes | Start with narrowly eligible non-sensitive local media jobs until policy is proven | PROPOSED |
| TD-07 | Who authorizes route changes/failover? | Owner-approved policy / governed policy service / other | No silent failover; route choice must be auditable | OPEN |

## 7. Source baseline and limitations

WB-11 records source pins for the ASTRA unified architecture, canonical executor matrix, executor routing inventory, autonomous queue and Claude-related workflows. Those files demonstrate that:
- ASTRA's canonical matrix assigns A0 coordination/admission duties.
- The reference queue names `mh-dev-01`, `mh-dev-02`, and `Voktors-Mac-mini.local`, not Alamo.
- The repository contains both an external Anthropic API-key worker path and a Claude-compatible local Ollama endpoint.
- Neither workflow presence nor historical qualification records prove that Alamo is running either mode, nor that a media-generation engine is qualified.

Static source review only. No tests, qualification, model/provider calls, credentials, host/runtime inspection, installation, infrastructure change, deployment, merge, rebase or cherry-pick occurred.

## 8. Next bounded step

WB-13: build a source-pinned requirement-to-contract-to-component-to-failure-control-to-verification matrix for the recommended Option C seam, while preserving Option A as the existing governed baseline. Identify which controls are already evidenced by current source, which require a new contract, and which require explicit owner/governance decisions. Do not implement the adapter or amend normative contracts in that pass.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
