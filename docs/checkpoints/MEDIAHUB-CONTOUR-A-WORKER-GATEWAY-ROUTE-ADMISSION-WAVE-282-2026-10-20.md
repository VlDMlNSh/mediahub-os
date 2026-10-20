# MediaHub OS — Wave 282: worker generic-gateway route admission and exact-head evidence

- Date: 2026-10-20
- Status: **BOUNDED FIX PROPOSED IN PR / EXACT-HEAD CI PASS / INDEPENDENT REVIEW OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Related fix proposal: https://github.com/VlDMlNSh/mediahub-os/pull/425
- Prior source finding: [Wave 280 — worker generic gateway fallback](MEDIAHUB-CONTOUR-A-WORKER-GENERIC-GATEWAY-FALLBACK-WAVE-280-2026-10-20.md)

## Executive result

Re-read the candidate branch for PR #425 and its exact-head check runs. The branch has a narrow two-file diff: it removes the generic `AstraGatewayRuntime().run_bounded({...})` fallback from `astra_github_agent.py`, rejects six generic language operations before gateway import, and adds static/mock-only regression tests. Exact-head Astra Verify and Astra Cloud Runtime Validation passed. The PR remains Draft/unmerged, and no independent review is recorded. This pass neither merges the candidate nor authorizes live dispatch.

## Snapshot and changed paths

- `main` HEAD: `80be45a70732b1d568164571d4273a6397792c3b`.
- PR #425 branch: `contour-a/fail-closed-generic-gateway-fallback-wave277`.
- Candidate HEAD: `ce44a47b0d327a5cca9593e529fe97b492ffaa4a`.
- `astra_github_agent.py` candidate blob: `386390079c3271739c8ca4713d10d5f2f70203f0`.
- New test blob: `12534024eb32a3c6e8d1f9f5b2ee7cdba599db47`.
- Compare against `main`: 2 commits ahead / 0 behind; exactly two paths:
  - `astra_github_agent.py` modified (+10/-15).
  - `tests/test_astra_github_gateway_route_admission.py` added (+57).
- Pull Request: [#425](https://github.com/VlDMlNSh/mediahub-os/pull/425), OPEN / DRAFT / UNMERGED.

## Source-level change

The old fallback imported `mediahub_runtime.astra_gateway.AstraGatewayRuntime` and called `run_bounded()` with a plain dictionary. The gateway's `run_bounded()` path expects `AstraTaskRequest`; its bounded lifecycle catches plan validation errors into an `AutonomousTaskResult`, which is not directly JSON serializable in the worker's published result. In addition, silently using the generic cloud-first orchestrator would be a different route from the approved GitHub-hosted Gemini controller.

The candidate now defines `UNADMITTED_GENERIC_GATEWAY_OPERATIONS` as exactly:
`research`, `architecture`, `review`, `documents`, `coding`, `coding_v2`.

After the concrete handlers, these operations raise `RuntimeError("gateway_route_not_admitted")` before importing the gateway. An operation that has been added to `OPERATIONS` but has no concrete handler raises `RuntimeError("operation_handler_not_implemented")`. The specific `health` handler remains intact.

Worker `main()` catches an execution exception and prepares a JSON-safe error dictionary with nonzero return code, then publishes the record before marking the command consumed. This prevents the prior non-serializable fallback result on this route, assuming publication itself succeeds. It does not prove every publication failure is recoverable or that a live worker is running this candidate.

## Static/mock-only test evidence

New tests in `tests/test_astra_github_gateway_route_admission.py`:
1. Verify the exact set of six generic operations is rejected.
2. Patch Python import so importing `mediahub_runtime.astra_gateway` would fail the test if attempted.
3. Verify the `health` handler still works without importing the gateway.
4. Verify source contains both fail-closed error codes and no `AstraGatewayRuntime().run_bounded(` fallback.

The tests do not call a provider, GitHub Actions dispatch, host, or secret. They prove the candidate's local Python control flow under mocks, not live-node behavior.

## Exact-head checks and review gate

- [Astra Verify #39453835133](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39453835133): SUCCESS. The run record states compile, 434 unit tests, and signed-command smoke test passed.
- [Astra Cloud Runtime Validation #39453835149](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39453835149): SUCCESS.
- Independent submitted reviews: none returned by the PR reviews endpoint.
- PR remains DRAFT; do not merge automatically.
- PR #421's controller-only Gemini workflow transition is separate and remains OPEN/DRAFT. Its independent review and actual non-Gemini caller-context probe are still open gates. Passing PR #425 does not authorize dispatch of Gemini.

## Disposition

The six generic operations are deliberately unavailable on this host-side worker until their route is explicitly admitted through the correct provider/executor contract. This is not a project-wide ban on engineering tasks: the approved GitHub-hosted controller remains the candidate cloud-agent path, subject to its own safety gates. Local Claude on Alamo must remain local-executor-only; this PR does not qualify or alter that path.

## Verification boundary

Verified by source and GitHub metadata: refs, exact candidate diff, changed-file blobs, new mock-only tests, exact-head CI conclusions and absence of submitted PR reviews. No local test run was performed in this pass. No Gemini dispatch, model/provider call, host/runtime/secret access, workflow dispatch, merge, deployment, route qualification or Contour A acceptance occurred.

## Next bounded step

Obtain a genuine independent review of PR #425 and verify the required checks against the exact current head. Separately complete the PR #421 caller-guard gate with independent route/secret review and a non-launching GitHub caller-context probe. Do not dispatch any model before those gates pass; do not merge either proposal automatically.
