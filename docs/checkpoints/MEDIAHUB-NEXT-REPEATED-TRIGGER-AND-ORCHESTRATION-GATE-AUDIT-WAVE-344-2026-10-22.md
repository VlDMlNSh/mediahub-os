# Wave 344 — repeated /next orchestration gate audit (2026-10-22)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
Checkpoint (working branch): https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-next-wave340-20261022/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
Draft evidence PR: https://github.com/VlDMlNSh/mediahub-os/pull/442

## Immutable target and current refs

- `refs/heads/main` -> `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`.
- Controller blob SHA on main: `9453403bba899a2400ee3fb874d32badd034c704`.
- PR #437 HEAD `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`, open, non-mergeable.
- PR #441 HEAD `9f40b90c3106662cfcc337c48f29e4794fa713dc`, open, non-mergeable.
- PR #442 current HEAD at the beginning of this pass `08db5eb9eb290b8ba348752a5e6d915086c7aa82`, draft/open/unmerged. A report-only follow-up may advance its head; re-read the final head before claiming its exact status.

## Controller source review

The workflow has two entry modes:
1. `workflow_dispatch` with default `mode=probe`, which is explicitly non-launching and intended to use no secrets;
2. bounded agent dispatch only when `workflow_dispatch` uses `mode=agents` and `confirm=yes`, or the issue-comment event satisfies the full predicate.

The issue-comment predicate in source is exact: issue #301, not a pull request, comment body exactly `/next`, and author association `OWNER`. The job additionally checks the admission variable and required secrets before dispatch. Controller code is at https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml.

Current evidence shows repeated issue-comment controller runs on main are skipped, including:
- run #39678989141, comment #6326943789;
- run #39678989202 (Astra chat control plane, same event);
- older controller runs #39678854650, #39676805940, #39676724385, and others on the same main SHA.
The triggering comment for run #39678989141 was a report announcement, not literal `/next`, so the skip matches the exact gate. No successful controller dispatch or Gemini child run IDs were established in this pass.

## CI, reviews, governance

- Main SHA has Astra Verify run #39669337754 SUCCESS.
- Exact-head check suites for PR #437 (#107496095390), PR #441 (#107524023551), and PR #442 (suite IDs recorded in earlier Wave 343 evidence) had been observed QUEUED with zero check runs; this pass did not establish a terminal successful CI state for those PR heads.
- Formal review lists for PR #437/#441/#442 were previously observed empty; no independent security review is established here.
- Branch-protection endpoint returns 403 `Resource not accessible by integration`; an empty ruleset list does not prove branch protection is absent. Required governance and effective token permissions therefore remain NOT VERIFIED.
- No secret values were read. No issue-comment trigger was posted and no workflow dispatch mutation was made.

## Executor / orchestration status

- Gemini Agent 1: NOT RUN — no controller dispatch ID, child run ID, immutable task manifest, or artifact digest.
- Gemini Agent 2: NOT RUN — no controller dispatch ID, child run ID, independent contract/test report, or artifact digest.
- Gemini Agent 3: NOT RUN — no controller dispatch ID, child run ID, security/provenance report, or artifact digest.
- Claude-FCC/Ollama on `Voktors-Mini.Dlink`: NOT RUN / NOT VERIFIED. SentinelX host ping/state previously responded, but a bounded `which agent-browser` command timed out; no browser session or local task evidence exists.
- Agent-browser: NOT RUN; skill requires `agent-browser skills get core` before use. Runtime CLI availability is not confirmed.
- No controller run ID or three Gemini child run IDs are reported as successful. No target manifest or artifacts/digests are available.

## Disposition

**BLOCKED / NOT QUALIFIED / NOT ACCEPTED.**

Next safe step: use the controller's documented no-secret `workflow_dispatch` probe only after authorized review confirms it is the intended test route and permissions allow it; then verify caller context and check scheduling. Do not substitute a report comment for the literal owner trigger, and do not run `mode=agents` until governance, security review, effective token scope, admission flag, and HMAC protocol are independently verified. Continue to keep Gemini transport on GitHub only and local Claude/browser work on the identified Mac only.
