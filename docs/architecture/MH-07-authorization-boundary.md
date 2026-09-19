# MH-07 — Authorization Boundary

Status: CANDIDATE; P0-07 mutation path BLOCKED.

Policy and authorization are conjunctive, not substitutive: P0-07 domain authorization ALLOW AND P0-07 policy ALLOW AND independently valid P0-04/P0-05 authorization = mutation may proceed.

P0-07 MUST NOT translate configuration.* or policy.* into P0-04 begin/commit/abort privileges, mutate AuthorizationContext, mint capabilities or bypass P0-05.

The approved composition mechanism is absent. Existing-context model, explicit authorization bridge, or revised P0-05 contract are ADR candidates; no choice is accepted here.
