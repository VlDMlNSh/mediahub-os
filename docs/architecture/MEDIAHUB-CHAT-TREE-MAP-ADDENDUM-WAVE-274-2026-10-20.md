# Map addendum — Wave 274: Alamo Claude router identity and non-paid route guards (2026-10-20)

## Status

Owner-clarification follow-up and public source identity review. Wave 273 remains the binding requirements record; this addendum names further candidate families without choosing or admitting a route. No change to Functional Baseline 2.0 or authority boundaries. Runtime enforcement and route qualification remain NOT VERIFIED.

## Recorded clarification

- ASTRA GOLD A0 remains the sole coordinator: decompose authorized missions into bounded, dependency-aware subtasks; schedule only to admitted GitHub-hosted cloud workers, user-owned MediaHub destinations, and local executors; own DAG/queue/claim/lease/retry/cancel/recovery/handoff/fencing/reconciliation/evidence aggregation. A3 remains independent.
- The GitHub-hosted cloud pool remains independent of Alamo and user-owned devices.
- Claude Code on Alamo is an executor/client, not proof of local inference. Its route MUST NOT use the Anthropic API directly or indirectly, paid Anthropic API authorization/credentials/billing, paid backend/fallback, silent rerouting, prohibited subscription credential reuse, or any policy/account/quota/billing bypass.
- FCC/fcc-claude, FreeLLMAPI, OmniRoute, OpenFlux and equivalents are **candidate names only**. Exact project/fork/version, authorization basis, provider/model allowlist, all upstream/fallback branches, terms/limits, non-paid cost class, credential handling, egress/data path, and Alamo binding must be verified before admission.
- Public descriptions show FCC and OmniRoute can support multiple provider/cost classes; therefore configuration presence or a "free" label is not sufficient. Paid and unknown paths must be denied by explicit allowlist and fail-closed negative tests.
- OpenFlux identity remains unresolved: current search surfaced same-name sources with other roles, not a verified Claude Code free-auth router. Do not infer identity or capability from the name; require the precise source URL and pinned version.
- No live router/provider call, credential access, Alamo inspection, agent dispatch, test execution, merge, deployment, qualification, or acceptance occurred.

## Evidence links

- [Wave 274 identity/route guard report](../checkpoints/MEDIAHUB-ALAMO-CLAUDE-ROUTER-CANDIDATE-IDENTITY-AND-NONPAID-ROUTE-GUARD-WAVE-274-2026-10-20.md)
- [Binding A0 hybrid dispatch and Alamo Claude routing requirements](MEDIAHUB-A0-HYBRID-DISPATCH-AND-ALAMO-CLAUDE-ROUTING-HARD-REQUIREMENTS.md)
- [Wave 273 owner hard requirements](../checkpoints/MEDIAHUB-A0-FREELLMAPI-FCC-ALAMO-CLAUDE-HARD-ROUTE-REQUIREMENTS-WAVE-273-2026-10-20.md)
- [Canonical project map](MEDIAHUB-CHAT-TREE-MAP.md)
- [Continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)

## Next bounded step

Continue with the authoritative A0 task-contract writer and trusted issuer/admission lifecycle. Reconcile destination and route-policy fields against accepted contracts, then add schema/static/mock-only denial fixtures for Anthropic API, paid/unknown fallbacks, ambiguous router identity, unsupported auth, missing egress/locality/budget, malformed DAG and duplicate cross-route claims. Keep all live route operations behind the existing gates.

Contour A remains NOT_PROVEN / BLOCKED. Contour B remains gated on Contour A deployment and independent acceptance.
