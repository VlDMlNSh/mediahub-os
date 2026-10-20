# Wave 268 — Owner hard constraints: A0 multi-tier routing and Alamo Claude non-paid authorization (2026-10-20)

## Status

OWNER-DIRECTED ARCHITECTURE REQUIREMENTS CONSOLIDATION; documentation-only. These requirements are binding design constraints for subsequent work. This report does not silently amend Baseline 2.0 or bypass existing governance, issuer/capability, qualification, security, review, deployment, or acceptance gates.

## Owner requirements recorded

1. **A0 is the hybrid mission coordinator.** ASTRA GOLD A0 decomposes a mission into bounded, dependency-aware subtasks and routes eligible tasks among three distinct destination classes: (a) the GitHub-hosted cloud-agent pool, (b) admitted user-owned MediaHub devices/instances, and (c) admitted local executors. A0 owns the hybrid task DAG, queue/claim/lease, dependency scheduling, retry, cancellation, recovery, and cross-route reconciliation.
2. **Claude is an Alamo-local executor only.** For the specified Claude route, the executor/client/workspace runs on Alamo. It must not use Anthropic API inference, paid Anthropic API credentials/billing, or any paid Anthropic API authorization route. Anthropic API use is prohibited even if a router abstracts the API call. No silent cloud fallback is allowed.
3. **FCC and similar routers are candidates for non-paid authorization/routing only.** FCC (including fcc-claude) and comparable specialized Claude Code routers may be evaluated only where the actual authorization path is non-paid for the prohibited Anthropic API route and remains compliant with upstream authentication, provider terms, usage limits, and access controls. Do not treat “free” as proof of permission. Verify upstream/provider, credential/auth class, billing/cost class, egress/data handling, router identity/version, and Alamo host binding. Unknown or unqualified routes fail closed. Do not use them to evade authentication, subscription conditions, provider controls, or rate limits.
4. **Execution location and inference location are different facts.** Claude Code running on Alamo does not prove the model itself is local. Do not claim local inference without independent evidence. Regardless of inference location, the Alamo Claude path must exclude Anthropic API and paid API authorization routes.
5. **Cloud pool independence.** The GitHub-hosted Contour A cloud pool must continue to operate without Alamo or user-owned MediaHub devices. Those destination classes are separately admitted targets, not dependencies of the cloud execution plane.
6. **Authority and safety.** Executors do not acquire A0 coordination authority or MediaHub Product State Authority. A direct-local Jarvis queue, if retained, requires a separately defined owner, authenticated issuer/capability, and lifecycle; it cannot bypass A0 for hybrid missions. No duplicate active claims across routes without stable task identity, idempotency, fencing, and explicit handoff.
7. **Admission and evidence.** Each destination requires identity, issuer provenance, capability checks, enrollment/admission, data locality and egress policy, budget/quota controls, revocation, bounded workspace/claims, result/evidence schema, and independent A3 verification. Missing or ambiguous policy means deny.
8. **Required negative tests before runtime use.** Schema/static/mock tests must reject: Anthropic API route or paid API credentials for Alamo Claude; unrecognized or unqualified FCC/router identities; missing issuer provenance; unknown destination; silent cloud fallback; cross-route duplicate claims; missing locality/egress policy; and malformed or unbound DAG/task identity. Real provider calls, host inspection, agent dispatch, or qualification remain blocked until the relevant gates authorize them.

## Source reconciliation

- Canonical map and checkpoint already contain the Wave 265/266 owner constraints; Wave 267 records that the implementation contracts remain incomplete. This wave makes the no-paid-Anthropic-API rule explicit and consolidates it with A0's three destination classes.
- Current source gap from Wave 267 remains: the inspected `AuthorizationContext` lacks issuer provenance; existing task ingress does not carry the full hybrid destination/DAG/route envelope; existing gateway evidence does not prove the required Alamo-specific API exclusion or FCC authorization class.
- Existing routing candidates `CLAUDE_FCC`, `CLAUDE_OMNIROUTE`, and `CLAUDE_CODE_DIRECT` are not runtime qualification evidence. FCC remains a candidate, not an approved route.
- The user's hard requirements do not by themselves authorize provider calls, secret access, agent dispatch, host access, paid usage, merge, deployment, or acceptance.

## Result

- Owner requirements: documented as hard target constraints for design and qualification.
- Implementation: NOT VERIFIED.
- Tests: NOT RUN in this documentation-only wave.
- Runtime/host/provider/dispatch: NOT INSPECTED/NOT INVOKED.
- Contour A: NOT_PROVEN / BLOCKED pending accepted ingress/issuer/destination contracts, negative tests, exact-head CI, independent review, runtime qualification, deployment, and acceptance.

## Next bounded step

Draft a versioned mission envelope and destination responsibility/lifecycle matrix against existing accepted contracts, preserving A0 authority and the non-paid Alamo Claude boundary; then implement static negative fixtures and mock-only tests. Do not invoke providers or dispatch agents as a substitute for those gates.

## Evidence links

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Map addendum — Wave 268](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-268-2026-10-20.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #421 — controller-only Gemini workflow calls](https://github.com/VlDMlNSh/mediahub-os/pull/421)
