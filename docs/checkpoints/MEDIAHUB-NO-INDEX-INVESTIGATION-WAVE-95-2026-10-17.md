# MediaHub OS — No-index configuration investigation, Wave 95

Date: 2026-10-17  
Scope: first bounded step only — diagnose the historical `--no-index` marker in the generated cloud-agent schema-validation lock. No source/config changes were made in this pass.

## Result

The previously reported ambiguity is resolved in the current working branch. The current generated lock does not contain `--no-index`; the current generator explicitly neutralizes pip configuration and sets the PyPI index.

## Evidence

- PR #337 is open, Draft, unmerged; latest observed PR head: `514f8f74a251c38e4d64e5f8ae3d7832537ddc13`.
- Current generator workflow blob: `c22d820ccb59bcbdbaf4bfa40125063f2c68d8e0`.
- Current lock blob: `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`.
- Current validation workflow blob: `bbe4f7e975a7ceb2c9fa7d2901bd484d06cbefc6`.
- Current lock contains 162 SHA-256 hash lines, includes `--index-url=https://pypi.org/simple`, and contains zero `--no-index` markers.
- Generator workflow sets `PIP_CONFIG_FILE=/dev/null`, `PIP_INDEX_URL=https://pypi.org/simple`, removes `PIP_NO_INDEX` via `env -u PIP_NO_INDEX`, and passes `pip-compile --no-config --index-url=https://pypi.org/simple`.
- Generator run [39048549631](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048549631) completed successfully on source SHA `d493b042bdf5bb0259b84f69dc48b43875d77474`. Its job log confirms the explicit environment and generated command comment, with no `--no-index`.
- Latest observed validation runs on PR head `514f8f74a251c38e4d64e5f8ae3d7832537ddc13` succeeded: [39049839864](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39049839864) and [39049836265](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39049836265). Both report successful hash-locked dependency installation, schema/fixture validation, cross-artifact checks, machine-readable report verification and provenance artifact upload.
- The last observed comparison with canonical docs branch `docs/mediahub-chat-tree-map-20261012` was 76 commits ahead / 20 behind, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. This is a branch divergence measurement, not a merge-readiness assertion.

## Interpretation and limits

The old report described an earlier snapshot; its `--no-index` observation is stale relative to the current branch. The present workflow is explicit about the package index and the current lock output agrees. Generator run `39048549631` is on an earlier commit than the current PR head; this pass did not trigger a new run against the latest head, nor perform an independent clean-room regeneration outside GitHub Actions. Therefore the narrow configuration ambiguity is resolved by current source inspection and existing successful run evidence, but final reproducibility qualification still requires a generator run on the final candidate head and artifact/hash comparison.

## Next bounded step

Run or verify lock generation on the latest PR head and compare the produced lock artifact byte-for-byte with the committed lock. Keep PR #337 Draft; do not merge while independent authority/schema review and branch-reconciliation gates remain open.

## Navigation

- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Active PR: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Prior Wave 87 report: https://github.com/VlDMlNSh/mediahub-os/blob/contour-a-schema-validation-wave81-20261017/docs/checkpoints/MEDIAHUB-CLOUD-AGENT-LOCK-REPRODUCIBILITY-AND-CI-VERIFICATION-WAVE-87-2026-10-17.md
