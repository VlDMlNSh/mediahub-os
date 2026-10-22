# Canonical map addendum — Claude-FCC-Ollama historical evidence (Wave 350, 2026-10-22)

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md). This addendum records prior evidence for reuse; it does not grant current runtime qualification.

## Historical evidence to reuse

- Commit [5b6c04587b73092859b26a0d058ab9d2a0d4094b](https://github.com/VlDMlNSh/mediahub-os/commit/5b6c04587b73092859b26a0d058ab9d2a0d4094b) implemented a bounded native Claude Code → Ollama Anthropic-compatible API check and structured marker evidence.
- The [MH-25 topology checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mh-25-two-node-autonomous-topology-1.0.md) records local Claude/FCC inference **PASS at proxy/API level**, but the headless Claude marker remains **BLOCKED/PENDING**.
- The [dual local executor checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mh-25-dual-local-executor-qualification-checkpoint-2026-10-02.md) records prior FCC proxy/API responsiveness, while stating that a 23-wave workflow PASS was not available from the then-used Actions endpoint.
- Therefore, reuse the old implementation and limited PASS as historical baseline; do not restart from zero, but do not treat it as fresh exact-SHA qualification. The exact successful historical Actions run/artifact IDs have not yet been recovered in this pass.
- Current SentinelX read-only attempt returned `agent_disconnected/duplicate_session`. No local model was invoked and no host configuration changed.

## Current cloud-agent gates

- `main` HEAD: `909d2ba6caeb2a84508978925126a074f3a934da`.
- PR [#443](https://github.com/VlDMlNSh/mediahub-os/pull/443) merged. Tested PR-head contract validation [39748357460](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39748357460), no-secret controller probe [39748357615](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39748357615), Astra Verify [39748357515](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39748357515) and Cloud Runtime Validation [39748357531](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39748357531) all succeeded. The PR probe did not launch Gemini children.
- PR [#437](https://github.com/VlDMlNSh/mediahub-os/pull/437) remains open at exact head `e7e99c2fe5f090df3a731b0a1a7f3fcb5335bd14`; status/run results are empty and formal reviews are zero, so CI/review remain NOT VERIFIED.
- Gemini Agents 1–3 are NOT RUN in this pass; no controller/child run IDs or artifacts. Physical servers are not used for Gemini transport.

Report: [Wave 350 historical Claude/Ollama evidence reconciliation](../checkpoints/MEDIAHUB-NEXT-HISTORICAL-CLAUDE-OLLAMA-EVIDENCE-RECONCILIATION-WAVE-350-2026-10-22.md).
