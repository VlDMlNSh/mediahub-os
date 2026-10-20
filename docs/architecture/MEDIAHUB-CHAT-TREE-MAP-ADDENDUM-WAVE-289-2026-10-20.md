# Canonical map addendum — Wave 289 (2026-10-20)

## Correction to Wave 288 permission-ceiling finding

- **Corrective report:** [Wave 289 — reusable-workflow permission-ceiling correction](../checkpoints/MEDIAHUB-GEMINI-REUSABLE-WORKFLOW-PERMISSION-CEILING-CORRECTION-WAVE-289-2026-10-20.md).
- [Canonical project map](MEDIAHUB-CHAT-TREE-MAP.md); [continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md); [Master Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md); [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- **Correction:** Wave 288's claim that workflow-level `permissions: {}` blocks the reusable child writes was invalid because the controller calling jobs themselves explicitly declare permissions. Job-level permissions govern those calling jobs and are the relevant ceiling passed to the reusable workflow. Do not use the Wave 288 claim as a proven blocker.
- This does not prove the transport is operational. PR #421 remains OPEN/DRAFT/UNMERGED with no independent submitted review; trusted positive caller context and the earlier non-launching probe failure remain unresolved. PR #426 remains separate and unmerged.
- **Next:** verify each caller-job/child-job permission pair and repository/org policy against exact-head run evidence; investigate the probe failure without assuming a permission cause. No dispatch, provider call, merge, deployment, qualification, or acceptance.
