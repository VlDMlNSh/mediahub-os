# MediaHub OS — Chat Continuation Context, Wave 378
Date: 2026-10-22. Status: context snapshot only; not a normative contract. Functional Baseline 2.0 and binding security/authority contracts remain authoritative.

## Canonical sources
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Functional Baseline 2.0: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md
- Governing Contour A issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Gemini controller: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml
- Related PRs: [#437](https://github.com/VlDMlNSh/mediahub-os/pull/437), [#441](https://github.com/VlDMlNSh/mediahub-os/pull/441), [#474](https://github.com/VlDMlNSh/mediahub-os/pull/474), [#485](https://github.com/VlDMlNSh/mediahub-os/pull/485), [#487](https://github.com/VlDMlNSh/mediahub-os/pull/487).

## Refs and status snapshot
At initial Wave 378 read: main HEAD `11d04d2f2687e9ba9215e4b67af2e450516960bb`; canonical docs branch `docs/mediahub-chat-tree-map-20261012` HEAD `937b6fa164d0e89e5e5781bf8c236e4fb862ad56`. Refresh every ref before further work; PR #487 head has since changed.
PR #487 is an open draft, unmerged, documentation-only, based on the canonical docs branch. Latest read found 8 changed files: map, Bootstrap, roadmap, checkpoint, map addendum, two architecture records, and report. Its exact-head CI and independent review were NOT VERIFIED (empty status/review results). Branch protection could not be read (HTTP 403), therefore NOT VERIFIED. Do not infer merge from a populated merge_commit_sha alone; re-fetch PR and refs.
PR #485 is another overlapping open draft for user-owned compute/context. Reconcile the two before merge. Two overlapping architecture records exist in #487:
- docs/architecture/MEDIAHUB-OWNER-ARCHITECTURE-DECISIONS-AND-TARGET-DESIGN-2026-10-22.md
- docs/architecture/MEDIAHUB-OWNER-ARCHITECTURE-DECISIONS-WAVE-378-2026-10-22.md
Select one canonical detailed record; retain the other only with a distinct documented purpose.

## Architecture decisions (proposed, not implementation)
- Contour A = GitHub-centered engineering fabric. Contour B = user/media compute and stays blocked until Contour A is deployed and independently accepted.
- Authority separation: owner approvals; Jarvis intake/simple permitted routing; ASTRA GOLD A0 decomposition/orchestration; GitHub Supervisor/controller engineering control plane; model workers untrusted; MediaHub Product State Authority sole canonical product-state mutation authority.
- Separate GitHub engineering queue and local media queue; shared identifiers/protocol do not imply mirrored mutable state.
- Preserve statuses PLANNED, AUTHORIZED, DISPATCHED, RUNNING, EXECUTED, VERIFIED, QUALIFIED, ACCEPTED, BLOCKED, NOT RUN, FAILED, CANCELLED, NOT VERIFIED.
- Strict local-first privacy. D0 public technical, D1 internal technical, D2 user media/private, D3 secrets/credentials/authority material. Unknown classification defaults deny. D2 stays local absent explicit task-specific egress authorization; D3 must not enter prompts, ordinary logs, agent workspaces or artifacts.
- Backups on approved owner nodes are encrypted; keys separated; integrity and restore drills required. Staged updates require provenance/compatibility gates, controlled activation and rollback. No automatic promotion.
- Recovery must check leases, prior result, idempotency and executor compatibility; quarantine ambiguous outcomes rather than blindly retry.
- Hardware notes (Mac mini 2018 coordination, Mac mini 2011 reportedly 16 GB Linux, possible future Ryzen 5 5600/RTX 3060 12 GB/32 GB RAM/1 TB NVMe, ~100k RUB) are assumptions, not verified/final.

## Contour A blockers and historical evidence
Issue #301 is controlling. Contour A remains NOT QUALIFIED / NOT ACCEPTED. CAF-Q-001…015 are documentary queue definitions, not a live scheduler.
Issue #301 includes historical Wave 81 evidence for PR #335 merged SHA `444fb34938c6785882070f34189b3f9ec7521f4d`: 3/3 Draft 2020-12 schema meta-validations, 3/3 positive fixtures, 13/13 invalid mutations rejected, 0 failures; artifact #12102957938, digest `sha256:633e1417aa41fc844b5d1c67c3ff2be417a98f72bcc6f055119023565d710e07`. This applies only to that exact SHA/test set. Compare current schema/fixture hashes before repeating tests.
Open gates include semantic authority/reference resolution, independent review, A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy, target manifest, controlled runtime execution and exact-head qualification.

## Agent restrictions
Gemini only via approved `.github/workflows/gemini-batch-dispatch-controller.yml`, and only after controller/security/governance gates pass. Never rename variables, create aliases, expose secret values, use alternate transports, or claim assignment without run evidence. Historical run 39817910784 on main SHA above was issue_comment/skipped, not a Gemini batch.
Claude/FCC/Ollama is separate and only on confirmed server 3 after exact SentinelX host ID, capabilities, allowlist and a qualified approved free route/no paid fallback are verified. Server 3 must not run/transport Gemini. Read current agent-browser skill before browser work.
No Gemini or Claude task was dispatched in this Wave 378 pass.

## Next pass
1. Refresh live main/docs branch/PR refs and Issue #301; read Bootstrap, map, checkpoint, roadmap, Baseline 2.0, controller and authority/privacy contracts.
2. Inspect all PR #487 changed files and links; reconcile the duplicate architecture records and overlap with #485.
3. Compare current schema/fixture SHAs to historical Wave 81 evidence; reuse evidence if identical, otherwise test only the delta on immutable SHA with tool/version and artifact digests.
4. Do not dispatch agents while mandatory gates remain open. Record missing evidence as NOT VERIFIED, not PASS.
5. After edits, reread each file, record commit/blob SHAs and exact-head CI/review; update dated report/checkpoint/map as needed. Do not merge or claim VERIFIED/QUALIFIED/ACCEPTED without evidence.
Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
