# Provisional map addendum — Wave 307: three-agent /next orchestration

Date: 2026-10-21. This addendum is on the unmerged working branch and is not part of the canonical map.

- Report: [Wave 307 — per-/next three-Gemini-agent orchestration contract](../checkpoints/MEDIAHUB-NEXT-THREE-GEMINI-AGENT-ORCHESTRATION-CONTRACT-WAVE-307-2026-10-21.md).
- Canonical Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md (blob SHA e21423ac619fdc9ef4381cca40b0e3675277c42c). Sections 1A–1C already define per-/next agent use and controller-only launch constraints.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md. The canonical map was not modified.
- Task matrix: Agent 1 implementation/research proposal; Agent 2 independent contract/test verification; Agent 3 security/governance review. All work from the same immutable target SHA with separate scopes, fail-closed evidence, and lead-session reconciliation.
- Live dispatch remains BLOCKED pending PR #421 controller-only workflow_call integration and all required independent review, exact-head CI, caller guard/secret-boundary, safe negative-context probe, and runtime/authority gates. The documentary CAF-Q queue is not a live scheduler.
- Do not report any agent as launched unless controller and all three child run/job IDs and terminal results are observed.

Canonical instruction changes do not automatically update ChatGPT Project Instructions; if needed, the project-level rule should be a short pointer to Bootstrap §1A and this Wave 307 matrix.