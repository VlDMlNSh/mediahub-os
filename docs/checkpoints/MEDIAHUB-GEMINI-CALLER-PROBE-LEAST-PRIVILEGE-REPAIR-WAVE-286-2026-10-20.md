# MediaHub Contour A — least-privilege caller-context probe repair (Wave 286)

**Date:** 2026-10-20  
**Execution class:** bounded GitHub Actions workflow/test change on draft PR #421; source read-back and exact-head CI inspection. No provider/model invocation.

## Objective

Resolve the startup-failing non-launching caller-context probe without broadening permissions, and remove path-level merge conflicts with PR #426. This is a test-harness and control-plane verification repair, not approval to launch Gemini.

## Code changes recorded on PR #421 branch

PR branch: `contour-a/workflow-call-controller-governance-wave243`  
Final verified branch HEAD at report time: `3141a44370694d78f76779243adb548318a745d7`  
Base `main`: `80be45a70732b1d568164571d4273a6397792c3b`.

- Added [read-only reusable observer](https://github.com/VlDMlNSh/mediahub-os/blob/3141a44370694d78f76779243adb548318a745d7/.github/workflows/gemini-reusable-context-probe-wave284.yml), blob `e05759d04f34f52cc7ad1b794b6718585ee2507f`. It uses only the Bash runner environment, has `permissions: {}` at workflow/job level, has no external `uses`, no checkout, no secrets, and no model/provider action.
- Added [uniquely named caller probe](https://github.com/VlDMlNSh/mediahub-os/blob/3141a44370694d78f76779243adb548318a745d7/.github/workflows/gemini-controller-context-probe-wave284.yml), blob `795d0786a8d1855dc5caf236e950eb6595dd23d4`. It has `permissions: {}`, no secret mapping, calls only the observer, and asserts the actual event/ref is a pull-request caller rather than the pinned trusted controller.
- Added [isolated workflow-contract validation](https://github.com/VlDMlNSh/mediahub-os/blob/3141a44370694d78f76779243adb548318a745d7/.github/workflows/gemini-workflow-contract-validation-wave284.yml), blob `ace5c3bf06130781f929966bdd1b49f66753d69d`. It uses read-only repository permission, pinned checkout/setup-python actions, actionlint and the dedicated static tests.
- Added [static positive/negative contract tests](https://github.com/VlDMlNSh/mediahub-os/blob/3141a44370694d78f76779243adb548318a745d7/tests/test_gemini_controller_context_probe_wave284_contract.py), blob `0691728f2de808ae8aeff4bcfe4f091ab158a450`. Assertions require empty workflow/job permissions, no secret key mapping, no model action, correct caller outputs, and unchanged guards on all three real Gemini children.
- Removed the legacy `.github/workflows/gemini-caller-context-probe.yml` and the old shared test path from the candidate branch. The empty `secrets: {}` mapping was omitted after actionlint rejected it; no secret is passed because the reusable call has no secret mapping.
- Restored `.github/workflows/astra-verify.yml` to the exact `main` blob `ae59d954f1ca6569a8d047589a2a54fd03e47f5b`. The lint/test checks now live in a separate, narrowly triggered workflow, so PR #421 no longer changes `Astra Verify`.
- Exact changed-file compare against `main`: 10 paths, 61 commits ahead / 0 behind. Current changed-file list no longer overlaps PR #426's changed paths. PR #426 remains a separate open draft; it is not merged or modified by this pass.

## CI evidence on the final candidate head

All run results below reference `3141a44370694d78f76779243adb548318a745d7`:

- [Astra Cloud Runtime Validation #39462792548](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792548): **SUCCESS**.
- [Dedicated Gemini workflow contract validation #39462792571](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792571): **SUCCESS**. This includes actionlint and the isolated positive/negative static contract tests.
- [Non-launching caller-context probe #39462792657](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792657): **SUCCESS**. The workflow observed untrusted PR caller context and the assertion job passed; no Gemini action or provider was invoked.
- [Astra Verify #39462792590](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792590): **IN PROGRESS at the last observation**; compile had completed and broad unit tests were still running. Do not label the full CI set green until this exact-head run reaches a terminal success result.

The immediately preceding failed contract-validation run [#39462525882](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462525882) produced a readable actionlint error: an empty `secrets: {}` section is invalid and should be omitted. That mapping was removed and a new exact-head validation passed. Older failure evidence should remain as historical attempt data, not be overwritten by the new result.

## Current governance state and limits

- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421): OPEN / DRAFT / UNMERGED. Independent review endpoint returned zero submitted reviews.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301): OPEN. It tracks authorization/governance work; its existence is not dispatch permission.
- `main` is unchanged. The candidate is a branch diff, not an accepted or released change.
- No Gemini dispatch, manual workflow dispatch, provider/model call, provider secret access, host access, merge, deployment, route qualification, or acceptance occurred. The only runtime workflow invoked by this pass was the non-launching context probe; the dedicated workflow performed lint/static tests.
- Contour A remains **NOT_PROVEN / BLOCKED** pending the required exact-head CI terminal state, independent security review, and confirmed repository governance/protection. Contour B remains gated until Contour A deployment and independent acceptance.

## Next bounded step

Verify `Astra Verify #39462792590` at the exact head above; if it fails, read the failed step log and make one minimal correction. Then obtain an independent review of the controller/caller guard, reusable workflow token ceilings, child secret routing and workflow provenance before asking governance to consider dispatch. Do not dispatch Gemini to test the guard.

## Canonical traceability

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 285 A0 ingress/issuer/approval source trace](MEDIAHUB-A0-INGRESS-ISSUER-APPROVAL-PRODUCER-TRACE-WAVE-285-2026-10-20.md)
- [Wave 284 startup-failure triage](MEDIAHUB-GEMINI-CALLER-PROBE-STARTUP-FAILURE-TRIAGE-WAVE-284-2026-10-20.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Bootstrap instruction](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
