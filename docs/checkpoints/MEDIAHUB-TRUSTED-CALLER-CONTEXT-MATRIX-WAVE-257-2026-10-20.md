# MediaHub OS Contour A — trusted caller-context matrix (Wave 257)

Date: 2026-10-20
Status: CONTRACT TEST EXPANDED / EXACT-HEAD CI GREEN / RUNTIME GATE STILL OPEN

## Bounded change
Expanded `tests/test_gemini_reusable_workflow_contract.py` with a table-driven trusted-controller context matrix. The positive case accepts only the exact approved controller ref on `workflow_dispatch`; negative cases reject:
- `workflow_call` and `push` events,
- a feature-branch controller ref,
- a different repository owner/name,
- a different workflow filename,
- a tag ref in place of `refs/heads/main`.

The existing structural contract checks still require the same exact trusted-controller guard in each child workflow, explicit per-agent secrets, immutable external action SHAs, and an OCI digest rather than the mutable MCP image tag.

## Evidence
- PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421) remains Draft/open; current head `bba29a062ff1d62177b855d7434e36d7be6698ba`, base `main` `80be45a70732b1d568164571d4273a6397792c3b).
- Test file blob SHA after read-back: `27ab484c8e659c798d449a1c302ec5fd48b2fca7`.
- [Astra Verify #39417467135](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39417467135): SUCCESS on the exact current head. Job steps for workflow lint, compile, and Gemini reusable-workflow contract tests all completed successfully.
- [Astra Cloud Runtime Validation #39417467160](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39417467160): SUCCESS on the exact current head.
- Previous Wave 256 evidence remains applicable to the unchanged image/action pins; see [Wave 256 report](MEDIAHUB-CLOUD-AGENT-MCP-IMAGE-DIGEST-WAVE-256-2026-10-20.md).

## Limitations and gates
The new matrix is a local contract/unit test, not a live GitHub Actions caller-context test. The available connected GitHub tool surface does not expose a workflow-dispatch operation, so no negative runtime invocation was performed. The test cannot by itself prove the real GitHub context values seen inside reusable workflows.

Independent review by another identity remains absent. PR #421 is still Draft and unmerged. Branch protection/governance integration remains open. No Gemini agent was launched, no secrets were accessed, and no merge/deployment/qualification occurred.

## Next step
Obtain independent review of the caller-context and secret boundary; arrange a controlled negative runtime test through the approved GitHub-hosted controller once an authorized dispatch surface is available; then verify branch protection and integrate only through the approved governance path.

## Navigation
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 256 controller revalidation](MEDIAHUB-CONTROLLER-REVALIDATION-WAVE-256-2026-10-20.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
