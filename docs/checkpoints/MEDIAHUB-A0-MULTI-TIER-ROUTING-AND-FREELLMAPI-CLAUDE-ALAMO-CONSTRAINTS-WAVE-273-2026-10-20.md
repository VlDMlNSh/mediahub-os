# Wave 273 — A0 multi-tier routing and explicit FreeLLMAPI/Claude-Alamo constraints (2026-10-20)

## Status and authority

**OWNER-DIRECTED HARD TARGET REQUIREMENTS RECORDED; IMPLEMENTATION/QUALIFICATION NOT VERIFIED.** This wave clarifies and supplements the owner lock in Wave 272. The requirements bind subsequent design and implementation planning; they do not amend Functional Baseline 2.0, replace governance/change control, qualify any route, or authorize live actions.

## Confirmed target architecture

ASTRA GOLD A0 is the sole hybrid mission/task coordination authority. For each authorized mission, A0 decomposes work into bounded, dependency-aware subtasks and dispatches eligible tasks among three destination classes:

1. The independent GitHub-hosted cloud-agent pool.
2. Explicitly admitted user-owned MediaHub devices or instances.
3. Explicitly admitted local executors, including Claude Code bound to Alamo.

A0 owns the DAG/scheduling decision, queue, claim/lease, retry, cancel, recovery, handoff/fencing, cross-route reconciliation and evidence aggregation. Executors are task-scoped only, may not mutate A0 coordination state, and do not gain MediaHub Product State Authority. Completion remains distinct from independent A3 verification. Unknown/unadmitted/revoked routes fail closed; no cross-route duplicate active task without an auditable fenced handoff. The cloud pool must qualify and run without Alamo or user-owned devices.

## Hard Claude-on-Alamo restrictions

- Claude Code is exclusively a local executor/client running on Alamo for this target architecture.
- The Alamo Claude route must not use the Anthropic API directly or indirectly (including through proxy, relay, adapter or router), paid Anthropic API credentials/authentication/billing, or a paid API fallback.
- No silent reroute from the Alamo Claude route to a different executor or paid service. Missing, ambiguous, revoked or disallowed routes must fail closed.
- Do not repurpose or pool subscription credentials, tokens or account authorization in a way the provider terms do not permit. Route eligibility must not be achieved by evading provider restrictions.
- A Claude Code process on Alamo does not prove the underlying inference is local. The backend/model, each selected upstream and actual egress must be declared and evidenced; a third-party model reached through Claude Code must not be described as the Claude model.

## FCC and FreeLLMAPI clarification

The owner's named component families are FCC/fcc-claude, FreeLLMAPI, and equivalent specialized Claude Code auth/router/adaptor components. These are **unqualified candidates only**. In particular, the exact FreeLLMAPI project/backend is not yet pinned. The name “FreeLLMAPI” is not evidence that the implementation, credentials, upstreams, or every fallback path are free or permitted.

Public source discovery surfaced distinct projects and layers that must not be conflated:
- [RobinHoodO/freellm-claude-code-router](https://github.com/RobinHoodO/freellm-claude-code-router) describes a Claude Code adapter/router that translates Anthropic-format requests and connects to a FreeLLMAPI backend, with selectable routing/fallback strategies.
- [lov0u/freellmapi](https://github.com/lov0u/freellmapi) and [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi) are separate repositories using the same project name; identity cannot be inferred from the name alone.

These links are initial identity leads, not a security review or admission decision. Before qualifying a candidate, pin exact repository/release/source digest and deployment, map every possible upstream/fallback, prove permitted authentication and applicable provider terms, document non-paid cost/billing/quota class, record version and egress/data path, verify Alamo binding, and add auditable deny tests for direct/indirect Anthropic API use and every paid/unknown fallback. A mixed free/paid gateway is not an eligible route unless its permitted non-paid allowlist and no-paid-fallback rule are enforced and evidenced. No bypass of provider controls, no credential leakage, and no secret values in GitHub.

## Source reconciliation

- Previous binding owner-directed requirement: [Wave 272](MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-CLAUDE-NONPAID-AUTH-HARD-REQUIREMENTS-WAVE-272-2026-10-20.md).
- New architecture requirement contract: [A0 hybrid dispatch and Alamo Claude routing hard requirements](../architecture/MEDIAHUB-A0-HYBRID-DISPATCH-AND-ALAMO-CLAUDE-ROUTING-HARD-REQUIREMENTS.md).
- The current candidate route YAML, ops/agent-fabric/providers/local-executor-routing-v2.yaml, blob af3d96fe91055af6ba79eded9c800d28d8c0c5c9, lists FCC and OmniRoute Claude lanes but marks the overall config ASTRA_GOLD_QUALIFICATION_GATED. It does not establish a qualified Alamo-bound route and contains no explicit FreeLLMAPI lane. It was not modified as part of this documentation pass.
- Wave 271 remains the latest detailed source reconciliation: AuthorizationContext does not itself establish trusted issuer provenance; FileTaskIngress lacks the complete hybrid DAG/destination/locality/auth-cost contract; the existing gateway/queue do not establish qualified multi-tier A0 runtime behavior.

## Required next bounded sequence

1. Trace the authoritative Task Contract producer/writer and approval/attestation lifecycle.
2. Map each mission/task field to an accepted contract and locate the smallest governed extension point; keep Wave 269 candidate-only until that review is complete.
3. Produce a destination responsibility/lifecycle matrix for cloud workers, user-owned MediaHub and local executors.
4. Add source-level/schema/static and mock-only negative fixtures for paid Anthropic API, hidden paid fallback, unknown router/upstream, unsupported authorization, untrusted/replayed issuer, unadmitted destination, missing locality/budget, malformed DAG and duplicate cross-route claims.
5. Only after accepted schemas, exact-head CI, independent review and explicit route qualification may runtime wiring be considered. Keep the GitHub-hosted cloud pool independent of Alamo.

## Refs, CI and verification limits observed

- Canonical documentation ref: docs/mediahub-chat-tree-map-20261012; HEAD before Wave 273 writes: 66828c648c246a242db17e14214900041ddc8b8f.
- main HEAD: 80be45a70732b1d568164571d4273a6397792c3b.
- Branch comparison main...docs/mediahub-chat-tree-map-20261012: diverged, docs ref ahead by 2,796 and behind by 44, merge base f0f406feb9f9816b009f4e6e756813541e53b9bc; the compare response was capped at 300 file entries and is not a full file-level integration audit. No merge/rebase attempted.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301): OPEN, last update observed 2026-10-20T14:17:18Z.
- PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421): OPEN/DRAFT, head 84e2d0bbb4163942f5ba010591cb5d3c9d6a7581, base 80be45a70732b1d568164571d4273a6397792c3b; independent reviews query returned none. The two recorded PR workflow runs 39425009654 (Astra Cloud Runtime Validation) and 39425009644 (Astra Verify) report SUCCESS; the combined-status endpoint returned no status contexts for the queried PR head. CI success does not approve this architecture or pass governance gates.
- No tests were run; no provider calls, secret access, host inspection, software installation, agent dispatch, merge, deployment, qualification or acceptance occurred in this wave.

## Navigation

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Current checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301); PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421)

**Result:** hard target requirements and FreeLLMAPI identity ambiguity recorded. Runtime enforcement and route qualification remain NOT VERIFIED. Contour A remains NOT_PROVEN / BLOCKED; Contour B remains gated on independent Contour A acceptance.
