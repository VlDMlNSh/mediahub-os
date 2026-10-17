# MediaHub OS — array-nested required-property negative fixtures, Wave 90

- Date: 2026-10-17
- Scope: one bounded test-coverage improvement in PR #337 / Contour A schema validation.
- Working branch: `contour-a-schema-validation-wave81-20261017`
- Implementation commit: `4ffd439ebb741f1d27753ef1e624ec8a2cd8bcb5`
- Workflow blob after change: `87db0e3fcfba9cf7373b7ba673325fc01eec6216`

## Finding

The schema-validation workflow already generated deterministic negative fixtures by removing present nested `required` properties from a generated valid instance. Its traversal followed object `properties`, but returned early for list instances. Therefore required fields inside object-valued array items were not included in that negative-fixture traversal.

## Change

Extended `nested_required_paths(node, instance, prefix)` to traverse schema `items` for each concrete array item before processing object properties. The existing removal-and-revalidation loop now also tests required fields under array-index paths. No schema, authority contract, fixture semantics, or production runtime behavior was changed.

## Verification evidence

- Workflow file was re-read after update; blob SHA: `87db0e3fcfba9cf7373b7ba673325fc01eec6216`.
- GitHub Actions run [39048283874](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048283874) completed successfully on implementation commit `4ffd439ebb741f1d27753ef1e624ec8a2cd8bcb5`.
- The successful job log reports nested-required negative-fixture counts of 37 for Task Envelope, 35 for Registry Record, and 45 for Evidence Manifest (117 total); all three schema suites passed.
- A second run [39048287670](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048287670) was still in progress at the last check; do not count it as a pass until its conclusion is observed.
- Schemas remain Draft 2020-12 and dependency installation remains hash-locked with `--require-hashes`.

## Current PR / integration state

- [PR #337](https://github.com/VlDMlNSh/mediahub-os/pull/337) remains Draft and unmerged.
- The working branch compare against `docs/mediahub-chat-tree-map-20261012` reported 56 commits ahead / 20 behind, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. Do not merge or reconcile automatically.
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Limits and next step

This is stronger generated fixture coverage, not independent schema review, production artifact-consumer qualification, or Contour A acceptance. The authority and governance gates in Issue #301 remain open, including A0 issuer/verifier lifecycle, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent review, and bounded worker/queue qualification.

Next: verify the remaining workflow run, then independently review the schema test harness and current authority/issuer contracts before any branch reconciliation. Preserve Draft status until required review and governance gates are satisfied.
