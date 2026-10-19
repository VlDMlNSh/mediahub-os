# MediaHub OS — PyPI bootstrap publisher-provenance gate review, Wave 152

- Date: 2026-10-19
- Status: **REVIEWED / TRUST GATE OPEN / NO DEPENDENCY CHANGE**
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical documentation branch HEAD observed at start: `28816f6b523c8cbc878ebd0575b17bc419669889`
- Main HEAD observed at start: `c06015e0b1526e0aaa6a522306052b077455aba5`

## Question

Can the outstanding provenance concern for the hash-locked `setuptools==84.0.0` bootstrap wheel be closed using primary PyPI evidence?

## Primary evidence

- Bootstrap lock path: `requirements/cloud-agent-lock-generation-bootstrap.lock`
- Blob SHA: `2cb89e822dabbe54a11e6b718ec8443b8891c926`
- Locked wheel SHA-256: `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`
- PyPI release page: https://pypi.org/project/setuptools/84.0.0/
- PyPI Integrity API specification: https://docs.pypi.org/api/integrity/
- File-level API route documented by PyPI: `GET /integrity/<project>/<version>/<filename>/provenance`.

The PyPI release page currently reports for the exact wheel `setuptools-84.0.0-py3-none-any.whl`: SHA-256 matches the lock above, upload date 2026-08-08, and **Uploaded using Trusted Publishing? No**. The source distribution page also reports No. See the release page's per-file metadata.

The Integrity API specification says the file-level endpoint returns a provenance object when provenance is available and documents 404 as “file has no provenance”. The direct endpoint response for this exact file could not be retrieved in this pass (the web retrieval returned a cache-miss error), so this pass does **not** claim an API 404, a cryptographic signature verification, or the absence of every possible third-party attestation.

## Security disposition

1. The byte digest is consistent with PyPI's displayed digest, but this only binds the lock to those bytes; it does not establish publisher identity.
2. The primary PyPI page is affirmative evidence that this file was **not uploaded via Trusted Publishing**.
3. No attestation bundle was successfully retrieved and cryptographically verified during this pass. Publisher provenance therefore remains **UNVERIFIED**.
4. Do not mark the bootstrap supply-chain gate closed. Keep the schema candidate Draft/unmerged. Do not silently regenerate the lock or substitute a dependency without a separate dependency review and fresh exact-head CI.
5. A follow-up may either verify a retrievable attestation against the exact wheel digest and an explicitly trusted identity, or propose a minimal bootstrap-toolchain change with documented dependency rationale, reproducible lock regeneration, and independent review.

## Live repository state observed

- PR #350: OPEN / DRAFT / UNMERGED; head `4c1ebafc5d33e8ae075a5bba85771d14aed4ac96`; GitHub reports mergeable, but independent review submissions are absent. Its base is behind the current canonical docs branch and the compare reports divergence; do not treat the mergeable flag as a complete integration/acceptance decision.
- PR #338: OPEN / DRAFT / UNMERGED; retained as a historical source candidate, not the integration target.
- Issue #301: OPEN. A0 issuer/ingress/lease/cancel/recovery, R-06 authority/privacy, and accepted runner/workspace/network target-manifest gates remain separate blockers.
- Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED**. Contour B remains gated.

## Work performed and limitations

- Re-read the exact bootstrap lock and confirmed the wheel hash.
- Checked the exact PyPI release file metadata and the official Integrity API contract.
- No repository code, dependency, workflow, secret, provider, dispatch, queue, merge, or deployment action was performed.
- This is a bounded evidence review, not independent security approval.

## Next step

Resolve the provenance gate explicitly: retrieve and verify the exact file's attestation if one is available, otherwise propose and review a minimal dependency/toolchain adjustment. Only then rerun lock reproducibility and exact-head CI. In parallel, continue the independent A0/R-06/target-manifest blockers under Issue #301.
