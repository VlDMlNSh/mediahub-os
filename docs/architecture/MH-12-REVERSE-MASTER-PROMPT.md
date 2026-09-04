# MH-12 REVERSE MASTER PROMPT

Use this document from the dedicated development chat when it needs the current MH-12 security contract.

## Development must preserve

- State Authority remains the sole canonical mutation authority.
- All security-sensitive operations require explicit authorization.
- Authentication is not authorization.
- Identity is not privilege.
- Network reachability, localhost, LAN or VPN is not authorization.
- Capability cannot self-grant or expand.
- Human privilege is not automatically inherited by services.
- Plugin and AI are untrusted computational principals unless explicit bounded trust is established.
- Cloud, update and recovery remain separate security boundaries.
- Consumer Boundary cannot be bypassed.
- Observability and diagnostics cannot become mutation authorities.
- Malformed/unknown/ambiguous security inputs fail closed.
- No implementation may silently create a second State Authority.

## Before implementation

1. Identify the relevant MH-12 architecture artifact.
2. Check its status: VERIFIED/ACCEPTED/FROZEN/PROPOSED/UNKNOWN/etc.
3. Check related ADRs and contradiction register.
4. Check compatibility with P0-03…P0-07.
5. If a required decision is UNKNOWN/PROPOSED, stop and request architecture/governance resolution rather than inventing a contract.

## Implementation flow

Architecture → ADR → Governance Authorization → Implementation → Tests → Security Verification → Evidence → Acceptance → Freeze.

## Required negative behavior

Unauthorized, malformed, expired, revoked, replayed, wrongly scoped, ambiguous or forged security inputs must not reach canonical mutation.

## Chat boundary

Do not move implementation debugging or feature development into MH-12. Return architecture questions, contradictions, required evidence and security decisions to MH-12; keep code changes in the dedicated development workspace.

## Current MH-12 gate

Architecture is complete. Governance acceptance, production qualification and freeze are not granted until implementation and verification evidence exist.
