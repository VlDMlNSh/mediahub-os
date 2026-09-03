# P0-07 — Mutation Authority Reconciliation v1.0

Status: IMPLEMENTATION CONSTRAINT

## Purpose

Define the only permitted composition between P0-07 configuration/policy authorization and the frozen P0-05/P0-04 mutation path.

## Authoritative layers

P0-07 is a domain boundary. It may validate configuration/policy documents, evaluate declarative policy, and decide whether a domain operation is authorized. It is not a state authority.

P0-05 remains the only consumer/integration boundary to State Authority.

P0-04 remains the sole canonical mutation authority.

## Authorization composition

A P0-07 mutation is permitted only when all applicable gates succeed:

1. request is structurally valid and bounded;
2. requested P0-07 capability is in the exact allow-list;
3. principal has an explicit P0-07 `(principal, capability, operation)` grant;
4. P0-07 policy evaluation returns ALLOW with no conflicting DENY;
5. P0-05 accepts the operation request and its AuthorizationContext;
6. P0-04 authorizes its own transaction lifecycle (`begin`, `commit`, or `abort`);
7. P0-04 transaction freshness/generation/integrity checks succeed;
8. publication occurs only through P0-04 atomic commit.

Failure of any gate is fail-closed.

## Capability mapping

There is no capability translation layer in P0-07 v1.

P0-07 capabilities such as `configuration.update` are domain capabilities. They MUST NOT be rewritten into P0-04 capabilities, injected into P0-04 authorization, or used to self-grant P0-04 access.

P0-04 authorization remains independently configured and independently enforced.

## Transaction model

P0-07 does not maintain a second version, generation, transaction, or publication authority.

The P0-04 transaction captures the canonical generation and state version at `begin` and rejects stale commits. P0-07 MUST rely on that existing mechanism rather than introducing a second expected-version protocol.

## Mutation shape

When mutation integration is implemented, the publication candidate MUST contain only the approved canonical state payload. P0-07 metadata such as capability, authorization decisions, expected version, proposal identifiers, or audit context MUST NOT be inserted into canonical state unless separately authorized as actual state data.

The authorized v1 publication unit is one complete configuration or policy document. Cross-document atomicity is not authorized.

## Prohibited

- direct State Authority calls from P0-07 domain code;
- capability translation or capability injection;
- self-grant or dynamic grant escalation;
- hidden retry, rebase, merge, or last-write-wins;
- second transaction/version authority;
- persistence;
- network, filesystem, subprocess, or credential dereference;
- executable policy or AI-directed mutation;
- cross-document atomicity;
- break-glass mutation path.

## Implementation gate

Before mutation code is added, the P0-05 request surface and its existing authorization behavior must be used exactly as implemented. If a required bridge is absent, that bridge is a governance/API change and must not be invented inside P0-07.
