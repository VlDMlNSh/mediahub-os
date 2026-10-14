# Jarvis / ASTRA reconciliation against owner decision D-03

- Date: 2026-10-14
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: SOURCE-ONLY DOCUMENTARY RECONCILIATION / DRAFT FINDINGS / NOT A NEW CANONICAL CONTRACT
- Scope: reconcile the owner-accepted Jarvis D-03 direction against the current ASTRA GOLD reference architecture, unified autonomous development system, executor capability matrix, Jarvis master prompt, and integration-contract draft.
- Prohibited scope respected: no code execution, tests, installation, credentials, model/provider calls, runtime/host inspection, infrastructure change, qualification, merge, rebase, cherry-pick or deployment.

## 1. Owner-accepted direction in scope

D-03, explicitly accepted by the owner on 2026-10-14, establishes:
- Jarvis is the top-level coordination layer for distributed hybrid autonomous engineering and is intended to coordinate the future cloud development system.
- Jarvis is intended to integrate directly with GitHub.
- Claude is an external intelligent/engineering executor through an approved interface; Ollama is a separate local runtime.
- A task/data-aware policy selects an eligible execution path. No silent local-to-cloud fallback.
- ASTRA coordinates engineering within granted authority.
- MediaHub Product State Authority retains exclusive canonical product-state mutation authority.

This is architecture direction only; it does not claim implementation or qualification.

## 2. Source anchors read on the documentation branch

| Source | Read-back blob SHA | Relevant current wording |
|---|---|---|
| `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md` | `b354acfa4cff595583a7f1778371143e9868f293` | §1 calls A0-ASTRA the single ASTRA GOLD engineering coordination authority and limits its state to ASTRA queue/claim/gate state; §3.3 lists permanent production lanes mh-dev-01 → Claude, mh-dev-02 → Claude, Voktors-Mac-mini.local → Claude; §3.4 lists GitHub Transport. |
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` | `610a611f42d19a55ab7a172e00068c40c5ce5da5` | Describes A0 Astra as mission decomposition/scheduling/claims/recovery; says GitHub is a transport/evidence substrate, not MediaHub State Authority; states Ollama is not a permanent Astra Gold queue executor. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | `9ad83781a8da53d1a8f540ede54eba95281f01c0` | A0 owns model selection within bounded executor/model admission; permanent Claude lanes; specialist roles may not write directly to canonical main or become another source of truth. |
| `docs/checkpoints/MEDIAHUB-JARVIS-MASTER-PROMPT-01.md` | `67a612c326c9aece8648634482b40a5c92bd6d1a` | Jarvis is the owner-provided umbrella label for engineering/orchestration; ASTRA/Astra Gold remains a bounded engineering subsystem; neither is MediaHub Product State Authority. The prompt is a working draft, not a new canonical baseline. |
| `docs/architecture/MEDIAHUB-UNIFIED-ARCHITECTURE-CONTRACT-V3-DRAFT-01.md` | `28d5f82a80df2002d39c06d2060a822fd7aae258` | Working-branch integration draft, explicitly not a new accepted baseline; separates MediaHub Product State Authority from ASTRA A0 queue/claim/gate authority and retains governance/release gates. |

## 3. Reconciliation findings

### R-01 — Jarvis top-level coordination vs ASTRA A0 sole ASTRA coordination authority
**Classification: RECONCILABLE BY SCOPE; wording needs to be explicit.**

D-03 places Jarvis at the system-wide engineering orchestration layer. ASTRA GOLD §1 makes A0 the single authority for ASTRA-internal queue/claim/gate state. These can coexist only if Jarvis coordinates missions and selects permitted execution paths across the wider system while A0 remains the sole writer/authority for ASTRA-internal claims, leases, queue progression and qualification gates. Jarvis must not become a second A0 or directly mutate ASTRA control state outside the ASTRA contract.

**Recommended draft wording:** “Jarvis owns system-level mission coordination and policy selection; ASTRA A0 owns ASTRA-internal queue/claim/lease/gate state and enforces ASTRA execution admission. Jarvis submits bounded missions through the ASTRA contract; it does not bypass A0.”

### R-02 — D-03 per-task Claude/Ollama routing vs permanent Claude production lanes
**Classification: REAL SCOPE/TOPOLOGY TENSION; no silent change authorized.**

ASTRA GOLD reference architecture and executor capability matrix name three permanent production lanes, all bound to Claude. The unified system explicitly says Ollama and other surfaces are not permanent queue executors. D-03 establishes a broader Jarvis target in which policy can choose Claude or a compatible local Ollama model per task. The new target must not be treated as already changing the qualified/current ASTRA production pool.

**Recommended disposition:** preserve the current permanent Claude lane contract for ASTRA GOLD until a separate, evidence-backed executor admission and qualification path authorizes a change. Model the Jarvis-wide local Ollama route as a target/candidate path outside the permanent ASTRA pool until that gate is met. No Ollama lane is admitted by this document.

### R-03 — Direct GitHub management vs GitHub as transport/evidence substrate
**Classification: RECONCILABLE BY CAPABILITY BOUNDARY; implementation details remain open.**

D-03 accepts direct Jarvis/GitHub integration. Existing ASTRA docs classify GitHub as transport/evidence substrate and prohibit specialist roles from writing directly to canonical main. These are compatible if “direct management” means authenticated, capability-scoped repository operations through a controlled adapter, not bypass of branch protections, review, target-SHA binding, A3 verification, evidence recording or human release authority.

**Recommended draft wording:** provide Jarvis with explicit repository capabilities (read/list/compare; create or update isolated branch artifacts only where authorized); gate writes by allowed path/branch and audit; never infer merge, release, deployment or production permission. Existing repository rules and owner approval gates remain authoritative. Exact scopes and permissions must be designed against the actual GitHub integration before implementation.

### R-04 — Product state and engineering control state
**Classification: NO CONFLICT IF EXISTING INVARIANT IS PRESERVED.**

D-03 preserves Product State Authority as exclusive canonical product-state mutation authority. ASTRA A0 owns only ASTRA-internal engineering-control state. Jarvis's top-level position does not grant either subsystem product-state mutation authority.

### R-05 — Policy routing and failover
**Classification: DESIGN DETAIL REQUIRED, NOT AN OWNER DECISION.**

Routing should be deterministic and auditable per task: task class, data classification, permitted egress, local model/runtime capability, executor admission state, budget and authorization. If the selected executor is unavailable or fails, stop or use only a separately policy-authorized fallback; no implicit local-to-cloud switch. The policy engine must preserve provider/model identity and attach the chosen route and evidence to the task record.

## 4. Bounded disposition

- D-03 remains OWNER-ACCEPTED as an architecture direction.
- Existing ASTRA GOLD normative lane, A0 authority, qualification and GitHub workflow constraints remain in force; this review does not rewrite them.
- Jarvis-to-ASTRA mission interface, GitHub adapter capability list, write scopes, branch/PR lifecycle, policy schema and audit record remain engineering design items.
- The unified v0.1 and v3 integration contracts remain drafts; this document does not accept either as a global baseline.
- No component admission, executor promotion, runtime implementation, qualification or operational readiness is claimed.

## 5. Next bounded step

Draft a narrow Jarvis control-plane / GitHub adapter contract with:
1. mission submission to ASTRA A0 and a single-writer rule for ASTRA internal state;
2. explicit GitHub read/write capabilities and path/branch scopes;
3. route decision record (task class, data class, executor, locality/egress decision, fallback rule, model/provider identity);
4. evidence requirements for diff, target SHA, review/A3 and final status;
5. explicit prohibited operations unless separately authorized: merge, release, deployment, production mutation and governance bypass.

Before implementation, compare the draft scopes with the actual repository integration/tool permissions. Do not alter the ASTRA permanent Claude lane or run qualification in this step.
