# MediaHub OS — current Contour A dispatch gate reconciliation (Wave 395)

Date: 2026-10-23

## Status
**CURRENT CONTROLLER SOURCE VERIFIED / CONTROLLER DISPATCH BLOCKED / GEMINI AGENTS NOT RUN / CONTOUR A NOT ACCEPTED**

## Immutable refs observed
- `main` HEAD: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Canonical documentation branch before this report: `062bb337de8faae5e6b12d8a3c5fde90cc013e4d`.
- Current controller blob on main: `28874450099e70b0f9d276600e6452c1b8e1b1a6`.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md), blob `f04873c9cbbf1ba8d45ccbfd3f6afc8cee916a41`; the Contents API returns empty content for this large file, so the map itself was not changed.
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).

## Controller architecture and governance history
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) merged at `f16e5bae202a78584f273132e7f88c6e25d3142e`, converting child workflows to reusable `workflow_call`.
- [PR #432](https://github.com/VlDMlNSh/mediahub-os/pull/432) then merged at `1a6e5a16ef9950b72dda04abd69a27f019922489`, restoring controller-mediated GitHub REST dispatch plus signed child authorization/HMAC. The current main history is a descendant of the #421 merge and contains the later #432 correction; this is sequential history, not an omitted merge.
- Current main controller source uses `workflow_dispatch` (default non-launching probe; agent mode requires explicit confirmation), plus the exact owner `/next` comment on Issue #301. It checks `vars.MEDIAHUB_GEMINI_BATCH_ENABLED`, uses `secrets.MEDIAHUB_GITHUB_TOKEN` and `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`, signs the three fixed-scope child dispatches, and monitors run IDs.
- Current child workflows still expose `workflow_dispatch`; they check HMAC and allowlisted target SHA/base/scope before provider steps. Thus controller route and HMAC checks are present, but technical exclusion of a direct child invocation is not equivalent to removing the trigger; do not claim absolute transport exclusivity.
- The owner-reported presence of the three settings is recorded in Issue #301 comment `6326517813`; values were not read and effective token scope remains unverified.
- Current Issue #301 acceptance list still has open A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy gates, and requires an accepted runner/workspace/network target manifest plus independent schema/semantic review. These are substantive pre-dispatch gates.

## Current CI and run evidence
- Exact-main Astra Verify run [39846843270](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39846843270) was recorded SUCCESS for main SHA `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`; the independent OpenRouter catalog-auth probe [39847014875](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875) succeeded but did not perform inference and does not qualify Gemini dispatch.
- Issue-comment controller runs created by Wave 394 report/PR comments were [39855458504](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39855458504), [39855430145](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39855430145), and [39855464924](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39855464924). Their controller/probe/admission/dispatch jobs are **SKIPPED** because the comments were not the exact owner `/next` trigger on Issue #301. No child run IDs were created by these events.
- PR #441 remains OPEN at head `9f40b90c3106662cfcc337c48f29e4794fa713dc`; formal reviews: 0; exact-head CI/review are **NOT VERIFIED**. It remains part of the outstanding independent-review evidence identified in Wave 393.
- PR #335 remains OPEN/DRAFT/UNMERGED at head `44e2bc7c735ad7f70294d66de8e08eb1da612e0d`, base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`; historical schema run [39044583119](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39044583119) succeeded, but the branch has no formal review and is behind current main. Current-main integration/CI for PR #335 is NOT VERIFIED.
- PR #437 and #458 are merged. No fresh Gemini controller run, child run/job IDs, or Gemini artifacts were created in this pass.

## Decision
Do **not** post an owner `/next` trigger or launch agents while the explicit Issue #301 A0 and R-06 acceptance gates remain open and PR #441's independent review is absent. Continue safe independent work. Do not read secret values, infer effective permissions from secret presence, bypass the controller, or claim that successful unrelated main CI qualifies the dispatch path.

## Next bounded step
Complete a source-bound, independent review of PR #441 and reconcile the A0 issuer/ingress/lease/cancel/recovery plus R-06 audit/privacy gates against the authoritative runner/workspace/network manifest. Then rerun the no-secret trusted-main controller probe through an approved invocation path and capture its exact run/job evidence. Only after the mandatory gates are actually closed should the owner `/next` controller route be considered.

## Actions not performed
No controller launch, Gemini child dispatch, provider/model call, secret-value read, deployment, merge, or qualification occurred in this pass.
