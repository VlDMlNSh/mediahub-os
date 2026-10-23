# MediaHub Chat Tree Map Addendum — Wave 428 — FreeLLMAPI pending check repair

- Date: 2026-10-23
- Status: **IMPLEMENTED ON PR #563 / EXACT-HEAD CI VERIFIED / REVIEW AND MERGE PENDING**
- Main SHA observed: `4fe1486e2062d276c4dba2ab8c9ed97f261e9086`
- Repair PR: [#563 — prevent FreeLLMAPI live qualification from holding main pending](https://github.com/VlDMlNSh/mediahub-os/pull/563)
- Repair report: [Wave 428](https://github.com/VlDMlNSh/mediahub-os/blob/fix/freellmapi-main-pending-check-20261023/docs/checkpoints/mediahub-freellmapi-pending-check-repair-wave428-2026-10-23.md)
- Prior merged PR: [#530](https://github.com/VlDMlNSh/mediahub-os/pull/530)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)

## Finding

PR #530 merged successfully at `4fe1486e2062d276c4dba2ab8c9ed97f261e9086`, but the post-merge commit status remained pending because FreeLLMAPI Live Qualification run [#39959271970](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39959271970) was queued with **zero jobs**. That workflow triggered on pushes to main but originally had only a self-hosted runner job. This was a stuck run, not an observed failing test. Do not mark it successful manually.

## Repair and current evidence

PR #563 splits deterministic contract tests onto GitHub-hosted `ubuntu-latest` and retains real provider discovery/inference only as a manually dispatched, owner-confirmed, exact-main-SHA-bound self-hosted job. It separates concurrency groups so the first push after the fix can cancel the old queued run; this cancellation has **not yet occurred** because PR #563 remains unmerged.

Current PR head `31e26e013ae428609a75dd611a8b0e7826aee7db` exact-head checks:
- [FreeLLMAPI workflow run 39962161545](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39962161545): **SUCCESS**; hosted contract job passed and the live gate/qualifier were skipped on the PR event.
- [Astra Verify 39962161549](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39962161549): **SUCCESS**.
- [Astra Cloud Runtime Validation 39962161538](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39962161538): **SUCCESS**.
- Submitted independent PR reviews: **NONE**. The PR is open, mergeable, and not merged.

## Cloud Claude and local Llama boundaries remain unchanged

- Cloud Claude route: GitHub-hosted FCC → OpenRouter concrete `:free` model only; owner and exact-SHA gates, no paid fallback; pinned ECC guidance remains guidance-only, with hooks/MCP/controller disabled. Do not make a new provider call until admission and independent review gates are satisfied.
- Local Llama candidate: `llama3.2:3b` works directly through Ollama on `Voktors-Mini.Dlink`, but the active FCC listener was previously observed on `0.0.0.0:8082` with `proxy_auth_enabled=false`, and the FCC model catalogue did not expose the Llama alias. Local FCC task execution remains **BLOCKED** until loopback/auth/model configuration and the actual FCC-routed call are verified.

## Next action

Obtain the required independent review for PR #563 and integrate only when all required gates pass. After merge, verify the new main push runs the hosted FreeLLMAPI contract tests and that run #39959271970 is canceled by the concurrency group; do not confuse that cancellation with live provider qualification. Live FreeLLMAPI inference remains a separate explicit owner-dispatched task.
