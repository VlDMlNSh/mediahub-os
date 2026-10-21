# MediaHub Chat Tree Map — Wave 312 Addendum

- Date: 2026-10-21
- Status: **PROVISIONAL WORKING-BRANCH INDEX / NOT CANONICAL UNTIL REVIEWED AND INTEGRATED**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Evidence report: [Wave 312 signed GitHub API controller repair](../checkpoints/MEDIAHUB-GEMINI-CONTROLLER-SIGNED-GITHUB-API-DISPATCH-REPAIR-WAVE-312-2026-10-21.md)
- Controller repair PR: https://github.com/VlDMlNSh/mediahub-os/pull/432
- Overlapping transport PR: https://github.com/VlDMlNSh/mediahub-os/pull/431

## Controller transport finding

PR #432 proposes a controller-only `MEDIAHUB_GITHUB_TOKEN` GitHub API dispatch route, shared immutable target SHA, explicit agent-mode confirmation, HMAC-signed bounded child inputs, pre-provider child signature validation, and fail-closed run correlation. Exact-head CI and the non-launching controller/caller-context probes passed for head `ea637eb55c87d44f0ce22730588e744c7470ee1d`. The controller's agent dispatch job was skipped during probe mode; no Gemini child was launched.

## Integration and authority boundary

- PR #432 remains OPEN/DRAFT/UNMERGED and has no formal submitted independent review.
- PR #431 overlaps the same controller/child paths and must be reconciled without discarding useful evidence.
- Repository secret availability, effective token permissions, repository/organization Actions policy, replay/partial-dispatch behavior, and independent security approval remain open.
- Gemini Agents 1–3: NOT RUN. Alamo Claude and browser lanes: NOT RUN because server-3 identity and approved non-paid route are not verified.
- Contour A remains NOT QUALIFIED / NOT ACCEPTED. No trusted agent-mode dispatch, provider/model call, merge, deployment, or acceptance occurred.

## Next step

Obtain a formal independent security review of the signed controller/child contract, verify effective governance and credential permissions without reading secret values, reconcile PR #431/#432, and only then consider a trusted no-secret positive-context probe. Do not merge or launch agent mode before those gates pass.

This addendum is a provisional index entry only. The canonical map itself is unchanged and remains authoritative at the URL above.
