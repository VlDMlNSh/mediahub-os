# MediaHub GitHub-hosted FCC Claude workflow test-coverage pass — Wave 402

Date: 2026-10-23

## Scope and target

- Target PR: [#502 — GitHub-hosted FCC Claude worker on OpenRouter free route](https://github.com/VlDMlNSh/mediahub-os/pull/502).
- PR branch: `contour-a/github-hosted-fcc-openrouter-free-wave400`.
- Current terminal target head: `acf0713924e98f64c8fcb8f637058ab5039d5107`. Earlier intermediate head `bd6d23d7cbf5aa551346b7df82e9fc72fbbc8cbb` had an Astra Verify failure that was subsequently resolved.
- Base/main: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Workflow blob: `8571678864c260c0e84392e2566a75856c3cf5f4`.
- Contract-test blob: `eb93f867ce48128daf4e784f4860da8a44de41ec`.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).

## Work completed

1. Added a dedicated GitHub-hosted workflow-contract job and included the test path in the workflow's pull-request path filter.
2. Corrected the worker's repeated credential-like prompt check so it fails closed instead of allowing a matching prompt through an `|| true` tail.
3. Fixed a contract assertion that did not match the quoted target-SHA guard.
4. Re-read both modified files and confirmed their current blob SHAs above.

## Exact-head CI evidence

- [FCC worker workflow run #39878373657](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878373657) on target head `bd6d23d7cbf5aa551346b7df82e9fc72fbbc8cbb`: **SUCCESS**.
  - [Install smoke job #120169497289](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878373657/job/120169497289): **SUCCESS**; FCC pinned-source install and entry-point checks passed.
  - [Workflow contract job #120169497584](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878373657/job/120169497584): **SUCCESS**, 4 tests passed.
  - Dispatch gate and bounded worker were **SKIPPED** on the pull-request event; no provider/model request was made.
- [Astra Cloud Runtime Validation #39878373601](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878373601): **SUCCESS**.
- [Astra Verify #39878373703](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878373703): **FAILED**. Its log reports `test_workflow_runs_only_installed_test_tools` failed because the workflow was classified as running pytest without installing it. This failure remains an exact-head blocker until the current merge ref is reconciled and the check passes.

## Security/admission disposition

The prior Wave 401 static review findings remain unresolved:

- F1: actual upstream provider/model provenance and request metadata are not captured.
- F2: repository read scope lacks a proven sensitive-path/task-path allowlist.
- F3: the generated patch artifact is not scanned alongside the text result.
- F4: the effective FCC configuration is not proven to have no fallback route.

The OpenRouter `openrouter/free` router selects among currently available free models; it does not guarantee Qwen or a stable model identity. Official documentation: https://openrouter.ai/docs/guides/routing/routers/free-router

Therefore:

- FCC install smoke: **SUCCEEDED**
- Workflow contract tests: **SUCCEEDED (4/4)**
- Full exact-head CI at the intermediate head `bd6d23d7cbf5aa551346b7df82e9fc72fbbc8cbb` initially failed Astra Verify; that failure was superseded by a later head
- Independent formal review: **NOT VERIFIED**
- Live inference: **NOT RUN**
- No-paid-fallback qualification: **NOT VERIFIED**
- Live dispatch: **BLOCKED**
- Contour A: **NOT ACCEPTED**

No secret values were read. No provider was invoked. No workflow dispatch, merge, deployment, or production action occurred.

## Next step

Resolve the Astra Verify workflow-hygiene failure at the current PR head, then fix F1–F4, add negative tests for fallback/config and artifact rejection, rerun all exact-head checks, and obtain an independent review. Only then consider a separately authorized, no-write inference smoke using the free-only route. Do not merge merely to unlock `workflow_dispatch`.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

 
## Terminal revalidation — current PR head

- Current PR #502 head: `acf0713924e98f64c8fcb8f637058ab5039d5107`.
- [FCC workflow run #39878467537](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878467537): **SUCCESS**; install smoke [job 120169811392](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878467537/job/120169811392) **SUCCESS**; contract tests [job 120169811173](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878467537/job/120169811173) **SUCCESS, 4/4**.
- [Astra Verify #39878467453](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878467453) and [Astra Cloud Runtime Validation #39878467451](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878467451): **SUCCESS**.
- The previous Astra Verify failure at intermediate head `bd6d23d7cbf5aa551346b7df82e9fc72fbbc8cbb` is superseded by this successful current-head run.
- Formal independent reviews: **0**. Wave 401 findings F1–F4 remain open. Dispatch-gate and bounded-worker were skipped; inference remains **NOT RUN** and live dispatch remains **BLOCKED**.
