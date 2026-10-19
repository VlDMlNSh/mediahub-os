# Wave 152 — PyPI bootstrap publisher-provenance gate review

- Report: [MEDIAHUB-PYPI-BOOTSTRAP-PUBLISHER-PROVENANCE-GATE-WAVE-152-2026-10-19.md](../checkpoints/MEDIAHUB-PYPI-BOOTSTRAP-PUBLISHER-PROVENANCE-GATE-WAVE-152-2026-10-19.md)
- Exact lock: `requirements/cloud-agent-lock-generation-bootstrap.lock`, blob `2cb89e822dabbe54a11e6b718ec8443b8891c926`; `setuptools==84.0.0` wheel SHA-256 `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`.
- PyPI's exact release-file page confirms the wheel digest and states Trusted Publishing was not used. The official Integrity API supports per-file provenance, but the exact endpoint response could not be retrieved in this pass; no signature or identity verification is claimed.
- Disposition: publisher provenance remains UNVERIFIED; do not close the supply-chain gate or change the dependency lock without a separate reviewed change and fresh exact-head CI.
- PR #350 remains Draft/unmerged without independent review. A0 issuer/ingress/lease/cancel/recovery, R-06 authority/privacy and accepted runner/workspace/network target manifest remain separate blockers. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED.
