# Canonical map addendum — Wave 363 four-executor orchestration

Date: 2026-10-22
Detailed report: [Wave 363](../checkpoints/MEDIAHUB-NEXT-FOUR-EXECUTOR-ORCHESTRATION-AND-SENTINELX-AUDIT-WAVE-363-2026-10-22.md)
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)

## Orchestration target

Each `/next` should use one immutable target SHA and one bounded task manifest, dispatch Gemini 1–3 through the approved GitHub Actions controller, and route the fourth task to Claude only through the positively qualified approved SentinelX host. Collect all four reports, reconcile IDs/digests, verify tests and changed paths independently, then prepare PRs without collapsing verification, review, merge, qualification or acceptance into one status.

## Current blockers

- The owner-reported `MEDIAHUB_GEMINI_BATCH_ENABLED=false` gate remains closed; no probe/batch was dispatched in Wave 363.
- Controller source is present at blob `3becd61702b3cad5a40f7d2a4de0b7fd6aee4b4f`, but source read is not runtime qualification.
- SentinelX host `Voktors-Mini.Dlink` pings successfully intermittently, but capabilities/state calls repeatedly fail with `duplicate_session` / `read_loop_ended`. No command or browser session was launched.
- Approved Alamo identity/allowlist remains unverified. Do not guess or substitute host.
- PR #444 is open, unmerged and exact-head CI/review NOT VERIFIED. PR #441 remains open and mergeability-blocked.

## Estimate

12–24 engineering hours for controller qualification, local route qualification, shared envelope/reconciliation, and an end-to-end reviewed run; this is an effort estimate, not a promise of elapsed time.

The detailed report is the evidence ledger for host inventory, error counts, exact refs, statuses and next steps.
