# MediaHub OS — Wave 281: Gemini caller-guard gate audit

- Date: 2026-10-20
- Status: **STATIC CONTRACT EVIDENCE PASS / LIVE CALLER-CONTEXT PROOF AND INDEPENDENT REVIEW OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Controller proposal: https://github.com/VlDMlNSh/mediahub-os/pull/421
- Prior generic-worker fallback finding: [Wave 280](MEDIAHUB-CONTOUR-A-WORKER-GENERIC-GATEWAY-FALLBACK-WAVE-280-2026-10-20.md)

## Executive result

PR #421 has substantive static contract coverage for the controller-only design: exact reusable-workflow children, no child workflow_dispatch, explicit provider-secret mapping, no secrets: inherit, a fixed controller workflow_ref guard attached to each actual jobs.engineer.if, negative fixtures for altered controller ref/event, mutable actions/container tags, secret inheritance and transport-token leakage, plus explicit confirm: yes gates. Exact-head CI currently reports success.

This is meaningful source/test evidence, but it is **not yet the complete dispatch gate**. The PR has no submitted independent review. The test suite's negative caller-context matrix is a non-launching Python/static simulation tied to the exact source expression; it does not prove which github.event_name and github.workflow_ref values GitHub evaluates inside a real reusable-workflow run. No live caller probe was run. Do not dispatch Gemini until independent review, caller/secret-boundary review, the required controlled negative caller-context test, governance/protection gates, and exact-head required checks are complete.

## Snapshot and refs

- main HEAD: 80be45a70732b1d568164571d4273a6397792c3b.
- PR #421 head: 84e2d0bbb4163942f5ba010591cb5d3c9d6a7581; base is the current recorded main SHA above; PR remains OPEN / DRAFT / UNMERGED.
- Controller .github/workflows/gemini-batch-dispatch-controller.yml on PR #421: blob da1d0254a993adcc224d5859a9a97bf609abd710.
- Reusable child blobs:
  - gemini-autonomous-engineering.yml: 983d3d06303f75f65de15ae2ee7f824403605e76
  - gemini-agent-2.yml: eefcc97f1cf9504218f48fd248f37aa8306cd309
  - gemini-agent-3.yml: 4608462d4b59c088bbf962412060e4b1b8a93519
- Contract test tests/test_gemini_reusable_workflow_contract.py: blob 5e9f9db8e033ab861d8fde93512f040b9f99459e.
- Controller contract test tests/test_gemini_transport_controller_contract.py: blob 161fc5a1d02b9d99ddf9819ab39a803981f05d67.

## Positive source findings

1. Controller is manually dispatched and requires the explicit string choice confirm with default no; the three child jobs are guarded by inputs.confirm == 'yes'.
2. Controller uses only three fixed local reusable workflows and explicitly passes one provider secret per child. It has no MEDIAHUB_GITHUB_TOKEN, REST child-dispatch call or secrets: inherit path in the inspected source.
3. Each child exposes workflow_call with a required task/base/scope and its own named provider secret; no standalone workflow_dispatch trigger was found in the three child files.
4. Each child applies the exact condition to its actual jobs.engineer.if: github.event_name == 'workflow_dispatch' && github.workflow_ref == 'VlDMlNSh/mediahub-os/.github/workflows/gemini-batch-dispatch-controller.yml@refs/heads/main'.
5. The controller's fixed GitHub MCP image is pinned to digest sha256:cbca61d547beec9b819b26bbfe6ac66ba6b373f1d6b64e8291e346bf524633e2. External actions in the inspected children are SHA-pinned.
6. The contract tests include a non-launching negative caller-context matrix for wrong event, branch, repository, workflow file and ref kind; negative source fixtures for loose or altered controller guards; and checks for direct child dispatch, secret inheritance, transport-token leakage and mutable action/container refs.

## Exact-head CI and PR gate state

- [Astra Verify #39425009644](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009644): SUCCESS.
- [Astra Cloud Runtime Validation #39425009654](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009654): SUCCESS.
- Submitted independent reviews: none returned by the PR reviews endpoint.
- Required caller-context proof: **PARTIAL** — mocked/static negative contexts exist, but no actual non-Gemini GitHub Actions caller-context probe is evidenced.
- Required governance/repository-protection state: not established by this source pass.
- Main still contains the previous standalone-dispatch workflow versions until an approved PR is integrated; PR branch safety does not itself harden main.

Related bounded proposals:
- [PR #425 — fail closed on generic host-side gateway fallback](https://github.com/VlDMlNSh/mediahub-os/pull/425), exact-head Astra Verify #39453835133 and Cloud Runtime Validation #39453835149 both SUCCESS; independent review absent.
- [PR #423 — retire two old-server workflows](https://github.com/VlDMlNSh/mediahub-os/pull/423), exact-head Astra Verify #39451818611 and Cloud Runtime Validation #39451818985 both SUCCESS; independent review absent. PR #422 is closed as a duplicate, unmerged.
- [PR #424 — docs-branch worker secret-regex/test restoration](https://github.com/VlDMlNSh/mediahub-os/pull/424) remains a separate docs-branch PR; do not mix it with the main-branch proposals.

## Safe next step

Design and review a **non-launching** GitHub caller-context probe whose probe job cannot invoke the Gemini action even if the guard is wrong; use it to observe caller-context values under GitHub's actual reusable-workflow semantics. A test-only probe must not pass working provider credentials or invoke provider/model steps. Keep the current PR Draft until independent review and all required gates pass. Do not simulate successful live caller behavior from the existing Python predicate test.

## Verification boundary

This pass was source/CI metadata review only. It did not dispatch workflows or Gemini, call a model/provider, access host/runtime or secrets, run tests locally, merge, deploy, qualify or accept Contour A. The exact-head CI checks listed above are GitHub Actions evidence; a live non-Gemini caller-context probe and independent review remain unverified.

Contour A remains **NOT_PROVEN / BLOCKED**. Contour B remains gated on Contour A deployment and independent acceptance.
