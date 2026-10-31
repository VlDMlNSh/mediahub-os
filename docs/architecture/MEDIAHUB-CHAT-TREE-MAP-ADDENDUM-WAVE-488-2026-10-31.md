# Wave 488 — GitHub-hosted runner target matrix

- [Wave 488 source-verified GitHub-hosted runner target matrix](../checkpoints/MEDIAHUB-GITHUB-HOSTED-RUNNER-TARGET-MATRIX-WAVE-488-2026-10-31.md)
- Establishes the current public-repository standard runner catalog, plan-dependent concurrency, ephemeral job lifecycle, dynamic egress, and the absence of a documented runner-to-runner bandwidth SLA.
- Separates GitHub-hosted ephemeral workers from existing self-hosted node contracts; recommends Ubuntu x64 as the current agent baseline, ARM64 as a qualification lane, and macOS M1 as a specialist Apple-Silicon lane.
- Decision: GO for independent parallel jobs and bounded artifact relay; NO-GO for production single-model tensor/pipeline sharding and persistent remote desktop on standard hosted runners.
- Status: candidate research only; no accepted target manifest, runtime benchmark, dispatch, qualification, deployment, or acceptance.
- Immutable documentation parent: `72a6725dbc7c38e37805e254377d293fcb141e7e`; source main snapshot: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301). Cloud-first priority proposal: [PR #595](https://github.com/VlDMlNSh/mediahub-os/pull/595).
