# Wave 404 — FCC free-route workflow indentation repair

Date: 2026-10-23

## Scope
Bounded source review and repair of PR #502's GitHub-hosted FCC/OpenRouter free-route candidate. This is candidate-branch evidence, not a canonical-map update or acceptance.

## Finding
The OpenRouter free-router probe step was indented as additional content under the preceding shell `run: |` block rather than as a sibling item in `bounded-worker.steps`. Consequently, the intended probe was not represented as a workflow step. The existing contract test also asserted a stale model literal (`open_router/openrouter/free`) rather than the current implementation, which selects a concrete `:free` model from the `openrouter/free` response and passes it as `open_router/${MODEL_ID}`.

## Changes
- Corrected the probe step indentation in `.github/workflows/mediahub-fcc-free-claude-worker.yml`.
- Added a regression assertion that the probe is a sibling workflow step.
- Updated the contract test to match the current concrete free-model selection and model pin.
- Kept the workflow disabled by default; no workflow_dispatch, provider inference, secret read, merge, or deployment was performed by this pass.

## Evidence
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/502
- Before repair, worker blob SHA: `d6086e7059bfd198ca8cda7c345d9d82e63a6740`.
- Repaired workflow blob SHA: `735db573625542e061b1ebeb75e1546720033dfb`.
- Latest test blob SHA: `68e77fec5ec74ef2d7d02e2cd36a04fa9dd6a865`.
- Repair commits: `b6f2c0b3cd0a62a5178b518f71d1e1af1835797b`, `df851a2b828242d85bfed0493c76a9ff31138f0c`, `591829a8f4a1f270ba16721aa65b5953cca876d0`, `868b10456315fe1001c296fdde8ca719dbee4a8d`.
- Workflow run `39880539263` on intermediate commit `df851a2b828242d85bfed0493c76a9ff31138f0c`: install smoke succeeded; contract test failed because its stale model literal did not match the implementation. The test was corrected afterward.
- Latest exact-head workflow-run query for `868b10456315fe1001c296fdde8ca719dbee4a8d` returned no runs. Exact-head CI is **NOT VERIFIED**. Formal PR reviews remain empty (**NOT VERIFIED**).

## Security and acceptance
- No live provider dispatch was initiated by this pass. Historical/intermediate run evidence is not evidence that the repaired worker can successfully execute.
- The candidate remains OPEN/DRAFT. Do not enable `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE` or run a live worker until current exact-head CI, independent review, and route/billing/fallback gates are verified.
- Contour A remains NOT ACCEPTED.

## Next
Obtain fresh exact-head CI for the repaired workflow and contract test, inspect all terminal jobs, and arrange independent review. Then re-evaluate whether the candidate is eligible for a controlled free-only probe; no paid fallback is permitted.
