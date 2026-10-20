# Map addendum — Wave 273: explicit FreeLLMAPI candidate gate and Alamo Claude non-paid-route boundary (2026-10-20)

## Status and authority

This addendum records the explicit owner clarification as a hard target-architecture requirement. The binding requirements are consolidated in the [A0 hybrid dispatch and Alamo Claude routing contract](MEDIAHUB-A0-HYBRID-DISPATCH-AND-ALAMO-CLAUDE-ROUTING-HARD-REQUIREMENTS.md) and the [canonical Wave 273 owner report](../checkpoints/MEDIAHUB-A0-FREELLMAPI-FCC-ALAMO-CLAUDE-HARD-ROUTE-REQUIREMENTS-WAVE-273-2026-10-20.md). The separate [supplemental repository-state note](../checkpoints/MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-FREELLMAPI-CLAUDE-ALAMO-CONSTRAINTS-WAVE-273-2026-10-20.md) records source and status reconciliation, not a competing decision. No specific router repository, authorization method, model/provider, version, or runtime route is approved. This addendum is not evidence of implementation, qualification, deployment, or acceptance.

## Binding target requirements

- **ASTRA GOLD A0 is the single hybrid mission coordinator.** It decomposes an authorized mission into bounded, dependency-aware subtasks and dispatches them only to admitted destination classes: (1) the independent GitHub-hosted cloud pool, (2) explicitly admitted user-owned MediaHub devices/instances, and (3) explicitly admitted local executors.
- **A0 owns the hybrid lifecycle:** DAG scheduling, queue/claim/lease, retry, cancellation, recovery, handoff/fencing, cross-route reconciliation, and evidence aggregation. Executors do not mutate A0 coordination state and do not gain Product State Authority. Execution completion does not replace independent A3 verification.
- **Cloud-pool independence:** the GitHub-hosted cloud pool must operate without Alamo or a user-owned MediaHub device as a hidden dependency.
- **Claude Code is an Alamo-local executor only** for this target architecture. The route MUST NOT use the Anthropic API, paid API authorization/credentials/billing, paid API backends through a proxy, paid fallback, or silent rerouting. This restriction applies to the Alamo Claude Code route, not merely to a particular proxy implementation.
- **FCC / fcc-claude, FreeLLMAPI, and similar router components are candidates only.** The owner's naming of FreeLLMAPI does not authorize a specific fork, upstream, build, endpoint, account-auth flow, or provider. Each candidate must be pinned to an exact repository/ref/version and independently assessed before admission.
- **A named “free” router is not proof of permitted free access.** Candidate admission requires evidence for upstream identity, explicit authorization basis, applicable service terms and limits, actual billing/cost class, provider/model allowlist, transitive routes, fallback behavior, version and supply-chain provenance, effective egress/data path, credential handling, and binding to Alamo. The selected route must fail closed when any field is unknown.
- **No bypass of provider controls:** do not bypass or disguise authentication, subscription eligibility, identity/age controls, provider quotas, terms or billing; do not relay paid API credentials through a proxy. A provider pool that mixes free, paid and local backends must have a strict allowlist that excludes every paid route for this Alamo executor and disables paid fallback. If a compliant non-paid route cannot be proven, do not enable it.
- **Keep client, executor host, and inference backend distinct.** Claude Code running on Alamo proves only the location of the client/executor process; it does not prove that model inference is local. Do not describe the proprietary Anthropic-hosted Claude model as locally hosted. Where true local inference is required, admit and name a local model/backend separately, with egress evidence.
- **Destination authorization is per task.** Each destination requires issuer/capability provenance, admission, scope, data-locality/egress policy, quota/budget, revocation checks and an auditable evidence envelope. No concurrent duplicate active claim across routes without explicit fenced handoff.

## Public candidate-source notes (not an adoption decision)

The public [FCC example](https://github.com/Factix/fcc) describes routing Claude Code traffic through a proxy to a mix of provider backends, including free, paid and local options. The public [FreeLLMAPI example](https://github.com/lov0u/freellmapi) describes a multi-provider gateway with a Claude-compatible Messages API surface. These are examples of candidate classes, not a selection of canonical upstreams and not evidence that a specific route is free, provider-permitted, Alamo-bound, or safe for MediaHub. Exact project/fork identity remains to be selected through source, license, terms, security and route review.

## Next bounded work

1. Trace the authoritative A0 task-contract producer/writer, trusted issuer/attestation lifecycle, and admission record.
2. Reconcile the candidate Wave 269 mission envelope with accepted schemas/contracts and create a destination responsibility/lifecycle matrix for cloud, user-owned MediaHub, and local executors.
3. Add schema/static/mock-only negative tests for paid-provider routes, paid fallback, prohibited Anthropic API, unknown FreeLLMAPI/FCC upstream, missing cost/auth class, unauthorized account/subscription flow, missing egress/Alamo binding, unknown destination, malformed DAG, duplicate cross-route claim and absent fencing.
4. Keep all live router/provider use, host inspection, credential access, agent dispatch, route qualification and deployment behind their existing gates.

## Current state at this pass

- Canonical documentation branch before this pass: `docs/mediahub-chat-tree-map-20261012`, observed HEAD `66828c648c246a242db17e14214900041ddc8b8f`.
- `main` observed HEAD: `80be45a70732b1d568164571d4273a6397792c3b`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) is OPEN. PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421) is OPEN/DRAFT at head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base `80be45a70732b1d568164571d4273a6397792c3b`; no independent reviews were returned.
- Exact-head checks [Astra Cloud Runtime Validation #39425009654](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009654) and [Astra Verify #39425009644](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009644) report SUCCESS for PR #421's current head. They do not validate this documentation delta or accept the target architecture.
- The GitHub rulesets endpoint returned an empty list. Branch-protection endpoints return 403 to this integration, so branch-protection requirements are not independently verified.
- This documentation-only pass did not run tests, call providers, inspect Alamo, access secrets, dispatch agents, merge, deploy, qualify or accept the system. Contour A remains NOT_PROVEN / BLOCKED; Contour B remains gated on Contour A deployment and independent acceptance.

## Canonical links

- [Canonical project map](MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 273 report](../checkpoints/MEDIAHUB-A0-FREELLMAPI-FCC-ALAMO-CLAUDE-HARD-ROUTE-REQUIREMENTS-WAVE-273-2026-10-20.md)
- [Continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
