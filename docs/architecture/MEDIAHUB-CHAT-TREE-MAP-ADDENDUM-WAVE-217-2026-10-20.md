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


### Wave 222 follow-up

- PR #420 remains the active Draft proposal. A semantic field-label defect was corrected: `job_status` held `GITHUB_JOB`, so the field is now `job_id` in all three workflows.
- Updated blobs: Agent 1 `21162f0771880d23d452e0d3b30dfa8b86db9b21`; Agent 2 `44b585b4481033fd1a4e3ac4c092669af90b8c65`; Agent 3 `026e59691281c27a43abe21109a8eb62f176fdc3`.
- Latest branch commit `d34c6cd646b59e83d75bf338739722464577dd56`; associated Astra Cloud Runtime Validation #39400178859 and Astra Verify #39400178898 were still in progress at last check. Earlier CI success applies to the earlier head only.
- Report: [Wave 221 and follow-up](../checkpoints/MEDIAHUB-GEMINI-FAILURE-DIAGNOSTICS-WAVE-221-2026-10-20.md). No merge, agent re-dispatch, or qualification.


- CI refresh for PR #420 head `d34c6cd646b59e83d75bf338739722464577dd56`: Astra Cloud Runtime Validation `39400178859` succeeded; Astra Verify `39400178898` was still running at the last check. The latter is not recorded as a pass until its final conclusion is observed.


## Wave 223 — diagnostic field correction and exact-head CI refresh (2026-10-20)

- Current main HEAD re-read: `80be45a70732b1d568164571d4273a6397792c3b`.
- PR [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420) remains unmerged. Prior exact-head CI for `d34c6cd646b59e83d75bf338739722464577dd56` completed successfully (runs [39400178859](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39400178859), [39400178898](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39400178898)); these are not dedicated workflow-lint or controlled failure-path tests.
- Corrected a reporting discrepancy: the JSON output key was `job`, not `job_id`, despite the variable being named `job_id`. The three child workflow proposals now emit `job_id`; read-back blob SHAs: `be6400d2f4d511bf7f12296b6e9505ddc10c9031`, `e46b6c107de41992009c7d960a0849ccc53df1ca`, `991ccecbfe8e5eda5568cd11be1be2daf061fcae`.
- Latest proposed head `d1ea86688ae5397e3149b1fb3b2192f0dc2bcb23`; exact-head CI completed successfully: [Astra Cloud Runtime Validation #39400954042](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39400954042), job `validate` / `118555237235`, and [Astra Verify #39400954055](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39400954055), job `verify` / `118555237769`. These are not dedicated workflow-lint or controlled failure-path tests.
- Branch is 9 commits ahead / 0 behind main. Open gates: independent review, dedicated workflow YAML lint, controlled failure-path artifact test, and action SHA pin review. No merge, redispatch, deployment, or qualification.


## Wave 224 — Gemini workflow lint and exact-head CI (2026-10-20)

- Report: [Wave 224 Gemini workflow lint and CI verification](../checkpoints/MEDIAHUB-GEMINI-WORKFLOW-LINT-AND-CI-WAVE-224-2026-10-20.md), report commit `b8de92f5741ff652be9f4b11c7e9d81bf95532e9`.
- PR [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420) branch head `eb61ac926ee0dd4a9c45bba3b03a3ef049c3f6a6`; compare against main `80be45a70732b1d568164571d4273a6397792c3b`: 10 ahead / 0 behind.
- Added actionlint v1.7.7 to Astra Verify for the three Gemini workflow files. Exact-head [Astra Verify #39401961171](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39401961171) and [Astra Cloud Runtime Validation #39401961153](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39401961153) both completed SUCCESS. The actionlint step and remaining Astra Verify steps passed.
- Workflow blob SHAs: Astra Verify `9b38238e59c45d06bffca5198ef1bd764c5fc467`; Agent 1 `be6400d2f4d511bf7f12296b6e9505ddc10c9031`; Agent 2 `e46b6c107de41992009c7d960a0849ccc53df1ca`; Agent 3 `991ccecbfe8e5eda5568cd11be1be2daf061fcae`.
- PR #420 remains Draft/unmerged, with no submitted reviews observed. Still open: independent review, authorized controlled failure-path test for sanitized diagnostic upload, and full-SHA pin review for `actions/upload-artifact@v4`. No Gemini redispatch, merge, deployment, or Contour A acceptance.


## Wave 225 — immutable upload-artifact action pin (2026-10-20)

- Report: [Wave 225 immutable pin](../checkpoints/MEDIAHUB-UPLOAD-ARTIFACT-IMMUTABLE-PIN-WAVE-225-2026-10-20.md).
- PR [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420) replaces the movable `actions/upload-artifact@v4` reference in all three Gemini child workflows with full SHA `cf430e030ddbb5b0abf93d22962f4752f3646cd9`, resolved from the official upstream `v7` tag.
- Upstream commit metadata identifies v7.0.2 dated 2026-10-07, reports a verified commit signature, and the pinned `action.yml` declares Node 24.
- Read-back workflow blobs: Agent 1 `89ded6bd650b6f14ab419151762dc3d4f2804a0d`; Agent 2 `7a067fd7093a31c243c9e1f0e2caeec701f29c18`; Agent 3 `d0e2e21d15523757293100f10a72e5e85232b7a2`.
- PR head `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`, 13 ahead / 0 behind main `80be45a70732b1d568164571d4273a6397792c3b`. Exact-head Astra Cloud Runtime Validation #39402774891 and Astra Verify #39402774885 were in progress when recorded; no pass is claimed yet.
- Independent review and authorized controlled failure-path test remain open. PR stays Draft/unmerged; no agent re-dispatch, secret read, deployment, or Contour A qualification.


### Wave 225 exact-head CI result

- Updated [Wave 225 report](../checkpoints/MEDIAHUB-UPLOAD-ARTIFACT-IMMUTABLE-PIN-WAVE-225-2026-10-20.md): [Astra Cloud Runtime Validation #39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891) and [Astra Verify #39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885) both completed SUCCESS on exact head `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`.
- Read-back confirmed Agent 2 workflow blob `7a067fd7093a31c243c9e1f0e2caeec701f29c18` contains the full SHA pin and no longer contains `actions/upload-artifact@v4`.
- Static CI success is not a controlled failure-path test. Independent review and authorized controlled test remain open; PR #420 remains Draft/unmerged.
