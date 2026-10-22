# MediaHub OS — Architecture Consolidation and Evidence Report, Wave 378

- Date: 2026-10-22
- Status: **DOCUMENTATION UPDATE IN WORKING PR / NOT CANONICAL UNTIL MERGED**
- PR: [#486](https://github.com/VlDMlNSh/mediahub-os/pull/486)
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical documentation base observed: `937b6fa164d0e89e5e5781bf8c236e4fb862ad56`
- `main` HEAD observed: `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Consolidated architecture: [hardware, privacy and operations](../architecture/MEDIAHUB-DISTRIBUTED-ARCHITECTURE-HARDWARE-PRIVACY-OPERATIONS-WAVE-378-2026-10-22.md)
- Machine-readable snapshot: [Wave 378 JSON](../context/MEDIAHUB-ARCHITECTURE-DECISIONS-WAVE-378.json)
- Tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Work performed in this documentation pass

- Consolidated owner-selected policies from the current architecture discussion: strict local-first privacy, encrypted own-node backups with separated keys and restore drills, staged updates with compatibility/provenance gates and rollback, queue separation, hybrid networking/observability, adaptive scheduling and evidence-aware recovery.
- Added an explicit hardware inventory and candidate media-server profile, distinguishing known facts from unknown values and unqualified proposals.
- Added a detailed reference architecture, machine-readable decision snapshot and a navigation entry in the canonical map file within the working PR branch.
- Added durable references to the Bootstrap, continuation checkpoint and Master Roadmap, including the future `/next` synchronization protocol.
- Preserved Baseline 2.0, existing authority/governance contracts and Contour A/Contour B gates.

## Hardware evidence boundary

- Mac mini 2018: six CPU cores reported in the project discussion; RAM is unknown and must be inventoried.
- Mac mini 2011: four CPU cores, 16 GB RAM, Linux; planned for background builds/tests and light tasks, not yet hardware-qualified by this document.
- Voktors-Mini.Dlink: historical project records identify macOS ARM64. Current runtime and local executor qualification remain NOT VERIFIED; it is not a Gemini transport.
- Future media server: about 100,000 RUB budget; Ryzen 5 5600 / RTX 3060 12 GB / 32 GB RAM upgradeable to 64 GB / 1 TB NVMe is a candidate only, not a purchase or performance guarantee.

## Verification

- GitHub refs, PR #486, Issue #301, canonical documentation base and main HEAD were inspected read-only before edits.
- The canonical map blob was retrieved at its full original size, appended without replacing its prior body, and written as a new blob in the working PR branch.
- Changed documents must be read back and their blob SHAs checked after the edits.
- JSON syntax validation and link/required-section checks are to be run against the final read-back.
- Exact-head CI and independent review for the final PR head: **NOT VERIFIED until live endpoints show the result**.
- No runtime tests, benchmarks, model inference, media processing, Gemini dispatch, local-host command, secret access, server change, merge, deployment or qualification was performed by this documentation pass.

## Current disposition

Architecture context is documented in a working branch and PR, not yet canonical. Runtime implementation is NOT CLAIMED; verification, qualification and acceptance remain separate. Related open PRs #474 and #485 must be reconciled during integration; no open PR is assumed merged based on its existence.

## Next bounded step

Read back every changed file from the final PR head, record blob SHAs and exact-head CI/review state, validate JSON and links, then reconcile append-only changes with the other open documentation PRs before any merge.
