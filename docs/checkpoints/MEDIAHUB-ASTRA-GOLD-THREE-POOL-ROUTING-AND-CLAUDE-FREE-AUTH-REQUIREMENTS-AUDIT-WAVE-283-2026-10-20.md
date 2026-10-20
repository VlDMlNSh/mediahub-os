# MediaHub OS — ASTRA GOLD Three-Pool Routing and Claude Free-Route Requirements Audit (Wave 283)

- Date: 2026-10-20
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **REQUIREMENT RECORDED / DOCUMENTARY AUDIT COMPLETE / RUNTIME NOT QUALIFIED**
- Purpose: record the user's clarified hard target architecture in GitHub and reconcile it against current source and active Contour A gates.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [the canonical documentation branch](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).
- Primary requirement contract: [Three-Pool Routing and Claude Free-Route Hard Requirements](../architecture/MEDIAHUB-ASTRA-GOLD-THREE-POOL-ROUTING-AND-CLAUDE-FREE-AUTH-HARD-REQUIREMENTS-WAVE-283-2026-10-20.md).

## 1. Owner direction captured

ASTRA GOLD A0 must decompose a delegated engineering mission and distribute bounded subtasks across three pool classes: (1) GitHub-hosted cloud workers, (2) separately admitted user machines in the MediaHub pool, and (3) Claude Code/local Claude as a local executor on Alamo only. For this multi-pool route, A0 is the dispatch/task-lifecycle authority; Jarvis must not bypass it with a second direct-local queue.

The local Alamo Claude lane is restricted to valid, source-pinned, explicitly admitted Claude Code-compatible routing through a proven zero-cost/free-tier route. Paid Anthropic API credentials/endpoints, paid Anthropic authorization, paid upstream paths, paid fallback, silent cost escalation, unauthorized credential reuse, or quota evasion are forbidden. FCC / FreeLLMAPI / OmniRoute / OpenFlux are owner-named candidate components, not automatically approved implementations. OpenFlux is specifically flagged for identity/role reconciliation because the existing A0 architecture describes its identified EDEAI candidate as a qualification-gated desktop agent rather than proving it to be a router.

This clarifies/supersedes the Wave 264 direct-local alternative for delegated multi-pool missions. It does not activate local routes now, weaken any issuer/capability/A3/Product State Authority boundary, or remove the requirement that the GitHub-hosted pool remain independently operable without user-owned hardware.

## 2. Source evidence refreshed

| Source | Current reviewed ref / SHA | Finding and limitation |
|---|---|---|
| `main` | `80be45a70732b1d568164571d4273a6397792c3b` | Implementation baseline not moved in this pass. |
| `docs/mediahub-chat-tree-map-20261012` before this pass | `e08ea614c85982592e39e62ae7738e623f676410` | Canonical documentation branch had Wave 282 at HEAD. |
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md@main` | blob `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | A0 is the ASTRA coordination/state authority; Claude Code and upstream/provider identities must be kept distinct; OpenFlux is a qualification-gated desktop-agent candidate. |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml@main` | blob `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` | Contains `CLAUDE_FCC`, `CLAUDE_OMNIROUTE`, and `CLAUDE_CODE_DIRECT`; routes require system admission and qualification. It does not prove an Alamo lane, no-paid-path rule, free-quota enforcement, or runtime qualification. |
| WB-14 Jarvis/A0 route source reconciliation | blob `4dead9e249603679f4193a5a0b0b0a13a04aa177` | A0 ingress, typed issuer, queue lifecycle and Alamo identity evidence remain open in that source pass. |
| PR #421 | head `77e101dfdeceb03eedb12fc823ab808a956a4fcb`, base `80be45a70732b1d568164571d4273a6397792c3b` | OPEN/DRAFT/UNMERGED; no independent review; latest returned Astra Verify failed and non-launching caller-context probe had startup_failure; Cloud Runtime Validation succeeded. Keep Gemini dispatch blocked. |
| PR #426 | head `6caf55977260e808a055c8c4b9a04d68eb050d8c`, base `80be45a70732b1d568164571d4273a6397792c3b` | OPEN/DRAFT/UNMERGED; Astra Verify and Cloud Runtime Validation succeeded; no independent review. This is a safe non-launching probe candidate, not approval to dispatch Gemini. |
| PR #425 | head `ce44a47b0d327a5cca9593e529fe97b492ffaa4a` | OPEN/DRAFT/UNMERGED; exact-head Verify and Cloud Runtime Validation succeeded; no independent review. |
| PR #423 | head `ccb302b03ce224059b898d4ac6599e9f46301721` | OPEN/DRAFT/UNMERGED; exact-head checks succeeded; no independent review. |
| Issue #301 | updated `2026-10-20T16:20:13Z` at time of read | OPEN; continue separating cloud-pool qualification from local/user-node admission. |

External source cross-checks used only to constrain claims, not to qualify software: [FCC README](https://github.com/bitplz/fcc/blob/main/README.md) states its proxy can select free, paid or local models, so tool identity alone cannot enforce the no-paid-route requirement; [OmniRoute Claude Code guide](https://omniroute.hagicode.com/en-US/guides/claude-code-configuration/) documents configurable gateway targets; the [FreeLLMAPI overview](https://kossolapov.com/en/blog/freellmapi-claude-code) distinguishes Claude Code from upstream routed models. No component was installed, invoked or security-reviewed in this pass.

## 3. GitHub changes in this pass

The following artifacts are added/updated on `docs/mediahub-chat-tree-map-20261012` only:
1. Primary hard-requirements contract: `docs/architecture/MEDIAHUB-ASTRA-GOLD-THREE-POOL-ROUTING-AND-CLAUDE-FREE-AUTH-HARD-REQUIREMENTS-WAVE-283-2026-10-20.md`.
2. This Wave 283 report.
3. Canonical map index.
4. Continuation checkpoint.
5. Master Roadmap addendum.

Issue #301 receives a linked top-level comment so the requirement is visible from the active cloud-agent-fabric work item. This documentary change does not change `main`, runtime policy, router configuration, or active credentials.

## 4. Ref, review and integration truth

- Documentation branch HEAD before the pass: `e08ea614c85982592e39e62ae7738e623f676410`.
- Main HEAD: `80be45a70732b1d568164571d4273a6397792c3b`.
- Compare result before this pass: DIVERGED, docs branch 2,877 ahead / 44 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`; compare response was capped at 300 file records. No wholesale merge/rebase was attempted.
- GitHub returned no branch rulesets. The queried branch payload listed `protected=false`; do not infer required reviews/protections exist.
- PR #421 / #423 / #425 / #426 are separate OPEN/DRAFT candidates; no independent review was returned for the reviewed candidates. PR #421's current CI regression remains a blocker.
- All updated docs are to be re-read and their final blob SHAs captured after this report is committed.

## 5. Checks and no-go actions

Read-only source/ref/status checks completed. No local tests were run in this documentation pass. No model/provider invocation, router installation, paid/free credential use, secret access, host inspection, workflow dispatch, Gemini agent invocation, merge, deployment, route qualification, or acceptance occurred.

Contour A remains **NOT_PROVEN / BLOCKED**. Contour B remains gated on Contour A deployment and independent acceptance.

## 6. Next bounded step

1. Reconcile issuer/capability, signed mission/task envelope, A0 ingress and cross-pool lifecycle before any runtime wiring.
2. Create a route-admission schema/matrix with explicit host binding, upstream identity, free entitlement, paid-fallback=false, quota/egress rules and candidate source pins; add static negative tests without calling providers.
3. Separately diagnose PR #421's failed Astra Verify / caller-context probe, get independent security review, and keep Gemini dispatch blocked until all evidence gates pass.

No route is currently claimed as available, free, installed, qualified or accepted merely because the target requirement is recorded.
