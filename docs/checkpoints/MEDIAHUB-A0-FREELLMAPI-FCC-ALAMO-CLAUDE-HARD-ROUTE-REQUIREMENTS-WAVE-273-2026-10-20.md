# Wave 273 — explicit FreeLLMAPI candidate gate and Alamo Claude no-paid-route requirements (2026-10-20)

## Status and authority

This report records the owner's explicit target-architecture requirements as binding constraints for subsequent design and implementation. It records a constraint delta to Wave 272, not a claim that the target has been implemented, qualified, deployed, or accepted. The existing Baseline 2.0, issuer/capability controls, governance gates, Product State Authority boundary and independent verification requirements remain unchanged.

## Owner-clarified hard requirements

### 1. ASTRA GOLD A0 hybrid decomposition and dispatch

ASTRA GOLD A0 is the single coordinator for an authorized hybrid mission. It decomposes missions into bounded, dependency-aware subtasks and dispatches eligible work across exactly these destination classes:

1. The independent GitHub-hosted cloud-agent pool.
2. Explicitly admitted user-owned MediaHub devices or instances.
3. Explicitly admitted local executors, including the Claude Code executor bound to Alamo.

A0 owns mission/DAG scheduling, queue, claims/leases, retry, cancellation, recovery, handoff/fencing, cross-route reconciliation and evidence aggregation. Executors execute their admitted task scope only: they do not mutate A0's internal coordination state and do not gain Product State Authority. Completion of execution remains distinct from independent A3 verification.

Each destination needs explicit admission, authenticated issuer/capability provenance, a bounded task scope, data-locality/egress controls, quota/budget, revocation checks and an auditable evidence envelope. No simultaneous active claim may exist across destination classes without an explicit fenced handoff. User-owned MediaHub destinations are opt-in and untrusted until independently admitted.

### 2. Cloud-pool independence

The GitHub-hosted cloud pool must be operable and qualify independently of Alamo and user-owned devices. Neither Alamo nor a personal MediaHub node may be a hidden prerequisite for the Contour A cloud-pool route.

### 3. Claude Code is an Alamo-local executor with a strict non-paid route boundary

For this target architecture, Claude Code runs only as a local executor process on Alamo. The Alamo Claude Code route MUST NOT use:

- the Anthropic API or an Anthropic-hosted paid inference route;
- paid API authorization, credentials, billing, or a paid backend reached through a proxy/router;
- paid route fallback after authentication, quota, router, network or provider failure;
- silent rerouting to a different destination or cost class.

This is an Alamo Claude Code route constraint; it is not a claim that the proprietary Anthropic Claude model can be hosted locally. The Claude Code client/executor process, execution host and inference backend are separate identities. Running Claude Code on Alamo does not prove that inference is local. If a requirement calls for local inference, the admitted local model/backend and measured/documented egress must be named separately.

No implementation may bypass provider authentication, account eligibility, identity/age protections, subscription/service terms, quotas or billing controls; conceal paid API use behind a proxy; or relay paid API credentials. If the selected route cannot prove an explicitly permitted non-paid cost/auth class and upstream policy compliance, it fails closed.

### 4. FCC and FreeLLMAPI are named candidates, not approved authorization

The owner explicitly names FCC/fcc-claude, FreeLLMAPI and similar specialized Claude Code routing/auth components as candidates for review. Naming a project does not select a canonical upstream/fork, approve its auth mode, prove that it is free, or admit its routes.

Before a component is admitted, record and verify at minimum:

- exact repository/fork, immutable commit/release, license and software-supply-chain provenance;
- the actual upstream provider/model selected per request and the permitted authorization basis;
- provider/service terms, applicable account/subscription eligibility, limits, quota and revocation behavior;
- actual billing/cost class, transitive route graph and failover policy;
- explicit provider/model allowlist for the Alamo route, with **all paid routes and paid fallback disabled**;
- credential origin, scope, handling and non-disclosure; effective egress/data path; runtime version and proof of binding to Alamo.

A mixed-provider router must not be treated as a blanket “free” route. In particular, the fact that a local proxy exposes an Anthropic-compatible API does not establish that its upstream is non-Anthropic, no-cost, permitted, or local. When any required property is unknown, the route remains unqualified and must fail closed. No provider-control, paywall, account, quota or billing bypass is permitted.

## Candidate-source observations

Public documentation currently provides examples of the relevant component class, but does not establish an approved MediaHub route:

- [FCC example repository](https://github.com/Factix/fcc) describes a proxy with multiple provider backends and free, paid and local routing options. The MediaHub Alamo route would need an explicit allowlist and disabled paid fallback; its mere existence does not satisfy that gate.
- [FreeLLMAPI example repository](https://github.com/lov0u/freellmapi) describes a multi-provider gateway with an Anthropic Messages-compatible surface for Claude clients. This is an API-shape compatibility claim, not proof that a particular instance is no-cost, policy-permitted, Alamo-bound or locally inferencing.
- Multiple public forks/variants exist for these names; this pass does not select one as the canonical upstream. The current roadmap also records unresolved FreeLLMAPI classification and FCC implementation identity.

## Source and status reconciliation before this pass

- Canonical docs branch: `docs/mediahub-chat-tree-map-20261012`, observed prior HEAD `66828c648c246a242db17e14214900041ddc8b8f`.
- `main` HEAD: `80be45a70732b1d568164571d4273a6397792c3b`.
- Source Wave 272 report blob: `010a6dcf08f76c05e9df7ba4a1d794f4b6602c58`; Wave 272 addendum blob: `a8a9bbeaf64db80e6111eccb9f9dea7dafc3987d`.
- Prior map blob before this pass: `c2b6f7d18f60c826f3471abb4d04aa5ef957d768`.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) is OPEN; it remains a tracker and is not authorization to dispatch, use credentials, call providers, merge or deploy.
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) is OPEN/DRAFT at head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base `80be45a70732b1d568164571d4273a6397792c3b`; no independent reviews were returned. The queried exact-head runs [Astra Cloud Runtime Validation #39425009654](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009654) and [Astra Verify #39425009644](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009644) were SUCCESS. They do not test or approve this requirements-only update.
- The repository rulesets endpoint returned an empty list; branch-protection endpoints returned 403 to the available integration. Required protection state therefore remains unverified.

## Changes made in Wave 273

- Created [Wave 273 map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-273-2026-10-20.md).
- Updated the canonical project map to index Wave 273 and link the hard requirements, addendum, checkpoint and roadmap.
- Updated the bootstrap instruction so the requirements are loaded on every relevant `/next`.
- Updated the continuation checkpoint and Master Development Roadmap with the new FreeLLMAPI/FCC clarification and next implementation sequence.
- Final document read-back identities after the associated writes:
  - Canonical map: blob `71d2409be45a5b0f0dd0dd726f5b1ba766669d16`, update commit `47f04065bfd2ebf14e7325f9ff8575d256ca6ff7`.
  - Wave 273 map addendum: blob `47cf21a18b8b49b764a406770bfa79317d3bd2a6`, creation commit `d4a575be33302032fac1094898b24fab3ce2d428`.
  - Bootstrap: blob `eabdc46adeab07bab12bd738d018d72165fc9a45`, update commit `4fede85583829c670b0034c64b2f88a84ea4041c`.
  - Master Development Roadmap: blob `c130b877f485cdcf70bb03fb2603653bc59c0a65`, update commit `4835b4acc6409933865bce681e3467e2ecf2fbba`.
  - Continuation checkpoint: blob `9b88c162e99db57320fa3163d9aeaa2d1ee53fd5`, update commit `07fe2df327b536473bb260423101002b29942e0e`.
  - Every listed file was fetched again after its write; the canonical map's 1,124,729-character blob was read by SHA because the Contents API did not return its full body. This report was subsequently read back by GitHub after its final evidence update; its resulting blob SHA is reported in the session summary.
  - Before the final report evidence update, canonical docs HEAD was `07fe2df327b536473bb260423101002b29942e0e`; `main` remained `80be45a70732b1d568164571d4273a6397792c3b`.

## Next bounded engineering step

Trace the authoritative A0 Task Contract producer/writer, trusted issuer and approval/attestation lifecycle. Reconcile destination and auth/cost fields against accepted contracts before changing runtime. Then add schema/static/mock-only negative tests for Anthropic API use, any paid backend/fallback on the Alamo Claude route, unknown or mutable router identity, prohibited account-auth flows, missing destination admission, missing locality/egress/budget, malformed DAG and duplicate cross-route claims. Do not call live providers or inspect Alamo as part of those static tests.

## Verification and non-claims

This pass is documentation and source reconciliation only. No tests were run; no provider/router was called; no credentials or secrets were accessed; Alamo was not inspected; no agent was dispatched; no merge, deployment, route qualification or system acceptance occurred. Runtime enforcement remains **NOT VERIFIED**. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains blocked until Contour A is deployed and independently accepted.

## Canonical links

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 273 map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-273-2026-10-20.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Bootstrap instruction](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
