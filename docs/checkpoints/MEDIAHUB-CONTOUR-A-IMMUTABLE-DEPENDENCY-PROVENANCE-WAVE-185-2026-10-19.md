# MediaHub OS Contour A — immutable dependency provenance (Wave 185)

- Date: 2026-10-19
- Scope: verify upstream source identities for mutable Gemini workflow dependencies; no workflow dependency was changed.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior audit: [Wave 182 Gemini workflow supply-chain audit](MEDIAHUB-CONTOUR-A-GEMINI-WORKFLOW-SUPPLY-CHAIN-AND-DISPATCH-AUDIT-WAVE-182-2026-10-19.md)
- Previous verification: [Wave 184 post-CI reconciliation](MEDIAHUB-CONTOUR-A-WAVE-184-POST-CI-EVIDENCE-RECONCILIATION-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Scope and current state

The three workflow files on `main` use `actions/checkout@v4`, `google-github-actions/run-gemini-cli@v0`, and `ghcr.io/github/github-mcp-server:v0.27.0`. All three references are human-readable tags rather than immutable content identifiers. This pass read the workflow source, upstream Git refs/commits and GitHub release metadata. It did not execute a workflow or change a dependency.

## 2. Upstream evidence

### actions/checkout

- Upstream ref: [refs/tags/v4](https://api.github.com/repos/actions/checkout/git/ref/tags/v4)
- Tag currently resolves to commit: `11d5960a326750d5838078e36cf38b85af677262`
- Commit: [11d5960a326750d5838078e36cf38b85af677262](https://github.com/actions/checkout/commit/11d5960a326750d5838078e36cf38b85af677262)
- GitHub API reports commit signature verification `verified=true`, reason `valid`; commit message is `backport fixes to releases-v4 (#2524)`.
- Interpretation: source commit identity and signature verification are established for this snapshot. The `v4` ref itself remains a mutable tag; any pin proposal must be reviewed against the intended checkout v4 behavior and action policy.

### google-github-actions/run-gemini-cli

- Upstream ref: [refs/tags/v0](https://api.github.com/repos/google-github-actions/run-gemini-cli/git/ref/tags/v0)
- Tag currently resolves to commit: `f77273f4c914e4bf38440cf36a0369cb64a37489`
- Commit: [f77273f4c914e4bf38440cf36a0369cb64a37489](https://github.com/google-github-actions/run-gemini-cli/commit/f77273f4c914e4bf38440cf36a0369cb64a37489)
- GitHub API reports commit signature verification `verified=true`, reason `valid`. Commit message identifies release `v0.1.22`; `action.yml` was readable at this exact commit.
- Interpretation: exact source commit and GitHub signature verification are established for this snapshot. The `v0` ref remains mutable. Pinning this commit is a candidate for a reviewed change, not an automatic approval.

### GitHub MCP Server container

- Upstream release: [v0.27.0](https://github.com/github/github-mcp-server/releases/tag/v0.27.0)
- GitHub release API reports `immutable=true`, published `2026-01-05T14:23:47Z`.
- Annotated Git tag object: `b50870084e1120ced9b5cd4c6aa177e8916f97da`; it points to source commit `2b352ab0b914cde8c16d44200a7cace9f400be71`.
- GitHub API reports the tag object is unsigned (`verified=false`, reason `unsigned`). The release provides a checksums asset, but this pass did not retrieve/verify its contents.
- Current workflow uses `ghcr.io/github/github-mcp-server:v0.27.0`. **Exact OCI manifest digest for this version was not verified** from authoritative registry/package evidence in this pass. Do not substitute a digest from another version, platform, mirror, or search result. The immutable GitHub release tag is not itself proof of the container's OCI digest or that the published container matches the source commit.

## 3. Decision

Do not edit the workflows in this pass. The two GitHub Actions have candidate immutable commit SHAs with valid GitHub signature-verification results. The MCP image still needs an authoritative, version-specific OCI digest and provenance/attestation verification. Workflow parity tests currently expect three mutable-reference findings per workflow (nine total), so any pinning change must update those tests and preserve parity across all three workflow files in the same reviewed change.

## 4. Verification and non-actions

- Upstream API refs, commits, action metadata and release metadata were read; no external package was pulled or executed.
- No repository tests were run manually.
- No Gemini workflow dispatch, secret read, host command, merge, deployment or qualification occurred.
- PRs #374, #375 and #376 remain open Draft; Issue #301 remains open as of this pass.
- SentinelX reports zero connected hosts; the enrolled Mac mini is offline, and `mh-dev-01` / `mh-dev-02` are user-disabled.

## 5. Next step

Obtain the OCI manifest digest specifically associated with `ghcr.io/github/github-mcp-server:v0.27.0` from the authoritative GitHub Container Registry/package metadata, then verify the digest's release/provenance relationship. After that, prepare one isolated PR pinning all three dependency types and update the parity test to assert exact reviewed refs/digests, with CI as the gate. Keep it Draft until independent review. Do not dispatch Gemini agents until supply-chain changes and workflow permissions have been reviewed.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
