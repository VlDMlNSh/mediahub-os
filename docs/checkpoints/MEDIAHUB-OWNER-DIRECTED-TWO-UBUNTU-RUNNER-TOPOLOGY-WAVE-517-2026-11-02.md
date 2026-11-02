# Wave 517 — two-Ubuntu-runner owner direction and Bootstrap reconciliation proposal

Date: 2026-11-02  
Documentation base branch: `docs/mediahub-chat-tree-map-20261012`  
Immutable documentation base HEAD: `d9a289b9113f7567711b641a7017eb814d6c259d`

## Purpose

The canonical Bootstrap still instructed every eligible `/next` to run Claude Code only on a separate “Alamo/server 3”. That conflicts with two later owner directions: “Alamo/Allamo” meant the local Ollama runtime (not a separate host), and the target placement is two Ubuntu runners:
- Runner 1: Ollama, FCC, Claude Code and selected ECC guidance.
- Runner 2: the approved Gemini controller and all three Gemini agents co-located on one host per batch.

This proposal updates current instructions while preserving historical reports and their provenance.

## Proposed changes

1. Replace the stale “Alamo/server 3” executor binding in Bootstrap with the two-runner target topology.
2. Preserve all security requirements from historical Wave 272/273 contracts that are not host-location specific: non-paid/free route verification, no Anthropic API/paid routes, no paid proxies/fallbacks, strict provider allowlists, egress and fail-closed behavior.
3. Make Runner 2 co-location an explicit implementation requirement. The current controller still dispatches three child workflows to three independent `ubuntu-latest` runner allocations; it does not satisfy co-location.
4. Require separate container/workspace/credential boundaries for three Gemini agents. The controller GitHub API token and HMAC key must never be inherited by agent processes.
5. Require measured vCPU/RAM/disk and actual runner identity before concurrency admission. Distinguish persistent self-hosted Ubuntu machines from ephemeral `ubuntu-latest` VMs.
6. State explicitly that this target does not authorize physical-server procurement or supersede Contour A cloud-pool priority.

## Current source evidence

- PR #623 Runner 1 candidate HEAD: `4ded07da6c262aa47fdca19289e5479a1580318d`.
- Runner 1 workflow blob: `12b684bbd3d475d64cac7e37bbaf64c65ce40529`.
- Runner 1 test blob: `a3cf0c8fffbe5fd049144619d388354b4704b1d8`.
- Exact-head CI: 8/8 terminal SUCCESS on the candidate HEAD. This was a PR contract run; all install/model/FCC/Claude live steps were SKIPPED.
- Main controller blob: `0a1246f6755020faf8b7e48d07bfff790bbaece3`; each of the three child workflows currently uses its own `ubuntu-latest` runner.
- Active SentinelX host: `host_5f7264034bdf0b51`, macOS ARM64, not Ubuntu. Desktop Commander sees `mh-dev-01` and `mh-dev-02` offline.
- Independent formal review of PR #623: 0; inline threads: 0.
- Gemini Agent 1/2/3: NOT RUN; controller dispatch gates remain open.

## Files updated in this documentation proposal

- `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` — current execution instructions.
- `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` — new Wave 517 index entry, without rewriting historical wave sections.
- `docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md` — append-only continuation record.
- `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md` — target topology and implementation/gate sequence.
- New addendum: `docs/architecture/MEDIAHUB-TWO-UBUNTU-RUNNER-TOPOLOGY-OWNER-DIRECTION-WAVE-517-2026-11-02.md`.

## Non-goals

No workflows/controllers were changed. No runner was provisioned. No credentials were read. No Gemini or Claude invocation, model/provider inference, merge, deployment, qualification or acceptance was performed. PR #623 has since merged into main at merge commit `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0` (source candidate HEAD `4ded07da6c262aa47fdca19289e5479a1580318d`). Its PR-event contract CI passed, but live install/model/FCC/Claude steps were skipped; Runner 1 runtime remains NOT RUN. This documentation PR does not qualify or accept that runtime.

## Required next implementation

Implement a reviewed same-host Runner 2 controller/agent execution design with isolated sandboxes, independent credentials, resource admission and behavioral secret-boundary tests. Separately qualify the Runner 1 Ollama/FCC/Claude route. Do not dispatch Gemini until independent security review, metadata-only secret/variable scope verification, trusted-main no-secret probe and all governance gates pass.

## Status

**DRAFT / PROPOSED / NOT ACCEPTED.** Canonical documentation branch remains unchanged until this PR is reviewed and merged.

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #623 Runner 1 code candidate](https://github.com/VlDMlNSh/mediahub-os/pull/623)
