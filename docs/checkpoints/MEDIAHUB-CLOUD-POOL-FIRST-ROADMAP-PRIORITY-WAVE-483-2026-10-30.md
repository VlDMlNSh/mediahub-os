# Wave 483 — Cloud Agent Pool First roadmap priority amendment (2026-10-30)

## Decision

Owner direction received: prioritize design, implementation, qualification, production deployment and independent acceptance of the Contour A GitHub-hosted cloud agent pool. Defer server hardware until the cloud pool is successfully deployed and independently accepted.

## Work performed

- Refreshed Issue #301 and relevant PR metadata (#594, #593, #592, #591, #590, #441, #437).
- Re-read the current repository's `.agents/skills/mediahub-next/SKILL.md` and `GEMINI.md` governance instructions.
- Confirmed Issue #301 remains OPEN and its ordered gates remain A0/R-06, target manifest, schema validation/review, Gemini hardening, read-only worker and controlled dispatch.
- Created a dedicated roadmap-priority amendment and map/checkpoint references on an isolated documentation branch.
- Explicitly sequenced P0 cloud pool, P1 cloud expansion, P2 server hardware/local compute, P3 Contour B.
- Kept all Issue #301 authority/security gates intact; no dispatch, provider call, credential access, host task, infrastructure mutation, merge or deployment.

## Important source retrieval limitation

The path `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md` returned GitHub Contents API 404 on both `main` and `docs/mediahub-chat-tree-map-20261012`. Search did not establish an alternate authoritative roadmap path. Therefore this pass does **not** claim that the original roadmap file was edited. Instead, it creates a clearly labeled priority amendment and links it from the canonical map/checkpoint. The authoritative legacy roadmap path/blob must be recovered and reconciled in a later pass.

## Immutable base / working branch

- Main SHA observed: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Canonical map blob: `75f62685459ec99ebf8be478f4e9096cdb842b1d` (Contents API returned empty; exact blob retrieval succeeded).
- Wave 482 checkpoint blob before this pass: `ed167fcada77d75c84bc7bfb3538a0b76061f8d0`.
- Working branch: `docs/wave483-cloud-pool-first-roadmap-20261030`.
- No runtime files changed.

## Priority sequence

1. **P0 — Cloud Agent Pool / Contour A:** close A0 issuer/ingress/lease/cancel/recovery and R-06; accept target manifest; validate schemas; independent review; harden GitHub-hosted Gemini workflows; implement the smallest read-only worker; qualify free routes and renewable quotas; controlled controller dispatch; operational soak; deploy and independently accept.
2. **P1 — Cloud expansion:** additional agents/providers/parallelism only after P0 acceptance and with all gates.
3. **P2 — Server hardware/local compute:** procurement/provisioning and local executor integration only after P0 deployment and independent acceptance.
4. **P3 — Contour B:** remains gated by Contour A deployment and independent acceptance.

## Current execution state

- Issue #301: OPEN; its gates remain controlling.
- PR #594: OPEN/DRAFT/UNMERGED; issuer provenance source gap documented, no runtime fix.
- PR #593/#592/#591/#590: OPEN/DRAFT/UNMERGED at last refresh; their CI/reviews remain unverified as previously recorded.
- Gemini controller: NOT RUN.
- Claude Code: NOT RUN.
- SentinelX: zero connected hosts; Voktors-Mini.Dlink offline; mh-dev-01 and mh-dev-02 disabled.
- Cloud pool: not deployed, not qualified, not accepted.
- Server hardware: DEFERRED by this priority amendment.
- No provider credentials/API calls, no secrets reads, no tests or runtime dispatch in this pass.

## Verification and status

This pass is a **roadmap design/documentation update**, not implementation or operationalization. File read-back and blob SHA verification, exact-head CI and PR status are recorded in the closeout after writes. The legacy roadmap artifact itself remains NOT VERIFIED because the expected path returned 404.

## Next step

Wave 484: recover the authoritative master roadmap path/blob, reconcile this amendment into the canonical master roadmap without losing prior IDs/content, then resume Issue #301's first open A0/R-06 gate. Do not procure server hardware until Contour A cloud pool is deployed and independently accepted.

## Links

- [Roadmap priority amendment](MEDIAHUB-MASTER-ROADMAP-PRIORITY-AMENDMENT-CLOUD-POOL-FIRST-WAVE-483-2026-10-30.md)
- [Map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-483-2026-10-30.md)
- [Canonical map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
