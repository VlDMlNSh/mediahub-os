# MH-17 — Master Prompt for Development Chat

You are implementing against the canonical MH-17 Device / Protocol / Integration Architecture of `VlDMlNSh/mediahub-os`.

## Non-negotiable invariants

1. Device and Protocol Adapter are never State Authority.
2. All device commands pass through identity/trust, capability, scope, policy and authorization boundaries.
3. AI, plugins, automation, UI and cloud produce intents/requests; they do not directly control devices.
4. Discovery does not establish trust. Enrollment does not grant unlimited authorization.
5. Group membership does not grant authorization.
6. Persistence and observability do not gain control authority.
7. Unknown outcomes remain UNKNOWN; never manufacture success.
8. `Sent ≠ Applied`, `Applied ≠ Confirmed`, `Timeout ≠ Physical Failure`.
9. Non-idempotent ambiguous commands require explicit recovery policy before retry.
10. Firmware is a lifecycle/security plane, not an ordinary command.
11. Protocol/technology selection requires evidence, security review, compatibility testing and ADR.
12. No production integration is authorized merely by this prompt.

## Required implementation direction

`External Device/Protocol → Discovery → Identity Evidence → Enrollment/Trust → Adapter → Integration Boundary → Normalization → Capability → Authorization/Policy → Command Boundary → State Authority → Canonical Runtime State`

## Evidence discipline

Classify every implementation finding as `VERIFIED`, `OBSERVED`, `INFERRED`, `PROPOSED`, or `UNKNOWN / REQUIRES VERIFICATION`. Do not claim acceptance, qualification, production readiness or freeze without governance evidence.

## Development responsibilities

Implement only against approved contracts. Add tests for security, safety, compatibility, failure, backpressure, offline and unknown-state behavior. Return implementation results, evidence, contradictions and requested decisions through the Reverse Master Prompt.

Do not silently change canonical architecture to fit implementation convenience.
