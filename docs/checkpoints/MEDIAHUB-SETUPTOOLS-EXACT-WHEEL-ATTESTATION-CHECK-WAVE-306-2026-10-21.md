# MediaHub OS — setuptools bootstrap attestation verification (Wave 306)

- Date: 2026-10-21
- Status: **NO PYPI PROVENANCE OBJECT RETRIEVED / BOOTSTRAP SUPPLY-CHAIN GATE OPEN**
- Scope: read-only verification of the exact wheel pinned by the existing bootstrap lock; no download/install/execute of the wheel and no dependency change.
- Candidate: [PR #374](https://github.com/VlDMlNSh/mediahub-os/pull/374), branch `contour-a-schema-validation-clean-wave129-20261019`.
- Exact file: `setuptools-84.0.0-py3-none-any.whl`
- Expected SHA-256 from the lock: `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`
- Prior audit: [Wave 305](MEDIAHUB-SETUPTOOLS-BOOTSTRAP-PUBLISHER-PROVENANCE-AUDIT-WAVE-305-2026-10-21.md).

## Evidence and method

1. Read the official PyPI Integrity API documentation: [PyPI Integrity API](https://docs.pypi.org/api/integrity/). It specifies the route `GET /integrity/<project>/<version>/<filename>/provenance` for retrieving the provenance object for an individual distribution.
2. Requested the exact route: [setuptools 84.0.0 wheel provenance endpoint](https://pypi.org/integrity/setuptools/84.0.0/setuptools-84.0.0-py3-none-any.whl/provenance). The fetch returned HTTP **404 page_not_found**. No provenance object or attestation payload was returned for this exact filename.
3. A separate read of the PyPI project page was challenged by the site and could not independently refresh the file-detail metadata in this pass. Wave 305 remains the source for the previously observed PyPI uploader/Trusted Publishing metadata and wheel digest.
4. The endpoint result is consistent with the wheel having no PyPI provenance object currently available through this API. It is not a cryptographic proof of maliciousness, and it does not validate the wheel against upstream source.

## Decision

- The pinned digest establishes the expected byte identity only when compared with an independently obtained artifact; it does not establish publisher identity or source-build provenance.
- Do not treat the upstream signed Git tag as proof that the PyPI wheel was built from that source.
- Keep the bootstrap supply-chain gate **OPEN / NOT PROVEN**. Do not promote PR #374 based on the current evidence and do not silently replace the dependency pin.
- Next technical step: use a disposable, credential-free environment to obtain the exact wheel and compare its contents against a build from the verified upstream source, with the source commit, build toolchain, commands, and resulting digests recorded. If that comparison cannot be made reproducible, propose a separately reviewed bootstrap artifact/source strategy. This remains a verification task, not an instruction to execute the pinned wheel.

## Current repository gate snapshot

- PR #374: OPEN; latest previously recorded tested head `3b1fc96beeedcc6cb38c7beeb5809f0004c6ac8a`; successful run `39222111677` is historical evidence for that exact head, not this provenance check. No formal approving reviews were returned by the review API in this pass.
- PR #430: OPEN/DRAFT; previously recorded head `331813fb4262de86911c726353c7bd47acf43b5b`. The exact-head workflow-run lookup returned an empty list and the review API returned no reviews. Empty results are not evidence that required checks are satisfied.
- Issue #301 remains OPEN. A0 issuer/ingress/lease/cancel/recovery, R-06 authority, accepted target manifest, dispatch authority, independent review, runtime qualification, and Contour A acceptance remain unresolved.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md), canonical documentation branch `docs/mediahub-chat-tree-map-20261012`. This pass does not mutate that branch or canonical map.

## Explicit non-actions

No package installation or execution, credential access, provider/model call, agent dispatch, merge, deployment, qualification, or acceptance occurred. This report is provisional evidence on the working branch/PR #430 and is not canonical acceptance.

## Next step

Complete a controlled, reproducible source-to-wheel comparison without executing the candidate wheel; independently review the result, then decide whether PR #374 can pass the bootstrap provenance gate. Keep Contour A **BLOCKED / NOT PROVEN** until the remaining governance and runtime gates also pass.
