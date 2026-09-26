# MH-01 INDEX — CANONICAL ARCHITECTURE CUSTODIAN

**System:** MediaHub OS 11.x LTS / MediaHub iOS  
**Repository:** `VlDMlNSh/mediahub-os`  
**Branch:** `recovery/full-functional-spec`  
**Status:** PROPOSED / REQUIRES VERIFICATION

## Canonical artifacts

- `MH-01-product-governance-system-charter.md`
- `MH-01-principles.md`
- `MH-01-scope.md`
- `MH-01-governance-model.md`
- `MH-01-change-control.md`
- `MH-01-acceptance-criteria.md`
- `MH-01-decision-log.md`
- `MH-01-evidence-register.md`
- `MH-01-dependency-map.md`
- `MH-01-to-MH-23-interface-contract.md`
- `MH-01-traceability-matrix.md`
- `MH-01-contradiction-register.md`
- `MH-01-master-prompt.md`
- `MH-01-reverse-master-prompt.md`

## Custodianship protocol

1. GitHub repository is the persistent canonical record.
2. MH architecture chats are temporary working custodians/readers of the repository, not the sole source of truth.
3. Development chats are separate and must not edit architecture semantics implicitly.
4. Development consumes the current Master Prompt plus referenced architecture artifacts.
5. Development returns a Reverse Master Prompt with evidence.
6. Architecture reconciles returned evidence before any canonical update.
7. Governance acceptance precedes freeze.
8. If chat state and GitHub differ, GitHub canonical artifacts win unless an explicit newer governance decision is recorded.
9. Every canonical change must carry a Git commit and decision/evidence trail.
10. Do not use architecture chats for production coding, deployment, or prolonged implementation discussion.

## Global frozen boundary

P0-03…P0-06 remain protected. Any change is a separate governance change.

## Synchronization rule

At the start of every architecture/development handoff, record the exact repository branch and commit. Do not rely on prior chat context alone.

## Current known open questions

Historical MH mapping; actual hardware topology; final persistence; OTA; hybrid cloud topology; external AI provider set; production network; RTO/RPO; HA; exact identity/PKI.

All remain UNKNOWN / REQUIRES VERIFICATION until evidence changes their status.