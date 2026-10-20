# MediaHub OS — A0 hybrid dispatch and Alamo Claude routing hard requirements

- Date: 2026-10-20
- Status: **OWNER-DIRECTED HARD TARGET REQUIREMENTS; BINDING FOR FUTURE DESIGN; RUNTIME ENFORCEMENT NOT VERIFIED**
- Scope: Contour A architecture and its gated target interface with later Jarvis / user-owned MediaHub execution
- Baseline: Does not amend Functional Baseline 2.0, grant Product State Authority, accept a candidate schema, or qualify/deploy a runtime route.

## 1. Single A0 coordination authority

ASTRA GOLD A0 is the single coordinator for hybrid missions. Once an authorized mission is accepted, A0 decomposes it into bounded, dependency-aware subtasks and schedules eligible work across these destination classes:

1. The independent GitHub-hosted cloud-agent pool.
2. Explicitly admitted user-owned MediaHub devices or instances.
3. Explicitly admitted local executors, including the Claude Code executor bound to Alamo.

A0 owns the mission/task graph, destination decision, queue, claim/lease, retry, cancellation, recovery, handoff/fencing, cross-route reconciliation and evidence aggregation. Executor processes are task-scoped workers only: they do not mutate A0 coordination state and do not gain MediaHub Product State Authority. Completion is not acceptance; independent A3 verification remains separate.

Every destination needs verified identity, trusted issuer/capability, task scope, data-locality/egress policy, quota/budget and cost class, revocation state, workspace/concurrency boundary and evidence requirements. An active task cannot be duplicated across destination classes without an explicit, auditable, fenced handoff. Unknown, unadmitted or unqualified destinations fail closed. Shared-file writes are serialized unless disjoint workspaces and claims are proven.

The GitHub-hosted cloud pool must remain operable and independently qualifiable without Alamo or any user-owned MediaHub/local device. Such devices may be additional admitted capacity, never a hidden dependency of the cloud pool.

## 2. Hard Claude Code / Alamo route restrictions

For this target architecture, Claude Code is **exclusively a local executor/client running on Alamo**. Its role is not a general cloud-pool worker and it may not silently switch to a different destination.

The Alamo Claude route MUST NOT use:

- The Anthropic API directly or indirectly, including via an API proxy, adapter, relay or router.
- Paid Anthropic API credentials, API billing, paid API authorization, or an Anthropic API route disguised as another provider path.
- Paid Anthropic API fallback when authentication, quota, policy, router or connectivity fails.
- Unapproved sharing, extraction or repurposing of subscription/login credentials, or any authentication route that violates applicable provider terms.
- Silent fallback from the Alamo-only Claude Code route to the cloud pool or another executor.

A local Claude Code process does **not** prove that the underlying model inference is local. Each execution must declare and evidence the real model/backend, upstream provider and egress path. Do not call a third-party or open-weight model “the Claude model” merely because Claude Code is the client.

## 3. FCC / FreeLLMAPI / equivalent route components

FCC/fcc-claude, FreeLLMAPI, OmniRoute, OpenFlux and similar specialized Claude Code auth/router/adaptor components are **candidate components only**, not approved routes by name. Their identity and function must be disambiguated and pinned to an exact repository/project, version or immutable source digest, deployment identity and configuration before qualification. Public FCC and OmniRoute descriptions include multi-provider routing and mixed cost classes, so they require an explicit Alamo-only provider/model allowlist and disabled paid/unknown fallback. FreeLLMAPI is a name used by multiple projects/forks, and its name or Anthropic-compatible API shape proves neither the actual upstream nor the authorization/cost class. OpenFlux is currently an unresolved identity: available public search results include similarly named projects with unrelated roles, and no specific Claude Code free-auth/router implementation has been verified. Do not infer its identity or capability from the name; it remains unadmitted until a precise source URL and pinned version are reviewed.

A candidate can be admitted for this route only after evidence establishes all of the following:

- The exact authorization mechanism and upstream/provider for every possible routing branch.
- Explicitly permitted use under the relevant upstream/provider terms, including any limits on personal accounts, automation, third-party clients, account pooling and redistribution.
- A verifiable non-paid authentication/cost class for the actual route, with billing and quota behavior documented; the word “free” or a project name does not prove this.
- No direct or indirect Anthropic API request, paid Anthropic API authorization, hidden paid fallback, credential relay or policy bypass on the Alamo Claude route.
- An allowlist of eligible backends plus auditable per-task selected-model/upstream and fallback decisions.
- Network egress, data handling/retention, version, secret boundary and explicit Alamo host binding.
- Visible fail-closed behavior if any condition is missing, revoked, ambiguous or violated.

FreeLLMAPI in particular must not be assumed to be an authentication method or a free route solely from its name; the exact intended project/backend and its upstream model/provider routes remain to be identified and reviewed. A router that can select both free and paid upstreams is not safe for this route unless its permitted non-paid allowlist and no-paid-fallback behavior are enforced and evidenced. No credentials, tokens or secret values are to be committed or copied into evidence.

## 4. Required deny cases and qualification evidence

Source-level, schema and mock-only negative tests must reject:

- Anthropic API use by the Alamo Claude route, directly or through a proxy/router; paid Anthropic API auth/billing; or a paid/unknown fallback.
- Unknown or unpinned FCC, FreeLLMAPI, OmniRoute, OpenFlux or equivalent identity, upstream, auth/cost class, terms status, version, egress or Alamo binding; any paid/unknown fallback reachable through a mixed-provider router.
- An untrusted/replayed issuer, missing capability/audience, unadmitted/revoked user-owned MediaHub or local executor, unknown destination or missing task scope.
- Missing DAG dependency identity, duplicate active cross-route claims, stale leases, unfenced handoff, silent failover, missing locality/budget policy or unverifiable result evidence.
- Any worker changing A0 queue/coordination state or MediaHub Product State Authority data outside its admitted capability.

Runtime wiring requires accepted source contracts, exact-head CI, independent review, explicit route qualification and auditable evidence. Documentation, configuration presence and passing static tests alone do not qualify a live route.

## 5. Authority and current limits

These owner-directed requirements govern subsequent design and implementation proposals. They do not authorize provider calls, secret access, host inspection, installation, live dispatch, merge, deployment or acceptance by themselves. Keep source reconciliation and negative-test work bounded; do not silently expand or change Functional Baseline 2.0. Contour B remains blocked until Contour A is deployed and independently accepted.

## 6. Navigation and traceability

- Canonical project map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Canonical Wave 273 owner requirements: [FreeLLMAPI/FCC/Alamo Claude hard-route report](../checkpoints/MEDIAHUB-A0-FREELLMAPI-FCC-ALAMO-CLAUDE-HARD-ROUTE-REQUIREMENTS-WAVE-273-2026-10-20.md)
- Supplemental repository-state reconciliation: [Wave 273 source note](../checkpoints/MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-FREELLMAPI-CLAUDE-ALAMO-CONSTRAINTS-WAVE-273-2026-10-20.md)
- Prior owner-lock: [Wave 272](../checkpoints/MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-CLAUDE-NONPAID-AUTH-HARD-REQUIREMENTS-WAVE-272-2026-10-20.md)
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301); PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421)

**Status summary:** target requirements recorded; runtime enforcement NOT VERIFIED; router identity/terms/egress and Alamo binding NOT QUALIFIED; Contour A remains NOT_PROVEN / BLOCKED.
