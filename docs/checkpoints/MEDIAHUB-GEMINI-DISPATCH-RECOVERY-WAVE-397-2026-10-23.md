# Wave 397 — Recover exact evidence for the 2026-10-22 Gemini controller batch

Date: 2026-10-23

## Decision

**CONTROLLER DISPATCH OBSERVED / AGENTS 1–2 WORKFLOW SUCCESS / AGENT 3 WORKFLOW FAILED / BATCH FAILED / PR REVIEW AND CURRENT-HEAD CI NOT VERIFIED / CONTOUR A NOT ACCEPTED**

## Immutable target and controller provenance

- Repository: [mediahub-os](https://github.com/VlDMlNSh/mediahub-os)
- Controller run: [39809515516](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39809515516), event `issue_comment`, source comment ID `6345154437`.
- Controller job `119931684523` failed; readiness job `119931641712` succeeded.
- Immutable target SHA used by all three children: `11d04d2f2687e9ba9215e4b67af2e450516960bb`.
- Target is historical and is not current main. Current main observed in this pass: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- The controller log explicitly records HTTP 204 acceptance for all three child dispatch requests, then reconciles the three child run IDs. The final batch gate failed because Agent 3 did not conclude success.
- No new controller run was started during this Wave 397 pass.

## Child-run ledger

| Role | Correlation ID | Run / job | Terminal status | Artifact |
|---|---|---|---|---|
| Agent 1 — bounded engineering | `cb031a6f-7895-4bdb-ab3a-00c01138779b` | [Run 39809549381](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39809549381) | SUCCEEDED | [Artifact 12440465374](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39809549381/artifacts/12440465374), digest `sha256:08e93ee129e841a38cff36f2009c8cdfb6c5f99eafa38884db169166172a0a29` |
| Agent 2 — research/architecture | `b85e3a6b-5413-4b92-b7d5-ef375b73ac3b` | [Run 39809552897](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39809552897) | SUCCEEDED | [Artifact 12438639378](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39809552897/artifacts/12438639378), digest `sha256:824e049d5a033f402b395022b48417df567ed6a31ea1de75d1ff2798d981700a` |
| Agent 3 — security/provenance | `66689ff8-f36a-4980-89fb-4ede0c72d2a1` | [Run 39809555931](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39809555931) | FAILED | [Artifact 12440805011](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39809555931/artifacts/12440805011), digest `sha256:f32aaa45a5d1fb3fd64e9c103b291285da986d5c8cff0b344fbe6a0939d911df` |

The artifact digests above are the GitHub Actions API's recorded ZIP digests. The ZIPs were downloaded and their content inspected; the digests were not independently recomputed in this pass.

## Results and failure analysis

### Agent 1

- Run and job completed successfully.
- Created evidence-only PR [#479](https://github.com/VlDMlNSh/mediahub-os/pull/479), head `63a9eb4800b716ec495cd0085e10ccf93eb0e967`, base target `11d04d2f2687e9ba9215e4b67af2e450516960bb`.
- PR remains open/unmerged. Exact-head checks returned zero check-runs; formal reviews returned an empty list. Both are **NOT VERIFIED**.
- Its change is a 30-line evidence checkpoint, not a runtime implementation.

### Agent 2

- Run and job completed successfully.
- Created evidence checkpoint `evidence/agent-2-verification-20261022.json`, blob SHA `b1c9341fbbc296805dfba65c17688c2dad168f72`, in PR [#480](https://github.com/VlDMlNSh/mediahub-os/pull/480), head `0dd20858ae56d9edc635fd7440036aeb3336c119`.
- The report maps existing tests and lists `pytest tests/test_astra_github_agent_contract.py` as reproducible; the agent artifact does **not** establish that this command was executed. Treat the checkpoint's self-reported PASS as documentary only, not independent CI evidence.
- PR remains open/unmerged. Exact-head check-runs returned zero; formal reviews returned an empty list. Both are **NOT VERIFIED**.

### Agent 3

- HMAC/signature verification job `119931797371` succeeded.
- Bounded Gemini job `119931853212` failed at the step validating an actionable PR result.
- The artifact shows 15 API requests with 6 errors for configured `gemini-3.5-flash-lite`; stderr contains provider HTTP 503 `UNAVAILABLE` / high demand. The GitHub MCP create-PR operation failed twice with provider-side 503s. The artifact's natural-language response claims an existing/published PR, but its own tool statistics show zero successful `create_pull_request` calls. That PR claim is **not accepted as evidence**.
- A security checkpoint file was created/updated on branch `agent-3-security-audit-20261022`, with reported blob SHA `be5fc56064ba9e46a16018ca5d33242b7927b1c8`; the branch head observed in repository inventory is `20c640df15e63b8227a87187224faaf0fdf78adc`. No associated PR was verified.
- Failure classification: **provider/model availability plus PR-publication failure; actionable PR gate failed**. Do not re-run the batch merely to retry Agent 3 without a new admission decision and a bounded mitigation.

## Current state and next step

- PRs #479 and #480 are open, unmerged, have no formal reviews, and no exact-head check-runs in the API response.
- Agent 3 output is not an independently reviewed security audit. Its branch/checkpoint is not a substitute for a PR and CI.
- This batch is a real historical dispatch, but it is **not** a successful three-agent batch, not qualification, and not acceptance.
- Issue #301 still has P0/A0 and R-06 governance/authority gates, target-manifest acceptance, semantic authority resolution, independent review, trusted-main probe and route qualification outstanding.
- Next: independently inspect #479/#480 as evidence-only PRs and decide whether to retain or close them; validate Agent 3's branch/checkpoint without trusting its unverified claims; fix or bound the observed 503/PR-publication failure before any future controller batch. Do not launch a new batch until current gates are independently proven.

## Navigation

- [Canonical chat tree map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 396 artifact verification](MEDIAHUB-CONTOUR-A-ARTIFACT-VERIFICATION-WAVE-396-2026-10-23.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Controller workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml)
