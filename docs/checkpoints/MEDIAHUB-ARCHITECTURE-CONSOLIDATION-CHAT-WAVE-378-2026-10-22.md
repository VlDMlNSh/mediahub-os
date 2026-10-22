# Wave 378 — Owner architecture decisions consolidated from chat

- Date: 2026-10-22
- Status: **DOCUMENTATION PROPOSED / IMPLEMENTATION NOT VERIFIED / NOT ACCEPTED**
- Canonical documentation branch at start: `docs/mediahub-chat-tree-map-20261012` @ `937b6fa164d0e89e5e5781bf8c236e4fb862ad56`
- Main HEAD at start: `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- Functional Baseline 2.0 blob SHA read-back: `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`
- Main controller blob SHA read-back: `28874450099e70b0f9d276600e6452c1b8e1b1a6`

## Work performed

Consolidated architecture decisions from the owner conversation into a design record and navigation addendum. Documentation only; no runtime, workflow or secret changed.

- Primary record: [Owner Architecture Decisions and Consolidated Target Design](../architecture/MEDIAHUB-OWNER-ARCHITECTURE-DECISIONS-AND-TARGET-DESIGN-2026-10-22.md).
- Map addendum: [Wave 378 architecture map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-ARCHITECTURE-WAVE-378-2026-10-22.md).

## Owner-confirmed decisions

1. Strict local-first privacy: user media and detailed local logs remain on own nodes; only explicitly authorized data and necessary filtered engineering evidence may leave.
2. Encrypted backups on user-owned nodes; keys separated from stored backups; integrity verification and periodic restore tests.
3. Staged updates with automatic provenance/compatibility checks, mandatory gates, controlled activation and rollback.

## Consolidated design scope

- Responsibility separation: Jarvis, ASTRA GOLD A0, GitHub Supervisor and MediaHub Product State Authority.
- Contour A engineering fabric versus Contour B user/media compute.
- Task envelopes, issuer/capability, immutable target references, lease/cancellation, bounded retry and idempotency.
- Engineering GitHub queue versus local media queue; hybrid observability with local detailed telemetry.
- Model catalog/placement, user-node admission, resource priorities and protective modes.
- Backup/restore and staged update contracts, explicit status vocabulary and acceptance gates.

## Source reconciliation at authoring time

- Main HEAD: `11d04d2f2687e9ba9215e4b67af2e450516960bb`.
- Canonical documentation branch HEAD: `937b6fa164d0e89e5e5781bf8c236e4fb862ad56`.
- PR #437 is merged. PR #474 is open/unmerged. PR #485 is open draft/unmerged and overlaps on user-owned compute; reconcile rather than duplicate or treat as accepted.
- PR #441 is open/unmerged and fetched response reported mergeability false.
- Combined-status endpoints returned empty status lists for PR #474 head `cf708ef988fcbe408581b7e61000025f6f765925` and PR #485 head `d0806eb52c66d230f89cb6cb615ce09d665bc4fc`; these are **NOT VERIFIED**, not PASS.
- Branch-protection read returned HTTP 403 (integration permission unavailable); effective protection is **NOT VERIFIED**.
- The canonical map blob `ba5731256321251b6a92b35d51f5bd0f2c1d4e86` was fetched by blob SHA (1,175,180 characters) so the map index can be preserved rather than replaced with a partial copy.
- Functional Baseline 2.0 remains authoritative; this proposal does not amend or supersede it.

## Scope and negative evidence

- No Gemini controller dispatch or child runs.
- No secrets or secret values accessed.
- No SentinelX host commands, local Claude task, browser task, deployment or production operation.
- No runtime tests, restore tests, benchmarks or model qualification.
- No merge, rollout or architecture acceptance.

## Result and next step

Review this proposal against Baseline 2.0, binding A0 issuer/task contracts, Product State Authority and PR #485 before treating details as binding. Exact-head CI and independent review must be checked after PR creation; absent status is NOT VERIFIED.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md).
