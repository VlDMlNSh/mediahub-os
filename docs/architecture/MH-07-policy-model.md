# MH-07 — Policy Model

Status: CANDIDATE.

Policy is bounded, deterministic, declarative, non-executable and device-local. v1 uses explicit ALLOW/DENY rules over exact operation/resource pairs.

Policy cannot mutate state, alter authorization grants, load plugins or invoke external work. Wildcards, inheritance, implicit priority, merge and LWW are forbidden. Conflicting applicable effects fail closed.

Current implementation evidence covers PolicyRule/Policy bounds, explicit effects and device-local scope. Rich predicates, modes and revision semantics remain CANDIDATE/REQUIRES VERIFICATION.
