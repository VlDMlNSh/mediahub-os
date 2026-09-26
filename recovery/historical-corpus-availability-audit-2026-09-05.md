# Historical MH-01…MH-23 Corpus Availability Audit

Date: 2026-09-05
Branch: recovery/full-functional-spec
Status: IN PROGRESS — availability audit, not acceptance

## Purpose

Determine which historical MH-01…MH-23 architectural evidence is actually available in the repository at the current recovery checkpoint, without treating absence from an index/search result as proof that a chat never existed.

## Evidence checked

1. Recovery branch tree at commit `28b6b5e0f66d57d38311c29c6a05db9aab64ab69`.
2. `architecture/` directory on `recovery/full-functional-spec`.
3. Repository file search for MH-01 and MH-23.
4. Repository commit search for MH-01 and MH-18.
5. Existing recovery/accepted and recovery/functional-themes inventories.

## Findings

- The current recovery branch definitely contains a substantial MH-03 architectural corpus, including acceptance criteria, command execution, contradiction register, decision log, degraded mode, error handling, event model, evidence register, health model, lifecycle, master prompt, recovery boundary, reverse master prompt, runtime dependencies/foundation/model/observability, service boundaries, startup/shutdown and sync records.
- The current branch also contains the reconstructed master architecture and recovery registries.
- Repository code search does not return MH-01 or MH-23 matches in its indexed search surface. This is evidence about the searchable corpus only; it is NOT evidence that those historical chats never existed.
- Commit search finds an MH-18 evidence-provenance commit (`fa9ba5f5d20f722f9a991804a8de2c4e35d47218`), confirming that MH-18 historical evidence was deliberately preserved in Git history.
- The available recovery corpus therefore cannot yet be treated as a complete machine-readable export of all MH-01…MH-23 conversations.

## Forensic classification

MH-01…MH-23 historical corpus completeness: UNKNOWN / INCOMPLETE EVIDENCE.

This must NOT be classified as capability loss.

Existing accepted functional baseline remains primary truth. Historical material remains evidence to be retained, reconciled, or explicitly marked UNKNOWN.

## Consequence

Exhaustive historical reconciliation cannot truthfully be marked COMPLETE until the missing historical corpus is made available through a machine-readable repository artifact, uploaded files, or another directly inspectable source.

No architecture distribution to MH-01…MH-23 and no production implementation authorization is implied by this audit.
