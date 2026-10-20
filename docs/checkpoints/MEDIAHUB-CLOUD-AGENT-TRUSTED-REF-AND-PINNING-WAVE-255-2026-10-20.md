# MediaHub OS Contour A — trusted controller ref and immutable action pinning, Wave 255

Date: 2026-10-20
Status: EXACT-HEAD CI PASSED / SECURITY AND INTEGRATION GATES OPEN

## Scope and governance

This wave continues the approved Option B controller-only workflow proposal in [Draft PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421). Routine agent use is intended after the controller gates pass, per [Issue #301 owner clarification](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6289835713). The transition remains on hold until its security and governance gates are complete. No agent was dispatched in this wave.

## Candidate and exact-head CI

- Branch: `contour-a/workflow-call-controller-governance-wave243`
- Checked commit: `fa1a38c321f96411644fe54e13ad7f6de226daa7`
- Base `main`: `80be45a70732b1d568164571d4273a6397792c3b`
- Compare: 23 commits ahead / 0 behind at last read.
- [Astra Cloud Runtime Validation #39415992351](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39415992351): SUCCESS.
- [Astra Verify #39415992480](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39415992480): SUCCESS. Log read-back: actionlint passed, 7 reusable-workflow contract tests passed, 438 Python unit tests passed, compile and signed-command smoke test completed.

## Security corrections

1. All three reusable child workflows now require both `github.event_name == 'workflow_dispatch'` and the exact trusted controller ref:
   `VlDMlNSh/mediahub-os/.github/workflows/gemini-batch-dispatch-controller.yml@refs/heads/main`.
2. Contract tests reject an untrusted feature-branch controller ref and the former loose `contains(github.workflow_ref, ...)` predicate.
3. Provider secrets remain explicitly mapped to their matching child; no `secrets: inherit` and no `MEDIAHUB_GITHUB_TOKEN` in the proposed controller/children.
4. Actions used by the child workflows and Astra Verify were pinned to observed/verified immutable commits:
   - `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` — [source commit](https://github.com/actions/checkout/commit/11d5960a326750d5838078e36cf38b85af677262), observed in the successful CI checkout logs.
   - `google-github-actions/run-gemini-cli@f77273f4c914e4bf38440cf36a0369cb64a37489` — [official v0.1.22 release commit](https://github.com/google-github-actions/run-gemini-cli/commit/f77273f4c914e4bf38440cf36a0369cb64a37489); its `action.yml` was read back at that exact commit (blob SHA `35af14fe781b3e02ecd20233897ec743b731bbd2`).
   - `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065` — [source commit](https://github.com/actions/setup-python/commit/a26af69be951a213d495a4c3e4e4022e16d87065), observed in the successful CI checkout logs.
5. The GitHub MCP server remains `ghcr.io/github/github-mcp-server:v0.27.0`. Its exact image manifest digest was not verified in this pass, so the mutable container tag remains an open provenance gate; no digest was guessed.

## Read-back blob SHAs on the PR branch

- Controller: `.github/workflows/gemini-batch-dispatch-controller.yml` — `da1d0254a993adcc224d5859a9a97bf609abd710`
- Agent 1: `.github/workflows/gemini-autonomous-engineering.yml` — `3b00192b540fce5b893cdd48588eaff218e327e4`
- Agent 2: `.github/workflows/gemini-agent-2.yml` — `685d3684642301c6fb0ee393fef7860be4533716`
- Agent 3: `.github/workflows/gemini-agent-3.yml` — `3b8d71636575a8746f0391ebee795450bca9b031`
- Astra Verify: `.github/workflows/astra-verify.yml` — `a087ccde747cc621f6003226e01abb10e33261dc`
- Reusable workflow contract tests: `tests/test_gemini_reusable_workflow_contract.py` — `e2db063519c2ffb5e39762ebba5d854837158933`
- Existing controller contract tests: `tests/test_gemini_transport_controller_contract.py` — `161fc5a1d02b9d99ddf9819ab39a803981f05d67`

## Remaining gates

- PR #421 remains Draft/unmerged; the review API returns no submitted reviews. The author’s own security note is a comment, not an independent GitHub review.
- A true controlled negative caller-context runtime test has not run. The available GitHub connector has no workflow-dispatch operation; do not bypass this limitation by launching Gemini from another transport.
- The MCP server image digest still needs verification and pinning.
- Genuine independent review, branch-protection/required-check review, and governed integration remain required before the first live batch.
- After integration, bounded routine agent runs may use the single controller with explicit `confirm: yes`, without another per-run owner prompt. This does not bypass issuer/capability, quota/budget, provider, review, or acceptance controls.

## Safety record

No agent workflow was dispatched. No provider secret was read, printed, or changed. No merge, deployment, release, or Contour A qualification was performed.

## Navigation

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 254 autonomy gate](MEDIAHUB-CLOUD-AGENT-AUTONOMOUS-USE-GATE-WAVE-254-2026-10-20.md)
- [Wave 253 caller-ref review](MEDIAHUB-CLOUD-AGENT-CALLER-REF-GUARD-REVIEW-WAVE-253-2026-10-20.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Draft PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
