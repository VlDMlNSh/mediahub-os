# MH-02 — Boundary Interface Contract

## Universal boundary contract

Every cross-domain interaction MUST carry attributable identity/provenance, authorization context, policy decision, contract/version identity and an auditable result.

### Request path
`Input → Identity → Authorization → Policy → Contract → Authority → Result → Observation → Evidence`

### Event path
`Authority → Event → Consumer → Proposal/Request → Governed Request Path`

Events are observational and cannot directly mutate canonical state.

### External path
`External → Adapter → Validation → Qualification → Policy Admission → Domain Contract`

### Data egress
`Classification → Authorization → Residency → Egress Policy → Transfer → Audit`

## Compatibility

All public/domain boundaries are versioned. Breaking changes require explicit migration/versioning handling; no silent contract widening.

## Failure

Boundary uncertainty fails closed. Timeout/retry/circuit-breaker/idempotency mechanics are implementation concerns delegated to downstream MH domains.

## Authority

No boundary may transfer canonical authority merely by passing data, hosting a copy, exposing an API, or executing a proposal.
