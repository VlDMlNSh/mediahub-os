# MediaHub Chat Tree Map — Wave 493 addendum (2026-10-31)

- Report: [Wave 493 — Gemini runner efficiency and provider credential readiness](../checkpoints/MEDIAHUB-GEMINI-RUNNER-EFFICIENCY-API-READINESS-WAVE-493-2026-10-31.md).
- Verified controller and three child workflow source: each child has separate authorization and execution jobs on `ubuntu-latest`; the three workflows do not target the owner's 20 physical computers.
- Recommended next design: sequential Agent 1 implementation → Agent 2 exact-PR contract/test review → Agent 3 exact-PR security/provenance review. This reduces peak runner concurrency and fixes the current race where reviewers may start before Agent 1 has produced a PR; it does not necessarily reduce total billed runner minutes.
- A single-runner/three-session design is deferred pending workspace/session/credential isolation tests.
- Exact credential references recorded in Wave 493; secret/variable presence and scope remain NOT VERIFIED. No aliases, credential creation, provider calls or dispatch.
- Public-repository self-hosted runners are not selected for untrusted agent jobs; GitHub security guidance warns of persistent compromise risk. The 20 computers require a separate runner trust-boundary decision.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
