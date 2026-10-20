# MediaHub Contour A — GitHub governance visibility and positive-probe safety audit (Wave 291)

**Date:** 2026-10-20  
**Scope:** read-only inspection of refs, workflow sources, rulesets, branch protection visibility, CI summaries and caller-context probe. No dispatch, secrets access, provider invocation, tests, merge or deployment.

## Ref and candidate status

- Canonical documentation branch HEAD before this report: `55714c393584fe742826e863c3133a78f28c0e9b`.
- `main`: `80be45a70732b1d568164571d4273a6397792c3b`.
- PR #421 head `3141a44370694d78f76779243adb548318a745d7` is 61 commits ahead of main, with merge base equal to main HEAD.
- PR #421 and #426 remain OPEN/DRAFT/UNMERGED; review API returned zero submitted reviews for both. The combined-status endpoint returned no status records in this inspection. Previously reported successful CI runs are not independent review or acceptance.

## Governance visibility

- Repository metadata says public; connected integration reports repository-level `admin: true`. This does not guarantee that the integration can access every GitHub administration endpoint.
- `GET /repos/VlDMlNSh/mediahub-os/rulesets` returned `[]`: no repository rulesets were exposed by this endpoint. This does **not** prove classic branch protection is disabled or establish organization-level policy.
- `GET /repos/VlDMlNSh/mediahub-os/branches/main/protection` returned HTTP 403 `Resource not accessible by integration`. This is an access limitation, not evidence that protection is absent.
- Effective Actions settings, allowed-actions policy, approval requirements and org-level policy remain unverified from this session.

## Positive trusted-controller probe: safety constraints

- Current main controller blob `99e5a87825aeb239568f96ecef004a102ff3e53b` has only `confirm: no|yes`; `confirm == 'yes'` gates the dispatch-and-verify job. It has no explicit read-only probe mode.
- PR #421 controller blob `da1d0254a993adcc224d5859a9a97bf609abd710` changes the transport architecture to reusable workflow calls. Each child workflow has a `probe_only` input, but the controller does not pass it in the inspected caller jobs; those jobs map Gemini API-key secrets. Therefore, do **not** test the positive path by dispatching the candidate controller with `confirm=yes`: it could launch model jobs.
- Safe design: a dedicated default-deny controller probe mode; separate read-only reusable observer; no secret mapping; no write permissions; explicit conditions making every agent/model/provider job unreachable in probe mode; assertions for `workflow_dispatch`, exact controller `workflow_ref`, and `trusted_controller=true`; logs/artifact evidence only. Statically validate the design before considering any trusted-context dispatch.
- Existing Wave 284 PR caller probe remains valid for the negative path only.

## Disposition and next action

No workflow dispatch, provider/model invocation, secrets/host access, tests, merge, deployment, qualification or acceptance occurred. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated.

An owner/admin must make the effective main branch protection and Actions/org policy visible to the reviewer because the current integration cannot read those endpoints. Next code change should be a no-secret controller probe mode, not a real agent dispatch. Keep PR #421 and #426 separate and unmerged pending independent review and governance evidence.

## Source links

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) · [PR #426](https://github.com/VlDMlNSh/mediahub-os/pull/426)
