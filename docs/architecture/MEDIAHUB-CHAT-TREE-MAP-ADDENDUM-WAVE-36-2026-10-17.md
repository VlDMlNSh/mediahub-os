# MediaHub OS — Project Map Addendum, Wave 36 (Existing Agent Registry and Admission)

- Date: 2026-10-17
- Parent map path: docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent map blob SHA observed: fcef1bf0c8329b76ad640f774d23493cfa9157a5
- Main HEAD reviewed: 99e7c0598bdc2f69201958aeb983f64c04504990
- Documentation ref: docs/mediahub-chat-tree-map-20261012
- Current pre-write branch comparison: DIVERGED, docs branch ahead 1,950 / behind 12, merge base f0f406feb9f9816b009f4e6e756813541e53b9bc.
- Status: **NAVIGATION ADDENDUM / SOURCE RECONCILIATION / PROPOSED / RUNTIME UNVERIFIED**

## New navigation entry

### MH-CLOUD-AGENT-ADMISSION-W36 — Existing Registry and A0 Admission Reconciliation

Primary document:
- [Existing Agent Registry, A0 Admission and Provider-Egress Reconciliation, Wave 36](../checkpoints/MEDIAHUB-EXISTING-AGENT-REGISTRY-A0-ADMISSION-AND-EGRESS-RECONCILIATION-WAVE-36-2026-10-17.md)

Companions:
- [Wave 36 Master Roadmap Execution Addendum](../checkpoints/MEDIAHUB-MASTER-ROADMAP-EXECUTION-ADDENDUM-WAVE-36-2026-10-17.md)
- [Wave 36 Agent Registry Admission Traceability Addendum](../checkpoints/MEDIAHUB-AGENT-REGISTRY-ADMISSION-TRACEABILITY-ADDENDUM-WAVE-36-2026-10-17.md)
- [Wave 36 Canonical Source Registry Addendum](../checkpoints/MEDIAHUB-CANONICAL-SOURCE-REGISTRY-ADDENDUM-WAVE-36-2026-10-17.md)
- [Wave 36 Continuation Checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-17-wave36.md)

## Confirmed findings

- Existing agent catalog: main / profiles/agent-registry.json v1.2.0.
- Existing architect/builder/verifier role registry: main / .github/agent-system/registry.yaml.
- Existing narrow provider-registry and provider-adapter JSON Schemas.
- Existing 23-lane queue manifest and local filesystem ClaimStore.
- Existing ASTRA governance and qualification schemas define A0/A1/A2/A3, claims, leases, credential lifecycle, G0–G11, and human launch authority.
- R-06 approval authority and issuer/ingress contract remain open; MH-12 secret store remains non-canonical pending evidence/ADR.
- Therefore Wave 36 recommends a compatible admission-contract extension, not a parallel registry or scheduler.
- GitHub-hosted execution can avoid an owner-operated always-on server; request egress remains an actual network-origin and service-region fact.

## Work status and boundaries

Wave 36 source reconciliation and companion traceability planning are documentary proposals. Runtime code, catalogs and workflows remain unchanged; there is no provider activation, model invocation or qualification claim from this wave.

## Map-body limitation

The parent map path was re-read and returned its blob SHA but an empty body via the GitHub connector, including line-range reads. Keep the parent map unchanged. Use this verified addendum and continuation checkpoint for new Wave 36 navigation until the original map body can be reliably retrieved and updated without replacing historical content.
