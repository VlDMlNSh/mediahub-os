# MediaHub OS — cloud-agent dispatch exclusivity governance proposal (Wave 236)

- Date: 2026-10-20
- Status: **PROPOSAL FOR EXPLICIT GOVERNANCE / NOT IMPLEMENTED / NOT ACCEPTED**
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Decision under review

The only policy-authorized cloud-agent/API launch route remains:

`.github/workflows/gemini-batch-dispatch-controller.yml` on GitHub-hosted Actions → its three fixed-scope Gemini child workflows.

The controller uses repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub REST dispatch and run monitoring. Never read/log the value, place it in an artifact or prompt, or expose it to a model/child process. No direct SentinelX, server shell, local CLI, ad-hoc script, unrelated workflow, or alternate transport is permitted. This is the binding policy, not evidence that GitHub technically prevents other principals from invoking child workflows.

## Current source-bound evidence

- Canonical policy blob: `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap blob: `77368971b90071812f82c384cdd3be813513a5dc`.
- Controller on `main`: `99e5a87825aeb239568f96ecef004a102ff3e53b`.
- Main child workflow blobs:
  - Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`: `09523d809530ae5b7bf528eab5fa53bc5deaf92d`.
  - Agent 2 `.github/workflows/gemini-agent-2.yml`: `259c8c82b8d90a39e1c90e65390e469b241b5581`.
  - Agent 3 `.github/workflows/gemini-agent-3.yml`: `91b5397001e088dfae2f450ee77c9c23118b5601`.
- Each child still declares `workflow_dispatch`; direct child invocation is therefore technically exposed at the workflow event contract. No evidence yet proves repository/organization controls deny all non-controller dispatch principals.
- The generic connector did not permit a read of the Actions permissions endpoint during this pass; the effective Actions policy and the principal type behind `MEDIAHUB_GITHUB_TOKEN` remain unknown. No secret value was read.
- PR #420 is open Draft, head `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`, 13 commits ahead / 0 behind base `80be45a70732b1d568164571d4273a6397792c3b`. Exact-head Astra Cloud Runtime Validation run [39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891) and Astra Verify run [39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885) both concluded success. PR review API returned no submitted reviews. These checks do not demonstrate dispatch exclusivity or the controlled failure-path artifact behavior.

## Proposed options for owner/governance decision

### Option A — retain REST dispatch, add enforceable authorization evidence

Keep the current controller-to-child REST dispatch contract only if repository/organization Actions policy and the token principal can be shown to prevent unauthorized direct child dispatch. Record the relevant non-secret settings, principal type/permissions, negative test evidence and exact refs. Do not infer this from the policy document alone.

### Option B — redesign children as controller-only reusable workflows

Prepare a separate, isolated change proposal that replaces child `workflow_dispatch` entry points with `workflow_call` and has the controller call each fixed-scope child job/workflow. Before implementation, resolve the current controller's sequential REST-dispatch/run-monitoring design against reusable-workflow execution semantics. Pass only each child's explicitly required provider secret; do not use `secrets: inherit`. Keep least-privilege permissions, fixed scopes, correlation IDs, sanitized failure diagnostics, fail-closed output validation, and no automatic merge/deploy. Test that direct dispatch is unavailable and controller calls still produce correlated, reviewable outputs. This changes the current binding orchestration contract and is **not authorized by this proposal itself**.

### Option C — document residual risk and keep dispatch disabled operationally

If neither enforcement evidence nor a reviewed redesign is available, keep agent dispatch unused; continue independent engineering that does not require cloud-agent execution. This is fail-closed and preserves the policy, but does not prove technical exclusivity.

## Required governance decision and acceptance tests

1. Choose A, B, or C and record the decision under Issue #301/change control before changing workflow event contracts or dispatch behavior.
2. Determine the non-secret Actions policy state and `MEDIAHUB_GITHUB_TOKEN` principal type without reading secret values.
3. If B is selected, produce a separate PR; require independent review, workflow YAML lint, exact-head CI, a negative direct-invocation test, a positive controller-invocation test, and a controlled failure-path artifact test.
4. Keep agent output untrusted; no automatic merge, deployment, qualification, or Contour B start.
5. After any implementation, read back all changed files and record commit/blob SHAs, run/job IDs and conclusions.

## Wave result

The sole policy-authorized route is persisted and source-verified. **Technical exclusivity remains NOT PROVEN.** No agent was dispatched; no workflow was triggered; no token value was read; no code or workflow contract was changed; no merge, deployment, or Contour A qualification is claimed.

## Navigation

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Transport policy](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md)
- [Bootstrap](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #420](https://github.com/VlDMlNSh/mediahub-os/pull/420)
