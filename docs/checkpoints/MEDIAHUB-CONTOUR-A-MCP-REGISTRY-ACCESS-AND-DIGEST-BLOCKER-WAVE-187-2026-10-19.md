# MediaHub OS Contour A — MCP registry access and digest blocker (Wave 187)

- Date: 2026-10-19
- Scope: one bounded retry using the public GitHub package-version page and direct GHCR manifest endpoint after Wave 186.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior report: [Wave 186 OCI digest verification](MEDIAHUB-CONTOUR-A-MCP-OCI-DIGEST-VERIFICATION-WAVE-186-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Evidence

1. Public package page fetched: [GitHub MCP Server package versions](https://github.com/github/github-mcp-server/pkgs/container/github-mcp-server/versions?tag=v0.27.0). The extracted page listed many digests but did not reliably associate a digest with tag `v0.27.0`; it also surfaced recent package versions. Those digests are not evidence for the requested historical tag and were not used.
2. Direct anonymous manifest request to `https://ghcr.io/v2/github/github-mcp-server/manifests/v0.27.0` returned HTTP 401 in the browser fetch environment. No registry token or authenticated registry client is available through this pass, so the manifest/index response and `Docker-Content-Digest` header were not obtained.
3. The direct release checksum asset `https://github.com/github/github-mcp-server/releases/download/v0.27.0/github-mcp-server_0.27.0_checksums.txt` remained unreachable from the browser fetch environment. Release API metadata still only confirms the checksum asset itself and its own digest; it does not identify the container image.
4. Main ref remains `c06015e0b1526e0aaa6a522306052b077455aba5`. Canonical docs branch before this wave was `344f7b61138adb43b9a3bd9eba97e38214abd1dc`.
5. PR #376 remains open Draft at head `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`. Its two observed workflow runs are completed/successful:
   - [Astra Cloud Runtime Validation run 39231107098](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39231107098)
   - [Astra Verify run 39231107074](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39231107074)
   These checks do not qualify the Gemini supply chain or a deployed worker.
6. Issue #301 is open; PRs #374, #375 and #376 remain open Draft/unmerged. SentinelX reports zero connected hosts, one enrolled Mac mini offline, and `mh-dev-01` / `mh-dev-02` user-disabled. Codex Tasks has no registered environments.

## Decision

**Do not pin the MCP image yet.** The exact `ghcr.io/github/github-mcp-server:v0.27.0` OCI manifest/index digest and release-to-image provenance remain unverified. Do not substitute package-page digests for other versions, checksum-file SHA, or source commit SHA. The available environment cannot complete the authenticated/authoritative registry inspection.

No workflow dependency was modified; no Gemini workflow dispatched; no secret accessed; no host command or manual test run; no merge, deployment, or qualification occurred.

## Next action

Use an authorized registry-capable environment to request the v2 manifest with appropriate `Accept` media types and record the returned manifest/index digest; resolve platform manifests; inspect release provenance/attestation and compare to the immutable release. If the required registry access cannot be made available, keep this as an explicit supply-chain blocker and continue other independent Contour A work without dispatching Gemini.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
