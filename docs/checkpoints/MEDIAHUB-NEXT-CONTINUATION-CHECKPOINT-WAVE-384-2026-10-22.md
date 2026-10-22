# MediaHub OS — continuation checkpoint, Wave 384

Date: 2026-10-22

- Research report: [Open-source agent architecture component selection](MEDIAHUB-OPEN-SOURCE-AGENT-COMPONENT-SELECTION-WAVE-384-2026-10-22.md).
- Map addendum: [Wave 384](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-384-2026-10-22.md).
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md.
- Main base SHA used for research branch: 11d04d2f2687e9ba9215e4b67af2e450516960bb.
- Research branch: research/oss-agent-components-wave384-20261022. This branch is not canonical and has not been accepted.

## Findings

- Reuse mature components rather than building a multi-agent framework from scratch, but retain MediaHub's issuer, capability, signed dispatch, provider policy, Product State Authority, provenance and governance contracts.
- Primary candidates for a controlled comparison: LangGraph, CrewAI and Microsoft Agent Framework. Do not adopt several competing orchestration runtimes at once.
- Temporal is a strong durable-workflow reference but a full service requires persistent infrastructure and does not become GitHub-only merely by running in Actions.
- promptfoo is a candidate for secret-free CI evaluations; Langfuse is optional observability with MIT core and separately licensed EE paths; Arize Phoenix carries ELv2 and needs legal review before reuse.
- GitHub-hosted Actions can execute bounded supervisor jobs, but a durable transactional queue needs a qualified persistent-state/lease design. Issues/artifacts/caches alone are not a proven queue.
- No code from candidate repos was copied, no dependency installed, no framework selected, and no real agent was dispatched.

## Agent work status

- Agent 1 candidate integration research: PLANNED / NOT DISPATCHED.
- Agent 2 independent license and test-matrix verification: PLANNED / NOT DISPATCHED.
- Agent 3 security/provenance audit: PLANNED / NOT DISPATCHED.
- Reason: controller prompts are currently fixed generic role tasks; the proposed topic-specific tasks require a reviewed controller contract update. Current PR #483 exact-head CI after the package-parser fix and independent review are NOT VERIFIED. Do not trigger the controller until the applicable gates are proven.

## Related engineering state

- PR #483: https://github.com/VlDMlNSh/mediahub-os/pull/483; latest observed head 9d55150cc6ec5fdff14a6c6b798faf30601c8b22.
- Earlier exact-head Astra Verify run 39815854894 failed test_workflow_runs_only_installed_test_tools because pinned package specifiers were not normalized by the test helper. The helper was updated to strip version/extras when collecting pip targets; a fresh exact-head CI result is still required.
- Formal independent review of PR #483: NOT VERIFIED.
- Production GitHub-hosted durable supervisor, task-specific signed Gemini routing and local worker lease/result protocol: NOT IMPLEMENTED / NOT VERIFIED.
- Contour A: NOT QUALIFIED / NOT ACCEPTED.

## Next step

Verify the parser fix and exact-head CI on PR #483, then benchmark the three orchestration candidates using one deterministic non-secret task fixture. Only after the controller contract can safely accept task-specific signed assignments and mandatory gates pass should topic-specific tasks be dispatched through the approved controller.
