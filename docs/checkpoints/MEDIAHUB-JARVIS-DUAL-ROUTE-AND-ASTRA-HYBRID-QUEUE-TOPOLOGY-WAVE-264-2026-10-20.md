# Wave 264 — Jarvis direct-local and ASTRA GOLD hybrid queue topology reconciliation (2026-10-20)

## Status
READ-ONLY SOURCE RECONCILIATION; owner clarification recorded as target architecture intent; NOT an acceptance of new normative contracts; NOT implemented, tested, qualified, deployed or host-verified.

## Owner clarification captured
Jarvis must support two distinct submission routes:
1. Direct local route: Jarvis may submit a bounded autonomous queue directly to an admitted local executor such as Claude Code on the intended Alamo host.
2. Hybrid distributed route: Jarvis may submit a mission/queue to ASTRA GOLD A0; A0 decomposes it into a dependency-aware task graph and schedules eligible tasks across the GitHub-hosted cloud pool and admitted local executors (including Claude/Alamo), then collects evidence and independently verifies outputs.

The previously described device-role target is retained as owner-supplied topology: Jarvis may run using Claude on the local Alamo host, intended to be a Mac mini 2018, while Codex API/tooling is installed on a MacBook. This is a target description, not verified inventory. “Claude on Alamo” must be disambiguated per route: Claude Code client/tool, Anthropic-hosted Claude model, and a Claude-compatible local backend are not the same thing.

## Source evidence re-read
- WB-14 source reconciliation on main, blob 4dead9e249603679f4193a5a0b0b0a13a04aa177: prior source reconciliation already lists WB-14B ingress/authority, WB-14C direct local queue, WB-14D cross-route lifecycle, and WB-14E provider/data locality as open. It says no Alamo lane exists in the reviewed permanent queue, Jarvis authenticated ingress is not proven, a direct-route queue owner is not named, and retry/cancel/recovery ownership is open.
- Corporation crosswalk on main, blob 721e4c994d4800df4605af52630ea75339971a27: task-graph/DAG decomposition, route policy, structured results and cross-route interfaces are partially covered or still proposals; the broader corporation proposal is not accepted as a complete normative contract.
- ASTRA GOLD unified design on main, blob e2067dc41b52983fc4e0b2549fb6af3c099cbc60: A0 is the single coordination/state authority; executors are not authority; Claude Code and Claude provider are distinct concepts.
- ops/agent-fabric/providers/local-executor-routing-v2.yaml, blob af3d96fe91055af6ba79eded9c800d28d8c0c5c9: CLAUDE_CODE_DIRECT exists as a qualification-gated executor path, not proof it is available or admitted on Alamo.
- runtime/mediahub_runtime/autonomous_queue.py, blob 72c4a5ccb367884fb02d247b1b8848ea62c3c6b1: current permanent queue pool does not establish a separate Alamo queue.
- tests/test_autonomous_queue_contract.py, blob e3466fd5f8d6d47a846f8ec75b0ab3ca46ed0dc7: tests assert fixed-target SHA, bounded concurrency and current queue boundaries; they do not prove Jarvis→Alamo route, task-DAG decomposition, or cross-route reconciliation.
- Tree inventory confirms ops/astra_orchestrator.py and ops/hybrid_orchestrator.py, but source presence is not a qualified production execution plane. The scripts reference a Linux filesystem root and local state, so they cannot be silently repurposed as the GitHub-hosted cloud pool.

## Target topology, with authority boundaries
~~~text
Jarvis — mission/task origin and high-level policy intent
  ├── Route A: direct local queue → admitted Claude Code/Alamo executor
  │             (separate queue lifecycle; issuer/capability + evidence required)
  └── Route B: signed/authorized mission envelope → ASTRA GOLD A0
                → task DAG + dependency scheduler
                ├── GitHub-hosted cloud workers
                └── admitted local executors (Claude Code/Alamo)
                → result/evidence reconciliation → independent A3 verification

A0 owns ASTRA queue/claim/lease/coordination state.
Jarvis does not mutate A0 internal state directly.
Neither route gains Product State Authority.
GitHub-hosted cloud pool does not depend on Alamo or a server.
~~~

## Open blockers to resolve before implementation/dispatch
1. Route-A authority/queue owner: define trusted Jarvis issuer, authenticated ingress, capability binding, queue ownership, idempotency key and approval attestation.
2. Cross-route task contract: one stable mission/task identity; schema/version; immutable source SHA; dependency graph; executor/provider/backend/egress identity; data class; deadline/budget; cancellation; retries; lease/fencing; checkpoint/recovery; artifact digests; terminal status and verifier.
3. No dual lifecycle authority: Route A owns only its explicitly scoped local queue. Route B queue/claim/lease/recovery remains A0-owned for ASTRA tasks. A task cannot be simultaneously claimed on both routes without a defined handoff/fencing protocol.
4. Route eligibility: direct local route and hybrid route must independently check executor identity, runtime/backend, current qualification, data locality, resource envelope, permission, budget/quota, availability and fallback policy. Local-only must fail closed, never silently fall back to cloud.
5. Task decomposition: A0 may split only into bounded child tasks with declared dependencies and disjoint workspaces/claims. Shared files need serialization; task completion is not acceptance; independent A3 verification remains mandatory.
6. Device/backend identity: verify Mac mini 2018/Alamo host identity and MacBook Codex installation only through a separately authorized inventory/qualification workflow. This pass did not inspect devices or run provider calls.
7. Cloud-only boundary: A0 cloud scheduling/dispatch/worker coordination for Contour A remains GitHub-hosted. Do not depend on the local Mac mini for cloud queue availability. Existing local scripts are not a substitute for the cloud controller.
8. Governance: preserve current Baseline 2.0 and existing ASTRA governance. This report records clarified target behavior; it does not grant runtime authority or qualify the route.

## Next bounded action
Continue the existing WB-14B/C/D sequence rather than inventing a new parallel contract: trace the Jarvis caller to the accepted A0 ingress and typed AuthorizationContext issuer; then draft a route-responsibility matrix for direct-local vs A0-hybrid lifecycle. After that, reconcile any required envelope/DAG schema against existing contracts and add static negative tests before any execution. Do not launch agents or touch hosts in this wave.

## Verification limits
Read-only repository inspection and documentation only. No local device was inspected, no queue was dispatched, no model/provider called, no secrets accessed, no tests executed, no server touched, and no merge/deployment/qualification/acceptance occurred.

## Navigation
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Prior source reconciliation: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-14-JARVIS-A0-AND-DIRECT-LOCAL-ROUTE-SOURCE-RECONCILIATION-2026-10-15.md
- Corporation proposal crosswalk: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-ARCHITECTURE-PROPOSAL-CROSSWALK-WAVE-01-2026-10-15.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301