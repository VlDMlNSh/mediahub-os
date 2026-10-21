# Wave 342 — controller issue-comment trigger diagnosis (2026-10-22)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
Prior Wave 341 report: MEDIAHUB-NEXT-EXACT-HEAD-ACTIONS-AND-EXECUTOR-RECHECK-WAVE-341-2026-10-22.md

## New finding: why the inspected controller runs were skipped

Freshly fetched controller source on `main` is blob SHA `9453403bba899a2400ee3fb874d32badd034c704`; current `refs/heads/main` resolves to `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`.

The workflow's `issue_comment` gate requires all of the following:
- issue number 301;
- the issue is not a pull request;
- comment body exactly equals `/next`;
- comment author association exactly equals `OWNER`.

The inspected run #39678989141 was an `issue_comment` event by the owner on main, but its comment ID `6326943789` contains a Wave 338 report announcement, not the literal body `/next`. Therefore the event does not satisfy the controller's dispatch predicate. Run #39678989141 and related issue-comment runs being SKIPPED is consistent with the workflow source; it is not evidence that Gemini dispatch succeeded or that secrets were validated.

Run details: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39678989141
Controller source: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml

## Exact-head checks and reviews

- PR #437 HEAD `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`: suite `107496095390` QUEUED, zero latest check runs, zero formal reviews.
- PR #441 HEAD `9f40b90c3106662cfcc337c48f29e4794fa713dc`: suite `107524023551` QUEUED, zero latest check runs, zero formal reviews.
- Wave 341 documentation PR #442 HEAD `deb35a504d832591f0a3a53fcb79b1817047009b`: suite `107543383571` QUEUED, zero latest check runs, zero formal reviews. PR remains draft.
- Main exact SHA has Astra Verify run #39669337754 SUCCESS, while controller run #39678989141 is SKIPPED. The main branch-protection API remains inaccessible (403); empty ruleset results do not establish absence or presence of required governance.

## Executor and dispatch status

- Gemini Agents 1–3: NOT RUN; no controller dispatch ID, child run IDs, target manifest, or artifacts/digests.
- No new workflow was dispatched. This integration exposes no dedicated GitHub Actions dispatch mutation; the fetch endpoint is read-only. No issue comment trigger was posted.
- SentinelX connectivity is known from the previous pass only; no local host command or browser session was executed in this pass. Ollama/Claude-FCC and agent-browser remain NOT VERIFIED/NOT RUN.
- No secrets were read; no merge, deployment, qualification, or acceptance occurred.

## Disposition

**BLOCKED / NOT QUALIFIED / NOT ACCEPTED.**

The next safe action is to complete the queued exact-head checks and independent security/governance review. Only after these gates are satisfied should a literal owner `/next` issue comment be considered as the controller trigger, with the controller's probe/agent admission predicates checked beforehand. Do not use a report announcement as if it were a trigger, and do not bypass a failing or unknown gate.
