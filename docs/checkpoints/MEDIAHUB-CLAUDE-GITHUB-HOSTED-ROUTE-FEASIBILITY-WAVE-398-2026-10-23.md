# MediaHub OS — Claude GitHub-hosted execution route feasibility (Wave 398)

Date: 2026-10-23
Target repository HEAD checked: `main` = `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`
Canonical documentation branch checked: `docs/mediahub-chat-tree-map-20261012` = `222528d30ace88ed7ab4bf75152a35b5bfcf126c`

## Decision

**REQUEST CONFIRMED / IMPLEMENTATION NOT STARTED / ROUTE GOVERNANCE CONFLICT OPEN / NO AGENT DISPATCHED / NOT VERIFIED**

The requested outcome is a Claude Code agent executing on GitHub-hosted ephemeral compute, without owner-operated physical hardware. A hosted Claude worker already exists, but it explicitly routes to metered Anthropic API. The free-route requirement is not met by that worker.

## Evidence re-read

1. Existing [MediaHub Claude bounded worker](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/mediahub-claude-worker.yml), blob SHA `e1260cfef88ac02bcc9d0cce67bb497820f5f63c`:
   - `runs-on: ubuntu-latest`, `timeout-minutes: 15`, manual `workflow_dispatch`.
   - Job is gated by `vars.MEDIAHUB_ALLOW_METERED_ANTHROPIC == 'true'`.
   - Injects `secrets.ANTHROPIC_API_KEY`, installs `@anthropic-ai/claude-code`, and runs with repository-local Read/Glob/Grep/Edit/Write tools; shell/network tools and git mutations are disallowed.
   - Therefore it is **hosted and bounded, but metered Anthropic**, not the requested no-cost route.

2. Existing [FCC upstream](https://github.com/Alishahryar1/free-claude-code) README describes a provider-routing layer usable by Claude Code and other clients. It also says provider free-tier availability and limits are provider-controlled and may change. This is a candidate component, not proof that a particular provider is currently free, authorized for MediaHub data, available from GitHub Actions, or guaranteed not to fall back to a paid provider.

3. The current project routing decision recorded during [Wave 369 in Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6342174085) says the generic provider router/direct provider smoke workflows conflicted with the canonical contract, and remediation was made through [PR #458](https://github.com/VlDMlNSh/mediahub-os/pull/458). The existing route contract distinguishes Gemini's controller-only cloud route from Claude/FCC/Ollama's local route. A GitHub-hosted FCC route would change that contract; adding a workflow before explicit policy reconciliation would create an alternate route.

4. [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open. Its current Contour A gates include unresolved live authority references (OPEN P0) and independent qualification requirements. No secrets were read in this pass.

## Bounded implementation design

If the project policy is updated to authorize this route, implement it as a separate PR, not by weakening the existing metered worker:

- Use a dedicated GitHub-hosted ephemeral `ubuntu-latest` workflow and a pinned, reviewed FCC/client version.
- Require an explicit route profile that names the exact free-tier provider/model and rejects paid fallback; fail closed on missing, ambiguous, expired, or exhausted free quota.
- Do not inject `ANTHROPIC_API_KEY`; do not silently reuse the existing metered workflow.
- Start with read-only repository inspection and a small bounded task; only enable edits after sandbox/tool boundaries, prompt filtering, artifact sanitization, and negative tests pass.
- Keep `permissions: contents: read`, `persist-credentials: false`, immutable target SHA, concurrency limits, timeouts, cancellation, and short artifact retention. No commit/push or production action in the first qualification slice.
- Verify the actual provider/model selected at runtime without logging credentials, and prove that exhausted/free-tier-unavailable cases terminate rather than fall back to paid inference.
- Record exact run/job IDs, runner image, dependency/model-route versions, target SHA, artifact digest, tests, and independent review before calling the path qualified.

## Current verification results

- Current `main` SHA confirmed: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Current canonical documentation branch SHA confirmed: `222528d30ace88ed7ab4bf75152a35b5bfcf126c`.
- Existing Claude worker blob SHA re-read: `e1260cfef88ac02bcc9d0cce67bb497820f5f63c`.
- PR #441 exact-head combined-status endpoint returned an empty status list and formal review list was empty: **NOT VERIFIED**, not PASS.
- PR #500 remains OPEN/DRAFT at head `ef4a0214213835e6d8170ab0fe90c1f038959f89`; exact-head status endpoint returned no statuses and review list was empty: **NOT VERIFIED**.
- No workflow was dispatched, no model/provider was invoked, no secret value was read, and no code/workflow was changed.

## Next step

Record an explicit owner/governance decision that authorizes or rejects a GitHub-hosted Claude Code + FCC/free-provider route and defines the allowed provider/model, no-paid-fallback semantics, data class, and secret boundary. Until that route is authorized, keep the existing local-only Claude/FCC/Ollama policy intact and do not launch the metered Anthropic worker as a substitute.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
