# MediaHub OS — Chat-to-GitHub Synchronization: Owner Decisions and Corporation Target Direction

- Date: 2026-10-15
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **OWNER-DECISION RECORD / TARGET-DESIGN DIRECTION; NORMATIVE SOURCE RECONCILIATION STILL REQUIRED**
- Purpose: preserve the user's explicit decisions and architectural direction from the current conversation so later chats can resume from GitHub rather than conversational memory.
- This record does not claim that any component is installed, implemented, tested, qualified, deployed or accepted at runtime.

## 1. Explicit owner decision: DEC-DEV-02 lifecycle split (Option C)

The owner explicitly approved the recommended Option C: split lifecycle responsibility into disjoint, typed domains.

1. **Jarvis** is the corporation-level mission coordinator: receives goals, plans work, selects permitted execution routes and eligible executors, and tracks results through defined interfaces. This is a target responsibility, not proof of an autonomous deployed Jarvis service.
2. **ASTRA A0** owns ASTRA-internal engineering workflow state under its accepted contract: queue/claim/lease/heartbeat/retry/cancellation and ASTRA-specific evidence/gate transitions. Jarvis must not create a competing ASTRA queue or mutate ASTRA-owned state directly.
3. **MediaHub Product State Authority** remains the sole canonical product-state mutation authority. Neither Jarvis, ASTRA, an LLM, an external provider, a cloud worker nor a GitHub adapter gains that authority by implication.

This records the owner's approval of the lifecycle split. It does **not** silently rewrite primary normative ASTRA prose that still uses broader “single coordination and state authority” wording. That source-level wording must be reconciled through controlled documentation change, preserving the accepted authority boundaries and Baseline 2.0.

## 2. Hybrid execution direction

The owner approved a hybrid execution approach, subject to the above authorities and policy:

- Jarvis may directly dispatch bounded work to an eligible local or external executor when the operation is explicitly permitted and does not require ASTRA's engineering lifecycle controls.
- Engineering missions that require dependency tracking, claims/leases, isolated workspaces, retries/cancellation, evidence gates or independent verification should be submitted through the sourced ASTRA A0 interface.
- A direct route is not a policy bypass. Authentication, capability scope, data classification, egress policy, audit, result validation and Product State Authority constraints still apply.
- A heavy specialized workload such as video generation is a candidate for direct routing to an eligible local or cloud executor if policy/capability/resource admission permits; this is not a claim that any current machine can perform it.
- Local Mac Pro inference remains the preferred route when suitable and permitted. `local-only` must fail closed without silent cloud fallback.

The exact accepted A0 ingress API and capability issuer/lifecycle must be sourced before implementation; do not invent endpoints or duplicate ASTRA queue state.

## 3. Two distinct multi-agent systems

The owner clarified the intended architecture as two cooperating but separately governed multi-agent systems:

### Internal MediaHub corporation
- The corporation is developed around Jarvis, ASTRA's existing engineering control, and additional specialized agent/executor roles connected by explicit interfaces.
- ASTRA is **not** to be expanded into the entire corporation. Its existing four-agent arrangement is treated as the current ASTRA subsystem, not as the corporation-wide agent roster or a proven scaling limit.
- New corporate roles should be added outside ASTRA when needed, using a registry/adapter/dispatcher design rather than duplicating ASTRA's internal controller.
- The number and identity of future agents are not fixed here; admit roles based on capability gaps, contracts, evidence and owner-approved policy.

### External cloud executor and its own controller
- The owner proposes that the external cloud executor may run its own ECC (Everything Claude Code) multi-agent controller **on the executor's side**.
- That external controller orchestrates its own local-to-that-executor agents; MediaHub treats the cloud service/controller as one external executor boundary and communicates through a bounded task/result contract.
- MediaHub does not take over the external controller's internal queue, agents, credentials or state. The external controller does not gain authority over MediaHub's canonical product state or internal ASTRA state.
- ECC remains **NOT ASSESSED / NOT ADOPTED** until an authoritative upstream revision, license, provenance, security/side-effect profile, compatibility and overlap with ASTRA are reviewed. This record does not authorize installation or import.

## 4. Task decomposition and result integration target

The corporation should support large missions decomposed into dependency-aware subtasks and concurrent execution where safe.

- Model, agent, executor, gateway, provider and authority are separate identities.
- Parallelize only tasks whose dependencies, data policy, capacity, isolation and integration boundaries permit it.
- Each task should have a stable identity, bounded objective, input/target revision, acceptance criteria, budget/deadline, cancellation/retry rules and expected result format.
- Results must identify provenance, artifacts/digests, status, checks, limitations and relevant evidence; remote results are untrusted until validated.
- Integration must detect contract/interface conflicts and preserve “blocked”, “partial”, “unverified” and “failed” as distinct states.
- Reuse existing ASTRA queue/lease/recovery and verification mechanisms within ASTRA's scope. Do not invent a second ASTRA queue or repurpose the single-inference schema as a mission DAG.

The corporation-wide DAG/result protocol remains a proposed gap to reconcile against existing schemas before drafting anything new.

## 5. Claude Code and local model route

- Owner-selected Scenario B: Claude Code is a client/tool surface configured to use a compatible local model backend on Mac Pro through the intended local gateway.
- This does not mean the hosted Claude model itself runs locally.
- Preserve separate configurations/routes for official Anthropic authorization, a compatible gateway to a local backend, native local LLM execution and other admitted executor adapters.
- Route identity, authentication and evidence must remain separate; no silent cloud fallback in local-only mode.
- No compatibility, runtime or route qualification is claimed by this record.

## 6. Next work, in order

1. Update the DEC-DEV-02 record/register and map so Option C is recorded as owner-approved, while tracking remaining normative source wording as a controlled reconciliation item rather than leaving the decision itself ambiguous.
2. Read the exact accepted ASTRA A0 ingress/claim/lease/cancellation/replay and security/capability issuer contracts; do not invent an API.
3. Reconcile existing agent registry, provider gateway, executor, task and evidence schemas; preserve historical IDs and avoid duplicates.
4. Resolve non-secret route identity for Alamo/runtime, FCC, FreeLLMAPI and other routers, Codex, and Claude Code route variants.
5. Assess ECC from an authoritative, revision-pinned upstream source only; no install/import until the source, license and security/side-effect review is complete.
6. Prepare a proposed versioned corporation task/result contract after the source crosswalk, then request owner approval only for genuinely architectural/product choices.
7. Keep Contour A deployment and independent acceptance as a gate before Contour B product development.

## 7. Safety and status boundary

No installation, tests, model/provider calls, credentials, host/runtime inspection, qualification, infrastructure change, deployment, merge, rebase or cherry-pick is authorized or claimed by this record. Documentation branch only. Normative contracts and Baseline 2.0 are not silently changed by this synchronization.
