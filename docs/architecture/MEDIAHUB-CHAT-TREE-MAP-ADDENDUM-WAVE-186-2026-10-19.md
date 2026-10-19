# MediaHub OS — project map addendum, Wave 186 (2026-10-19)

- Status: MCP v0.27.0 OCI digest remains unverified; no workflow changes.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 186 report: [MCP OCI digest verification](../checkpoints/MEDIAHUB-CONTOUR-A-MCP-OCI-DIGEST-VERIFICATION-WAVE-186-2026-10-19.md)
- Previous report: [Wave 185 immutable dependency provenance](../checkpoints/MEDIAHUB-CONTOUR-A-IMMUTABLE-DEPENDENCY-PROVENANCE-WAVE-185-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

Wave 186 confirmed GitHub release metadata for v0.27.0 and its checksum asset ID `336567456`. The API's SHA-256 `d346c3f69e6682e2f0bae9ac2fea648c4a5212615b127d48eabdb47433063afb` identifies the checksum asset itself, **not** the container image. The asset contents could not be retrieved, and no authoritative package-page result could be tied to the exact v0.27.0 image. Other version digests were explicitly rejected. The annotated Git tag is unsigned and points to source commit `2b352ab0b914cde8c16d44200a7cace9f400be71`.

No image digest was guessed and no workflow dependency was changed. PRs #374/#375/#376 remain Draft. SentinelX has zero connected hosts. No Gemini dispatch, secret read, host command, manual tests, merge, deployment, or qualification occurred.

Next: obtain exact OCI manifest/index digest and release provenance using an authorized registry-capable environment. Only then consider a reviewed pinning PR. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
