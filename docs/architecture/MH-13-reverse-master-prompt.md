# MH-13 — REVERSE MASTER PROMPT

**Domain:** MH-13 Privacy / Data Governance  
**Artifact:** `docs/architecture/MH-13-privacy-data-governance.md`  
**Historical original:** NOT RECOVERED  
**Reconstruction:** AUTHORIZED  
**Current architecture state:** ACCEPTED RECONSTRUCTION  
**Frozen:** NO  
**Production implementation:** NOT AUTHORIZED

## Control point

The historical MH-13 artifact was not recovered. The canonical Git record is the governance-authorized reconstructed artifact. Its accepted status does not convert it into a historical original.

## Authority

MH-13 governs privacy/data governance. It does not become State Authority, Persistence authority, Media authority, AI authority, or Cloud authority. State Authority remains the sole canonical mutation authority through Boundary → Authorization → State Authority.

## Boundaries

- MH-12 — Security/trust/authentication/authorization.
- MH-14 — Persistence and durable lifecycle.
- MH-17 — Device/protocol behavior and device-specific privacy application.
- MH-18 — Media/content-specific privacy application.
- MH-21 — Hybrid-cloud/distributed-AI privacy application.
- MH-23 — Long-term compatibility/migration/evolution.

## Invariants for development consumers

- Data use is purpose-bound.
- Data collection/processing/transfer is minimized.
- Applicable privacy classification precedes governed external egress.
- External transfer is explicit, authorized, bounded and observable.
- Retention and deletion remain lifecycle concerns coordinated with Persistence.
- Protected/private data is redacted from unauthorized telemetry, diagnostics, audit and external channels.
- Audit evidence must not unnecessarily disclose protected payload.
- AI has no privacy authority and cannot weaken MH-13 restrictions.
- No implicit provider trust is assumed.
- No hidden mutation path is permitted.
- Unknown classification never authorizes external transfer.
- Derived data is not automatically less sensitive.
- Metadata may itself be sensitive.
- Backup/restore does not remove privacy obligations.

## Unknowns

Exact historical taxonomy, classification levels, consent/data-subject model, residency, retention periods, deletion/backup semantics, provider guarantees, AI-provider rules, plugin/telemetry privacy contracts and exact historical provenance model remain UNKNOWN / REQUIRES VERIFICATION unless separately accepted in Git.

## Development contract

This reverse prompt is architecture input, not implementation authorization. Production implementation remains separately governed.

If development discovers a material architecture change, do not silently edit the architecture reference. Return the proposal, evidence and impact analysis through the governance/Git review path. Accepted architectural changes must be committed to Git and reflected in the appropriate architecture artifact/register.

## Return packet

A development chat returning to MH-13 should provide:

1. proposed change;
2. affected invariants;
3. affected domains/dependencies;
4. P0 contract impact (must be explicit);
5. security/privacy/AI/cloud/persistence/media/device impact;
6. evidence and verification results;
7. unknowns/contradictions introduced or resolved;
8. requested governance decision.
