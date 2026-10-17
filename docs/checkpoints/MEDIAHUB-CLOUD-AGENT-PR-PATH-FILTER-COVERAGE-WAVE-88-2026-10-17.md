# MediaHub OS — PR validation path-filter coverage, Wave 88 (2026-10-17)

## Scope

A bounded CI correctness pass on PR #337. The target was to ensure pull requests that change the pinned validator dependencies or lock-generation workflow actually schedule the schema-validation workflow.

## Finding

Before this change, `.github/workflows/cloud-agent-schema-validation.yml` had a `pull_request.paths` allowlist covering schema JSON files and the schema-validation workflow only. A PR that changed only the requirements input/lock or the lock-generation workflow could therefore omit this validation workflow on the PR event. Push-triggered validation on the working branch did not fully close this review-trigger coverage gap.

## Change

Extended the `pull_request.paths` allowlist to include:

- `requirements/cloud-agent-schema-validation.in`
- `requirements/cloud-agent-schema-validation.lock`
- `.github/workflows/cloud-agent-lock-generation.yml`

The existing schema-file and schema-validation-workflow filters remain. The workflow still declares `permissions: contents: read`, uses pinned action SHAs, checks out the immutable event SHA, and installs the lock with `pip install --require-hashes`.

## Evidence

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Working branch: `contour-a-schema-validation-wave81-20261017`
- Change commit: `56e329676e373fe621b53d81daddf50882246a90`
- Updated workflow blob SHA: `31aaa4f2a35df446bae0b49e1bf4dc4f2daaed10`
- The file was fetched again after the write; the three additional path filters were present.
- Latest observed PR head at report creation: `56e329676e373fe621b53d81daddf50882246a90`.
- Validation run [39047324292](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39047324292) was in progress and run [39047328133](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39047328133) was queued at the time of observation. These are not recorded as passing.
- PR #337 remained open and Draft, not merged.
- Branch comparison with canonical docs branch: 51 ahead / 18 behind; merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. This is substantial divergence and is not approval to merge.

## Boundaries and remaining gates

This pass did not merge branches, access secrets, invoke model providers, dispatch workers, deploy Contour A, or start Contour B. Issue #301 remains open. Independent schema/authority review, accepted runner/workspace/network manifest, A0 issuer/verifier lifecycle, R-06 audit/privacy authority, and bounded worker/queue qualification remain explicit gates.

The canonical documentation-branch map was not modified. Use the [canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md), [PR #337](https://github.com/VlDMlNSh/mediahub-os/pull/337), and [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) as navigation anchors.

## Next step

Recheck the workflow runs for this exact commit and review the PR-event path filters. Then continue independent review of the authority/schema contracts and plan file-level reconciliation against the canonical documentation branch; keep PR #337 Draft until all governance gates are independently satisfied.
