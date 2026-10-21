# MediaHub OS — setuptools bootstrap publisher-provenance audit (Wave 305)

- Date: 2026-10-21
- Status: **HASH IDENTITY CONFIRMED / PUBLISHER ATTESTATION ABSENT / SUPPLY-CHAIN GATE OPEN**
- Candidate branch: `contour-a-schema-validation-clean-wave129-20261019`
- Candidate PR: https://github.com/VlDMlNSh/mediahub-os/pull/374
- Validation workflow source: `.github/workflows/cloud-agent-lock-generation.yml`
- Workflow blob SHA: `22ed52a9252630bfa62b5fbb7d37ea79c84f8b82`
- Bootstrap lock blob SHA: `2cb89e822dabbe54a11e6b718ec8443b8891c926`
- Prior reconciliation: [Wave 304](MEDIAHUB-CLOUD-AGENT-VALIDATION-REUSE-AND-REF-AUDIT-WAVE-304-2026-10-21.md)
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing Issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Question

Does the bootstrap lock's `setuptools==84.0.0` wheel have publisher provenance sufficient to close the supply-chain concern recorded in PR #374?

## Evidence recovered

1. The candidate's bootstrap lock pins:
   - `setuptools==84.0.0`
   - wheel SHA-256 `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`.
   - Lock comment explicitly says hash pins verify bytes, not publisher identity; independent review is pending.
2. The official PyPI file-detail page for [setuptools 84.0.0](https://pypi.org/project/setuptools/84.0.0/) lists the same wheel SHA-256, upload date 2026-08-08, **“Uploaded using Trusted Publishing? No”**, and uploader client `twine/7.0.0 CPython/3.14.6`. The source distribution page reports the same publishing status/client.
3. The [upstream GitHub release page](https://github.com/pypa/setuptools/releases) shows v84.0.0's tag and commit as verified signatures. This establishes signature status for the upstream tag/commit displayed there; it does **not** by itself cryptographically bind the PyPI wheel bytes to that tag or source tree.
4. PyPI's [attestation documentation](https://docs.pypi.org/attestations/) explains that per-file attestations can bind distribution digests to publisher/build identity and source provenance. The inspected PyPI file page does not report Trusted Publishing for this wheel; no matching file attestation was independently verified in this pass.
5. The lock-generation workflow uses `--require-hashes --only-binary=:all:`, sets the index URL to PyPI, and checks the installed version. Those are useful reproducibility and source-selection controls, but they do not establish who published the package.

## Finding

- **Byte identity: CONFIRMED** — the hash pinned in the repository matches the SHA-256 shown by official PyPI for the named wheel.
- **Upstream release signature: OBSERVED** — the upstream v84.0.0 tag/commit is shown as verified on GitHub.
- **PyPI publisher identity / wheel-to-source attestation: NOT ESTABLISHED** — PyPI explicitly says Trusted Publishing was not used, and this pass did not independently verify a signed attestation connecting the downloaded wheel digest to the upstream source/build identity.
- This is not evidence that the wheel is malicious. It is an evidence gap in publisher/build provenance. A SHA-256 pin proves that downloaded bytes match the expected digest; it does not authenticate the publisher.

## Decision

Do not silently replace or unpin the dependency. Keep PR #374 Draft and the supply-chain gate open until a reviewer verifies one of these evidence paths:

1. Obtain and cryptographically verify a PyPI/in-toto attestation for the exact wheel digest, if one exists despite the file page's Trusted Publishing field; record the verification command/tool version and result.
2. If no suitable attestation exists, compare the exact wheel contents with a wheel built from the verified upstream source/tag in an isolated, documented build, including reproducibility limits and a complete file-level diff; have an independent reviewer assess the result.
3. If neither path is practical, select a justified bootstrap toolchain with stronger available provenance and regenerate/retest the lock in a separate reviewed change. Do not change versions only to silence the finding.

## Scope and safety

This pass inspected repository metadata and public release metadata only. It did not download/install the package, execute the package, modify dependency pins, dispatch workflows, access credentials, call a model/provider, merge, deploy, or qualify Contour A.

## Next step

Run the attestation-verification procedure against the exact wheel URL/digest in a disposable, credential-free environment. Record whether an attestation exists and its verified source identity. If absent, stop short of claiming publisher provenance and proceed with a reproducible source-build comparison or a separately justified bootstrap replacement.

**Disposition: PR #374 SUPPLY-CHAIN REVIEW REQUIRED; CONTOUR A BLOCKED / NOT_PROVEN.**
