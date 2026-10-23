# Chat tree map addendum — Wave 399: owner approval and free-route admission boundary

Date: 2026-10-23

- Report: [Wave 399 owner approval reconciliation](../checkpoints/MEDIAHUB-CLAUDE-FREE-ROUTE-ADMISSION-WAVE-399-2026-10-23.md).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).
- Main SHA checked: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`; docs branch before this addendum: `35a52ec2915c34fd4c946dc565f7327ec48d285c`.
- Owner approval for a separate GitHub-hosted Claude Code + FCC PR is recorded in [Issue #301 comment 6354035391](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6354035391). It authorizes design/implementation only; live dispatch, merge, deployment and acceptance remain separately gated.
- FCC upstream observed at `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`, release `v6.16.16`, AGPL-3.0-only. Pin a reviewed immutable release/commit.
- FCC lists free-labelled aliases, but none is selected as a MediaHub route yet. FCC `MODEL_FALLBACKS` is an optional ordered list and README warns it may use multiple providers. A no-paid-fallback invariant needs exact model/provider evidence and negative tests.
- **Disposition:** owner approval **RECORDED**; exact route admission **BLOCKED pending named provider/model and verified no-paid-fallback semantics**; workflow implementation **NOT STARTED**; dispatch **NOT RUN**; qualification **NOT VERIFIED**; Contour A **NOT ACCEPTED**.
