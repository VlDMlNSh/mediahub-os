# Provisional map addendum — Wave 306: exact wheel attestation check

Date: 2026-10-21. This addendum is on the unmerged working branch and is not part of the canonical map.

- Detailed evidence: [Wave 306 — setuptools exact-wheel attestation check](../checkpoints/MEDIAHUB-SETUPTOOLS-EXACT-WHEEL-ATTESTATION-CHECK-WAVE-306-2026-10-21.md).
- Canonical map remains [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md), on `docs/mediahub-chat-tree-map-20261012`; not modified.
- PyPI documents `GET /integrity/<project>/<version>/<filename>/provenance`. The exact setuptools 84.0.0 wheel endpoint returned HTTP 404 and no provenance payload. Treat this as no provenance object retrieved for the exact file, not evidence of maliciousness.
- Pinned wheel SHA-256 remains `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`; byte digest does not prove publisher/source-build identity.
- Bootstrap provenance gate: **OPEN / NOT PROVEN**. Do not promote PR #374 on the current evidence. Next: controlled, credential-free, reproducible source-to-wheel comparison without executing the candidate wheel.
- PR #430 remains OPEN/DRAFT/UNMERGED; exact-head workflow-run lookup for recorded head `331813fb4262de86911c726353c7bd47acf43b5b` returned no runs, and no formal reviews were returned. Recheck the live head and required checks before integration.
