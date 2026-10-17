# MediaHub OS — Cloud-Agent Lock Reproducibility and CI Verification (Wave 87)

- Date: 2026-10-17
- Status: **LOCK REPRODUCIBILITY VERIFIED FOR THE CURRENT INPUT/TOOLCHAIN SNAPSHOT; HASH-LOCKED INSTALL AND SCHEMA FIXTURES PASS**
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Continuation checkpoint: [Wave 87 continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-17-wave87.md)

## 1. Work completed

1. Re-read the lock input, generator workflow, generated lock, Wave 86 report, current continuation checkpoint, canonical map, Master Roadmap, PR #337 and Issue #301.
2. Located successful lock-generation run [39045574488](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39045574488), which produced artifact ID `12105503066` from source commit `287fc64638a6ddd968912441f123b6c933c124be`. Its artifact ZIP digest was `sha256:4e8f45a9e2bfb1c27e4a91dd27ca46584d125fd2c9b765c2fa3cd7f937146cdf`.
3. Found that the committed lock lacked the standalone leading comment line emitted by `pip-compile`. This was a byte-level reproducibility defect; package pins and per-package hash counts matched, but the file was not identical to generator output.
4. Updated `.github/workflows/cloud-agent-lock-generation.yml` so pushes changing `requirements/cloud-agent-schema-validation.lock` also trigger lock generation. Workflow blob SHA: `c1a4b9d4b191c5c64412abc0a86568ac6d7f563a`.
5. Restored the generator-emitted leading comment line in the committed lock. Lock blob SHA: `16c9fc637333c55420902871837bd2f9e47f5c4d`.
6. Re-ran lock generation against commit `6242eebd35b5182feda7180a7ea997105b07ea07` using [run 39046196776](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046196776). The emitted lock was compared line-for-line against the checked-in lock and **matched exactly**. Artifact ID `12106350476`; ZIP digest `sha256:682fd8135f1e90bdbd8e75416ba3fccbb014e8a1895b18cdf64629deffc1dbc9`.
7. The validation job passed `pip install --require-hashes` and Draft 2020-12 schema checks plus positive, nested-required negative, additional-property, enum, date-time, cross-artifact reference and cross-artifact mismatch fixtures. Evidence: [run 39046201242](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046201242). Runs [39046224814](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046224814) and [39046228193](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046228193) also passed on subsequent branch head `f840f226700ff3f5bbc4a141f8b922593bac7ce4`.

## 2. Evidence and integrity

- Direct input: [cloud-agent-schema-validation.in](https://github.com/VlDMlNSh/mediahub-os/blob/contour-a-schema-validation-wave81-20261017/requirements/cloud-agent-schema-validation.in), blob SHA `46aa24e6ab56bc0bc1c69e29ffa778e7f2c74635`.
- Lock: [cloud-agent-schema-validation.lock](https://github.com/VlDMlNSh/mediahub-os/blob/contour-a-schema-validation-wave81-20261017/requirements/cloud-agent-schema-validation.lock), blob SHA `16c9fc637333c55420902871837bd2f9e47f5c4d`; 18 pinned distributions, 162 SHA-256 package hashes.
- Generator uses Python 3.12, `pip==24.3.1`, `pip-tools==7.4.1`, `--generate-hashes`, and SHA-pinned checkout/setup-python/upload-artifact actions.
- Initial generator run [39045260463](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39045260463) failed at lock generation; it is retained as historical failure evidence. Subsequent successful runs and exact output comparison supersede it for the current snapshot.
- Latest PR state observed before the documentation commits: open, Draft, unmerged, GitHub `mergeable=true`; no independent reviews were submitted. Branch comparison against the canonical documentation branch was `diverged`, 31 ahead / 18 behind, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. These counts are relative to the PR base, not `main`.

## 3. Boundaries and remaining blockers

- This verifies dependency lock generation and schema-validation CI; it does **not** establish full autonomous-environment acceptance.
- Issue #301 remains open: A0 issuer/verifier lifecycle, R-06 audit/privacy authority, accepted runner/workspace/network target manifest, independent schema review, and qualification of the bounded read-only worker/queue path remain outstanding.
- PRs #332 and #333 remain separate work; this pass did not merge them.
- No provider invocation, credential access, task dispatch, deployment, Contour B work, release, qualification or acceptance occurred.
- Node.js deprecation warnings for the pinned Actions were non-fatal in the observed runs; they should be handled as a separate maintenance item after compatibility/provenance review.

## 4. Next step

Re-read the final branch head and checks after the Wave 87 documentation commits, then perform independent file-level schema/authority review and a deliberate branch reconciliation. Keep PR #337 Draft until review and Issue #301 gates are closed.

## Canonical navigation

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [PR #337](https://github.com/VlDMlNSh/mediahub-os/pull/337)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)


## Subsequent branch-head revalidation (2026-10-17, 15:46 UTC)

A later workflow revision on the same working branch made the package source explicit. The report above records the earlier verified snapshot; this section records the newer branch state and supersedes earlier workflow/lock SHAs for current-state navigation.

- Latest observed implementation HEAD: `91f28b32829e3c581b8c05a75238b0a3e276c669`.
- Current generator workflow blob: `89a0a3ee07ee72b10c790af94f9561f54b5ae751`. It sets `PIP_INDEX_URL=https://pypi.org/simple`, leaves `PIP_NO_INDEX` empty, and includes the committed lock file in its push path filter.
- Current lock blob: `4273a245d10425f3270b30de054a76b545c2e935`. The generated command header records `--index-url=https://pypi.org/simple`; the generator output and checked-in lock were again compared line-for-line and matched exactly.
- Latest successful generator run: [39046513655](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046513655), source HEAD `91f28b32829e3c581b8c05a75238b0a3e276c669`, artifact ID `12105873011`, artifact ZIP digest `sha256:21b4c123d1c4a3e3d5ee3a103bfec21ab892e79421a9fb0c831677125203aacb`.
- Latest observed schema-validation runs on that HEAD both passed: [39046513729](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046513729) and [39046516128](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046516128).
- Follow-up note: the autogenerated pip-compile command comment still contains `--no-index` even though the workflow explicitly sets the PyPI index and `PIP_NO_INDEX` is empty. Generation and validation passed, but the effective package-source configuration should remain an explicit review point before treating the dependency pipeline as fully qualified.
