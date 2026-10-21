# MediaHub OS — lock-generation trigger correction, Wave 91

- Date: 2026-10-17
- Scope: one bounded CI trigger correctness correction on PR #337.
- Working branch: `contour-a-schema-validation-wave81-20261017`
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Finding

The Wave 88 controlled-PyPI report states that changing only the generated lock should not trigger lock regeneration. The live workflow contradicted that statement: its `push.paths` list included `requirements/cloud-agent-schema-validation.lock`. This could schedule a generation run for a lock-only change, even though the lock is an output, not a source input.

## Change

Removed only `requirements/cloud-agent-schema-validation.lock` from the lock-generation workflow's push path filters. The workflow remains triggered by:
- `requirements/cloud-agent-schema-validation.in`
- `.github/workflows/cloud-agent-lock-generation.yml`
- manual `workflow_dispatch`

The schema-validation workflow still includes the lock file in its own path filters; dependency changes therefore continue to schedule validation. No package versions, hashes, credentials, permissions, schemas, fixtures, or runtime authority were changed.

## Evidence

- Previous workflow blob: `951631787208740daf7999e71df24beb625b9910`.
- Correction commit: `d493b042bdf5bb0259b84f69dc48b43875d77474`.
- New workflow blob read back from GitHub: `c22d820ccb59bcbdbaf4bfa40125063f2c68d8e0`.
- Read-back matched the exact submitted content.
- Assertions from read-back: lock-only trigger absent; input trigger present; workflow-file trigger present.
- Prior successful controlled generator runs: [39046826239](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046826239) and [39046901040](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046901040). Both report the same input and lock SHA-256 values; latest artifact ID `12106331705`, ZIP digest `sha256:fa5a99df325011844a8998a8f9db848cc691ebd69f2ff55fde4dfe2ba9ece599`.
- Before this correction, latest observed PR head was `97e82dc9d1b45a10da40abb5007fec2935325c5e`; schema validation passed on that head in [39048424851](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048424851) and [39048421851](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048421851). Those runs do not qualify the new correction commit; fresh checks are required.

## Remaining gates

- PR #337 is open, Draft, and unmerged. No independent submitted review records were observed.
- PR #335 has a competing schema-validation workflow implementation. Wave 89 documents a consolidation requirement; neither PR should be blindly merged.
- PR #337 is substantially diverged from the canonical docs base. Latest pre-change comparison was 65 ahead / 20 behind, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
- Issue #301 gates remain open: A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent schema review, and bounded worker/queue qualification.
- No provider call, secret access, dispatch, deployment, merge, or acceptance occurred in this pass.

## Next step

Verify fresh schema-validation CI on the correction and report commits. Then resolve the documented PR #335/#337 workflow collision through explicit consolidation and independent review before any integration.
