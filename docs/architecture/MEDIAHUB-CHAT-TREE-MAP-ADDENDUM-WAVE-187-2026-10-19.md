# MediaHub OS — project map addendum, Wave 187 (2026-10-19)

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 187 report: [MCP registry access and digest blocker](../checkpoints/MEDIAHUB-CONTOUR-A-MCP-REGISTRY-ACCESS-AND-DIGEST-BLOCKER-WAVE-187-2026-10-19.md)
- Prior report: [Wave 186 OCI digest verification](../checkpoints/MEDIAHUB-CONTOUR-A-MCP-OCI-DIGEST-VERIFICATION-WAVE-186-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

Wave 187 retried the public package page and direct GHCR manifest URL. The package page exposed multiple digests but did not reliably associate one with `v0.27.0`; direct anonymous manifest access returned HTTP 401, and the release checksum asset remained unreachable in this browser context. No digest was inferred or substituted.

Main HEAD remains `c06015e0b1526e0aaa6a522306052b077455aba5`. PR #376 remains Draft/unmerged at `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`; its observed Astra Verify and Cloud Runtime Validation runs passed. Issue #301 open; PRs #374/#375/#376 Draft; SentinelX has zero connected hosts and Codex Tasks no registered environments.

Next: obtain exact OCI digest and provenance through an authorized registry-capable environment. Do not dispatch Gemini before supply-chain and permission review. No workflow edits, dispatch, secret reads, host commands, manual tests, merge, deployment, or qualification occurred. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
