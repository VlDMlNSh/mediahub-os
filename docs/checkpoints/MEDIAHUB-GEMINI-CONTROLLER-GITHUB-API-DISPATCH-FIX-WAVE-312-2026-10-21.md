# Gemini controller GitHub API dispatch correction — Wave 312 (2026-10-21)

## Status

**IMPLEMENTED ON DRAFT PR / NOT MERGED / NOT QUALIFIED / NO GEMINI DISPATCH.**

- PR: [#432 — controller GitHub API dispatch and signed child authorization](https://github.com/VlDMlNSh/mediahub-os/pull/432)
- Working branch: `fix/gemini-controller-api-dispatch-wave312-final`
- PR base commit: `f16e5bae202a78584f273132e7f88c6e25d3142e`
- Latest known PR head: `17e5609671441cbf6dfa964ec29fabb2a9f7b338`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Map addendum: [Wave 312](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-312-2026-10-21.md)
- Governance gate: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Root defect

The main controller blob `4cec1aa234fd9ccb0d41533b37248fff079c79c5` used local `workflow_call` children and explicitly claimed that no transport token was needed. That did not satisfy the required GitHub API transport through `MEDIAHUB_GITHUB_TOKEN`, and independent child run IDs/common immutable target were not represented by the contract.

## Implemented in PR #432

- Replaced reusable child calls with GitHub REST `workflow_dispatch` calls to the three fixed child workflow files.
- The controller resolves one full commit SHA (or validates an explicitly supplied full SHA), then passes the same immutable target to all three children.
- `MEDIAHUB_GITHUB_TOKEN` is referenced only in the controller's dispatch/monitor step; it is not passed to children, prompts, Gemini, artifacts, summaries or logs. No `secrets: inherit`.
- Added a distinct HMAC authorization secret, `MEDIAHUB_DISPATCH_HMAC_KEY`. The controller signs a canonical payload containing workflow filename, dispatch ID, target SHA, task, base ref and scope. Each child verifies the signature and allowlisted inputs before the Gemini/provider step.
- Children check trusted `workflow_dispatch` on `refs/heads/main`, require base `main` and scope `contour-a`, and checkout the shared target SHA.
- The controller dispatch job is gated to `workflow_dispatch` on `refs/heads/main` with explicit `mode=agents` and `confirm=yes`. Default mode remains non-launching `probe`.
- Added/updated static contract tests for the API transport, HMAC boundary, immutable target and fail-closed monitoring.

## Exact blob evidence

At latest read-back on the PR branch:

| File | Blob SHA |
|---|---|
| `.github/workflows/gemini-batch-dispatch-controller.yml` | `3268dbf08cbcf4869b6ec608c9d61c34ac213154` |
| `.github/workflows/gemini-autonomous-engineering.yml` | `a4160266e4da8dce00862936c6d4a3a7c17026f5` |
| `.github/workflows/gemini-agent-2.yml` | `71adf89707c45fbfabdcfdb35fe0381d4583d647` |
| `.github/workflows/gemini-agent-3.yml` | `507aa2cadefb3e8bdd8d210713c011152b202529` |
| `tests/test_gemini_controller_context_probe_wave284_contract.py` | `980d3868a2f9adbac842da7802289f4755f5e083` |
| `tests/test_gemini_controller_positive_context_probe_wave292_contract.py` | `5ab7799653ec51696939a2115d6e5c02ed18c8f6` |
| `tests/test_gemini_reusable_workflow_contract.py` | `ec1cd102afa273d67a6a24ac68e5ee47bc09ae1e` |
| `tests/test_gemini_transport_controller_contract.py` | `5182b5f0e12a37c756342298642d100a9d4edbd0` |

## CI and verification evidence

- Initial exact-head contract run [39603593758](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39603593758) failed because the legacy Wave 284 test still required `workflow_call`. This exposed a stale test contract; it was updated to assert the signed `workflow_dispatch` gate.
- Exact-head CI for `ea637eb55c87d44f0ce22730588e744c7470ee1d` is terminal **SUCCESS**:
  - [Workflow contract validation #39604609734](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609734) — actionlint and contract suite succeeded.
  - [Astra Verify #39604609752](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609752) — full Python test suite succeeded (444 tests).
  - [Non-launching caller-context probe #39604609755](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609755) — PR context denied as expected.
  - [Controller run #39604609766](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609766) — probe/assertion jobs succeeded; `dispatch_and_monitor` was **SKIPPED**.
  - [Astra Cloud Runtime Validation #39604609921](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609921) — succeeded.
- Earlier failures were useful contract regressions: stale tests still required `workflow_call` and one test had a tuple-unpacking defect. Those tests were corrected and the full suite is green on the exact latest head.
- Formal independent reviews of PR #432: **0 visible** at latest check. PR #432 remains Draft and unmerged.
- Governance and effective repository token permissions are not yet independently verified. Issue #301 remains open.

## Security prerequisites and blockers

1. Configure `MEDIAHUB_DISPATCH_HMAC_KEY` as a separate high-entropy repository secret before enabling agent dispatch. It must not equal `MEDIAHUB_GITHUB_TOKEN` and must never be exposed to Gemini.
2. Verify `MEDIAHUB_GITHUB_TOKEN` has only the minimum required repository permissions: Actions write for workflow dispatch/run monitoring and Contents read to resolve the immutable target commit. Do not print or inspect its value.
3. Keep PR #432 Draft/unmerged until updated exact-head CI, independent security review, governance evidence, and no-secret probe acceptance are recorded.
4. Do not invoke agent mode during this gate. No controller dispatch of the three Gemini children occurred in Wave 312; Agent 1/2/3 run IDs: **NOT RUN**.
5. Claude Code on Alamo/server 3 and browser automation remain **NOT RUN** until the designated host and permitted free/non-paid route are positively verified.

## Next step

Wait for all exact-head checks on PR #432 to complete, repair any remaining failures, then obtain a formal independent review of the exact head and verify effective token/governance policy. Only after those gates and accepted integration, run the default no-secret trusted-context probe. Do not launch Gemini as part of that probe.

