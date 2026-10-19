# MediaHub OS — project map addendum, Wave 185 (2026-10-19)

- Status: upstream source identities verified for two GitHub Actions; OCI digest for the MCP image remains unresolved. No workflow dependencies changed.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 185 report: [Immutable dependency provenance](../checkpoints/MEDIAHUB-CONTOUR-A-IMMUTABLE-DEPENDENCY-PROVENANCE-WAVE-185-2026-10-19.md)
- Previous supply-chain audit: [Wave 182](../checkpoints/MEDIAHUB-CONTOUR-A-GEMINI-WORKFLOW-SUPPLY-CHAIN-AND-DISPATCH-AUDIT-WAVE-182-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

Evidence summary:
- `actions/checkout@v4` currently resolves to signed/verified commit `11d5960a326750d5838078e36cf38b85af677262`.
- `google-github-actions/run-gemini-cli@v0` currently resolves to signed/verified commit `f77273f4c914e4bf38440cf36a0369cb64a37489` (release commit message identifies v0.1.22).
- `ghcr.io/github/github-mcp-server:v0.27.0` maps to source commit `2b352ab0b914cde8c16d44200a7cace9f400be71`; the annotated tag is unsigned. Release API says immutable, but an authoritative OCI digest and digest-to-source provenance were not verified. No digest was guessed.

No workflow was dispatched; no secret read, host command, manual test, merge, deployment or qualification occurred. PRs #374, #375 and #376 remain Draft. SentinelX has zero connected hosts.

Next: verify the exact OCI digest and provenance for MCP Server v0.27.0, then prepare an isolated reviewed pinning PR and update parity tests in lockstep. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
