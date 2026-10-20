# MediaHub OS Contour A — pin GitHub MCP server image digest, Wave 256

Date: 2026-10-20
Status: EXACT-HEAD CI PASSED / CONTROLLER NOT INTEGRATED

## Scope

This bounded wave closes the mutable GitHub MCP server container reference identified in Wave 255. It does not launch agents or integrate PR #421.

## Verified upstream image provenance

The official GitHub Container Registry version record for [GitHub MCP Server v0.27.0](https://github.com/orgs/github/packages/container/github-mcp-server/630595547?tag=v0.27.0) lists the Linux amd64 image digest as:

`sha256:cbca61d547beec9b819b26bbfe6ac66ba6b373f1d6b64e8291e346bf524633e2`

All three Gemini child workflows now use the digest-pinned image:

`ghcr.io/github/github-mcp-server@sha256:cbca61d547beec9b819b26bbfe6ac66ba6b373f1d6b64e8291e346bf524633e2`

The workflows run on the standard Ubuntu x64 hosted runner. The tag `:v0.27.0` was removed from the runtime invocation. Contract tests now reject the mutable tag and require the pinned digest.

## Candidate and CI

- PR: [Draft #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- Branch: `contour-a/workflow-call-controller-governance-wave243`
- Checked commit: `d25cad4343126e6f6770247d48abec1c7f6c2b9b`
- Base `main`: `80be45a70732b1d568164571d4273a6397792c3b`
- Compare: 27 commits ahead / 0 behind at last read.
- [Astra Cloud Runtime Validation #39416621016](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39416621016): SUCCESS.
- [Astra Verify #39416620952](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39416620952): SUCCESS. Read-back of job logs confirms actionlint passed, 9 reusable-workflow contract tests passed, 440 Python unit tests passed, compile passed, and signed-command smoke test passed.

## Read-back blob SHAs on the PR branch

- Controller `.github/workflows/gemini-batch-dispatch-controller.yml`: `da1d0254a993adcc224d5859a9a97bf609abd710`
- Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`: `983d3d06303f75f65de15ae2ee7f824403605e76`
- Agent 2 `.github/workflows/gemini-agent-2.yml`: `eefcc97f1cf9504218f48fd248f37aa8306cd309`
- Agent 3 `.github/workflows/gemini-agent-3.yml`: `4608462d4b59c088bbf962412060e4b1b8a93519`
- Astra Verify `.github/workflows/astra-verify.yml`: `a087ccde747cc621f6003226e01abb10e33261dc`
- Reusable-workflow contract tests `tests/test_gemini_reusable_workflow_contract.py`: `063c8f4ab2f3906d0b4f207dac429b921d5710c2`
- Controller contract tests `tests/test_gemini_transport_controller_contract.py`: `161fc5a1d02b9d99ddf9819ab39a803981f05d67`

## Remaining gates

1. Genuine independent review by a different identity. The connected identity is the PR author; a formal review submission from it was rejected and is not an independent review.
2. Controlled negative caller-context runtime test proving a feature-branch controller causes child jobs to skip without invoking Gemini. The available GitHub connector has no workflow-dispatch operation; this test has not been run. Do not bypass this limitation with direct child dispatch or another transport.
3. Branch-protection/required-check review and governed integration. PR #421 remains Draft/unmerged.
4. After integration and verification on `main`, run the first bounded three-agent batch through the controller using explicit `confirm: yes`; record controller/job evidence and inspect outputs before routine repeats.

## Safety record

No cloud agent was launched. No provider secret was read, printed, or changed. No merge, deployment, release, or Contour A qualification is claimed. The proposed `workflow_call` controller remains inactive on `main`; the legacy REST dispatch route remains on hold.

## Navigation

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 255 action-ref hardening](MEDIAHUB-GEMINI-ACTION-REF-HARDENING-WAVE-255-2026-10-20.md)
- [Wave 254 autonomous-use gate](MEDIAHUB-CLOUD-AGENT-AUTONOMOUS-USE-GATE-WAVE-254-2026-10-20.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Draft PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
