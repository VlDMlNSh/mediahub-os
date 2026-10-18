# Bootstrap publisher-provenance review — Wave 152 — 2026-10-18

## Result
**Publisher provenance is NOT independently verified.** The pinned bytes are hash-locked, and the upstream GitHub release tag/commit appears signed, but the PyPI distribution files report that they were **not uploaded using Trusted Publishing**. Therefore this review cannot bind the downloaded wheel to an authenticated PyPI publishing workflow. Keep the bootstrap publisher-provenance risk OPEN; do not treat hashes alone as publisher identity.

## Repository evidence
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Bootstrap lock blob: `2cb89e822dabbe54a11e6b718ec8443b8891c926`.
- The lock comment explicitly states that hashes verify bytes, not publisher identity or independent security review.
- Locked package: `setuptools==84.0.0`.
- Locked wheel SHA-256: `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`.
- The package lock path recorded by PR #338 is `requirements/cloud-agent-lock-generation-bootstrap.lock`; it exists on the PR candidate branch, not at the tested canonical branch path. No branch integration was performed.
- PR #338 current fetched head: `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`; open/Draft/unmerged.
- Current comparison against the canonical documentation branch: **DIVERGED, 20 ahead / 193 behind**, merge base `2bd41b5f71006597a7669a4b7154abc58f87af5d`. This is fresher than Wave 151's 20/184 snapshot; do not integrate mechanically.
- PR #338 prior successful validation was on merge ref SHA `dce0bc01c04020560b2842de6ab5cf190348f0fa`, not exact head `fd12ee...`; prior artifact ID `12110676230`, digest `sha256:7957517179ce91c469e851996d2141410640c008da90c6f0c35f879ac185bb3c`. Fresh CI after any reconciled base is required.

## Independent public-source evidence
- PyPI release page for setuptools 84.0.0 lists the wheel and its SHA-256 as above, uploaded 2026-08-08, with **“Uploaded using Trusted Publishing? No”** and uploader `twine/7.0.0 CPython/3.14.6`: https://pypi.org/project/setuptools/84.0.0/
- The upstream GitHub release page shows v84.0.0 and states the tag/commit has GitHub verified signature metadata: https://github.com/pypa/setuptools/releases
- PyPI's official attestation documentation explains that attestations can bind a release distribution digest to a publisher identity and that consumers should verify attestations cryptographically: https://docs.pypi.org/attestations/
- PyPI's official consuming-attestations guide describes the verification path: https://docs.pypi.org/attestations/consuming-attestations/
- These are distinct trust signals: a signed source tag does not prove that the specific wheel uploaded to PyPI was built from that tag or published by a specific trusted workflow. The release page's “No” Trusted Publishing result leaves that binding unestablished in this review.
- This pass did not fetch the wheel, compute its digest independently, query the PyPI Integrity API for a machine-verifiable attestation bundle, or verify the Git signature cryptographically. It is a bounded public-metadata review, not a complete supply-chain audit.

## Disposition
1. Keep bootstrap publisher provenance **OPEN / NOT INDEPENDENTLY VERIFIED**.
2. Before accepting the bootstrap lock, verify a machine-readable PyPI attestation for the exact wheel digest, including signer identity and source repository/workflow; if no suitable attestation exists, document an explicit alternative trust decision and independent artifact/source comparison.
3. Confirm the full hash lock matches the exact candidate branch and rerun the validator workflow against a reconciled base and record exact tested SHA, run/job IDs and artifact digest.
4. Keep PR #338 Draft/non-mergeable until full tree/history reconciliation, provenance disposition and fresh CI pass.
5. Continue canonical provider registry consumer census at `ops/qualification/provider_model_registry.json`; do not create a duplicate registry.

## Authority and evidence boundary
Issue #301 remains open. GOV-CAP-01…07 and R-06 remain unresolved; this review does not choose issuer semantics or authorize runtime execution. Jarvis, ASTRA A0 and MediaHub Product State Authority remain distinct. No credentials were inspected, no provider was called, no workflow was dispatched, no test was run, and no code/branch was merged or deployed.

## Canonical map
https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
