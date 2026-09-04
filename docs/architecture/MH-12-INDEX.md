# MH-12 — SECURITY ARCHITECTURE

Status: **ARCHITECTURE COMPLETE / GOVERNANCE REVIEW REQUIRED**

This directory is the durable architectural record for MH-12. The MH-12 chat is a short-lived architecture work surface; GitHub is the durable source of record.

## Authority

- Security controls trust, identity, authentication, capability, authorization, policy enforcement, boundaries, isolation, compromise handling and recovery.
- Security is **not** the canonical mutation authority.
- State Authority remains the sole canonical mutation authority under P0-03/P0-04.
- Consumer Boundary remains mandatory under P0-05.
- P0-07 remains implementation-in-progress and its known authorization/API gap is not bypassed by MH-12.
- Observability reports security state; it does not enforce security.

## Canonical flow

External/Input → Integration Boundary → Consumer Contract → Identity → Authentication → Trust → Capability → Authorization → Policy → Command/Proposal → Consumer Boundary → State Authority → Event → Audit/Observability

## Current gate

Architecture: COMPLETE
Threat model: COMPLETE
Security boundaries: COMPLETE
Identity/authentication/authorization/capability/trust: DEFINED
Implementation: NOT AUTHORIZED by this architecture record
Production qualification: NOT GRANTED
Governance acceptance: NOT GRANTED
Freeze: NOT GRANTED

## Required artifacts

See `MH-12-security-architecture.md` and the artifact list recorded there. Detailed domain artifacts may be added without changing this status unless governance explicitly accepts a new baseline.

## Mandatory invariants

1. State Authority is the sole canonical mutation authority.
2. Authentication does not imply authorization.
3. Identity does not imply privilege.
4. Authorization does not bypass State Authority.
5. Network reachability, localhost, LAN or VPN do not imply trust/authorization.
6. Capability cannot self-grant or silently expand.
7. AI and plugins cannot self-authorize.
8. Cloud cannot become local authority.
9. Observability and diagnostics cannot become mutation authority.
10. Recovery cannot silently bypass security.
11. Update cannot silently increase privilege.
12. Secrets never become ordinary telemetry.
13. Malformed and ambiguous security input fails closed.
14. Unknown entities are not silently trusted.
15. Security failure cannot silently become authorization success.
16. No second State Authority may be introduced.

## Governance rule

Architecture ≠ implementation. Implementation requires ADR → governance authorization → implementation → tests → security verification → evidence → acceptance → freeze.

Do not modify frozen P0-03…P0-06 to unblock MH-12/P0-07 without explicit governance authorization and contradiction analysis.
