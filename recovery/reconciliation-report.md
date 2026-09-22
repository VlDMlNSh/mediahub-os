# MediaHub Forensic Reconciliation Report

Date: 2026-09-05
Status: IN PROGRESS — not an acceptance record

## Executive result

The accepted master passport establishes a substantially complete product-level functional baseline. The forensic pass confirms that the architecture must be reconstructed around capabilities and contracts rather than around historical P0-P8 boundaries or chat ownership.

## Reconciled principles

1. Functional requirements are primary.
2. Home Assistant remains internal and hidden behind MediaHub.
3. Surveillance recording is a native MediaHub capability; separate NVR is not mandatory.
4. Surveillance storage and Personal Media Library storage remain distinct logical domains.
5. Local-first/offline-first is a runtime property, not a cloud-hosted approximation.
6. Local Cluster and Cloud Development are separate trust/control contours.
7. Security, privacy, identity, trust and authorization are cross-cutting.
8. Product variants are capability-specific, not merely packaging variants.
9. Professional Engineering is a first-class product contour.
10. Deferred technical choices remain explicit open items.

## Historical recovery finding

The GitHub source inventory identifies a materially broader historical MH-18 media architecture than the current mainline. It must be reconciled into the master capability model rather than discarded. Because the full text of all MH-01…MH-23 chats is not exposed as one machine-readable corpus in this runtime, exhaustive historical reconciliation cannot yet be claimed.

## Duplicate policy

Canonical capabilities are unique by product meaning. A capability may have multiple supporting domains, contracts and UI surfaces without creating duplicate function records.

## Ownership policy

Each canonical capability receives one owner. Supporting domains do not become co-owners of authority. State authority, command authority and security authority are explicit boundaries.

## Semantic gaps still open

- Exact State Authority semantics and mutation model.
- Exact Home Assistant version/fork/adapter boundary.
- Vendor/protocol support matrix and device families.
- KINCONY firmware authenticity and safe flashing workflow.
- Surveillance transport, recording modes, retention and recovery details.
- Storage pool/filesystem/rebalance details.
- Network AP/mesh/controller replacement details.
- Local cluster coordination/scheduling/failover.
- Cloud compute contribution/privacy/metering.
- Mobile transport and iOS/Android platform limits.
- Gaming transport/capture/input topology.
- HomeKit/Yandex/Loxone technical bridge mechanisms.
- Exact security threat model, cryptographic algorithms and key lifecycle.

## Acceptance gate

MASTER ARCHITECTURE remains DRAFT until the historical corpus gap is closed to the required level, all material conflicts are reconciled or explicitly accepted as deferred, and the user performs acceptance.

## P0.6 PR #80 reconciliation — 2026-09-21

Status: VERIFIED_LOCAL_RECONCILIATION / NO INTEGRATION

Scope: reconcile PR #80 remote/local evidence without push, merge, cherry-pick, ready-state change, release action, or production authorization.

Remote Git evidence observed read-only from `origin`: `refs/pull/80/head` = `40f700981c6dceb4bfa47e69c43f539f15db686d`; `refs/pull/80/merge` = `e6caca15405eabc7102b17b5c12f6c407c87401b`.

Local control point at compilation: `HEAD` = `ff328899626e912a18d64553a5902010a6725252`; `HEAD^{{tree}}` = `39bbedc5067aa0a9064b06ef2ad6bc76585560db`; R4 = `471f709f5633feab7aeb62dd3ea52effad6d2bc4`; R4 ancestry = PASS.

The remote PR head was observed as a ref but was not imported into this worktree. No merge, cherry-pick, push, release, production authorization, credential access, or State Authority mutation was performed.

Acceptance: exact remote/local SHAs are recorded, lineage remains intact, and the evidence explicitly preserves the non-integration boundary.

## P0.1 current control-point reconciliation — 2026-09-21

Status: VERIFIED_LOCAL_RECONCILIATION

Repository control point at task compilation: branch `engineering/mh21-sandbox-lifecycle-20260910`; HEAD `46d87676bf5381732f5e8410c0f124567490d4d5`; tree `966929c70ffe983d43c01efb47e8a78b55aa3336`.

R4: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`; R4 ancestry: PASS. Worktree: clean at task compilation.

Active execution infrastructure observed: one autonomous OS loop owner, one watchdog owner, and one hybrid orchestrator process; the authoritative worktree remains `/home/mediahub/dev/mediahub-os-autonomous`. Parallel worktrees remain separately owned and were not modified by this task.

Boundary: this record is reconciliation evidence only. No R4 mutation, history rewrite, destructive cleanup, user-work overwrite, merge, release, or production authorization is performed.

## P2.6 Home Assistant source-of-truth verification — 2026-09-21

Status: VERIFIED_LOCAL_SUBSCOPE / P2.6 NOT CLOSED

Scope: verify only the existing normative functional-baseline statements and control gates. No Home Assistant runtime access, State Authority mutation, provider execution, or production operation is part of this task.

Acceptance evidence: `ops/verify_functional_baseline.sh` is the repository-native deterministic gate. It requires the normative functional baseline, governance and invariant registry to identify Home Assistant Core, MediaHub State Authority, the canonical AI escalation path, locked release state and unauthorized production state; it also requires exact R4 ancestry and R4 tree identity.

Architectural boundary: this evidence confirms the repository's declared source-of-truth boundary. It does not qualify an operational Home Assistant adapter, runtime integration, command path, or production deployment.

## P0.2 master-queue ownership/provenance reconciliation — 2026-09-22

Status: VERIFIED_LOCAL_SUBSCOPE / P0.2 NOT CLOSED

Scope: reconcile the existing persisted master queue with the repository's existing machine-readable dispatch and governance registries. This record is a projection only and does not create authority or replace canonical registries.

```yaml
p02_projection_version: 1
source_head: ab52504e3e3e2f85cd22b064df9d392a01175a0b
source_tree: 79ddd9622167e1341a39982ad375f50c7412aa03
queue_sha256: f4e069fe5b68fe9b67315e8899d091562b1f8a1581d2cbcbb44533a82efdc9c9
dispatch_sha256: 7b5a8a7d4656b9c928648ef774263210634983c4fc09f24939949c75dfecdfc6
projection_only: true
authority_grant: false
r4_mutation: false
existing_architecture_sources:
  - specification/capability-registry.yaml
  - specification/contract-registry.yaml
  - specification/dependency-graph.yaml
  - specification/invariant-registry.yaml
  - docs/ops/control-plane/MH01-23-QUEUE-DISPATCH-2026-09-19.yaml
stale_dispatch_references:
  - mh-1: P0.6
  - mh-2: P2.1
  - mh-3: P0.4
  - mh-4: P2.4
  - mh-5: P0.3
  - mh-6: P1.3
  - mh-7: P1.3
  - mh-8: P1.5
  - mh-9: P1.6
  - mh-10: P1.6
  - mh-11: P1.7
  - mh-12: P9.1
  - mh-13: P1.2
  - mh-14: P9.4
  - mh-15: P0.4
  - mh-16: P10.1
  - mh-17: P3.1
  - mh-18: P4.1
  - mh-19: P5.3
  - mh-20: P6.1
  - mh-21: P8.1
  - mh-22: P11.1
  - mh-23: P0.1
worktree_branch_inventory:
  - engineering/mh21-sandbox-lifecycle-20260910
  - parallel/cluster-failover
  - parallel/cluster-health
  - parallel/cluster-lifecycle
  - parallel/cluster-membership
  - parallel/core-egress
  - parallel/core-model
  - parallel/core-provider
  - parallel/core-resilience
  - parallel/core-state
  - engineering/mh01-pr80-reconciliation-20260918
  - engineering/mh10-cloud-adapter-readiness-20260918
  - engineering/mh11-codex-readiness-20260918
  - engineering/mh12-security-redteam-20260918
  - engineering/mh14-p94-sandbox-authority-20260919
  - engineering/mh19-p5.3-mobile-api-compatibility-20260919
  - engineering/mh04-execution-admission-redteam-20260918
  - engineering/mh05-recovery-audit-20260918
  - engineering/mh07-ai-registry-20260919
  - engineering/mh08-plugin-extension-continuation-20260919
  - parallel/native-headers
  - parallel/native-proposal
  - parallel/native-recovery
  - parallel/native-target
  - parallel/native-tests
  - parallel/native-tests2
  - autonomous/claude-os-build
  - controller-hardening/evidence-encoders-20260921
  - controller-hardening/p02-queue-provenance-20260922
  - controller-hardening/p052-terminal-provenance-20260921
  - controller-hardening/p07-readiness-20260921
  - controller-hardening/p12-admission-types-20260921
  - controller-hardening/p12-fallback-field-20260921
  - controller-hardening/p12-fallback-fix-20260921
  - controller-hardening/p27-authority-verification-20260921
  - controller-hardening/queue-compiler-20260921
  - controller-hardening/queue-compiler-p01-20260921
  - controller-hardening/queue-compiler-p06-20260921
  - controller-hardening/queue-compiler-p26-20260921
  - recovery/p05-delivery-provenance-20260921
  - evidence/mh-22-pr80-reconciliation
``

Acceptance boundary: the projection is bound to the exact current-tree HEAD/tree and queue/dispatch hashes captured at compilation, inventories observed worktree branches, and explicitly reports dispatch references that do not correspond to observed live worktree branches.

Governance boundary: no R4 mutation, history rewrite, merge, parallel-lane modification, credential access, production authorization, or State Authority mutation is performed.
