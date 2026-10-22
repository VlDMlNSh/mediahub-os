# MediaHub Contour A — launch-time and dispatch-readiness recheck (Wave 397)

Date: 2026-10-23

## Decision
**LAUNCH ETA NOT COMMITTABLE / GEMINI AGENTS NOT DISPATCHED / CONTOUR A NOT ACCEPTED**

The approved controller defines a 40-minute job timeout for the combined dispatch-and-monitor step. If all governance/admission gates are already satisfied and the child workflows start promptly, allow **up to 40 minutes for dispatch plus monitoring**; this is a controller ceiling, not a promise that all agents will finish successfully within that time. No new controller run was started in this pass.

## Current evidence
- `main` HEAD: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf` (commit message: Add bounded OpenRouter catalog auth probe (#492)).
- Approved controller: [gemini-batch-dispatch-controller.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml). Its `dispatch_and_monitor` job has `timeout-minutes: 40`; it fails closed unless `vars.MEDIAHUB_GEMINI_BATCH_ENABLED` is true and requires `secrets.MEDIAHUB_GITHUB_TOKEN` plus `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`. Secret values were not read and effective configuration was not tested.
- The controller's dispatch path requires a trusted `main` ref, explicit agent-mode confirmation for manual workflow dispatch (or the narrowly scoped owner `/next` issue-comment trigger on Issue #301), then dispatches and monitors three child workflows against one immutable target SHA.
- [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437) is now MERGED. This repairs/extends controller contract tests but does not establish effective secret configuration, close issuer/admission authority, or qualify provider/model execution.
- [PR #335](https://github.com/VlDMlNSh/mediahub-os/pull/335) remains OPEN / DRAFT / UNMERGED at head `44e2bc7c735ad7f70294d66de8e08eb1da612e0d`; formal review list is empty and combined status endpoint returned no statuses. Therefore independent review and current exact-head CI are NOT VERIFIED.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN. Prior verified artifact evidence still says `AUTHORITY_REFERENCES_UNRESOLVED` OPEN P0; schema/fixture tests do not resolve live issuer, grant, reviewer, route, policy, or revocation authority references.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md), blob SHA `f04873c9cbbf1ba8d45ccbfd3f6afc8cee916a41`.

## Gate assessment
- Controller source/40-minute ceiling: **VERIFIED** by read-back of `main`.
- Batch admission variable effective value: **NOT VERIFIED** (configuration value intentionally not inspected).
- Required secrets present, correctly named, scoped and effective: **NOT VERIFIED** (values intentionally not read; no dispatch probe).
- PR #335 independent review and current exact-head CI: **NOT VERIFIED**.
- A0 issuer/admission and R-06 audit/privacy governance gates: **BLOCKED / OPEN P0** on existing evidence.
- Gemini Agents 1–3: **NOT RUN**. No controller run ID, child run IDs, artifacts, or agent results exist from this pass.
- Contour A: **NOT ACCEPTED**.

## Estimate
A responsible launch ETA cannot be given while the P0 authority gate and independent-review/current-head evidence remain unresolved. Once those gates are closed and effective controller configuration is confirmed through an approved no-secret readiness path, budget up to **40 minutes** for the controller's combined dispatch/monitor window, then allow additional time for artifact review and independent verification. Passing the controller run alone is not Contour A acceptance.

## Next step
Close or explicitly disposition the A0 `AUTHORITY_REFERENCES_UNRESOLVED` P0 finding and R-06 governance requirements; obtain independent review and reconcile/revalidate PR #335 on the current canonical docs head. Then perform a bounded, no-secret readiness check and only after all gates pass launch through the approved controller. Do not bypass the controller or infer success from absent CI results.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
