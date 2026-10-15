# MediaHub OS — Contour A WB-11: Proposed Alamo/Claude Heavy-Local-Workload Routing and Executor Source Trace

- Date: 2026-10-15
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **OWNER PROPOSAL RECORDED / SOURCE TRACE PARTIAL / NOT AN ACCEPTED TOPOLOGY / NOT IMPLEMENTED / NOT QUALIFIED**
- Scope: record the owner's proposal that ASTRA should focus on engineering tasks (coding and related work), while heavy local workloads (example: video generation) may be sent directly to Claude running on the local machine called “Alamo”, without mandatory ASTRA A0 mediation. The owner explicitly says this is a proposal, not the final structure.
- This working document does not replace Baseline 2.0 or amend accepted normative contracts.

## 1. Owner proposal — not a final decision

The following is recorded as **PROPOSED / OPEN FOR ARCHITECTURE REVIEW**, not accepted:

1. ASTRA remains the specialized engineering execution system for software development, code changes, architecture/contract work and associated verification/evidence workflows.
2. A separate direct workload route may send eligible heavy local jobs to an executor hosted on the machine the owner calls **Alamo**, without passing through ASTRA A0's queue.
3. Claude / Claude Code is named as the proposed local execution client on Alamo. Heavy workloads such as video generation are examples of a workload class, not proof that Claude itself is the media-generation engine. The actual video-generation engine/backend is **UNKNOWN**.
4. Jarvis may act as mission coordinator and route-selection requester, but a routing proposal does not grant it executor, approval, product-state or queue-state authority.
5. The final structure may retain both routes, select one, or use a bounded adapter. No permanent topology decision is made in this document.

### Critical terminology distinction

“Claude running locally on Alamo” can refer to at least two materially different designs:
- a local client/agent process running on Alamo while using an external Claude/Anthropic service; or
- a local Claude-compatible interface backed by an on-machine model runtime (the repository contains a qualification workflow using an Ollama-backed Claude-compatible endpoint).

These are not equivalent for privacy, egress, compute, latency, cost, availability or model identity. The repository's existence of both patterns is not evidence that the proposed Alamo path currently runs either one. Until the owner’s intended execution mode and source-backed runtime evidence are clear, classify the route's **model location/provider/data egress as UNKNOWN** and do not label it “fully local”.

## 2. Source-pinned evidence

All source references below were read from `main` at HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`; this is static source evidence, not proof that the workflows ran or that any executor is available on the new hardware.

| Source | Blob SHA | Evidence | Limit |
|---|---|---|---|
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` | `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | Distinguishes Claude Code as a local execution client from Claude as a provider/gateway identity; defines A0 queue/claim/lease/dispatch/recovery and permanent executor lanes. | Does not prove the Alamo machine or the proposed direct heavy-workload route is registered or qualified. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | `da26185254d9954fcee204f81ecca129bf052e7c` | Defines A0 as global coordination/state authority, model/executor admission and resource qualification. | Canonical ASTRA workflow policy may constrain the proposal; bypassing A0 requires an explicit reconciled route contract, not a silent exception. |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` | `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` | Lists executor-only client/transport paths, including Claude-related paths; requires provider identity and timeout; executor identity mismatch is blocked. | The inventory does not prove Alamo is registered or that the proposed video-generation workload is supported. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Implements a bounded queue reference with a permanent executor pool including `mh-dev-01`, `mh-dev-02`, and `Voktors-Mac-mini.local`, with explicit executor/node binding. | Alamo is not shown in the inspected permanent pool. The pool may be historical/current implementation state, but cannot be assumed to match the new target topology. |
| `.github/workflows/astra-local-claude-qualification.yml` | `7f7dc2d65481e2cc80a1db94b41a1e60ed117ffd` | Includes a self-hosted executor qualification path and a Claude-compatible local endpoint backed by Ollama/model `qwen2.5-coder:3b`. | Workflow presence does not prove a current PASS, Alamo placement, or suitability for video generation. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Defines distributed worker dispatch for explicitly named executor/node pairs and bounded timeouts. | Does not show an accepted Jarvis → Alamo direct queue contract. |
| `.github/workflows/mediahub-claude-worker.yml` | `e1260cfef88ac02bcc9d0cce67bb497820f5f63c` | Defines a bounded Claude Code worker path using `ANTHROPIC_API_KEY` and explicit workflow gating. | This is an external-provider credential path, not evidence of fully local model inference. It is not proof that Alamo uses it. |
| `docs/checkpoints/mh-25-dual-local-executor-qualification-checkpoint-2026-10-02.md` | `12739de5ed8eacc400255505b93672281914c9c8` | Records a prior local-executor qualification checkpoint with some executor availability marked NOT_FOUND/BLOCKED/PARTIAL and no workflow PASS claimed for a relevant run. | Historical checkpoint; it cannot qualify the new target hardware or Alamo route. |
| `docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-10-JARVIS-DIRECT-LOCAL-EXECUTOR-ROUTE-AND-CONTRACT-EVIDENCE-MATRIX-2026-10-15.md` | `7dfe9fa64a688cb8b16b5782dc48fa87d7027474` | Defines a 17-control matrix for a direct local-executor route, including identity, approval, queue owner, lease/fencing, idempotency, isolation, recovery and evidence. | WB-10 is a general owner-directed route contract matrix, not acceptance of this specific Alamo/Claude proposal. |

## 3. Proposed workload classes and routing policy

The table below is a proposal for review, not an approved routing policy.

| Workload class | Proposed execution domain | Proposed path | Admission prerequisites | Status |
|---|---|---|---|---|
| Coding, refactoring, repository engineering | ASTRA engineering lane | Jarvis → ASTRA A0 → accepted engineering executor | Task contract, repository/worktree scope, authenticated executor, allowed tools, timeout, independent verification/evidence | ALIGNED WITH EXISTING ASTRA DESIGN; current target qualification unknown |
| Architecture/contract analysis | ASTRA engineering lane, with independent reviewer | Jarvis → ASTRA A0 → scoped executor → independent verification | Stable source pins, contract traceability, reviewer independence, no self-acceptance | PROPOSED CLASSIFICATION; route policy not requalified |
| Heavy local video/media generation | Alamo-hosted media executor, possibly coordinated by local Claude client | Jarvis route request → Alamo-local queue/adapter → media-generation backend | Exact backend/model, hardware/VRAM or unified-memory needs, disk/scratch, queue lifecycle, isolation, data locality, cancellation, quota and output validation | OWNER EXAMPLE / EXECUTOR UNKNOWN |
| Other heavy local batch work | Candidate local executor chosen by resource profile | Route decision → accepted executor-specific queue | Explicit capability/resource profile and qualification evidence | CANDIDATE ONLY |
| Tasks requiring ASTRA qualification gates, ASTRA queue state or engineering promotion | ASTRA A0 route | Jarvis → ASTRA A0 | Existing ASTRA governance/verification gates remain authoritative | DO NOT BYPASS WITHOUT EXPLICIT RECONCILIATION |
| Sensitive, privileged or product-state mutation tasks | Accepted authority-specific route only | No direct route unless contract explicitly permits | Verifiable approval and authority-specific consumer boundary | FAIL CLOSED WHILE UNRESOLVED |

## 4. Minimum requirements for a future Alamo direct route

Before this proposal can be accepted or implemented, the architecture needs:

1. **Node identity and profile:** owner-confirmed meaning of “Alamo”; exact machine model, OS/build, CPU/GPU or Apple Silicon/Metal capabilities, memory, storage, network and security-update lifecycle.
2. **Execution identity:** distinguish local Claude Code/client process, local model runtime, gateway/transport, and actual model/provider identity. Preserve the true provider and egress facts in evidence.
3. **Workload capability:** identify the actual video-generation engine and its model/version, accelerator requirements, license, input/output formats, scratch-space requirements, limits and qualification criteria. Do not infer video-generation capability from “Claude”.
4. **Queue ownership:** name the local queue lifecycle owner; define persistence, atomic claim, lease/fencing, duplicate suppression, idempotency, bounded retry, cancellation, worker loss and restart recovery. Jarvis may request dispatch but does not implicitly become a second authoritative queue controller.
5. **Security:** authenticated Jarvis caller, scoped task identity, approval attestation for sensitive actions, secrets isolation, network/egress policy, local data handling, and audit trail.
6. **Result contract:** bind result to task, route, Alamo node identity, executor/provider/model identity, exact input/source revision, output artifact digests, status and provenance.
7. **Resource admission:** prevent large video jobs from starving engineering tasks; set queue depth, concurrency, CPU/GPU/memory/disk quotas, deadlines, backpressure and preemption policy.
8. **Route failure semantics:** no silent fallback to a cloud provider or to A0; any failover is explicit, policy-controlled and auditable.
9. **Independent evidence:** executor qualification and workload-specific verification are separate from architecture approval; the executor cannot qualify its own output.
10. **Governance reconciliation:** align the proposal with the canonical executor matrix, A0 authority model, existing route decisions and product-state boundaries before changing normative contracts.

## 5. Open questions and blockers

- **AL-01:** What exact physical host is “Alamo”? Is it the 2018 Mac mini, the 2011 Mac mini Server, or another machine? Do not infer.
- **AL-02:** Does “Claude on Alamo” mean Claude Code running on Alamo and connecting to an external Anthropic service, or a local Claude-compatible model endpoint backed by a local model? Evidence currently shows both patterns exist in repository workflows, but does not tie either to Alamo.
- **AL-03:** Which actual video-generation engine/model will perform generation? Claude may coordinate a media backend; its presence alone does not prove generation capability.
- **AL-04:** Who owns the Alamo local queue lifecycle and persistent state?
- **AL-05:** Is the proposed direct route allowed to process only non-sensitive local media tasks, or a broader task class? The owner has not specified a final scope.
- **AL-06:** What hardware/software/data locality requirements apply to video workloads?
- **AL-07:** How does the proposed route reconcile with the current ASTRA executor matrix that assigns A0 global coordination/state authority and model/executor admission?
- **AL-08:** No current source trace proves Jarvis can dispatch directly to Alamo; no implementation, qualification or acceptance is claimed.

These are not blockers to continuing independent documentation review. They are blockers to selecting or qualifying the final topology.

## 6. Recommendation

Keep the architecture **pluggable and route-policy-driven** rather than hard-coding the proposed structure now:

- Keep ASTRA A0 as the governed engineering queue and its existing lifecycle authority for ASTRA engineering work.
- Treat direct Alamo execution as a candidate, separate execution domain for explicitly eligible heavy local jobs.
- Place a small, contract-defined route adapter/dispatcher between Jarvis and execution domains, without giving it product-state authority. If the owner ultimately wants Jarvis to enqueue directly without an adapter, that boundary must be explicitly defined and accepted rather than left implicit.
- Use one queue lifecycle owner per execution domain and a common mission/result/evidence envelope.
- Require explicit route selection, resource admission and no silent fallback.
- Defer final placement until the Alamo identity, model/provider mode, media backend and hardware profile are confirmed.

This recommendation is not an accepted owner decision and does not modify normative source contracts.

## 7. Explicit non-claims and restrictions

- No code was modified, no tests or qualification were run, and no model/provider was invoked.
- No credentials were used; no host/runtime inspection, installation, infrastructure change, deployment, migration, merge, rebase or cherry-pick occurred.
- Workflow files were read as source only. Their presence is not evidence of a successful run.
- Existing permanent executor mappings and previous qualification artifacts are not accepted as the target topology for new hardware.
- Baseline 2.0, historical decision IDs and the Contour A → Contour B acceptance gate remain unchanged.

## 8. Next bounded step

WB-12: create a proposal/decision matrix comparing (A) ASTRA-only execution, (B) ASTRA engineering + direct Alamo heavy-workload route, and (C) ASTRA + Alamo behind a common Jarvis route adapter. Compare authority clarity, queue/recovery complexity, data locality, resource isolation, verification/evidence, and migration cost. Keep all options marked PROPOSED until the owner explicitly selects one.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
