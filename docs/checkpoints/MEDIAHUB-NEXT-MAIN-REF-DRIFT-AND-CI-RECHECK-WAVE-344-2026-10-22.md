# Wave 344 — main ref drift and exact-head CI recheck (2026-10-22)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
Working PR #442: https://github.com/VlDMlNSh/mediahub-os/pull/442

## Ref and source evidence

- At the start of this pass, `refs/heads/main` was `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`; a later fresh read in the same pass resolved main to `f4ad65acdb82d25b93845279361502b6737e1d21`. Treat the latter as the latest observed main SHA, but this ref movement needs correlation to the commit history before assuming the reason.
- Controller file read from main still returned blob SHA `9453403bba899a2400ee3fb874d32badd034c704` (14,728 chars).
- Bootstrap, canonical map and Master Roadmap were last read in Wave 343; no changes to those canonical files were made in this pass.
- Working PR #442 advanced to HEAD `59e0a199889e2c5db5093ff42776439a64208721`; it remains OPEN, draft, unmerged, mergeable=true, base `docs/mediahub-chat-tree-map-20261012`.

## Exact-head CI

- PR #437 HEAD `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`: check suite `107496095390` still QUEUED, zero check runs.
- PR #441 HEAD `9f40b90c3106662cfcc337c48f29e4794fa713dc`: check suite `107524023551` still QUEUED, zero check runs.
- PR #442 HEAD `59e0a199889e2c5db5093ff42776439a64208721`: suite `107570082450` QUEUED, zero check runs.
- Latest observed main SHA `f4ad65acdb82d25b93845279361502b6737e1d21`: suite `107553033246` (freebuff-web) QUEUED with zero check runs; suite `107557209401` (GitHub Actions) QUEUED with one check; suite `107553038685` completed SUCCESS with one check.
- Main exact-SHA workflow runs returned: Astra Verify run `39685040842` completed SUCCESS; Astra autonomous queue supervisor run `39686595751` remains QUEUED.
- Formal review retrieval needs a corrected connector argument (`repo_full_name`, not `repository_full_name`); this pass therefore does not claim new review evidence.

## Controller and executor status

- The controller's issue-comment dispatch requires issue #301, not a PR, exact comment body `/next`, and author association `OWNER`. Prior run `39678989141` was skipped because comment `6326943789` announced a report rather than containing the literal trigger.
- Gemini Agents 1–3: NOT RUN. No current controller dispatch ID, child run IDs, target manifest, or artifact digests.
- SentinelX host `Voktors-Mini.Dlink` / `host_5f7264034bdf0b51` remains listed as operational; state query returned transient `agent_disconnected/read_loop_ended`. No host command, browser session, or local Claude/Ollama job was run.
- Governance, branch-protection policy (prior endpoint returned 403), effective token scope, independent controller security review, and approved non-launching probe remain NOT VERIFIED. No secret values were accessed, no trigger comment was posted, and no dispatch or merge was attempted.

## Disposition

**BLOCKED / NOT QUALIFIED / NOT ACCEPTED.**

Next: correlate main SHA movement using commit metadata; resolve the persistently queued exact-head check suites; obtain independent review and verify governance/token scope; then perform only an approved non-launching probe. Local executor work remains separate and must use only the identified Mac host after a supported, bounded session is available.
