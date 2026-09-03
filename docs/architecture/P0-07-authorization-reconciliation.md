# P0-07 Authorization Reconciliation v1.0

Status: IMPLEMENTATION RECONCILIATION — NO P0-04/P0-05 CHANGE AUTHORIZED

## 1. Purpose

Define the authorization relationship between the P0-07 configuration/policy boundary and the frozen P0-05/P0-04 mutation path without introducing a second State Authority or changing frozen contracts.

## 2. Existing authorities

P0-07 owns only configuration/policy domain validation and P0-07 operation authorization. It is not a state authority.

P0-05 remains the sole consumer/integration boundary. P0-04 remains the sole canonical mutation authority.

## 3. Capability separation

P0-07 capabilities are exact, operation-specific domain capabilities:

- configuration.read
- configuration.validate
- configuration.propose
- configuration.update
- configuration.replace
- configuration.reset
- configuration.delete
- policy.read
- policy.validate
- policy.propose
- policy.update
- policy.replace
- policy.reset
- policy.delete

P0-04 authorization remains independently required for State Authority operations. P0-07 authorization MUST NOT be treated as a replacement for P0-04 authorization.

## 4. Required mutation path

For an authorized P0-07 mutation:

    caller
      -> P0-07 request validation
      -> P0-07 capability authorization
      -> P0-07 policy evaluation
      -> P0-05 consumer boundary
      -> P0-04 begin
      -> isolated candidate validation
      -> P0-05 commit
      -> P0-04 atomic publication

No direct P0-07 import or invocation of State Authority mutation APIs is permitted.

## 5. Authorization composition

Authorization is conjunctive, not substitutive:

    P0-07 authorization ALLOW
    AND
    P0-07 policy ALLOW
    AND
    underlying P0-04/P0-05 operation authorization
    =
    mutation may proceed

Any missing or denied component MUST fail closed.

P0-07 MUST NOT mint, translate, or self-grant a P0-04 capability. A caller context presented to P0-05 must already carry an authorization that P0-04 accepts for the required operation.

## 6. Operation mapping

P0-07 domain operation and P0-04 transaction operation are distinct namespaces.

P0-07 `update`, `replace`, `reset`, and `delete` describe the domain request. They MUST NOT be passed to P0-04 as if they were P0-04 operation names.

The P0-04 transaction lifecycle remains exactly `begin`, `commit`, and `abort`.

A future P0-07 mutation service may therefore perform:

1. authorize the P0-07 domain operation;
2. construct a bounded candidate document;
3. invoke P0-05 `begin` with a context independently authorized for P0-04 `begin`;
4. set the complete candidate payload;
5. invoke P0-05 `commit` with the transaction's bound P0-04 authorization;
6. fail closed on stale generation/revision or any validation error.

No LWW, retry, rebase, merge, patch, or conflict-resolution mechanism is introduced.

## 7. Policy operation representation

P0-07 policy rules may use the exact P0-07 capability string as the operation identifier when policy is intended to authorize a capability-level action. The implementation MUST use one representation consistently and MUST NOT silently reinterpret a rule as a different capability.

## 8. Security prohibitions

The following remain prohibited:

- modifying P0-03 through P0-06;
- direct access to P0-04 from P0-07 mutation code;
- bypassing P0-05;
- capability translation that grants new authority;
- wildcard or inherited capabilities;
- hidden retry/rebase/LWW;
- persistence, network, filesystem, subprocess, credential resolution;
- autonomous AI mutation;
- dynamic plugin grants.

## 9. Implementation gate

This document authorizes only the reconciliation described above. It does not grant production qualification and does not authorize changes to frozen P0-04/P0-05 contracts.
