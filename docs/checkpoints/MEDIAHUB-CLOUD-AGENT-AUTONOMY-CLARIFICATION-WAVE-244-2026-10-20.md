# MediaHub OS — cloud-agent autonomy clarification (Wave 244)

Date: 2026-10-20
Status: OWNER-DIRECTED CLARIFICATION / ROUTE GATES STILL APPLY

## Owner direction and correction

The owner clarified in this conversation that MediaHub OS development is intended to proceed autonomously and quickly, including using the available cloud agents as engineering capacity. The previous “dispatch ON HOLD” wording was too easy to read as a project-wide or indefinite prohibition. That was not the intended development posture. The hold is a temporary technical/governance gate for the current controller transition, not a reason to stop independent engineering or to require another owner prompt for every routine agent run.

The latest direction is recorded as authorization to proceed with controller-only cloud-agent dispatch after the currently required controller implementation gates are satisfied. This supersedes the earlier requirement for a separate per-run owner authorization after integration. It does **not** waive independent review, exact-head CI, negative caller-context tests, secret-boundary checks, repository protections, capability/issuer rules, provider/quota restrictions, or the controller's explicit `confirm: yes` input.

## Verified state in this wave

- Binding transport policy on the canonical docs branch was re-read at blob SHA `301c100a494646fe376e26a3f39fea5f42590968`.
- Bootstrap was re-read at blob SHA `beb0de42af395d99acc1c63c8a1293524598cac8`.
- Continuation checkpoint was re-read at blob SHA `ac6a3a48fd0e5e1dfb1314ab3f4e24bf2eb3e2e9`.
- Map addendum was re-read at blob SHA `a1c3a6720b083e7c65001cff6aeb5fdb25f64399`.
- The only approved launch route remains GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` and its three fixed-scope child workflows. Do not launch agents from SentinelX, a server shell, local CLI, ad-hoc scripts, or alternate workflows/transports.
- PR #421 remains Draft and unmerged: https://github.com/VlDMlNSh/mediahub-os/pull/421. The branch `contour-a/workflow-call-controller-governance-wave243` compares 11 commits ahead / 0 behind `main` at base `80be45a70732b1d568164571d4273a6397792c3b`.
- PR #421 proposes replacing REST child dispatch with controller-called `workflow_call` jobs, removing standalone child `workflow_dispatch`, explicitly passing only child-specific provider secrets, and adding contract tests/actionlint.
- Exact-head CI recorded in the existing project evidence passed: Astra Cloud Runtime Validation #39414529957 and Astra Verify #39414529912. The review API currently returns no submitted reviews; a controlled negative caller-context test remains required. Therefore no agent was launched in this wave and the new controller route is not yet integrated/accepted.
- The current `main` controller is still the older REST-dispatch implementation (blob SHA `99e5a87825aeb239568f96ecef004a102ff3e53b`); the proposed controller on the PR branch has blob SHA `da1d0254a993adcc224d5859a9a97bf609abd710`. These are distinct states; do not describe the proposed workflow-call implementation as already active on `main`.

## Required next actions

1. Obtain genuine independent review of PR #421, focusing on `github.workflow_ref` caller-guard semantics/bypass scenarios, permission ceiling, and provider-secret flow.
2. Add or verify the controlled negative caller-context test without launching Gemini.
3. Re-run and verify all required checks at the exact latest PR head. Fix findings and re-read changed files/SHA.
4. Integrate only after required review and checks pass under project governance/branch protection.
5. Then use the single controller route for bounded agent work without another per-run owner prompt; the controller's own explicit confirmation input and all security/authority gates remain mandatory. Record run IDs, job conclusions, artifact/PR references and commit provenance.
6. Continue independent Contour A work in parallel; do not let the controller gate stall unrelated work.

## Security and acceptance boundaries

- Never read, print, decode, upload, or pass `MEDIAHUB_GITHUB_TOKEN` to agents/models. Under the proposed reusable-workflow architecture, do not use `secrets: inherit`; pass only the specific provider secret needed by each child.
- No alternate transport or paid fallback. No automatic merge based solely on agent output. Contour A remains unqualified until its separate acceptance criteria are met; Contour B remains blocked until Contour A is deployed and independently accepted.

## Navigation

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- PR #421: https://github.com/VlDMlNSh/mediahub-os/pull/421
- Governing issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
