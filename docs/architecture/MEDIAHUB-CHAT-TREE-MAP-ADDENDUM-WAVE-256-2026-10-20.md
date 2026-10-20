# MediaHub Chat Tree Map Addendum — Wave 256 (2026-10-20)

## GitHub MCP server OCI digest pin

- Report: [MEDIAHUB-CLOUD-AGENT-MCP-IMAGE-DIGEST-WAVE-256-2026-10-20.md](../checkpoints/MEDIAHUB-CLOUD-AGENT-MCP-IMAGE-DIGEST-WAVE-256-2026-10-20.md).
- Official GHCR record for `v0.27.0`: https://github.com/orgs/github/packages/container/github-mcp-server/630595547?tag=v0.27.0.
- Verified Linux amd64 digest: `sha256:cbca61d547beec9b819b26bbfe6ac66ba6b373f1d6b64e8291e346bf524633e2`. All three child workflows now use `ghcr.io/github/github-mcp-server@sha256:cbca61d547beec9b819b26bbfe6ac66ba6b373f1d6b64e8291e346bf524633e2`; the mutable tag was removed from runtime invocation.
- Draft PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421), checked commit `d25cad4343126e6f6770247d48abec1c7f6c2b9b`, base `main` `80be45a70732b1d568164571d4273a6397792c3b`, 27 ahead / 0 behind.
- Exact-head [Astra Cloud Runtime Validation #39416621016](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39416621016) and [Astra Verify #39416620952](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39416620952) both SUCCESS. Verify logs: actionlint, 9 contract tests, 440 Python unit tests, compile, and signed-command smoke test passed.
- Current blob SHAs: controller `da1d0254a993adcc224d5859a9a97bf609abd710`; Agent 1 `983d3d06303f75f65de15ae2ee7f824403605e76`; Agent 2 `eefcc97f1cf9504218f48fd248f37aa8306cd309`; Agent 3 `4608462d4b59c088bbf962412060e4b1b8a93519`; Astra Verify `a087ccde747cc621f6003226e01abb10e33261dc`; contract tests `063c8f4ab2f3906d0b4f207dac429b921d5710c2`.
- Still open: independent review from another identity; controlled negative caller-context runtime test; branch-protection/governance integration. PR #421 remains Draft/unmerged. No agent launch, secret access, merge, deployment, or qualification.
- [Canonical map](MEDIAHUB-CHAT-TREE-MAP.md) · [Checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md) · [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
