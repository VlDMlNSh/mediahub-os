# MediaHub OS Contour A — MCP image digest provenance recheck (Wave 196)

- Date: 2026-10-19
- Canonical branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous checkpoint: [Wave 195](MEDIAHUB-NEXT-CONTINUATION-CHECKPOINT-WAVE-195-2026-10-19.md)
- Governance tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Question

Can public registry evidence currently map the workflow's `ghcr.io/github/github-mcp-server:v0.27.0` reference to an exact immutable OCI manifest digest suitable for a reviewed candidate pin?

## Evidence reviewed

1. The upstream [v0.27.0 release notes](https://newreleases.io/project/github/github/github-mcp-server/release/v0.27.0) establish that the source release exists and summarize its changes. They do not provide a manifest digest for the workflow's image reference.
2. The official [GitHub Container Registry package page](https://github.com/github/github-mcp-server/pkgs/container/github-mcp-server/) was surfaced in public search. The current package page presents SHA-named image versions and per-version digests, but the retrieved evidence did not establish which digest, if any, corresponds to tag `v0.27.0`.
3. A digest found on a package-version page is not sufficient unless the version-to-tag/architecture mapping is established. No digest is inferred from the version number, tag text, release commit, or unrelated package entry.
4. Prior Waves 185–187 established that the v0.27.0 release checksum asset was available, but its content was not obtained and the tag object was unsigned. A checksum of the checksum asset itself is not the image manifest digest.

## Disposition

**Exact image digest remains UNRESOLVED.** The reviewed public evidence is useful for identifying the official package and release, but does not safely prove the mapping from the workflow's mutable `:v0.27.0` reference to a specific immutable OCI manifest. Do not substitute any unrelated digest and do not edit the production workflow in this pass.

A sufficient next evidence package must bind: exact registry repository, original tag, platform/manifest-list or platform-specific digest, registry-returned manifest bytes/headers, capture timestamp, and provenance/signature or attestation details. If the tag no longer resolves or the mapping cannot be reconstructed, document that limitation rather than guessing.

## Current governance and qualification boundary

The latest re-read of Issue #301 still shows 42 comments, with Wave 192 comment `6265270600` as the latest retrieved relevant entry; no later independent governance decision was found in that tracker history. PRs #374/#375/#376 remain open and unmerged. Main's generated qualification truth continues to show ASTRA GOLD G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED. Branch-protection/review settings remain unverified.

No code or workflow was changed, no workflow dispatched, no credentials or secrets accessed, no host commands or tests executed, and no merge/deployment/qualification occurred.

## Next step

Obtain an authoritative tag-to-manifest mapping and provenance evidence for the exact MCP image, while separately obtaining the recorded governance disposition for the brokered-write boundary. Then update only a reviewed candidate, validate its exact diff and provenance, and run the existing negative/failure-path test oracle in an isolated disposable boundary.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
