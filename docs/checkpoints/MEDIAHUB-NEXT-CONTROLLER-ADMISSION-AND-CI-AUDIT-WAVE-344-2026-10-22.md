# Wave 344 — controller admission and exact-head status audit (2026-10-22)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
Controller: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml

## Immutable target and source evidence
- Main ref still resolves to `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`.
- Controller blob SHA `9453403bba899a2400ee3fb874d32badd034c704`.
- Bootstrap blob SHA `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical map blob SHA `38d8903bc640fd37009f0fc19a11ea7869840dbc`; Contents endpoint returns empty content, while blob API previously yielded the full map.
- Canonical checkpoint blob SHA `3bb3ea262c2a30c8f780d36eb61902833325fb29`; canonical branch does not yet contain recent working-branch Wave 342/343 appendices.
- Master Roadmap blob SHA `cea169e55e02903ab9871d51ff643b3da7ef0e8c`.

## Current PR heads and exact-head CI
- PR #437 HEAD `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`, open/non-mergeable. Check suite `107496095390`: QUEUED, 0 check runs.
- PR #441 HEAD `9f40b90c3106662cfcc337c48f29e4794fa713dc`, open/non-mergeable. Check suite `107524023551`: QUEUED, 0 check runs.
- PR #442 HEAD `c3d5230e002837263c930126cce14899de137052`, draft/open/unmerged. Check suite `107550813359`: QUEUED, 0 check runs. Actions runs query for this exact SHA returned 0.
- Formal review lookup was attempted with the wrong connector argument key and rejected; therefore current review state is NOT VERIFIED in this pass. Earlier checks recorded zero reviews, but that is not re-asserted as current without a valid call.
- Main Astra Verify run `39669337754` completed SUCCESS on main SHA. Main controller issue-comment run `39678989141` completed SKIPPED, with all four jobs skipped.

## Controller admission logic inspected
The source uses `permissions: {}` and has two trigger paths:
1. workflow_dispatch mode `probe` is non-launching and maps no credentials;
2. agent mode requires `mode=agents` and `confirm=yes`, or an issue_comment on issue #301 with no PR, body exactly `/next`, and author association `OWNER`.

The child-dispatch job additionally checks `vars.MEDIAHUB_GEMINI_BATCH_ENABLED`, reads `secrets.MEDIAHUB_GITHUB_TOKEN` and `secrets.MEDIAHUB_DISPATCH_HMAC_KEY` only inside the dispatch job, validates an explicit immutable target SHA, and signs per-child requests. The skipped historical run was triggered by owner comment `6326943789`, which announces a report rather than containing literal `/next`; it therefore did not reach the dispatch path. No new trigger or dispatch was issued.

## Security and execution disposition
- Owner's prior confirmation that the three settings exist is retained; no secret values were accessed. Effective token scope, repository governance/required checks, and independent controller security review remain NOT VERIFIED.
- Branch protection endpoint returns 403; ruleset listing is empty. Neither result proves branch protection is absent.
- Gemini Agents 1–3: NOT RUN. No current controller dispatch ID, child run IDs, target manifest, or artifact digests.
- SentinelX host `Voktors-Mini.Dlink` / `host_5f7264034bdf0b51` was previously confirmed responsive to ping/state/capabilities. A read-only browser CLI lookup timed out; no browser session or local Claude-FCC/Ollama job was run in this pass.
- No secret reads, issue-comment trigger, workflow dispatch, host modification, merge, deployment, qualification, or acceptance.

## Disposition and next step
**BLOCKED / NOT QUALIFIED / NOT ACCEPTED.**

Next: resolve why GitHub check suites remain queued with zero check runs; obtain independent review of controller admission/HMAC and PR #437; verify branch governance and effective token scope via authorized metadata-only evidence; only then run the controller's approved non-launching probe. Re-establish a bounded SentinelX session before attempting the required `agent-browser skills get core` step or local free/no-paid-fallback Claude-FCC/Ollama qualification.
