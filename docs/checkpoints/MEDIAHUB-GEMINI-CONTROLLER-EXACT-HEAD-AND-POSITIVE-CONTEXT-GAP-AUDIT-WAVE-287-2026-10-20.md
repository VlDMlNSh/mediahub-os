# MediaHub Contour A — Gemini controller exact-head and positive-context gap audit (Wave 287)

**Date:** 2026-10-20  
**Execution class:** read-only source, Git reference, pull-request review metadata, and exact-head GitHub Actions audit. No workflow dispatch, Gemini/provider invocation, secret access, merge, or deployment.

## Objective

Reconcile the final Wave 286 CI state on PR #421 and determine whether the caller-context guard is runtime-qualified for both untrusted and trusted paths. Keep the Gemini launch gate closed until the trust boundary and independent review are evidenced.

## Verified repository state

- Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os).
- `main` HEAD: `80be45a70732b1d568164571d4273a6397792c3b`.
- Canonical documentation branch at audit start: `docs/mediahub-chat-tree-map-20261012`, HEAD `2b84e27dee1e4825859d03e330d3e26de10e9fc6`.
- Branch comparison: documentation branch DIVERGED from main, 2,897 commits ahead / 44 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No merge/rebase/cherry-pick attempted.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN; it is an execution tracker, not a dispatch grant.
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) remains OPEN / DRAFT / UNMERGED. Exact head `3141a44370694d78f76779243adb548318a745d7`; base main `80be45a70732b1d568164571d4273a6397792c3b`; compare is 61 ahead / 0 behind. Ten paths are changed. The submitted-review endpoint returned **zero reviews**.

## Exact-head checks — refreshed after Wave 286

All check evidence below is bound to PR #421 head `3141a44370694d78f76779243adb548318a745d7`.

- [Astra Cloud Runtime Validation #39462792548](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792548): **SUCCESS**.
- [Gemini workflow contract validation #39462792571](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792571): **SUCCESS**; the dedicated workflow runs actionlint and static positive/negative contract tests.
- [Non-launching caller-context probe #39462792657](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792657): **SUCCESS**.
- [Astra Verify #39462792590](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792590): **SUCCESS**, terminal state refreshed from GitHub; updated at `2026-10-20T17:07:17Z`.

Wave 286's source report recorded Astra Verify as still in progress at the time of capture. The later terminal result is success; this audit supersedes that one stale observation, but does not replace or rewrite the historical report.

## Source-level security review

Reviewed exact-head blobs:

- Controller `.github/workflows/gemini-batch-dispatch-controller.yml`, blob `da1d0254a993adcc224d5859a9a97bf609abd710`.
- Gemini children `gemini-autonomous-engineering.yml` (`f67d62b721bcd8b86ef3a9491db5db2f50de6b1d`), `gemini-agent-2.yml` (`9fced7999c0ab5a5a8b9666fd92791726b64fc66`) and `gemini-agent-3.yml` (`460f69408e0429bf70e3f71c3281fe792cc0bdf2`).
- Reusable observer `.github/workflows/gemini-reusable-context-probe-wave284.yml`, blob `e05759d04f34f52cc7ad1b794b6718585ee2507f`.
- PR caller probe `.github/workflows/gemini-controller-context-probe-wave284.yml`, blob `795d0786a8d1855dc5caf236e950eb6595dd23d4`.
- Caller probe static contracts, blob `0691728f2de808ae8aeff4bcfe4f091ab158a450`.

Observed protections on the candidate:

1. The controller has a manual `confirm` choice defaulting to `no`; the three fixed child jobs and aggregate summary require explicit `yes`. The controller does not use `MEDIAHUB_GITHUB_TOKEN`, REST child dispatch, or inherited secrets.
2. The three children expose `workflow_call`, not `workflow_dispatch`. Their engineering jobs require `probe_only != true`, a positive observed trusted-controller predicate, `workflow_dispatch`, and the exact pinned controller workflow ref. Their workflow/job caller-observation jobs have empty token permissions. Provider secrets are mapped explicitly per child, rather than inherited.
3. The standalone PR probe and reusable observer declare empty permissions, do not checkout code or use external actions, do not map provider secrets, and do not call a model/provider action.
4. The successful runtime probe observed and rejected the **untrusted pull-request caller**: the event was `pull_request`, the observed workflow ref named the separate probe workflow, and the trusted-controller output was `false`.

## Residual blocker: the positive caller path is not runtime-proven

The current runtime probe is triggered by `pull_request` and asserts that this PR workflow is **not** the trusted controller. It establishes the negative case only. The unit test that returns true for the literal expected `workflow_dispatch` / main-controller pair is a static predicate test; it is not a runtime observation from that trusted controller. Therefore the audit does **not** conclude that a legitimate controller call is positively recognized at runtime.

Safe follow-up design, not executed here: add a distinct controller-only probe mode that calls only the no-credential reusable observer, has `permissions: {}`, maps no provider secrets, and statically proves that all three Gemini action jobs are unreachable in probe mode. Then obtain independent review of the caller/ref semantics and secret/token ceiling. Do not implement probe mode by merely passing `probe_only` to existing child jobs while continuing to map their API keys; the probe path should have no secret mapping at all.

## Gate decision

**PR #421 remains a candidate, not accepted. Do not dispatch Gemini.** Exact-head CI is now green, and the real untrusted PR context is rejected. Independent submitted review is absent, positive trusted-controller runtime context is unproven, and the repository governance/protection gate remains unresolved. The read-only source review in this report is not an independent review and cannot substitute for one.

No workflow dispatch, Gemini/model/provider invocation, provider-secret access, host access, merge, deployment, route qualification or acceptance occurred. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated.

## Canonical traceability

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap instruction](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Wave 286 caller-probe repair report](MEDIAHUB-GEMINI-CALLER-PROBE-LEAST-PRIVILEGE-REPAIR-WAVE-286-2026-10-20.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
