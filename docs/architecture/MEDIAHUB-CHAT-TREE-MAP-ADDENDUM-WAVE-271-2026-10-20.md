# MediaHub OS — map addendum, Wave 271 (2026-10-20)

- Status: read-only source reconciliation; Wave 268/270 owner requirements remain binding target constraints; Wave 269 remains a draft.
- Report: [Wave 271 — A0 issuer/task contract reconciliation](../checkpoints/MEDIAHUB-A0-ISSUER-TASK-CONTRACT-RECONCILIATION-WAVE-271-2026-10-20.md).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).
- Checkpoint: [current continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md).
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md).

## Findings
1. Existing Task ingress blob `59e1254aa61cc8f55f53bd1e179631e81c441393` validates a small request contract but has no trusted issuer/capability provenance, destination admission, DAG, locality/egress or cross-route fencing.
2. `AuthorizationContext` blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` contains principal/capability only; its explicit allow-list is not signed-ingress or replay protection.
3. Gateway blob `10985e4ad8f682313d08e7492ecc1856a8bce20f` is cloud-first with local Ollama; local queue blob `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` is filesystem-backed. Neither is a qualified hybrid A0 plane.
4. Provider registry/adapter schemas are not the mission-envelope schema. FCC/OmniRoute/Claude direct are candidates only, not admitted routes.

## Hard constraints retained
A0 owns hybrid task lifecycle and distributes bounded tasks among the independent GitHub-hosted pool, admitted user-owned MediaHub and admitted local executors. Claude/Claude Code is exclusively a local Alamo executor for this target; Anthropic API and paid Anthropic API authorization/billing routes are prohibited; no silent fallback. FCC/equivalent requires evidence and must not bypass provider controls. Unknown issuer/destination/auth-cost class/locality policy fails closed. Independent A3 verification and Product State Authority separation remain mandatory.

## Next
Trace the authoritative Task Contract producer/writer and approval/attestation lifecycle. Map the candidate fields to existing contracts before adding static/mock-only negative fixtures or changing runtime code.
