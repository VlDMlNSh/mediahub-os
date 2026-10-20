# Wave 272 — A0 multi-tier dispatch and Alamo Claude non-paid-auth hard constraints (2026-10-20)

## Status and authority

This is an owner-directed requirements lock for the target architecture. It is binding for subsequent design and implementation work. It does **not** claim that the requirements are already enforced in runtime, that a proposed schema is accepted, or that any route is qualified.

## Owner-confirmed target architecture

ASTRA GOLD A0 is the single coordinator for hybrid missions. It decomposes an authorized mission into bounded, dependency-aware subtasks and distributes eligible tasks among exactly these destination classes:

1. The independent GitHub-hosted cloud-agent pool.
2. Explicitly admitted user-owned MediaHub devices or instances.
3. Explicitly admitted local executors, including the Claude Code executor bound to Alamo.

A0 owns mission/DAG scheduling, task queue, claim/lease, retry, cancellation, recovery, handoff, fencing, cross-route reconciliation and evidence aggregation. Executors perform only their admitted tasks. They do not gain Product State Authority or the authority to mutate A0 queue/coordination state. Independent A3 verification remains separate from execution completion.

Each destination must be explicitly admitted and bound to issuer/capability, task scope, data-locality/egress policy, quota/budget, revocation status and evidence requirements. Active work cannot be duplicated across destinations without an explicit fenced handoff. Shared-file changes require serialization or disjoint workspaces. Unknown or unqualified routes fail closed.

The GitHub-hosted cloud pool must remain operational without Alamo or any user-owned MediaHub/local device. Local-device availability is not a prerequisite for cloud-pool qualification.

## Hard Claude-on-Alamo restrictions

For this architecture, Claude/Claude Code is permitted **only as a local executor running on Alamo**. The execution host restriction is not proof that model inference is physically local; locality claims must match measured and documented egress.

The Alamo Claude route MUST NOT use:
- the Anthropic API, whether directly or through a proxy/router;
- paid Anthropic API credentials, API billing, or paid API authorization routes;
- a paid API fallback after an auth, quota, router or connectivity failure;
- silent rerouting of a Claude-local task to another destination.

The route MAY consider FCC/fcc-claude or a similar specialized Claude Code auth/router component only when its specific upstream and authorization mechanism is documented, the mechanism is explicitly permitted by the relevant upstream terms, and non-paid auth/cost class, billing behavior, terms/limits, version, data egress and Alamo binding are verified. “Free” in a component description does not prove permission or a zero-cost route. Router use must not bypass provider controls, disguise API traffic, or relay paid API credentials. If the route cannot prove the required permitted non-paid class, it must fail closed. No API key values or secret contents are needed or permitted as evidence.

## Required policy and negative-test contract

Before enabling any route, the mission/task policy and tests must reject:
- an Anthropic API endpoint, paid Anthropic API auth/billing class or indirect paid API proxy for the Alamo Claude route;
- a missing/unknown router, upstream, auth/cost class, billing behavior, terms status, version, egress destination or Alamo host binding;
- missing/untrusted/replayed issuer, absent capability/audience, unadmitted destination or revoked route;
- silent fallback, expired/duplicate cross-route claims, malformed DAG/task identity or missing locality/budget policy.

Tests for these constraints should start as source-level/schema/static and mock-only negative fixtures. A static test or a config entry alone is not live route qualification. No real provider call or device inspection is authorized by this documentation requirement.

## Evidence reconciliation

- Wave 270 owner requirements and roadmap sync: [report](MEDIAHUB-A0-OWNER-HARD-REQUIREMENTS-AND-ROADMAP-SYNC-WAVE-270-2026-10-20.md), [map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-270-2026-10-20.md).
- Wave 271 source reconciliation: [report](MEDIAHUB-A0-ISSUER-TASK-CONTRACT-RECONCILIATION-WAVE-271-2026-10-20.md), [map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-271-2026-10-20.md).
- Wave 271 confirmed that `AuthorizationContext` does not establish trusted issuer provenance by itself, `FileTaskIngress` lacks the complete hybrid DAG/destination/locality/auth-cost contract, and the existing cloud-first gateway/filesystem queue do not establish qualified A0 hybrid execution.
- Routing candidates in `ops/agent-fabric/providers/local-executor-routing-v2.yaml` remain unqualified until upstream, auth/cost, terms, egress and Alamo binding are evidenced.

## Next bounded implementation sequence

1. Trace the authoritative Task Contract producer/writer and approval/attestation lifecycle.
2. Map each required mission/task field to the existing canonical contract and identify the extension point; do not wire the Wave 269 draft into runtime before that reconciliation.
3. Build a destination responsibility/lifecycle matrix and static/schema/mock-only negative fixtures for all denials above.
4. Require exact-head CI, independent review and explicit route qualification before enabling runtime traffic.
5. Keep the cloud pool Alamo-independent. Keep Contour B blocked until Contour A is deployed and independently accepted.

## Current project state and verification limits

- Canonical documentation branch before this wave: `docs/mediahub-chat-tree-map-20261012`; observed Wave 271 commit: `4f19a0f9d4dedb5e6b686f4614218530c5694a26`.
- `main` HEAD observed: `80be45a70732b1d568164571d4273a6397792c3b`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) is OPEN.
- PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421) is OPEN/DRAFT at head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base `80be45a70732b1d568164571d4273a6397792c3b`; no independent reviews were returned. Exact-head workflow runs [39425009654](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009654) and [39425009644](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009644) reported SUCCESS for that PR head when queried; these do not approve the architecture or waive review/governance gates.
- This documentation pass did not run tests, invoke providers, inspect Alamo, access secrets, dispatch agents, merge, deploy, qualify or accept the system.

## Required navigation

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Current checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #421: https://github.com/VlDMlNSh/mediahub-os/pull/421

**Result:** hard target requirements recorded; runtime enforcement NOT VERIFIED; tests NOT RUN; Contour A remains NOT_PROVEN / BLOCKED.


## Documentation write/read-back evidence

- Canonical map update was committed through the Git Data API because the Contents API returned an empty body for this 1.12-million-character file: commit `a304d49503acd5a3b595cb23de471b308a5405fe`, resulting map blob `c2b6f7d18f60c826f3471abb4d04aa5ef957d768`. The operation used base tree `bd48baa95a6b16e1d43868b9df2b817795e6904c`, created tree `d8e2f2fbc273ee044711f6e868b0d05b57bf93c2`, and advanced the branch with an expected-head check.
- Wave 272 map addendum blob: `a8a9bbeaf64db80e6111eccb9f9dea7dafc3987d`; create commit `3f38ccedf06b9d32ff90cce6d6f8a1561fc33298`.
- Bootstrap blob after hard-requirement insertion: `22116389a05b7f6527340065ee5578ab00e6ffa0`; update commit `ef4b35f706a0c5ed6a99ccec71ffc3b61df9d8a8`.
- Roadmap blob after Wave 272 addition: `7aa82e807b2e1df0c5ae11606bda40ae8aeddebd`; update commit `8743e68bc472bccb9042e599398a362aac865664`.
- Checkpoint blob after ordering/evidence correction: `c19e1761f22c537c661db861d29f521666161481`; update commit `8dc2c0e202563d9f1560b9aee64635fe240be0b7`.
- These are documentation Git objects only. They do not establish runtime enforcement, route qualification, system deployment or Contour A acceptance.
