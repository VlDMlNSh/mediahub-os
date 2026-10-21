# Wave 343 — exact-head CI and executor liveness recheck (2026-10-22)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-next-wave340-20261022/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Immutable target and source reads

- Current main ref: `refs/heads/main` -> `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`.
- Controller on main blob SHA: `9453403bba899a2400ee3fb874d32badd034c704`.
- Canonical map blob SHA: `38d8903bc640fd37009f0fc19a11ea7869840dbc`; Contents endpoint returns empty text, but blob API successfully read 1,165,629 characters.
- Bootstrap blob SHA: `75f30750183efe8c6877368e9f0ada48f8e81ea7`, 38,070 characters.
- Canonical checkpoint blob SHA: `3bb3ea262c2a30c8f780d36eb61902833325fb29`, 393,805 characters; it trails the Wave 342 working-branch checkpoint, so the canonical documentation branch has not yet incorporated the Wave 342/343 evidence.
- Master Roadmap blob SHA: `cea169e55e02903ab9871d51ff643b3da7ef0e8c`, 788,951 characters.

## Exact-head CI and review

- PR #437: HEAD `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; suite `107496095390` remains QUEUED with zero latest check runs. Formal review list is empty. PR open, not mergeable.
- PR #441: HEAD `9f40b90c3106662cfcc337c48f29e4794fa713dc`; suite `107524023551` remains QUEUED with zero latest check runs. Formal review list is empty. PR open, not mergeable.
- PR #442: HEAD `5da1dea0b57e70c695ee8b40f28e1d2a96d548d2`; suite `107544433195` remains QUEUED with zero latest check runs. Formal review list is empty. PR open, draft, unmerged.
- Main SHA has Astra Verify run `39669337754` SUCCESS. Controller issue-comment run `39678989141` SKIPPED, with all four jobs skipped. Its source predicate requires a literal owner comment `/next`; the triggering comment `6326943789` announced a report and was not the literal trigger. No Gemini child runs were found.
- Branch protection API returned 403. Ruleset listing returned an empty list; neither result establishes branch governance, required reviewers, or effective token scope.

## SentinelX / local executor

- SentinelX host listing identifies `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`, macOS 14.7.4 ARM64, SentinelX 0.22.0; one host slot is active.
- Ping succeeded. Capabilities and state succeeded on retry after one transient `agent_disconnected/read_loop_ended` response.
- A bounded read-only `which agent-browser` exec request timed out after 30 seconds with no command result. This does not establish whether the CLI is installed; do not retry identical request. No browser session was started, no `agent-browser skills get core` was executed, and no local Claude/Ollama job ran.
- Agent-browser skill instructions were re-read: the installed CLI's `agent-browser skills get core` is required before using the browser. Host identity is confirmed, but runtime availability and browser session remain unverified.

## Dispatch / governance

- Gemini Agents 1–3: NOT RUN; controller dispatch ID and child run IDs absent; no evidence manifests or artifact digests.
- Owner-reported presence of `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`, and `MEDIAHUB_GEMINI_BATCH_ENABLED` is recorded, but values were not read. Effective token permissions, trusted-main non-launching probe, independent controller security review, and governance requirements remain NOT VERIFIED.
- No issue-comment trigger, workflow dispatch, host modification, secret read, merge, deployment, qualification, or acceptance occurred.

## Disposition and next action

**BLOCKED / NOT QUALIFIED / NOT ACCEPTED.**

1. Resolve queued check suites or obtain evidence why the check provider is not scheduling exact-head checks.
2. Obtain independent security review of PR #437 and controller admission/HMAC path.
3. Verify governance and effective token scope through an authorized metadata-only route.
4. Only after gates close, use the controller's approved non-launching probe; do not dispatch agents merely to diagnose a skipped run.
5. Re-establish a bounded SentinelX read-only session through a supported method; then verify agent-browser core instructions and the local free/no-paid-fallback Claude-FCC/Ollama route.
