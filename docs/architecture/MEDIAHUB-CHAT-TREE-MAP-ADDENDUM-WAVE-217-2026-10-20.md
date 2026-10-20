# MediaHub OS Contour A — map addendum, GitHub Transport Wave 217

Date: 2026-10-20

This addendum records the GitHub-hosted controller integration and runtime dispatch. It supplements, but does not replace, the canonical map.

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 217 evidence report: [MEDIAHUB-CONTOUR-A-GITHUB-TRANSPORT-CONTROLLER-WAVE-217-2026-10-20.md](../checkpoints/MEDIAHUB-CONTOUR-A-GITHUB-TRANSPORT-CONTROLLER-WAVE-217-2026-10-20.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Controller PR #408 merged as `27edfd5f04c6704ee7136c6cc73cf46f9731beb7`.
- Workflow input fix PR #411 merged as `7d86e852bf5837bc7dcf650327b22c1b27886efa`.
- Controller run [39396582084](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396582084) successfully executed the dispatch step using `MEDIAHUB_GITHUB_TOKEN`.
- Child runs: Agent 1 [39396593650](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396593650) SUCCESS with PR [#413](https://github.com/VlDMlNSh/mediahub-os/pull/413); Agent 2 [39396596067](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396596067) IN_PROGRESS at report time; Agent 3 [39396598015](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396598015) SUCCESS with PR [#414](https://github.com/VlDMlNSh/mediahub-os/pull/414).
- Do not mark the batch complete until the controller and Agent 2 finish. Agent-produced PRs remain proposals and require independent review.
- The canonical map Contents API returned empty content despite its known blob SHA. It was not overwritten; this addendum is the safe navigation update pending a reliable full-file read.


## Wave 218 — persistent cloud-agent transport rule (2026-10-20)

- Binding owner-directed policy: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md](MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md).
- Bootstrap section 1B now mandates the GitHub-hosted Actions controller and `MEDIAHUB_GITHUB_TOKEN`; direct SentinelX/server/local CLI agent launches are prohibited.
- Wave report: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-RULE-WAVE-218-2026-10-20.md](../checkpoints/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-RULE-WAVE-218-2026-10-20.md).
- Runtime batch: controller dispatch succeeded but monitor failed because Agent 2 failed actionable-PR validation; Agent 1 and Agent 3 jobs succeeded. See report for exact run IDs.
- Canonical map file itself was not overwritten due to empty Contents wrapper output; this addendum records navigation and evidence safely.


## Wave 219 — runtime diagnosis and independent PR review (2026-10-20)

- Report: [Wave 219 diagnosis and review](../checkpoints/MEDIAHUB-GEMINI-TRANSPORT-FAILURE-AND-AGENT-PR-REVIEW-WAVE-219-2026-10-20.md).
- Agent 2 failed after repeated GitHub MCP file-read errors, Gemini free-tier input-token quota exhaustion and max-session-turn exhaustion; no stdout artifact was produced. Controller correctly reported the batch failure; dispatch itself succeeded.
- PR #413 and #414 received REQUEST_CHANGES reviews (IDs 5582981729 and 5582982170). PR #413 has an unverified fixed timestamp; PR #414's schema-gap claims need exact schema-source and validator evidence. Neither merged.
- Continue only through the GitHub-hosted controller with MEDIAHUB_GITHUB_TOKEN; no paid fallback or alternate launch transport.


## Wave 220 — Gemini failure-handling evidence review (2026-10-20)

- Report: [Wave 220 failure-handling review](../checkpoints/MEDIAHUB-GEMINI-FAILURE-HANDLING-REVIEW-WAVE-220-2026-10-20.md).
- Re-read all three child workflows on `main`: Agent 1 blob `09523d809530ae5b7bf528eab5fa53bc5deaf92d`; Agent 2 blob `259c8c82b8d90a39e1c90e65390e469b241b5581`; Agent 3 blob `91b5397001e088dfae2f450ee77c9c23118b5601`.
- Agent 2 job `118540763883` log shows an unconfigured `update_topic` call, repeated GitHub MCP read failures, Gemini free-tier input-token quota exhaustion, then `FatalTurnLimitedError`. The post-step validator had no usable stdout JSON and failed closed.
- The Gemini action's internal artifact-upload step was skipped in this failed run; current workflow validation steps use `if: success()`. Proposed next change: best-effort outer diagnostic upload with `if: always()`, no secret-bearing files, plus stricter stop-on-first-tool-error prompt language. No workflow edits or rerun were performed.
- Preserve approved GitHub Actions controller transport, no paid fallback, no auto-merge, and no qualification claims. Mainline workflow modifications require a separate reviewed PR and exact-head CI.


## Wave 221 — sanitized Gemini failure diagnostics proposal (2026-10-20)

- Report: [Wave 221 implementation and verification status](../checkpoints/MEDIAHUB-GEMINI-FAILURE-DIAGNOSTICS-WAVE-221-2026-10-20.md).
- Draft PR [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420) proposes an always-run sanitized diagnostic JSON artifact for all three child workflows and an explicit stop-after-MCP-error prompt rule.
- PR head `2016c1c99a44cbf9b700d0a1eba777a9964fed09`; child workflow blob SHAs: Agent 1 `e3de99ec9299b33a9c12e126aba785d55cfb71d9`, Agent 2 `75d9db95a9ccb75e5dfaba373f6d6ac77883fe11`, Agent 3 `b730bfb426450cda45a4252db6b4e370959e2061`.
- Read-back confirms the new steps and unchanged fail-closed validator. Exact-head CI was in progress when checked; not yet accepted. No agent rerun or merge.
- Raw stdout/tool arguments are deliberately not copied to the new artifact; it contains only run metadata, booleans, and tool-name success/failure counts. Controlled runtime failure-path validation is still required.


### Wave 221 CI result update

- PR #420 exact head `2016c1c99a44cbf9b700d0a1eba777a9964fed09`: associated Astra Cloud Runtime Validation run `39399830230` and Astra Verify run `39399830302` both completed with `success`.
- These are general repository checks, not dedicated workflow YAML lint or a controlled Gemini failure-path run. The PR remains a proposal; no merge, agent rerun, or qualification.
- Report updated with exact job IDs and verification boundary.
