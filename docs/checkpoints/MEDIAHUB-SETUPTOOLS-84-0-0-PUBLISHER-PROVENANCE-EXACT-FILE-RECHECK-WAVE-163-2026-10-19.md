# MediaHub OS — exact-file PyPI publisher-provenance check — Wave 163

- Date: 2026-10-19
- Status: **BLOCKING EVIDENCE / NOT INDEPENDENTLY VERIFIED**
- Repository: `VlDMlNSh/mediahub-os`
- Work branch: `docs/contour-a-wave-163-pypi-publisher-provenance-20261019`
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Scope: one supply-chain acceptance item carried forward from Wave 152; read-only public metadata/API checks.

## 1. Finding

The exact PyPI Integrity API routes for both release files of `setuptools==84.0.0` return HTTP 404. PyPI's official Integrity API documentation explicitly defines 404 as “file has no provenance.” Therefore publisher provenance is **not available from PyPI's Integrity API for these exact release files at the time of this check**.

This is stronger than the previous unverified assumption that an attestation might be retrievable, but it does not establish that the files are malicious or that no other independent provenance source exists. Do not treat a source-tag signature as proof that the uploaded wheel was built and published from that source.

## 2. Exact evidence

### Official package metadata

- Release page: https://pypi.org/project/setuptools/84.0.0/
- JSON metadata: https://pypi.org/pypi/setuptools/84.0.0/json
- Package version: `84.0.0`
- Wheel: `setuptools-84.0.0-py3-none-any.whl`
- PyPI-reported wheel SHA-256: `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`
- File size: 818,216 bytes
- Upload timestamp: `2026-08-08T18:27:56.719708Z`
- PyPI JSON reports `has_sig: false`; this is file metadata, not a substitute for the Integrity API result.

### Integrity API routes

- Wheel provenance: https://pypi.org/integrity/setuptools/84.0.0/setuptools-84.0.0-py3-none-any.whl/provenance — HTTP 404.
- Source archive provenance: https://pypi.org/integrity/setuptools/84.0.0/setuptools-84.0.0.tar.gz/provenance — HTTP 404.
- API contract: https://docs.pypi.org/api/integrity/
- The official contract specifies `GET /integrity/<project>/<version>/<filename>/provenance` and states that 404 means the file has no provenance. The response does not contain an attestation bundle or publisher identity to cryptographically verify.

## 3. Acceptance disposition

| Claim | Disposition | Reason |
|---|---|---|
| PyPI lists the exact wheel digest | VERIFIED AS PUBLISHED METADATA | Official release JSON returns the SHA-256 above |
| PyPI Integrity API provides provenance for the wheel | NOT AVAILABLE / BLOCKED | Exact-file endpoint returned 404 under documented semantics |
| Wheel is cryptographically bound to an approved publisher workflow | NOT VERIFIED | No provenance object is available to verify |
| Upstream source release signature proves the wheel publisher/build | NOT ESTABLISHED | A source-tag signature does not bind the uploaded wheel to that source/workflow |
| Safe to close publisher-provenance gate | NO | Requires an explicit accepted alternative trust decision or a different exact artifact with verifiable provenance |

No wheel or archive was downloaded, no local hash was recomputed, no package was installed, and no credential or provider was accessed. This is a public metadata/API inspection only.

## 4. Recommended next action

1. Treat this exact wheel as **provenance-unverified** for any trust decision that requires publisher attestation.
2. Inspect the existing bootstrap lock/manifest consumers to establish whether this exact artifact is required or whether an approved alternative artifact is already pinned; do not silently replace dependencies.
3. If the exact wheel is mandatory, obtain an explicit supply-chain risk disposition from the accountable owner, with evidence and compensating controls recorded. Do not infer approval from a successful hash-lock installation.
4. If an alternative package version/artifact is proposed, verify its exact PyPI Integrity API response and digest, then review compatibility and update the existing canonical lock/manifest through the normal PR/CI path.
5. Keep Contour A qualification blocked until the bootstrap dependency provenance requirement is either satisfied or explicitly dispositioned by the accepted governance authority.

## 5. Repository context and evidence boundary

At the start of this wave, live refs were re-read:
- `main`: `c06015e0b1526e0aaa6a522306052b077455aba5`
- canonical documentation branch `docs/mediahub-chat-tree-map-20261012`: `28816f6b523c8cbc878ebd0575b17bc419669889`
- Functional Baseline 2.0 blob: `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, status ACCEPTED / CANONICAL IMMUTABLE REFERENCE POINT.
- Existing provider registry `ops/qualification/provider_model_registry.json` blob: `62328126fd2cd8879a73bb6812adcacd3e2abe84`; no duplicate registry was created.

This wave did not change runtime code, dependency locks, workflows, secrets, provider routing, runner state, or deployment configuration. No test or CI pass is claimed. No merge, deployment, qualification, or independent acceptance occurred.

**Disposition:** bootstrap publisher provenance remains OPEN / BLOCKING / NOT INDEPENDENTLY VERIFIED. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains gated.
