# MediaHub OS — DeepSeek Cloud Pool Admission Assessment (Wave 387)

Date: 2026-10-22  
Status: **IMPLEMENTATION PRESENT / CREDENTIAL NOT VERIFIED / LIVE EXECUTION NOT RUN / NOT QUALIFIED**

## Scope and immutable references

- Repository main source snapshot: `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- Cloud authorization baseline: `docs/architecture/MH-CLOUD-AUTH-BASELINE.md`, blob `075652ad031e92f7d0c9231db6f40f5f45cd77b8`
- Provider auth probe: `ops/qualification/hybrid_agent_auth_probe.py`, blob `1fb0cb41d219eaf26dc830c8585a790c89a5cb50`
- Cloud orchestrator: `runtime/mediahub_runtime/cloud_orchestrator.py`, blob `24c28197df7baca49abd81956752a7a5092506d9`
- Provider registry: `ops/qualification/provider_model_registry.json`, blob `62328126fd2cd8879a73bb6812adcacd3e2abe84`
- Provider auth probe tests: `tests/test_hybrid_agent_auth_probe.py`, blob `238e2b9881bafb59e9bab63217e84d89b92e904c`
- Qualification workflow: `.github/workflows/astra-provider-qualification.yml`, blob `d3160088fbef4fce152ed7335f0acaa3bb440378`
- Qualification contract: `docs/qualification/ASTRA-GOLD-CLOUD-EXECUTOR-EXTENSION-2026-10-02.md`, blob `262d82d13dd764c46c9f40851c32789b44a9e0ea`
- Governing Contour A issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Confirmed existing components

1. `DEEPSEEK_API_KEY` and `MEDIAHUB_DEEPSEEK_MODEL` are already named in the cloud authorization baseline.
2. The auth probe has a DeepSeek `/models` check. This proves only an authentication/model-list endpoint response when actually run; it does not prove model inference.
3. The cloud orchestrator already registers a native DeepSeek route using `DEEPSEEK_API_KEY` and `MEDIAHUB_DEEPSEEK_MODEL`.
4. The provider model registry includes `deepseek-1`, base URL `https://api.deepseek.com/v1`, with candidate models `deepseek-chat` and `deepseek-reasoner`. These are repository-configured candidates, not a live availability claim.
5. Existing probe tests assert that DeepSeek is registered and missing credentials fail closed without exposing secret names/values in results.
6. The A3 provider workflow maps `secrets.DEEPSEEK_API_KEY` to the runner environment, but is a `workflow_call` workflow targeting a self-hosted `mediahub-provider` runner. Its existence does not establish that the secret exists or that the runner is available/admitted.

## Security and execution disposition

- No API key was provided to this session. No secret value was read, transmitted, generated, or stored.
- Available GitHub actions in this session expose no repository-secret write operation and no workflow-dispatch operation. Secret creation and live dispatch therefore could not be performed from these tools.
- The DeepSeek API is identified by the repository as a paid API. No budget or paid-call authorization is inferred from the request to add a provider; do not run billable inference until the owner has explicitly enabled the credential and accepted the intended cost.
- Current `main` combined-status and PR-workflow-run lookups returned empty results for SHA `11d04d2f2687e9ba9215e4b67af2e450516960bb`; this is **NOT VERIFIED**, not CI PASS.
- Contour A remains governed by Issue #301. The extension contract requires the admission ladder `REGISTERED → CREDENTIAL_PRESENT → AUTH_SUCCESS → MODEL_DISCOVERY_PASS → PROBE_PASS → EXECUTION_PASS → RESULT_VALIDATION_PASS → A3_VERIFIED`, 23 fresh isolated rounds for each cloud path, independent A3 review, and isolation/timeout/replay/recovery evidence.
- No workflow was dispatched. No provider request or paid inference was executed. No agent was qualified or accepted.

## Required next steps

1. Owner creates `DEEPSEEK_API_KEY` as a GitHub Actions repository secret using GitHub Settings; never paste the value into chat, a commit, an issue, logs, or artifacts.
2. Owner verifies whether the intended A3 runner `mh-dev-02` is available and admitted. Do not substitute another runner or route.
3. Select and set `MEDIAHUB_DEEPSEEK_MODEL` as a repository variable only after checking current provider model availability and cost; candidate registry entries are not proof of current availability.
4. Run the existing non-secret unit tests on a reviewed immutable SHA, then use the authorized qualification workflow/command path for model discovery and one bounded synthetic inference, with explicit cost limits and sanitized evidence.
5. Complete 23 fresh isolated DeepSeek rounds, independent review, exact-SHA CI, and required isolation/timeout/replay/recovery checks before changing `DEEPSEEK_DIRECT` from `NOT_PROVEN`.
6. Only after DeepSeek is independently qualified should the next cloud executor be selected.

## Evidence classification

- Existing implementation: **VERIFIED BY SOURCE READ**
- Secret configured: **NOT VERIFIED**
- Authentication: **NOT RUN**
- Model discovery: **NOT RUN**
- Live inference: **NOT RUN**
- A3 qualification: **NOT RUN**
- Independent review / Contour A acceptance: **NOT VERIFIED / NOT ACCEPTED**

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md


## Follow-up found during Wave 387 — stale model IDs

A live official-docs check found the repository registry still listed `deepseek-chat` and `deepseek-reasoner`, which are legacy model aliases according to the provider changelog. The current documented model ID for DeepSeek-V4.1-Flash-1017 is `deepseek-flash`; the provider labels this a paid API and pricing varies by peak/off-peak time. Sources: [official model/pricing page](https://api-docs.deepseek.com/quick_start/pricing/) and [official changelog](https://api-docs.deepseek.com/updates/?release=deepseek-coder).

A separate source-bound fix is proposed in [PR #489](https://github.com/VlDMlNSh/mediahub-os/pull/489): provider registry model list and cost classification refresh plus a regression test. The branch read-back confirmed the retired aliases are absent and the expected new model/cost metadata are present. Exact-head status/workflow-run queries returned empty lists; CI remains **NOT VERIFIED**. PR #489 is open, draft, unmerged. The focused test has not been executed in this session.


## CI refresh after PR #489 opened

- PR #489 exact head: `219724adc95f24fbb74a36e4816ffd44e8638892` (open, draft, unmerged).
- Astra Cloud Runtime Validation run [39840474749](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39840474749): **SUCCESS**; job `120039845740`, contract validation and cloud runtime tests completed successfully.
- Astra Verify run [39840474441](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39840474441): **IN PROGRESS** at last read; job `120039843941`, still installing test dependencies; compile, cloud admission unit tests and signed-command smoke test were pending. The focused DeepSeek registry test is therefore **not yet verified as executed**.
- Combined status endpoint returned an empty list, so it is not treated as a pass. No provider secret was used and no live DeepSeek inference was run.


## Final exact-head CI refresh (2026-10-22)

PR #489 exact head `219724adc95f24fbb74a36e4816ffd44e8638892` remains open, Draft, and unmerged. Current workflow evidence:

- [Astra Cloud Runtime Validation #39840474749](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39840474749): **SUCCESS**, job `120039845740`; contract validation and cloud runtime tests passed.
- [Astra Verify #39840474441](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39840474441): **SUCCESS**, job `120039843941`; compile, Cloud admission unit tests, and Signed command smoke test all completed successfully.
- Focused test file `tests/test_deepseek_model_registry.py`, blob `b89c4b0dd0053376ea505b156fc0861b1f3fb656`, is present in the exact PR head. The workflow's aggregate unit-test pass is verified; the output does not isolate this new test by name, so its individual execution is not separately proven.
- PR review API returned no reviews. Independent review remains **NOT VERIFIED**. Combined status list was empty; workflow run conclusions above are the available CI evidence.
- Official DeepSeek docs were rechecked: the model-list endpoint and current changelog identify `deepseek-flash` as the current Flash model ID; legacy `deepseek-chat` and `deepseek-reasoner` were scheduled for discontinuation. Sources: [model list](https://api-docs.deepseek.com/api/list-models/), [changelog](https://api-docs.deepseek.com/updates/?release=deepseek-coder).
- Credential configuration remains **NOT VERIFIED**. No key was supplied to this session, no secret was created/changed, no live auth/model discovery/inference was executed, and no paid API request was made. DeepSeek remains **NOT QUALIFIED** pending secret confirmation, admitted runner, live bounded probe, 23 fresh isolated rounds, independent review, and remaining A3 gates.
