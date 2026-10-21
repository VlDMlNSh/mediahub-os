# Wave 319 — PR #432 source-bound security review (2026-10-21)

## Disposition

**SOURCE-ONLY REVIEW COMPLETED / FORMAL INDEPENDENT REVIEW NOT PRESENT / NOT QUALIFIED / NO DISPATCH.**

This is an additional source inspection, not a formal GitHub approving review and not a substitute for a second independent reviewer. No secrets were read, no workflow was dispatched, and no runtime/provider behavior is claimed.

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/432
- Inspected PR head: `269b57b8b9c412261c97c4811bd49cbb4122ba03`
- Inspected controller blob on PR branch: `9453403bba899a2400ee3fb874d32badd034c704`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governance issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Source checks

1. **Transport separation:** the controller's dispatch/monitor job uses `MEDIAHUB_GITHUB_TOKEN` for GitHub API calls. The three child workflow sources do not reference this token and the reviewed controller/child contracts prohibit `secrets: inherit`.
2. **Explicit dispatch boundary:** the controller's agent job is gated to a `workflow_dispatch` on `refs/heads/main`, `mode=agents`, and `confirm=yes`; probe is the default. The issue-comment bridge is separately limited to issue #301 (not a PR), exact body `/next`, and `author_association == OWNER`.
3. **Immutable target:** the controller resolves a full SHA, confirms the returned commit SHA equals the requested SHA, and places the same SHA in all three signed child payloads.
4. **HMAC authorization:** the controller signs a canonical JSON payload with sorted keys and compact separators; each child reconstructs the same field set and uses `hmac.compare_digest`. The child authorization job has `permissions: {}`, checks repository/event/ref, SHA shape, UUID-like dispatch ID, `base_ref=main`, and `scope=contour-a`; provider execution depends on authorization success.
5. **Partial/ambiguous dispatch:** the controller records each intended child before POST, does not print exception bodies, distinguishes definite HTTP 4xx from ambiguous transport/5xx outcomes, correlates runs by unique dispatch ID in the run title, and fails the batch on non-success or timeout.
6. **Evidence boundary:** the inspected workflow summaries record shared target SHA, correlation IDs, dispatch status, child run IDs and conclusions. No artifact digest or successful child execution exists for this pass because no dispatch occurred.

## Residual risks / required evidence

- Formal review submissions on PR #432 remain zero in the current GitHub review listing. This pass must not be treated as the required independent review.
- Existing CI validates YAML/actionlint and static source contracts, but the reviewed test changes are largely source-string assertions. They do not, by themselves, prove runtime HMAC interoperability, tamper rejection, secret configuration, effective token permissions, API behavior under rate limits, or the GitHub run-title reconciliation assumptions.
- The UUID shape regex `[0-9a-f-]{36}` checks length/character class, not canonical UUID structure. This is not a credential bypass by itself, but should be tightened and negatively tested for precise input validation.
- The controller's HTTP error wrapper reads up to 300 bytes of response body into an exception string. Current catch blocks avoid printing the exception string and log only the HTTP code/type; preserve this non-disclosure invariant in future edits and tests.
- A comment in ChatGPT does not produce a GitHub issue-comment event. Automatic dispatch for every ChatGPT `/next` remains unimplemented/unproven without an explicitly authorized event bridge.
- Alamo/server 3 identity, capabilities, allowlist, browser availability and non-paid Claude route remain unverified. No Claude/browser session ID exists.
- Issue #301 still requires A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy, accepted runner/workspace/network manifest, Draft 2020-12 schema validation with format assertions and negative fixtures, and semantic reference resolution.

## Exact-head CI context

At inspected head `269b57b8b9c412261c97c4811bd49cbb4122ba03`, these runs report success:
- [Contract validation 39647070718](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070718)
- [Controller probe 39647070682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070682)
- [Astra Verify 39647070683](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070683)
- [Cloud Runtime Validation 39647070609](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070609)
- [Non-launching caller probe 39647070781](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070781)

The controller dispatch job was skipped in the inspected probe. These results are not evidence of a successful three-agent run.

## Next bounded step

Add executable, secret-free tests for the exact canonical HMAC payload and negative cases (wrong workflow filename, task tamper, target SHA tamper, wrong scope/base, malformed UUID, invalid/missing signature), and tighten UUID validation. Run them through PR CI. In parallel, obtain a separate formal review tied to the same exact head. Keep the controller unmerged and agent dispatch disabled until all governance, secret configuration, and route gates are evidenced.
