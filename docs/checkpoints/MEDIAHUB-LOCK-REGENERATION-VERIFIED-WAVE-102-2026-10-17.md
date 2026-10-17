# MediaHub OS — lock regeneration verified (Wave 102, 2026-10-17)

## Outcome

**Byte-for-byte lock regeneration is verified for the candidate commit.** The separate lock-generation workflow ran successfully; its artifact contains the regenerated lock and a zero-byte diff. The workflow's explicit `git diff --exit-code -- requirements/cloud-agent-schema-validation.lock` gate passed.

## Source references

- Candidate PR [#338](https://github.com/VlDMlNSh/mediahub-os/pull/338): open, Draft, unmerged.
- Candidate commit [`29d72044ae77086df3380358816da2e15a940725`](https://github.com/VlDMlNSh/mediahub-os/commit/29d72044ae77086df3380358816da2e15a940725).
- Lock-generation workflow run [39053279868](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39053279868): success; trigger `push`; workflow run #15.
- Job [117456037581](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39053279868/job/117456037581): `generate`, success. Steps for Python setup, pip pin, pip-tools install, generation, diff capture, artifact upload and reproducibility assertion all completed successfully.
- Artifact ID `12108193539`, name `cloud-agent-schema-validation-lock-29d72044ae77086df3380358816da2e15a940725`, size 7,034 bytes, GitHub digest `sha256:ea7a0a91247045a83a78f2ad254bf8c046a0b4f78a11e95ce38fbfeb690b0c62`, expires 2026-10-24.
- Downloaded ZIP SHA-256 independently recomputed in the execution environment: `ea7a0a91247045a83a78f2ad254bf8c046a0b4f78a11e95ce38fbfeb690b0c62` — matches GitHub's artifact digest.
- ZIP contents: regenerated `requirements/cloud-agent-schema-validation.lock` (15,083 bytes) and `artifacts/cloud-agent-schema-validation-lock.diff` (0 bytes). The empty diff is consistent with the successful byte-for-byte assertion.
- Candidate workflow blob SHA: `bc6a50bb93ec8ba32aacc7e3b7f973a6311cb072`.
- Input blob SHA: `46aa24e6ab56bc0bc1c69e29ffa778e7f2c74635`; checked-in lock blob SHA: `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`.
- Exact-head schema validation separately passed in [run 39053283811](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39053283811), with artifact digest `sha256:898ffd15cc92d639116f873a046de7a192adcd07a7d3e31165579f20bb235476`.

## Interpretation and remaining gaps

- Lock regeneration reproducibility: **PASS for the recorded candidate SHA and runner environment**. This is evidence for this specific run, not a guarantee across future runner/image/package-index changes.
- Bootstrap integrity: **OPEN**. The workflow still installs `pip==24.3.1` and `pip-tools==7.4.1` by version from PyPI without a dedicated hash-locked bootstrap. Successful generation does not establish artifact integrity of those bootstrap packages.
- The run emitted GitHub notices that actions targeting Node.js 20 are being forced to Node.js 24, and that `ubuntu-latest` is scheduled to migrate to Ubuntu 26 beginning 2026-10-19. These are reproducibility/maintenance signals to handle deliberately, not failures in this run.
- PR #338 remains Draft/open/unmerged. Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open. A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent review and bounded worker/queue qualification remain open.
- No provider calls, secret access, agent dispatch, deployment, merge or Contour A acceptance occurred.

## Next bounded step

Harden the lock generator's bootstrap integrity without circularly trusting the generated lock. Evaluate a stable existing mechanism first; then pin and verify bootstrap artifacts/hashes and validate the change with a fresh lock-generation run. Consider runner image pinning and Node.js 24-compatible action revisions as separate reproducibility maintenance, preserving full-SHA action pins and least privilege.
