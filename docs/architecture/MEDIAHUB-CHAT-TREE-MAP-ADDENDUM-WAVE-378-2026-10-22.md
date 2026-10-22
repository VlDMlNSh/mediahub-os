# MediaHub Chat Tree Map — Wave 378 Addendum

- Date: 2026-10-22
- Status: **PROPOSED DOCUMENTATION ADDENDUM / NOT CANONICAL UNTIL MERGED**
- Primary report: [Distributed Compute Architecture Decisions — Wave 378](../checkpoints/MEDIAHUB-DISTRIBUTED-COMPUTE-ARCHITECTURE-DECISIONS-WAVE-378-2026-10-22.md)
- Canonical navigation map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Related control-plane tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Related pending owner-directed context record: [PR #485](https://github.com/VlDMlNSh/mediahub-os/pull/485)

## Architecture topics covered

This addendum indexes the owner-selected architecture decisions for model catalog/artifact placement, approved cloud API execution, separated GitHub engineering and local media queues, hybrid networking, adaptive resource scheduling, lease/result/idempotency/compatibility-based recovery, and hybrid observability.

## Decision and acceptance boundary

- The linked report records owner decisions and labels proposed defaults separately.
- It does not modify Functional Baseline 2.0, authority contracts or governance gates.
- It does not authorize Gemini dispatch, paid fallback, external media transfer, product-state mutation, merge, deployment or server configuration changes.
- Runtime implementation and qualification remain NOT RUN / NOT VERIFIED / NOT QUALIFIED.
- This addendum is not part of the canonical map until its documentation PR is reviewed, required checks are verified and the change is merged.

## Next bounded architecture passes

1. Finalize privacy, telemetry redaction, retention and evidence-publication policy.
2. Define node-loss recovery, backup/restore, model update/rollback and disconnected-operation semantics.
3. Consolidate decisions into a conflict-checked architecture and acceptance matrix.


## Consolidated hardware, privacy and operations references

- [Full architecture proposal](MEDIAHUB-DISTRIBUTED-ARCHITECTURE-HARDWARE-PRIVACY-OPERATIONS-WAVE-378-2026-10-22.md)
- [Machine-readable decision snapshot](../context/MEDIAHUB-ARCHITECTURE-DECISIONS-WAVE-378.json)
- [Dated evidence report](../checkpoints/MEDIAHUB-ARCHITECTURE-CONSOLIDATION-REPORT-WAVE-378-2026-10-22.md)

Owner-selected policies now recorded: strict local-first data egress; encrypted owner-node backups with separated keys and restore tests; staged updates with compatibility/provenance gates and rollback. Hardware profiles distinguish known inventory from candidate sizing. See the full architecture for node roles, model placement, quotas, recovery, disconnected operation, evidence and acceptance criteria.