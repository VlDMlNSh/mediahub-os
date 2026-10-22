# Wave 394 continuation checkpoint — 2026-10-22

This dated addendum supplements, and does not replace, the canonical checkpoint.

- Detailed report: [Wave 394 Gemini controller gate reconciliation](MEDIAHUB-NEXT-GEMINI-CONTROLLER-GATE-RECONCILIATION-WAVE-394-2026-10-22.md).
- Map addendum: [Wave 394](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-394-2026-10-22.md).
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Main SHA: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`; canonical docs SHA at inspection: `343eeb760b1d49df8371db674e51ffc5942701a9`.
- Current controller blob `28874450099e70b0f9d276600e6452c1b8e1b1a6` uses GitHub REST workflow dispatch for the three children; child workflows still expose `workflow_dispatch`. This conflicts with the approved Option B workflow_call-only governance target.
- PR #441 open at `9f40b90c3106662cfcc337c48f29e4794fa713dc`, base `ad99e1bebfeda0da799da94dd83a8f2e50a9acd0`, non-mergeable; formal reviews empty and exact-head CI/status not returned. Treat as NOT VERIFIED.
- Gemini Agents 1–3 NOT RUN; no secret reads; no inference; no remote host commands. Contour A NOT ACCEPTED.
- Next: implement a narrow correction in a code PR; enforce controller-only `workflow_call`, remove child `workflow_dispatch`, preserve least privilege and HMAC/issuer gates, add positive/negative tests, require independent review and exact-head CI before any live dispatch.

