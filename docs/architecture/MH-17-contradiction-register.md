# MH-17 — Contradiction Register

**Status:** OPEN

| ID | Contradiction | Impact | Required resolution |
|---|---|---|---|
| C-001 | Target trust/lifecycle includes quarantine, revocation and authorization; current lifecycle schema does not | Security semantics cannot be represented distinctly | ADR + versioned lifecycle contract |
| C-002 | `schemas/domain/identity.schema.json` models `protocol_ids` and `hardware_ids` as objects, while nested Device identity models them as arrays | Contract inconsistency | Reconcile schemas before implementation |
| C-003 | Device/capability schemas permit broad nested `object` fields | Weak structural enforcement at integration boundary | Introduce explicit nested contracts/bounds |
| C-004 | Existing tests contain a duplicated `test_event_is_immutable_fact_boundary` method | Test quality ambiguity; second definition shadows first | Correct test corpus and verify |
| C-005 | P0-06 explicitly excludes networking/external execution, while MH-17 requires device integration | Integration cannot be assumed already authorized | New MH-17 governance scope must be approved |

No contradiction is silently resolved by reinterpretation.