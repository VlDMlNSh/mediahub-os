# P0-04 Gate State Machine v1.0

## Status

Prepared as a governance/control artifact. It does not grant implementation authorization.

## States

- `PREPARED`: architecture, security, privacy, test, and evidence preparation complete enough to enter governance transition.
- `AUTHORIZED`: explicit P0-03 decision authorizes P0-04 within a bounded scope.
- `IMPLEMENTING`: implementation is occurring only on the authorized immutable baseline.
- `VERIFYING`: functional, adversarial, security, privacy, and capability evidence is being collected.
- `BLOCKED`: a stop condition or missing prerequisite prevents progress.
- `ACCEPTED`: P0-04 implementation has explicit acceptance based on evidence.
- `REJECTED`: implementation or evidence fails the gate and must not be accepted.

## Allowed transitions

`PREPARED -> AUTHORIZED` only after explicit P0-03 governance decision with authority, timestamp, and scope.

`AUTHORIZED -> IMPLEMENTING` only after baseline and entry-gate verification.

`IMPLEMENTING -> VERIFYING` only when the implementation slice is complete for the declared verification scope.

`VERIFYING -> ACCEPTED` only after required evidence, security/privacy review, and explicit acceptance authority.

Any state -> `BLOCKED` on a mandatory stop condition or missing prerequisite.

`VERIFYING -> REJECTED` when a blocking invariant or security requirement fails and no valid acceptance condition exists.

`REJECTED -> IMPLEMENTING` only through a new controlled remediation cycle with a new exact commit and renewed evidence.

`BLOCKED -> PREPARED` only after the blocking condition is resolved and the preparation state is re-established.

## Forbidden transitions

- `PREPARED -> IMPLEMENTING`
- `PREPARED -> ACCEPTED`
- `AUTHORIZED -> ACCEPTED` without implementation and evidence
- `VERIFYING -> ACCEPTED` without security/privacy review
- Any transition that silently changes authorized scope
- Any transition based solely on source inspection when execution evidence is required

## Fail-closed rule

If the current state, authorization, baseline, evidence identity, or acceptance authority is ambiguous, the gate enters `BLOCKED` rather than assuming permission.

## Scope invariants

P0-04 remains deterministic and in-memory only. Persistence, network, subprocess, production appliance, installer/recovery, update engine, cloud, and hardware persistence require separate authorization.

## Security/privacy invariants

The state machine preserves default-deny authorization, isolated candidates, atomic publication, stale rejection, independent integrity validation, checkpoint immutability, restore-as-new-revision, sanitized diagnostics, synthetic test data, and evidence hygiene.

## Historical boundary

No historical MH-02…MH-16 responsibility is inferred.
