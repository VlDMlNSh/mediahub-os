# MediaHub OS Contour A — caller-guard contract hardening (Wave 257)

Date: 2026-10-20
Status: IMPLEMENTED / EXACT-HEAD CI GREEN / RUNTIME GATE STILL OPEN

## Scope
Strengthen the reusable-workflow contract test so the trusted caller-context guard must be the actual `jobs.engineer.if` expression in each of the three Gemini child workflows, rather than merely appearing somewhere in the file.

## Change
- Added `test_trusted_caller_guard_is_the_engineer_job_condition` to `tests/test_gemini_reusable_workflow_contract.py`.
- The test parses each child workflow with YAML BaseLoader and asserts the actual `engineer.if` equals both conditions: `github.event_name == 'workflow_dispatch'` and the exact trusted controller ref `VlDMlNSh/mediahub-os/.github/workflows/gemini-batch-dispatch-controller.yml@refs/heads/main`.
- This closes a static-test blind spot where a guard string could exist in a comment or unrelated YAML field while the executable job condition drifted.

## Evidence
- PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421), head `d8d8997bbfc48d20b08c9d4e6e0a5aecca4411be`, base `main` `80be45a70732b1d568164571d4273a6397792c3b`; remains Draft/open.
- Changed test blob SHA: `33149b9265f6dd458a7b3460cf7caf6277a981b3`.
- [Astra Cloud Runtime Validation #39417784502](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39417784502): SUCCESS on exact head.
- [Astra Verify #39417784544](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39417784544): SUCCESS on exact head; job steps for actionlint, compile, reusable-workflow contract tests, cloud admission tests, and signed-command smoke test all succeeded.
- Official GHCR [v0.27.0 Linux amd64 version record](https://github.com/orgs/github/packages/container/github-mcp-server/630595547?tag=v0.27.0) confirms the MCP image digest pinned in all three children: `sha256:cbca61d547beec9b819b26bbfe6ac66ba6b373f1d6b64e8291e346bf524633e2`.

## Limits and remaining gates
- This is static contract evidence, not a runtime proof of GitHub's reusable-workflow caller context.
- The connected GitHub action surface provides no workflow-dispatch operation, and no agent-dispatch attempt was made. The controlled negative caller-context runtime test remains open.
- No independent review is recorded; PR #421 is still Draft.
- Branch protection API returned 403 (integration lacks permission), so branch protection requirements remain unverified rather than assumed.
- No Gemini agent was launched, no provider secret was accessed, and no merge, deployment, or Contour A qualification occurred.

## Next
1. Obtain genuine independent review and verify required branch protection through an authorized route.
2. Run a controller-owned negative test with `confirm=no` or a dedicated safe fixture, confirming all child jobs skip and no Gemini invocation occurs; separately verify the caller guard on the actual trusted controller path.
3. Only after those gates pass, run a bounded three-agent batch and retain controller run ID, child conclusions, artifacts, and provenance.

## Navigation
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 256 controller revalidation](MEDIAHUB-CONTROLLER-REVALIDATION-WAVE-256-2026-10-20.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
