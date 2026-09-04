# MH-04 Security Foundation

Status: PROPOSED / architecture in progress.

MH-04 inherits MH-01..MH-03 and P0-03..P0-06 without redefining them. Security is a governed control layer, not an authority path.

## Invariants
- State Authority is the sole canonical mutation authority.
- Identity, authentication, authorization, capability and policy do not mutate state.
- UI/API/device/plugin/AI/cloud/runtime service cannot bypass the governed command path.
- Security may ALLOW, DENY or QUARANTINE; it never creates shadow authority.
- Ambiguity and unverifiable authorization fail closed.

## Canonical path
External Input -> Integration Boundary -> Consumer Contract -> Capability/Command -> Identity -> Authentication -> Authorization -> Policy -> State Authority -> Canonical Mutation -> Event -> Observers.

Technology choices remain candidate until evidence, compatibility, security and architecture decision.

## Acceptance
Requires parent compatibility, authority-path, trust-boundary, identity, authorization, capability, failure, observability, historical reconciliation and contradiction reviews.