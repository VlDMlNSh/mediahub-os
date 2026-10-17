# Gemini Read-only Workflow Incomplete-Response Fail-Closed Fix — Wave 105

- Date: 2026-10-17
- Scope: PR #334, branch `security/gemini-readonly-hardening-20261017`; no provider dispatch.
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- PR: [#334](https://github.com/VlDMlNSh/mediahub-os/pull/334)

## Finding

Review of the current primary workflow found a real failure-path defect: its response `aborted` and response `error` handlers invoked `reject(...)` although that callback was not defined in the primary workflow's scope. The request-level error handler separately updated the manifest, but response-level abort/error paths could raise a `ReferenceError` instead of reliably recording a failed incomplete response. The retry workflow already had a promise-scoped rejection callback, so the defect was isolated to the primary workflow.

## Changes

- Defined one scoped, idempotent `reject` handler in `.github/workflows/gemini-readonly-audit.yml`.
- The handler records `status=FAILED`, `provider_status=TRANSPORT_ERROR`, a bounded failure class, and completion timestamp; it suppresses response bodies and sets a nonzero process exit code.
- Added a `settled` guard so duplicate transport/error events cannot overwrite the final result; the completed-response path claims settlement before HTTP/JSON/output validation.
- Routed request errors through the same handler.
- Added a regression assertion in `scripts/test_gemini_readonly_workflows.py` that the handler exists before abort usage, request errors share the handler, and output writing remains after the response-end event.

## Exact revision and blob evidence

- Final PR head: `3b19bae1b6a19da1c46fff5ced8b6c60c8f8e15d`
- Workflow blob `.github/workflows/gemini-readonly-audit.yml`: `4cbeff07f20e698d2c2d26118743c754271e0042`
- Regression test blob `scripts/test_gemini_readonly_workflows.py`: `5c0e178e5180ab7adfcfb69a84132e31a4d984f4`
- Prior workflow blob: `7ced644d519d7d51cb40607109a233a3382d4700`
- Prior test blob: `b794ac9fe69faae61295fde2841eaee7e08a7956`

## CI evidence on exact head

All three runs completed successfully on `3b19bae1b6a19da1c46fff5ced8b6c60c8f8e15d`:

- [Gemini Read-only Workflow Contract #39068081607](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068081607) — success; actionlint and security-contract regression job passed.
- [Astra Cloud Runtime Validation #39068081597](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068081597) — success.
- [Astra Verify #39068081606](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068081606) — success.

## Status, limits, and next step

- PR #334 remains **OPEN / DRAFT / UNMERGED**. The base SHA observed during this pass is `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`; do not treat green CI as independent review or qualification.
- This pass did not call Gemini or any other provider, read credentials, dispatch the workflow, admit a queue task, merge, deploy, or accept Contour A.
- The added regression is a source-level contract assertion, not a socket-level integration test. It does not establish behavior for every Node.js HTTP event ordering.
- Next: add a provider-free local HTTP regression harness or a narrow shared response-validation seam to exercise complete valid responses, non-2xx responses, over-limit bodies, and truncated/aborted responses. Keep it isolated from credentials, provider endpoints, queue admission, and production dispatch. Then obtain independent security review of PR #334.
