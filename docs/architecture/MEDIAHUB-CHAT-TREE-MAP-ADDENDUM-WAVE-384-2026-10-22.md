# MediaHub OS — chat tree map addendum, Wave 384

Date: 2026-10-22

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

Research report: [Open-source agent architecture component selection, Wave 384](../checkpoints/MEDIAHUB-OPEN-SOURCE-AGENT-COMPONENT-SELECTION-WAVE-384-2026-10-22.md).

- Initial candidates: LangGraph, CrewAI and Microsoft Agent Framework for mutually exclusive primary orchestration options; Temporal as a durable-workflow reference/managed-service option; promptfoo for CI evaluation; Langfuse for optional observability.
- Arize Phoenix's repository LICENSE is ELv2; do not treat it as permissively licensed OSS for reuse without legal review.
- GitHub Actions is an ephemeral execution layer, not by itself a transactional durable queue.
- No component was installed or copied. No framework was selected.
- Three topic-specific agent tasks are PLANNED only. The approved Gemini controller currently has fixed role prompts; custom research tasks require a reviewed controller contract change and all dispatch gates.
- Research branch is non-canonical and unaccepted pending PR review.
