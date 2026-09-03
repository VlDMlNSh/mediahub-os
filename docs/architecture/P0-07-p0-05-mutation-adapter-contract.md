# P0-07 → P0-05 Mutation Adapter Contract v1.0

Status: IMPLEMENTATION BLOCKED — GOVERNANCE/API GAP

## Finding

The current P0-05 `ConsumerBoundary` exposes `begin`, `update`, `commit`, and `abort`, but its `begin` path authorizes the supplied context directly against P0-04's `begin` operation. Its `commit` and `abort` paths likewise use the transaction's P0-04 authorization context.

P0-07 defines a separate exact capability inventory (`configuration.*`, `policy.*`) and a separate device-local authorization model. The current repository contains no approved mechanism that maps a P0-07 capability grant into a P0-04 transaction capability without changing authorization semantics.

## Security conclusion

A P0-07 mutation adapter MUST NOT:

- call P0-04 directly;
- replace or mutate the P0-04 `AuthorizationContext`;
- translate `configuration.update` or another P0-07 capability into `begin`/`commit`/`abort` privileges;
- create a second State Authority;
- self-grant P0-04 permissions;
- bypass P0-05;
- weaken P0-04 default-deny behavior.

Therefore a fully implemented P0-07 mutation adapter is **blocked** until an explicit governance/API contract authorizes how a domain-authorized P0-07 operation obtains the independently required P0-04 transaction authorization.

## Safe work that remains authorized

P0-07 may continue to implement and test:

- bounded configuration/policy models;
- deterministic validation;
- deterministic policy evaluation;
- exact P0-07 authorization;
- inert proposals;
- inert plugin capability grants;
- read-only domain operations;
- security regression tests.

## Required governance decision before mutation

The project must explicitly choose one of the following architectural directions:

1. **Existing-context model:** P0-07 callers already possess an independently authorized P0-04 transaction capability, and P0-07 only gates the domain operation before invoking P0-05.
2. **Approved authorization bridge:** a future governance-controlled layer explicitly composes P0-07 domain authorization with P0-04 transaction authorization without translating or self-granting capabilities.
3. **Revised P0-05 contract:** a governance change extends P0-05 with an explicit, independently authorized domain-operation interface.

Until one is accepted, mutation publication remains unauthorized. No code should guess the mapping.

## Frozen boundaries

P0-03, P0-04, P0-05, and P0-06 remain unchanged and frozen.

Production qualification remains not granted.
