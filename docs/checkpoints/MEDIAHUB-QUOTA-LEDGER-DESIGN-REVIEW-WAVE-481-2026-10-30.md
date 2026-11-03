# Wave 481 — quota-ledger contract design review (2026-10-30)

## Status

**DESIGN REVIEW RECORDED / IMPLEMENTATION BLOCKED / INDEPENDENT REVIEW NOT VERIFIED.**

This pass reviews the proposed Wave 480 quota-ledger contract. It does not implement a runtime, execute provider calls, read credentials, dispatch agents, install a gateway, or authorize a transport.

## Immutable targets and repository evidence

- Main snapshot observed in the preceding repository read: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7. Current main ref freshness remains NOT VERIFIED by a direct ref/HEAD read in this pass.
- Canonical documentation branch: docs/mediahub-chat-tree-map-20261012.
- Wave 480 contract branch: docs/wave480-quota-ledger-contract-20261030.
- Wave 480 contract blob: 6492ddb7f7ee5adfe29f66e10ad4ec8012341154.
- Wave 480 review/report blob: ae891fdeba3ce4dcd254c86e50dc3bd88e9ffd33.
- Wave 480 checkpoint blob on its branch: 59ea09047a4cd67d6b5549241218b4ccbf2e5689.
- PR #592: OPEN / DRAFT / UNMERGED; head 0436139834f93c5621b3cf54d37d16f135403662; base canonical branch at bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4; 4 commits ahead, 0 behind. Exact-head workflow runs and combined statuses returned empty arrays. Formal review submissions/comments: none. CI and independent review NOT VERIFIED.
- Issue #301 remains OPEN. Its documented A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy gates remain prior to bounded worker admission; issue is not a live scheduler or authorization for provider activity.
- Active Ruleset 26108066 was previously verified to require five exact contexts and strict status checks. Classic branch-protection/effective combined policy remains NOT VERIFIED due integration API access limits.
- SentinelX currently reports zero connected hosts. Voktors-Mini.Dlink is offline; mh-dev-01 and mh-dev-02 are disabled. Claude task NOT RUN.
- Gemini controller NOT RUN. No controller run ID or child IDs exist for this pass.

## Review findings

The following are design findings from this review, not an independent A3 security review.

### F1 — Lifecycle is a list, not a transition contract (HIGH)

The contract enumerates AVAILABLE, RESERVED, IN_FLIGHT, SETTLED, RELEASED, UNKNOWN and BLOCKED, but does not define the allowed transition graph, transition guards, terminal states, or illegal-transition behavior. For example, it does not state whether UNKNOWN can transition to SETTLED after reconciliation, or whether BLOCKED is a route state versus a reservation state.

**Required correction:** define reservation and route as separate state machines; enumerate every allowed transition, actor, precondition, idempotency behavior and terminal condition. Reject every unlisted transition.

### F2 — Reservation expiry, lease ownership and crash recovery are underspecified (HIGH)

There is no reservation expiry/lease duration, owner/fencing token, heartbeat rule, or recovery procedure for a worker that crashes after reserving but before recording send intent. This can strand quota indefinitely or allow a stale worker to send after a replacement worker has reclaimed the reservation.

**Required correction:** add lease owner, monotonically increasing fencing token, expiry timestamp, recovery rules, and an explicit guarantee that expired/reclaimed reservations cannot be sent by stale workers. Do not equate lease expiry with proof that a provider request was not sent.

### F3 — Revocation has a TOCTOU race (HIGH)

Q012 says a revoked route must not make a new outbound call, but there is no atomic relationship between route authorization, reservation commit and outbound send. A route can be revoked after the admission check but before the request leaves the process.

**Required correction:** specify a route-generation/version captured by reservation, a final pre-send authorization check, and a defined linearization point. State exactly which revocation races are prevented and how an already-sent request is reconciled.

### F4 — Quota units and reservation estimation are not defined (HIGH)

The contract refers to quota unit, limit, remaining amount and usage_units without defining request/token/second dimensions, input/output token estimates, rounding, safety margins, model-family aggregation, or treatment of provider-reported usage differing from reservation estimates.

**Required correction:** define typed quota dimensions and units, canonical integer representation, conservative reservation estimate, overage behavior, provider usage normalization, and whether multiple dimensions must be reserved atomically.

### F5 — Partial settlement and adjustments are missing (MEDIUM/HIGH)

Exactly-once logical settlement is asserted, but there is no model for partial usage, provider corrections, late usage reports, refunds/credits, or adjustments after initial settlement.

**Required correction:** use immutable settlement events with idempotent event IDs and a derived ledger balance; specify correction/compensation semantics without mutating historical evidence.

### F6 — Idempotency scope and retention are ambiguous (HIGH)

Stable per-task-attempt keys are required, but uniqueness scope, canonical key construction, retention horizon, cross-worker deduplication, and behavior after archival/expiry are unspecified. Returning an existing reservation/result in Q015 is insufficient if the first attempt remains unresolved.

**Required correction:** define a globally unique attempt identity and provider/account/quota-scope binding, durable uniqueness constraints, retention longer than the maximum retry/reconciliation horizon, and response behavior for every existing lifecycle state.

### F7 — UNKNOWN reconciliation is not operationally specified (HIGH)

UNKNOWN is a sound safety state, but the contract does not define reconciliation sources, polling/backoff limits, provider request IDs, operator escalation, terminal timeout, or conditions that prove safe release/retry. Some providers do not expose idempotent request lookup.

**Required correction:** define per-provider reconciliation capability and evidence grades. Where outcome cannot be proven, preserve UNKNOWN and block the affected quota scope; never infer safe retry from elapsed time alone.

### F8 — Retry-After parsing and cooldown scope need precision (MEDIUM)

The 429 policy does not define delta-seconds versus HTTP-date parsing, invalid/past values, clock skew, maximum accepted duration, or interaction with provider reset timestamps and concurrent cooldown updates.

**Required correction:** define standards-compliant parsing, trusted clock policy, monotonic cooldown extension, malformed-header fallback, and exact scope of cooldown.

### F9 — Transaction ambiguity and outbox boundary are not specified (HIGH)

Q014 fails closed on ambiguous ledger transactions, but there is no protocol for commit acknowledgement loss, durable send-intent/outbox records, or recovery that distinguishes “reservation committed” from “provider request sent”. A database commit and network send cannot be treated as one atomic transaction.

**Required correction:** define a durable transactional outbox/send-intent protocol with explicit states and crash-point recovery matrix. The protocol must never claim exactly-once external execution unless the provider supports it; otherwise preserve at-most-once dispatch intent and UNKNOWN outcomes.

### F10 — Evidence schema lacks integrity and correlation requirements (MEDIUM)

Evidence fields omit schema version, event ID, actor/worker identity, fencing token, route-policy version, reservation estimate, quota dimension/unit, provider request ID, reconciliation evidence reference, and tamper-evident chain/correlation fields.

**Required correction:** version the evidence schema, define required correlation identifiers and integrity controls, and ensure all fields remain non-secret.

## Disposition

- Wave 480 contract: **PROPOSED / INCOMPLETE FOR IMPLEMENTATION**.
- This Wave 481 review: **SUCCEEDED** as a bounded design review by the current author; **NOT INDEPENDENT**.
- Independent security/provenance review: **NOT VERIFIED**.
- Draft 2020-12 schema and negative fixtures: **NOT RUN**.
- Q001–Q015 conformance tests: **NOT RUN**.
- Runtime/gateway/provider activity: **NOT RUN**.
- Gemini and Claude execution: **NOT RUN**.
- Merge, deployment, qualification, adoption and acceptance: **NOT RUN**.

## Acceptance criteria before implementation

1. Revise contract to define separate route and reservation state machines and a complete transition table.
2. Specify lease/fencing, route revocation linearization, durable send intent/outbox, crash recovery and UNKNOWN reconciliation.
3. Define quota dimensions, units, conservative reservation estimates, partial settlement and adjustment events.
4. Define idempotency identity/scope/retention and Retry-After parsing/cooldown semantics.
5. Publish a versioned Draft 2020-12 JSON Schema and negative fixtures for every prohibited/malformed state.
6. Obtain genuine independent security/provenance review and record formal review evidence.
7. Only then implement deterministic fake-provider tests for Q001–Q015; do not install gateways or contact real providers.

## Governance and executor record

- Issue #301 remains the controlling gate; no gate is waived by this review.
- No secrets were read, copied, modified or exposed.
- No provider API calls were made.
- No Gemini workflow dispatch or child job was created.
- SentinelX connected host count is zero; no third-server Claude task was run.
- No transport allowlist or router policy was changed.

## References

- [PR #592 — Wave 480 proposed quota-ledger contract](https://github.com/VlDMlNSh/mediahub-os/pull/592)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Wave 480 contract](MEDIAHUB-CLOUD-QUOTA-LEDGER-CONTRACT-WAVE-480-2026-10-30.json)
- [Wave 480 security review](MEDIAHUB-CLOUD-QUOTA-LEDGER-SECURITY-REVIEW-WAVE-480-2026-10-30.md)
- [Canonical chat tree map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
