# MediaHub OS Contour A — MCP OCI digest verification (Wave 186)

- Date: 2026-10-19
- Scope: bounded follow-up on the unresolved `ghcr.io/github/github-mcp-server:v0.27.0` image identity. No workflow dependency was changed.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous report: [Wave 185 immutable dependency provenance](MEDIAHUB-CONTOUR-A-IMMUTABLE-DEPENDENCY-PROVENANCE-WAVE-185-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Evidence obtained

1. GitHub release API for [GitHub MCP Server v0.27.0](https://github.com/github/github-mcp-server/releases/tag/v0.27.0) reports the release as immutable and lists an uploaded checksum asset:
   - Asset: `github-mcp-server_0.27.0_checksums.txt`
   - Asset ID: `336567456`
   - API-reported checksum-file digest: `sha256:d346c3f69e6682e2f0bae9ac2fea648c4a5212615b127d48eabdb47433063afb`
   - API asset metadata: [GitHub release asset API](https://api.github.com/repos/github/github-mcp-server/releases/assets/336567456)
2. The annotated Git tag object `b50870084e1120ced9b5cd4c6aa177e8916f97da` points to source commit `2b352ab0b914cde8c16d44200a7cace9f400be71`. GitHub API reports the tag signature as `unsigned`.
3. The public package search surfaced package pages and manifests for other versions/identifiers, but no result could be reliably tied to the exact `v0.27.0` tag. Those unrelated digests were rejected rather than reused.
4. The GitHub connector returned a 404 for the direct release-asset download URL and does not allow direct GHCR/package-version endpoints in this session. A browser fetch of the checksum asset also failed. Therefore the checksum-file contents were not read, and no OCI digest for the exact v0.27.0 image was verified.

## Conclusion

**The OCI digest remains unresolved.** The checksum asset's own SHA-256 is not the image digest and must not be substituted for it. The release tag, source commit, and package metadata do not by themselves prove the exact registry manifest digest or the source-to-image provenance.

No workflow files were modified. No digest was guessed. This is a verified blocker, not a successful pinning result.

## State and non-actions

- Issue #301 remains open.
- PRs #374, #375 and #376 remain open Draft PRs and unmerged.
- Wave 183 CI remains recorded as successful on PR #376 head `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`; this is not supply-chain qualification.
- SentinelX has zero connected hosts; Mac mini offline; `mh-dev-01` and `mh-dev-02` user-disabled.
- No Gemini dispatch, secret access, host command, manual tests, merge, deployment, or qualification occurred.

## Next action

Use an authorized environment with registry access to resolve the exact OCI manifest/index digest for `ghcr.io/github/github-mcp-server:v0.27.0`, verify its platform manifests and release provenance/attestation, and compare against the exact published release. Record evidence before proposing a pinning PR. The checksum file may corroborate release archives but cannot alone establish the container manifest digest.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
