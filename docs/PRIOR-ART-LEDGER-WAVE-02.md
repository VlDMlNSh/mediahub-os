# MediaHub Prior-Art Ledger — Wave 02

Status: QUALIFIED FOR IMPLEMENTATION
Date: 2026-09-09
Rule: ADR-002 GitHub Prior-Art-First Engineering

## Scope

Wave 02 establishes provider registry and adapter boundaries. Before implementation, prior art was re-checked against the currently qualified gateway corpus.

## Findings

### Bifrost

Provider implementations are specialized rather than assuming one wire format fits every upstream. This supports a MediaHub adapter boundary with explicit provider identity and translation responsibility.

### LiteLLM

Provider selection and deployment/routing logic are separated from lower-level provider handling. This supports keeping registry metadata separate from routing authority.

### OmniRoute

Provider management includes normalization/validation and defensive handling. MediaHub therefore validates provider identity and endpoint scheme at registration and does not permit arbitrary runtime endpoints.

## Native decisions

1. Registry owns qualified provider metadata only.
2. Adapter owns wire translation only.
3. Routing authority remains outside the registry.
4. Credentials remain outside both registry records and adapters.
5. Endpoint registration requires HTTPS.
6. Duplicate provider identities are rejected.
7. Adapter identity must equal registered provider identity.
8. Capability declarations are explicit and are later checked by the capability matrix.
9. Third-party gateway code is not imported as a runtime dependency.

## Derived security tests

- reject HTTP provider endpoints;
- reject duplicate identities;
- reject adapter/provider identity mismatch;
- reject unregistered providers;
- keep credentials out of registry records;
- keep policy authority outside adapter implementation.

## Result

Wave 02 registry contract is qualified for continued development. Routing, retry and circuit-breaker implementation remains a separate prior-art gate and is not implicitly approved by this ledger.
