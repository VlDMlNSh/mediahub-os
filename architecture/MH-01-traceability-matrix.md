# MH-01 Traceability Matrix

Status: PROPOSED / REQUIRES VERIFICATION.

| Principle | Requirement | Architecture rule | Implementation constraint | Verification | Governance |
|---|---|---|---|---|---|
| Local-first | Core local operation | Local primary path | No mandatory cloud dependency | Offline qualification | MH-01/MH-02/MH-22 |
| Safety-first | Safety dominates optimization | Ordered safety hierarchy | No bypass | Safety tests/review | MH-01 |
| Authority-first | One canonical mutator | State Authority only | No second writer | Authority scan | P0 governance |
| Explicit authorization | Permission precedes mutation | Auth boundary before State Authority | Reject unauthorized commands | Negative tests | MH-07/MH-12 |
| Deny-by-default | Unknown denied | No implicit allow | Secure default | Negative tests | MH-12 |
| Deterministic core | Critical operation local/deterministic | AI optional to critical path | No mandatory inference | Offline deterministic tests | MH-03 |
| AI non-authoritative | AI proposes | Proposal→policy→authorization→command | No direct mutation | Boundary/authority tests | MH-10 |
| Cloud non-authoritative | Cloud external | Contracted external compute | No State Authority access | Boundary tests | MH-21 |
| Observable | Critical behavior traceable | Event/diagnostic path | No silent critical mutation | Observability tests | MH-11 |
| Recoverable | Safe recovery | Recovery authority isolated | Verified recovery path | Recovery qualification | MH-16 |
| Privacy-by-default | Local/private | Explicit export boundary | Bounded data egress | Data-flow audit | MH-13 |
| Least privilege | Minimum authority | Capability-scoped rights | No broad privilege | Privilege audit | MH-12 |
| Explicit trust | Discovery insufficient | Verified/enrolled trust lifecycle | No presence-based authorization | Trust tests | MH-17 |
| Bounded interfaces | Controlled coupling | Contract-only cross-domain authority | No arbitrary calls | Architecture review | MH-02 |
| Fail closed | Ambiguity denies | No implicit permission | Reject uncertainty | Negative tests | MH-12 |
| Reproducibility | Evidence-backed behavior | Versioned decisions/artifacts | Reproducible build/test records | Reproduction review | MH-01 |
| Governance before irreversible change | Review first | Change gate before implementation | No silent break | Governance audit | MH-01 |
| Compatibility-aware evolution | Preserve contracts | Migration for breaks | Versioned compatibility | Compatibility suite | MH-23 |
| Evidence-first | Claims require evidence | Status/evidence register | No claim without source | Evidence audit | MH-01 |

Traceability is incomplete until each downstream MH supplies its domain-level implementation and verification evidence.