# MediaHub OS — Wave 504: exact required CI context names on every main PR

- Date: 2026-10-31
- Status: **EXACT-HEAD REQUIRED CI VERIFIED / INDEPENDENT REVIEW NOT VERIFIED / MERGE NOT ACCEPTED**
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Implementation PR: https://github.com/VlDMlNSh/mediahub-os/pull/613
- Target Alamo PR: https://github.com/VlDMlNSh/mediahub-os/pull/610
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Immutable source refs

- Main/base: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- PR #613 final HEAD: `237948e03088c3ea43608b0c284327c552d34f4b`.
- PR #613 base SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Active ruleset: `MediaHub-main-autonomous-merge`, ID `26108066`.
- Canonical docs branch HEAD at start of this documentation proposal: `d9a289b9113f7567711b641a7017eb814d6c259d`.

## 1. Root cause

Wave 503 proved PR #610 had five successful Check Runs, but none matched the five exact context names required by the active ruleset. PR #613 initially removed path filters from three workflows, but inspection of the exact PR branch showed that this alone was insufficient: workflow-level names and job-level Check Run names differed from the ruleset contexts. Astra Verify also had a `paths-ignore` exclusion on pull_request.

## 2. Bounded implementation in PR #613

The PR branch now:
- Removes only the `paths` filters from the Gemini workflow contract, AI Factory verification, and provider contract verification pull_request triggers.
- Sets explicit job-level names to the exact ruleset contexts:
  - `.github/workflows/astra-cloud.yml`: job `validate` → `Astra Cloud Runtime Validation`.
  - `.github/workflows/astra-verify.yml`: job `verify` → `Astra Verify`.
  - `.github/workflows/mediahub-ai-factory-verification.yml`: job `verify` → `AI Factory verification`.
  - `.github/workflows/mediahub-provider-contract-verification.yml`: job `verify` → `provider contract verification`.
  - `.github/workflows/gemini-workflow-contract-validation-wave284.yml`: job `validate` → `Gemini workflow contract validation (Wave 284)`.
- Removes `paths-ignore` from the Astra Verify pull_request trigger only; its push filters remain intact.
- Expands `tests/test_required_ci_workflow_trigger_coverage.py` to assert every required workflow runs for every PR targeting main and that all five job names exactly match the ruleset contexts.

Changed-file blob SHAs at final PR HEAD:
- `astra-cloud.yml`: `14f37463670129bee5e84bb7e632751a2beca088`.
- `astra-verify.yml`: `7a70ff2b0e7b058fcf1ee9fd59a53628df864141`.
- `mediahub-ai-factory-verification.yml`: `93e731afcbff0a99dd1c41d62b202dcfa3dc1fa6`.
- `mediahub-provider-contract-verification.yml`: `3194a046efa62ebf7932bca124ad28fc4bb6c513`.
- `gemini-workflow-contract-validation-wave284.yml`: `6fea96b839bbb1fde1e7c7b99cd3672d82ea595d`.
- `tests/test_required_ci_workflow_trigger_coverage.py`: `53a89e06a849a5a1ccb2836179601c6bedb5fefd`.

## 3. Exact-head CI evidence

GitHub Check Runs API was read for exact PR #613 HEAD `237948e03088c3ea43608b0c284327c552d34f4b`. All five ruleset contexts were terminal SUCCESS:

| Required context | Workflow run ID | Result |
|---|---:|---|
| Astra Cloud Runtime Validation | 41190324945 | **SUCCESS** |
| Astra Verify | 41190324972 | **SUCCESS** |
| AI Factory verification | 41190324916 | **SUCCESS** |
| provider contract verification | 41190324922 | **SUCCESS** |
| Gemini workflow contract validation (Wave 284) | 41190324920 | **SUCCESS** |

The Gemini non-launching controller probe run `41190324940` also completed:
- Probe job `124505624022`: SUCCESS.
- Caller-context assertion job `124505640387`: SUCCESS.
- Admission job `124505624666`: SKIPPED.
- Dispatch job `124505657131`: SKIPPED.

This was a no-secret, non-launching probe. No Gemini child, model/provider, or live runtime was invoked. Combined legacy commit statuses are empty; they are not used to override the five successful exact Check Runs.

## 4. Review, merge and downstream impact

- PR #613 remains OPEN / DRAFT / UNMERGED; mergeable=true.
- Formal reviews: 0; inline review threads: 0.
- CI is **VERIFIED** for the exact PR head; independent review is **NOT VERIFIED**.
- PR #610 remains on older base/head and still has 0/5 required exact contexts on its immutable current head. The new names only help after PR #613 is reviewed and integrated into main; PR #610 must then be rebased/updated and retested against the new main.
- No merge, owner workflow_dispatch, secret access, Gemini dispatch, provider/model invocation, Alamo/Ollama/FCC/Claude runtime, deployment, qualification or acceptance occurred.
- No secret values were accessed.

## 5. Next gates

1. Obtain an independent security/CI review of PR #613's workflow trigger and context-name changes.
2. Only after review, integrate PR #613 through the protected main process; do not bypass the ruleset.
3. Rebase/update PR #610 onto the new main and verify all five exact contexts on its new immutable head.
4. Obtain independent review of the Alamo-role runner workflow and behavioral evidence contracts.
5. Only after all gates pass, consider the owner-authorized manual dispatch from main with `confirm=true` and exact current main SHA. Inspect runtime logs and artifact digest; keep Alamo equivalence NOT VERIFIED until separately qualified.

## Disposition

| Gate | State |
|---|---|
| Required workflow trigger coverage | **VERIFIED** on PR #613 HEAD |
| Exact five ruleset Check Run contexts | **5/5 SUCCESS** on PR #613 HEAD |
| Non-launching controller probe | **SUCCESS; dispatch SKIPPED** |
| Independent review PR #613 | **NOT VERIFIED** |
| PR #613 merge / acceptance | **NOT ACCEPTED** |
| PR #610 exact contexts | **0/5 on its current immutable HEAD** |
| Alamo/Ollama/FCC/Claude live runtime | **NOT RUN** |
| Alamo equivalence | **NOT VERIFIED** |
| Contour A acceptance | **NOT ACCEPTED** |
| Contour B | **GATED** |

---
Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
