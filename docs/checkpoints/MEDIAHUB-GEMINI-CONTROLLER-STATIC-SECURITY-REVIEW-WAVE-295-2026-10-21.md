# MediaHub Contour A — Gemini controller static security review (Wave 295)

**Date:** 2026-10-21  
**Status:** bounded source-level review completed; no new code or runtime qualification. Candidate remains unmerged.  
**Scope:** verify the controller-only candidate's static caller/secret/permission boundaries, reconcile exact-head CI and current PR/file refs, and record the remaining evidence gaps. This is not a submitted independent GitHub review.

## 1. Exact refs and source provenance

- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`, HEAD before this pass `06725e97fb70c096f05b29932afef68ec9749e47`.
- `main`: `80be45a70732b1d568164571d4273a6397792c3b`; current `.github/workflows/gemini-batch-dispatch-controller.yml` blob `99e5a87825aeb239568f96ecef004a102ff3e53b`.
- Candidate PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421): branch `contour-a/workflow-call-controller-governance-wave243`, HEAD `185f55b63121b1aece7e60f6c087ecfceab2721e`, controller blob `4cec1aa234fd9ccb0d41533b37248fff079c79c5`.
- PR #421 remains OPEN / DRAFT / UNMERGED, base `main` at `80be45a70732b1d568164571d4273a6397792c3b`. Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN.
- Current PR #421 and PR #426 changed-file inventories are disjoint: #421 has 11 paths; #426 has 3 paths. The Wave 293 overlap statement is superseded by this fresh inventory and must remain visible only as historical evidence.
- The documentation branch comparison against `main` is DIVERGED: 2,921 commits ahead, 44 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc` (the compare API only exposes a bounded file list). Do not merge, rebase, or synchronize the entire documentation branch as part of this pass.

## 2. Source-level control-flow review

Inspected the candidate controller, reusable observer, three child workflows, Wave 292 contract test and dedicated contract-validation workflow. Blob SHAs:
- Observer `e05759d04f34f52cc7ad1b794b6718585ee2507f`.
- Positive-context contract test `e1a229cbfb134d3548df727eab4f644dc221a51f`.
- Contract-validation workflow `b7416b1f41463a075ebb7d1ba147c2291bd64967`.
- Agent 2 child `9fced7999c0ab5a5a8b9666fd92791726b64fc66`.
- Agent 3 child `460f69408e0429bf70e3f71c3281fe792cc0bdf2`.

Observed at source level:
1. Controller mode defaults to `probe`; accepted modes are `probe` and `agents`; the three model jobs require `workflow_dispatch`, `mode=agents` and explicit `confirm=yes`.
2. Probe job calls a dedicated reusable observer with empty permissions, no secret mapping, no checkout and no model action. The observer itself and its job both specify empty permissions and do not declare/use provider credentials.
3. Each child is configured as `workflow_call`, not as an independently dispatchable `workflow_dispatch` workflow. Each child engineer job is guarded by `probe_only != true`, the observed trusted-controller result, event type and the exact main-controller workflow ref.
4. The PR-context probe and assertion fail closed for an untrusted `pull_request` caller. The source contract tests cover the intended default-deny structure and relevant workflow paths.
5. Action and container references observed in the child definitions are SHA-pinned.

**Static-review result:** no new direct source-level bypass was established in this bounded pass. This finding is limited to the inspected candidate source; it is not a runtime proof, a repository/org policy proof, or an independent approval.

## 3. Exact-head CI evidence re-read

At candidate HEAD `185f55b63121b1aece7e60f6c087ecfceab2721e`, the five associated workflow runs remain terminal SUCCESS:
- [Astra Verify #39475766199](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766199) — 453 tests recorded in the workflow evidence.
- [Workflow contract validation #39475766192](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766192).
- [Astra Cloud Runtime Validation #39475766251](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766251).
- [Non-launching caller-context probe #39475766469](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766469).
- [Wave 292 controller probe #39475766513](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766513).

The observed PR run context was `pull_request`, `refs/pull/421/merge`, `trusted_controller=false`; model jobs were skipped. CI success belongs to this exact candidate SHA and does not apply to a future changed head.

## 4. Open gates and disposition

- Submitted independent reviews on PR #421: **zero**. Submitted independent reviews on PR #426: **zero**.
- Effective repository/org Actions policy and branch-protection/ruleset requirements remain unverified; the prior API 403 is a visibility limit and is not evidence that protection is absent.
- Trusted positive `workflow_dispatch` context has not been observed at runtime. Static assertions are not a substitute for that evidence.
- Current `main` still carries the old REST-dispatch controller using `MEDIAHUB_GITHUB_TOKEN`; the proposed reusable-workflow controller exists only on the unmerged candidate. Do not describe the target route as active.
- No Gemini dispatch, model/provider call, secret access, host access, workflow dispatch, local test execution, merge, deployment, qualification or acceptance occurred in this pass.

**Decision:** keep PR #421 and #426 Draft/unmerged. The next controller gate is genuine independent security review and verifiable repository/org governance evidence. Only after reviewed integration may the default no-secret probe be run to collect trusted positive-context evidence. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated.

## 5. Sources of truth

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Accepted Functional Baseline 2.0 on main](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
