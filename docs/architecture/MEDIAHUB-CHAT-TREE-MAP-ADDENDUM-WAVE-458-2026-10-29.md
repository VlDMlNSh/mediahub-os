# MediaHub OS — Canonical Map Addendum, Wave 458 (2026-10-29)

- Scope: **STEP 2A ONLY — OSV-SCANNER SOURCE-CONTRACT AND EXECUTION PREFLIGHT**
- Status: **STATIC CLI/JSON CONTRACT CHECKED / TOOL INTEGRITY NOT VERIFIED / RUNTIME NOT RUN / SCA BLOCKED**
- Detailed report: [Wave 458 OSV-Scanner qualification preflight](../checkpoints/MEDIAHUB-OSV-SCANNER-QUALIFICATION-WAVE-458-2026-10-29.md).
- Input pinning: [Wave 457](../checkpoints/MEDIAHUB-DEPENDENCY-AUDIT-INPUT-PINS-WAVE-457-2026-10-29.md), blob `d82ee45893c6d0a2a68a290c2b1475cd93d117a2`; exact snapshots remain the bounded eight-input matrix recorded there.
- MediaHub immutable main target: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.

## Evidence

- OSV-Scanner v2.7.0 source commit `bfe2f84abd2f09fe0b83ba7f6dad40d296762f40`; GitHub commit signature response `verified=true / reason=valid`. Tag object `7ef17deffedb9e9b751fe6c6c328a88de29d9cf4` has `verified=false / unknown_key`; release metadata says `immutable=false`.
- Pinned docs blobs: `docs/usage.md` `f6d68845d275fe477674e8e738830a5d354d03ad`; `docs/output.md` `025bc1a3f1cb69a1b901e4b43ccfb2029f23fbae`; `docs/installation.md` `de0479312f21fcd6fb5d2ca617c7c1ac9629379b`. They document `scan -L ... --format json`, JSON on stdout, diagnostics on stderr, and SLSA verification.
- Asset/checksum/attestation API digest metadata is recorded in the detailed report but not independently recomputed. This container has no OSV-Scanner/SLSA verifier and cannot resolve `github.com`; no release binary was executed.

## Disposition

Runtime integrity/command qualification **NOT VERIFIED**, runtime CLI probe **NOT RUN**, all eight scans **BLOCKED / NOT RUN**. PR #583 and #585 remain OPEN/DRAFT/UNMERGED with zero formal reviews and empty/pending combined status; effective branch governance remains NOT VERIFIED. No Gemini batch, provider inference, secret access, merge, deployment, qualification or component adoption occurred.

Next: verify the release binary/checksum/SLSA bundle in an approved network-enabled ephemeral environment, then perform runtime CLI/JSON fixture validation before any dependency scans.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
