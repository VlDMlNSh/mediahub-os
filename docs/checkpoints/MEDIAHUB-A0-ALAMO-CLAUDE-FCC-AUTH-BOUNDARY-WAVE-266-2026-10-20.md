# Wave 266 — A0 routing and Alamo Claude Code authorization boundary (2026-10-20)

## Status
OWNER-CLARIFIED HARD ARCHITECTURAL REQUIREMENTS RECORDED. This is a target contract and qualification plan, not evidence of implementation, provider authorization, runtime behavior, or acceptance.

## Binding owner requirements
1. **A0 hybrid decomposition and routing.** ASTRA GOLD A0 decomposes hybrid missions into bounded, dependency-aware subtasks and distributes eligible work across (a) the GitHub-hosted cloud pool, (b) admitted user-owned MediaHub devices/instances, and (c) admitted local executors. A0 remains the authority for hybrid mission/task state, DAG dependencies, claims, leases, retries, cancellation, recovery and cross-route reconciliation. Executors return results/evidence; they do not gain ASTRA or MediaHub Product State Authority.
2. **Alamo is the only intended Claude execution location.** Claude Code work covered by this requirement executes on the Alamo local executor. It must not be routed through Anthropic's paid API route or use Anthropic API credentials/billing. Do not silently fall back to Anthropic-hosted inference or another cloud route.
3. **FCC and similar router boundary.** FCC (fcc-claude) and comparable specialized Claude Code authorization/routing components are candidate mechanisms for an allowed non-paid Claude Code authorization path. The architecture must preserve this as an explicit route class, separate from ANTHROPIC_API. The user's requirement is not permission to bypass provider authentication, subscription terms, usage limits, safeguards, or access controls. A route is eligible only after its real upstream/auth method, terms/policy compatibility, credential type, network destinations, and cost class are evidenced and qualified. If that cannot be proven, fail closed; do not infer that “free” means authorized.
4. **Execution location is not the same as inference location.** “Claude is a local executor on Alamo” means the executor/client process and workspace run on Alamo. It does not, by itself, prove that model inference is local. The allowed FCC/similar route must be separately characterized. Regardless of transport, Anthropic API use and paid API authorization routes remain forbidden for this Alamo Claude path. Do not require or claim a locally hosted model unless separately specified and proven.
5. **Route separation.** Use distinct route identities at minimum for CLAUDE_CODE_ALAMO_FCC_AUTH (qualification-gated, non-paid authorized route), other candidate authorized Claude Code routers (each separately identified and qualified), and ANTHROPIC_API (explicitly denied for Alamo Claude). CLAUDE_CODE_DIRECT is not proof that FCC auth is active, that the process is on Alamo, or that API use is absent.
6. **Hybrid destination classes.** A0 may route to GitHub-hosted cloud workers, admitted user-owned MediaHub, and admitted local executors. User-owned MediaHub is a distinct class requiring device/instance identity, enrollment/admission, issuer/capability, data locality/egress policy, budget/quota, revocation, and evidence controls. The cloud pool must remain operable without Alamo or user-owned devices.
7. **No authority or lifecycle bypass.** Direct-local Jarvis queueing, if retained, requires a separately named owner and authorization/lifecycle contract. It cannot bypass A0 for tasks submitted as A0 hybrid missions. Stable task IDs, idempotency/fencing, explicit handoff and no duplicate active claims are required. Unknown route, unknown credential/upstream, ambiguous authority, failed admission, or missing evidence is denied.
8. **No implicit governance change.** These owner requirements do not modify accepted Baseline 2.0, authorize runtime dispatch, secret access, provider calls, merge, deployment, or production acceptance. Preserve issuer/capability and independent A3 verification gates.

## Target topology
```text
Jarvis / mission origin
  ├─ optional separately authorized direct-local queue → Alamo Claude Code executor
  │      └─ only a qualified non-paid authorized auth/router path; no Anthropic API
  └─ authorized mission envelope → ASTRA GOLD A0
         ├─ bounded task DAG + dependency/lease/recovery lifecycle
         ├─ GitHub-hosted cloud-agent pool
         ├─ admitted user-owned MediaHub instances/devices
         └─ admitted local executors (Alamo Claude Code; FCC/similar route separately qualified)
         → result/evidence reconciliation → independent A3 verification
```

## Existing source evidence and gaps
- ops/agent-fabric/providers/local-executor-routing-v2.yaml on main, blob af3d96fe91055af6ba79eded9c800d28d8c0c5c9, already lists CLAUDE_FCC (transport fcc, launcher fcc-claude), CLAUDE_OMNIROUTE, and CLAUDE_CODE_DIRECT. It is marked qualification-gated. It does not prove Alamo host binding, upstream auth method, free/non-paid status, API exclusion, or active admission.
- architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md on main, blob e2067dc41b52983fc4e0b2549fb6af3c099cbc60, distinguishes Claude Code as a local execution client and FCC/OmniRoute as transport/gateway mechanisms. It does not by itself prove the specific route's authorization/cost/egress properties.
- The provider/model registry ops/qualification/provider_model_registry.json on main, blob 62328126fd2cd8879a73bb6812adcacd3e2abe84, is a mixed-scope candidate registry, not an accepted allowlist for this route.
- Repository code search returned no usable indexed matches for FCC/Anthropic API constraints; this is not proof that no other implementation exists. The next pass must use the canonical map and a bounded source inventory.
- The prior [Wave 265 report](MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-LOCAL-CLAUDE-REQUIREMENTS-WAVE-265-2026-10-20.md) records A0 multi-tier routing and the initial Claude boundary; this Wave 266 record clarifies FCC/non-paid authorization and explicitly separates execution location from inference location.

## Required verification sequence
1. Reconcile the accepted A0 ingress and typed issuer/AuthorizationContext contract with the existing mission/task and destination registries.
2. Define route metadata for executor location, auth mechanism, upstream/provider, credential class, billing/cost class, allowed egress, and qualification evidence. Never store credential values in registry files.
3. Add static/schema negative fixtures that reject ANTHROPIC_API or paid API credentials for Alamo Claude, reject unknown/unqualified FCC/router variants, reject implicit cloud fallback, and reject a route that lacks verified host/auth/upstream identity.
4. Add mock-based tests for destination admission, A0 task ownership, idempotency/fencing and explicit cross-route handoff. Keep user-owned MediaHub separate from cloud workers.
5. Only after review and authorization, run isolated runtime qualification proving the actual route. Do not dispatch real tasks or access secrets as part of the static-contract pass.

## Result of Wave 266
- Requirements and gaps documented; no implementation claim.
- No provider/API call, credential read, host inspection, workflow dispatch, test execution, merge, deployment, or qualification performed.
- Contour A remains NOT_PROVEN / BLOCKED until its required gates and independent acceptance are complete.

## Navigation
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 265 A0 multi-tier requirements](MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-LOCAL-CLAUDE-REQUIREMENTS-WAVE-265-2026-10-20.md)
- [Master development roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Draft controller PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
