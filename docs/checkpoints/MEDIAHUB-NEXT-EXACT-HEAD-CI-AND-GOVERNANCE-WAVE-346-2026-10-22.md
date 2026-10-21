# Wave 346 — exact-head CI and documentation branch recheck (2026-10-22)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Immutable refs observed

- `refs/heads/main` -> `f4ad65acdb82d25b93845279361502b6737e1d21`.
- Controller blob SHA `9453403bba899a2400ee3fb874d32badd034c704`.
- Canonical map blob SHA `38d8903bc640fd37009f0fc19a11ea7869840dbc` (Contents API empty; blob API previously returned full 1,165,629-character content).
- Bootstrap blob SHA `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical checkpoint blob SHA `3bb3ea262c2a30c8f780d36eb61902833325fb29`; canonical checkpoint is behind the working-branch checkpoint and has not absorbed Waves 342–345.
- Master Roadmap blob SHA `cea169e55e02903ab9871d51ff643b3da7ef0e8c`.

## Exact-head CI

- Main exact SHA `f4ad65acdb82d25b93845279361502b6737e1d21`: Astra Verify run `39685040842` completed SUCCESS; URL https://github.com/VlDMlNSh/mediahub-os/actions/runs/39685040842. A separate Freebuff check suite `107553033246` is QUEUED with zero checks.
- PR #437 HEAD `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`: Freebuff suite `107496095390` QUEUED, zero checks; PR remains open and non-mergeable.
- PR #441 HEAD `9f40b90c3106662cfcc337c48f29e4794fa713dc`: Freebuff suite `107524023551` QUEUED, zero checks; PR remains open and non-mergeable.
- PR #442 HEAD was observed changing during this pass. Initial snapshot `c3d5230e002837263c930126cce14899de137052` had suite `107550813359` QUEUED/zero checks; a later PR metadata snapshot returned HEAD `ffef2980b82bfc18a9f7018b52863f50a20ee5bd`. The suite result is stale for that later HEAD; do not claim exact-head CI for the current PR #442 without another check.
- Formal review state remains to be rechecked with the correct review API parameters. The previous review call failed schema validation and is not evidence of an empty review list.
- Branch-protection endpoint returns 403; an empty ruleset list is inconclusive and does not establish governance.

## Controller and executors

- Controller workflow source blob remains `9453403bba899a2400ee3fb874d32badd034c704`.
- Historical controller issue-comment run `39678989141` was SKIPPED because the triggering owner comment was a report announcement rather than exact body `/next`. It did not dispatch Gemini.
- Gemini Agents 1–3: NOT RUN; no controller run ID, child run IDs, correlated target manifest, or artifact digests.
- SentinelX host `Voktors-Mini.Dlink`, ID `host_5f7264034bdf0b51`, is listed operational; ping and summary capabilities responded. The previous read-only `which agent-browser` request timed out, so CLI availability/browser session remain unverified. No host command was retried or executed in this pass.
- No secrets were read, no issue trigger was posted, and no workflow dispatch, host mutation, merge, deployment, qualification, or acceptance occurred.

## Disposition

**BLOCKED / NOT QUALIFIED / NOT ACCEPTED.**

Next safe work:
1. Re-fetch PR #442 HEAD and query its exact-head check suite, not the previous SHA.
2. Diagnose the persistent queued Freebuff suites through permitted provider metadata or request provider-side repair; do not infer a pass from the successful Astra Verify run.
3. Obtain independent controller/HMAC review and verify governance/effective token scope through authorized metadata-only paths.
4. Only after these gates pass, run the approved no-secret, non-launching probe; keep Gemini agents NOT RUN until then.
5. Re-establish a bounded supported SentinelX read-only route, then run `agent-browser skills get core` only if CLI availability can be established without expanding host permissions.
