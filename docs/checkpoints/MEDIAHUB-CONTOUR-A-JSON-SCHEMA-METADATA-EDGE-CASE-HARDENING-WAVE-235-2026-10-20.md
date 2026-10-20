# MediaHub OS — JSON Schema metadata edge-case hardening (Wave 235)

- Date: 2026-10-20
- Status: **BOUNDED IMPLEMENTATION + EXACT-HEAD CI VERIFIED; PR STILL DRAFT**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Target PR: https://github.com/VlDMlNSh/mediahub-os/pull/388

## Scope and defect

Independently re-read PR #388 at pre-change head `4a131acf6484f6e370625b0ebc454ee7b4b5116c`. The metadata envelope validated `properties.schema_version` by calling `.get()` without checking that the subschema was an object. Draft 2020-12 permits boolean subschemas, so an otherwise meta-schema-valid input could raise an unhandled `AttributeError` instead of the validator's normal fail-closed diagnostic. A second edge case allowed a numeric `const` to evade the metadata-specific string constraint whenever `type: string` was also present.

## Change and read-back evidence

Updated only the existing PR #388 branch `contour-a/schema-validator-draft202012-wave214`; `main` was not changed.

- Final PR head: `815fa4af497a593f321ee692f64f53a12dcad061`.
- Validator blob: `50e85da3e9d3a2cd806236bcb6650b11764b4955`.
- Test blob: `75b99297cf94997b66663ecb66eb0caea477d7f1`.
- Added explicit rejection for non-object `schema_version` subschemas and non-string `const` values.
- Added two negative tests: boolean `schema_version` subschema and contradictory numeric `const` under a string type.
- Re-read both changed files after write. The test file now has 9 focused tests.
- PR comparison to main: 4 commits ahead, 0 behind; merge base `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- Exact-head Astra Verify run [39375449122](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39375449122) SUCCESS. Log confirms `compileall`, complete unittest discovery, **435 tests / 0 failures**, and the signed-command smoke test.
- Exact-head Astra Cloud Runtime Validation run [39375449153](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39375449153) SUCCESS; job steps for contract validation and cloud runtime tests completed successfully.
- Submitted non-approval COMMENT review on PR #388 (review ID `5581127268`) with source-bound evidence and remaining scope limits.

## Limits and global state

PR #388 remains OPEN / Draft. This change does not implement semantic `$ref` resolution or validate a runtime payload corpus. Issue #301 remains OPEN; accepted target manifest, A0 issuer/ingress/lease/cancel/recovery, R-06, source-bound worker/publisher separation, clean-room deployment and independent acceptance remain open. Contour A stays NOT_PROVEN / BLOCKED; Contour B remains gated.

The oversized canonical map still has blob SHA `2187b4ca50792fe073f0979442c0f73432a2f6f9`. Contents API returns an empty body for that blob; the GitHub connector exposes `create_tree` but does not expose a tree/ref read operation or branch-head tree SHA. I did not construct a tree from scratch, guess the base tree SHA, overwrite the map with partial text, or merge/rebase the diverged documentation branch. The map remains unchanged pending a safe verified Git-data base-tree route.

No provider credentials were read, no provider was called, no cloud/server resources changed, and no merge, deployment, Contour A qualification or acceptance occurred.

## Next bounded action

Resolve safe map update capability (obtain the current documentation-branch tree SHA through an authorized Git-data read and preserve the complete existing tree), then continue worker/publisher credential isolation and A0 issuer/capability/replay/revocation gates. Do not merge PR #388 solely on green CI; independent review and all relevant acceptance gates remain separate.
