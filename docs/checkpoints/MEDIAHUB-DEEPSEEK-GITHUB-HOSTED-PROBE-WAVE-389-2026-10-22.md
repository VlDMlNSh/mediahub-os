# MediaHub OS — Wave 389: GitHub-hosted DeepSeek one-shot probe (2026-10-22)

## Decision and boundary

The owner clarified that cloud-agent/provider execution must use GitHub Transport and must not use physical servers as executors. This pass corrects the previous route selection. It adds a dedicated GitHub-hosted workflow for exactly one explicitly confirmed DeepSeek inference request; it does not invoke the existing self-hosted multi-provider qualification workflow.

Owner-reported configuration:
- Repository secret DEEPSEEK_API_KEY: configured.
- Repository variable MEDIAHUB_DEEPSEEK_MODEL=deepseek-flash: configured.
- Authorized spend: one inference request, maximum intended budget USD $0.01.

Secret presence is owner-reported; the secret value was not read.

## Source and implementation evidence

- PR #489 was merged by the owner. Merge commit: ce99b1d51e6fa420a32dafb70b65ae65fed5017e.
- Main registry blob SHA: 8c0f95d33a6fc85128b3a7aa37157c2dca74bbca; DeepSeek is now deepseek-flash, cost class paid_api, persistence class api. Retired aliases are absent.
- Probe PR: [#490](https://github.com/VlDMlNSh/mediahub-os/pull/490), branch feat/deepseek-github-hosted-one-shot-probe-wave-389-20261022, head SHA 3b9add632a6d2b62024afd1d7a1d5d2efa4b2e60, base SHA ce99b1d51e6fa420a32dafb70b65ae65fed5017e. PR remains Draft/Open/Unmerged; formal review list is empty.
- Workflow blob SHA: b4e81310c7a6d15c9b3b18c27b3587afd447859a, path [deepseek-github-hosted-one-shot-probe.yml](https://github.com/VlDMlNSh/mediahub-os/blob/feat/deepseek-github-hosted-one-shot-probe-wave-389-20261022/.github/workflows/deepseek-github-hosted-one-shot-probe.yml).
- Contract test blob SHA: 2e76b3a9ffc2e6994201b004489de8b839c1755e, path [test_deepseek_github_hosted_probe_contract.py](https://github.com/VlDMlNSh/mediahub-os/blob/feat/deepseek-github-hosted-one-shot-probe-wave-389-20261022/tests/test_deepseek_github_hosted_probe_contract.py).

Workflow guardrails: GitHub-hosted ubuntu-latest only; workflow_dispatch only; requires confirm_request=true and refs/heads/main; validates the configured model; sends one POST to the official DeepSeek Chat Completions endpoint; no retries, redirects, model discovery, provider iteration or fallback; output limit 8 tokens; secret and response text are not printed; sanitized evidence records target SHA, request count, status, token usage, request ID and conservative peak-price estimate. Official pricing reference: https://api-docs.deepseek.com/quick_start/pricing/ (current documented peak rates used for the estimate: input $0.30 / million tokens and output $1.20 / million tokens).

## Exact-head CI

At PR head 3b9add632a6d2b62024afd1d7a1d5d2efa4b2e60:
- [Astra Cloud Runtime Validation #39842162125](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39842162125): SUCCESS.
- [Astra Verify #39842162475](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39842162475): SUCCESS. Its unit-test step reports 471 tests, OK.
- These results verify the PR source/contract CI, not live provider execution. The focused new test was included in the aggregate test discovery, but a separate per-test invocation was not recorded.

## Execution status

- Dedicated inference request: NOT RUN.
- Request count: 0.
- DeepSeek authentication/model discovery/inference: NOT VERIFIED.
- Provider qualification / A3 acceptance: NOT QUALIFIED / NOT ACCEPTED.
- PR #490 independent review: NOT VERIFIED.
- GitHub-hosted workflow dispatch: not available as a write action in the connected GitHub toolset; PR is not merged and no browser-triggered dispatch was attempted.
- No physical server, local Ollama, local Claude, or self-hosted runner was used for this cloud probe.
- No secret values were read, copied, printed, or committed.

## Next step

Obtain independent security review of PR #490, merge only after the required review/gates pass, then dispatch the workflow on main with confirm_request=true. Verify the resulting workflow run and sanitized artifact before describing the test as successful. A successful single request is a smoke test only; it does not qualify the provider or satisfy the separate 23-round/A3 qualification ladder.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
