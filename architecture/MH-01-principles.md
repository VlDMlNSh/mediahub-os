# MH-01 Principles

Status: PROPOSED / REQUIRES VERIFICATION.

| ID | Principle | Requirement | Architecture rule | Verification | Governance gate |
|---|---|---|---|---|---|
| P-01 | Local-first | Core works locally | No mandatory cloud dependency | Offline test | MH-01/MH-02 |
| P-02 | Safety-first | Safety dominates optimization | Fixed safety hierarchy | Safety review | MH-01 |
| P-03 | Authority-first | One canonical mutator | State Authority only | Authority-path audit | P0 governance |
| P-04 | Explicit authorization | Actions require permission | Authorization precedes mutation | Negative tests | MH-07/MH-12 |
| P-05 | Deny-by-default | Unknown is denied | No implicit allow | Negative tests | MH-12 |
| P-06 | Deterministic core | Critical core independent of inference | AI cannot be required for critical execution | Offline deterministic test | MH-03 |
| P-07 | AI non-authoritative | AI proposes | Inference→proposal→policy→authorization→command | Authority scan | MH-10 |
| P-08 | Cloud non-authoritative | Cloud is external compute | No direct State Authority access | Boundary test | MH-21 |
| P-09 | Observable | Critical behavior visible | Events/diagnostics are first-class | Observability tests | MH-11 |
| P-10 | Recoverable | Failure must be recoverable | Recovery privilege isolated | Recovery test | MH-16 |
| P-11 | Offline-capable core | Internet outage cannot destroy core | Local execution path | Offline qualification | MH-02/MH-22 |
| P-12 | Privacy-by-default | Data stays local unless authorized | Explicit export boundary | Data-flow audit | MH-13 |
| P-13 | Least privilege | Minimum rights | Capability-scoped permissions | Privilege audit | MH-12 |
| P-14 | Explicit trust | Discovery is not trust | Enrollment/verification required | Trust tests | MH-17 |
| P-15 | Bounded interfaces | Domains interact via contracts | No arbitrary cross-domain authority | Architecture review | MH-02 |
| P-16 | Fail closed | Ambiguity cannot grant authority | Deny on uncertainty | Negative tests | MH-12 |
| P-17 | Reproducibility | Decisions/behavior evidence-backed | Versioned artifacts and evidence | Reproduction review | MH-01 |
| P-18 | Governance before irreversible change | Architecture changes are controlled | Breaking changes require governance | Change audit | MH-01 |
| P-19 | Compatibility-aware evolution | Preserve valid contracts | Explicit migration for breaks | Compatibility suite | MH-23 |
| P-20 | Evidence-first engineering | Claims require evidence | Status-tag every fact/decision | Evidence audit | MH-01 |

## Universal invariants

`Command ≠ Event`; `Desired State ≠ Runtime State`; `Audit ≠ Domain Event`; `Knowledge ≠ Authority`; `Prediction ≠ Observation`; `Simulation ≠ Execution`; `Persistence ≠ State Authority`; `Cache ≠ Canonical State`; `AI Recommendation ≠ Authorization`.

Any downstream design that violates a universal invariant is BLOCKED pending explicit governance decision.