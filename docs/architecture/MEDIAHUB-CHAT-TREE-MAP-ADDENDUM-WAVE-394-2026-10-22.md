# Wave 394 — Gemini controller governance reconciliation

Date: 2026-10-22. Full evidence: [Wave 394 report](../checkpoints/MEDIAHUB-NEXT-GEMINI-CONTROLLER-GATE-RECONCILIATION-WAVE-394-2026-10-22.md). Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).

- Main HEAD at inspection: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`; controller blob `28874450099e70b0f9d276600e6452c1b8e1b1a6`.
- PR #421 merged and PR #437 merged, but current main still exposes `workflow_dispatch` on all three child workflows. Controller source dispatches those child workflows via GitHub REST API. This does not satisfy owner-approved Option B's controller-only `workflow_call` contract.
- PR #441 remains open, non-mergeable, without formal review; its exact-head CI/status APIs are empty. Review/CI NOT VERIFIED.
- Controller dispatch NOT RUN; no child run IDs were created. Issue #301 remains open; Contour A NOT ACCEPTED.
- Next: reconcile current main with Option B in a focused implementation PR, then require independent review and exact-head CI before dispatch.

