# Wave 265 — Owner-mandated A0 routing and local-only Claude boundary (2026-10-20)

## Status
OWNER-CLARIFIED HARD ARCHITECTURAL REQUIREMENTS RECORDED IN PROJECT DOCUMENTATION. This records target constraints; it does not claim implementation, qualification, deployment, or acceptance.

## Binding owner requirements
1. ASTRA GOLD A0 is the hybrid orchestration and task-state authority. For a hybrid mission it decomposes work into bounded dependency-aware subtasks and schedules eligible subtasks across:
   - the GitHub-hosted cloud-agent pool;
   - user-owned MediaHub devices/instances (the user’s “user MediaHub” execution tier);
   - separately admitted local executors.
2. Claude is exclusively a local executor on Alamo. No Anthropic API, Anthropic-hosted inference, API-key route, or automatic cloud fallback may be used for Claude work. “Claude on Alamo” must be implemented and qualified as a local execution/backend route, not presumed to mean the Claude Code CLI magically runs the model locally. Exact local backend/runtime and proof of local inference remain an open qualification item.
3. A0 remains the single authority for hybrid queue state, task claims, leases, dependency scheduling, retry/cancel/recovery, and cross-route handoff. Executors return bounded results/evidence and never gain ASTRA or MediaHub Product State Authority.
4. User-owned MediaHub execution is a distinct destination class with explicit device/instance identity, enrollment/admission, issuer/capability, data locality/egress policy, budget/quota, revocation, and evidence requirements. It is not equivalent to GitHub-hosted workers or arbitrary local machines.
5. Direct-local Jarvis queue submission, if retained, is a separate route with its own named queue owner and authorization/lifecycle contract. It must not bypass A0 for tasks submitted as hybrid A0 missions. Cross-route execution requires stable task identity, idempotency/fencing, explicit handoff, and no duplicate active claims.
6. The cloud pool must remain operational without Alamo or user-owned MediaHub devices. Local-only mode must fail closed and must not silently route to Anthropic API or any cloud model.
7. These requirements do not authorize runtime dispatch, credential access, provider calls, changes to accepted Baseline 2.0, or bypass of governance/issuer/capability/acceptance gates.

## Architecture topology
```text
Jarvis / mission origin
  ├─ optional separately-authorized direct-local queue → Alamo local Claude executor
  └─ authorized mission envelope → ASTRA GOLD A0
       ├─ task DAG / dependency scheduler / lease & recovery authority
       ├─ GitHub-hosted cloud-agent pool
       ├─ admitted user-owned MediaHub instances/devices
       └─ admitted local executors (Alamo: Claude local-only)
       → result/evidence reconciliation → independent A3 verification
```

## Required implementation/qualification gates
- Define/version the typed mission and child-task envelope: stable IDs, DAG dependencies, source SHA, data class, route constraints, budget/deadline, issuer/capability, and expected evidence.
- Define destination registry classes and admission/revocation contracts for cloud workers, user-owned MediaHub, and local executors.
- Prove local-only Claude backend on Alamo, including model/runtime identity, network-egress denial for Anthropic endpoints, no API secret dependency, and negative tests for cloud fallback. Do not assume host inventory or software installation.
- Define A0 queue ownership and idempotent claim/lease/fencing, cancellation, retries, recovery, dead-letter, checkpoint, and cross-route handoff semantics.
- Enforce user/device data-locality and egress policy before dispatch; unknown destination or ambiguous authority is denied.
- Add static schema/negative fixtures first, then isolated mock-based tests. Real dispatch/runtime qualification remains separately gated.
- Independently verify results/evidence; task completion is not acceptance.

## Evidence reviewed this wave
- Canonical docs branch: `docs/mediahub-chat-tree-map-20261012`.
- Current main HEAD verified via GitHub API: `80be45a70732b1d568164571d4273a6397792c3b`.
- Draft PR #421 remains open, not merged; head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base `80be45a70732b1d568164571d4273a6397792c3b`.
- Issue #301 remains open and explicitly states its tracker is not authorization for dispatch, credential access, provider calls, merge, deployment, or qualification.
- Wave 264 source reconciliation: blob `9721d9ae304db97bb1b2a170df22127276f25323`; map addendum blob `7a79b50c7c0468df6e6415e8dbd2c019e7239d25`.
- Current continuation checkpoint blob read from canonical branch: `90235431e5d2063c6ea6c0f5e1f58a50b0722db1`; roadmap blob: `fa4a35d4e2ed766a6f44d34c62d761bdbbded668`.
- The canonical map Contents read returned an empty body despite a valid blob SHA; the map blob was read directly by SHA (1,114,776 characters) before appending this wave entry. This avoids treating the empty Contents response as an empty map.
- No workflow was dispatched, no provider/API was invoked, no secret was read, no host was inspected, and no test/qualification/deployment/merge was performed in this wave.

## Next bounded step
Reconcile existing mission/task and destination schemas against these constraints; locate accepted A0 ingress and AuthorizationContext issuer contracts; draft a destination-class responsibility matrix and static negative fixtures that forbid Anthropic API routes for Alamo Claude. Do not execute tasks until authority and admission contracts are established.

## Navigation
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Master development roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Draft controller PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
