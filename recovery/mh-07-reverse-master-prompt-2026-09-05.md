# MH-07 REVERSE MASTER PROMPT — 2026-09-05

## 1. MH identifier
MH-07

## 2. Historical scope
Historical MH-07 configuration/policy contour. Exact historical corpus is not fully accessible from the current evidence surface.

## 3. Source evidence
Canonical recovery control point, redistribution master prompt, projection matrix, capability/contract/invariant/decision/dependency registries, master architecture draft, implementation map/baseline, accepted functional additions, plus the current MH-07 architecture contour and P0-07 implementation-boundary evidence.

## 4. Provenance
GitHub branch `recovery/full-functional-spec` is the canonical reconciliation source. Current MH-07 implementation evidence resides on the P0-07 development branch and remains non-authoritative for acceptance.

## 5. CAP mapping
Relevant supporting capabilities: CAP-029, CAP-030, CAP-040, CAP-044, CAP-048, CAP-049, CAP-052, CAP-054, CAP-055, CAP-058. No ownership transfer. CAP-001…CAP-058 remain preserved.

## 6. Requirement mapping
Configuration = desired behavior; Policy = admissibility; Authorization = principal/operation authority; Runtime State = actual effective state; P0-04 = sole mutation authority; controlled P0-05 ingress; deterministic fail-closed evaluation; bounded immutable non-executable representations; stale fail-closed; inert AI/plugin proposals; no unauthorized persistence/execution/network behavior.

Historical requirement completeness: EVIDENCE_GAP.

## 7. Contract mapping
Relevant: CTR-001, CTR-002, CTR-003, CTR-004, CTR-005, CTR-006, CTR-009, CTR-010, CTR-012, CTR-013, CTR-014, CTR-015, CTR-016, CTR-017, CTR-018, CTR-019, CTR-020, CTR-021, CTR-023, CTR-024, CTR-025, CTR-026, CTR-029, CTR-031, CTR-032, CTR-035, CTR-036.
No contract is changed by this result.

## 8. Invariant mapping
Relevant protected invariants include INV-001, INV-002, INV-003, INV-005, INV-006, INV-007, INV-008, INV-009, INV-010, INV-014, INV-015, INV-016, INV-018, INV-020, INV-021, INV-022, INV-023, INV-024, INV-025, INV-026, INV-027, INV-028, INV-029, INV-030.
No invariant is changed.

## 9. Decision mapping
Directly relevant accepted decisions: DEC-001, DEC-002, DEC-005, DEC-006, DEC-008, DEC-009, DEC-010, DEC-012. DEC-A-001…DEC-A-004 remain DRAFT.

## 10. Architecture/boundary mapping
Configuration/Policy is a cross-cutting control contour above the frozen state/consumer/security/runtime boundaries. Canonical path: validation → policy → authorization → consumer boundary → State Authority → runtime application. No direct mutation or alternate authority.

## 11. Classification
RETAIN: desired-behavior configuration, admissibility policy, deterministic fail-closed evaluation, authorization separation, sole State Authority, bounded immutable representations.
REMAP: P0-05 interaction and proposal/AI/plugin boundaries as supporting cross-cutting mechanisms.
RECONCILE: P0-07→P0-05 authorization composition.
UNKNOWN: complete historical MH-07 corpus, exact runtime/persistence/observability implementation semantics.
REPLACE: none established by this reconciliation.
RETIRE: none justified.

## 12. Contradictions
Primary open contradiction: current P0-07 publication requires composition of domain authorization with lower-layer authorization, while the current P0-05 surface has no approved composition mechanism. This is a governance/API gap, not permission to alter frozen P0-03…P0-06.

## 13. Missing evidence
Complete historical MH-07 corpus; exact historical tests/acceptance; authorization composition decision; runtime application/rollback evidence; persistence authorization; observability/privacy evidence.

## 14. Dangling/stale references
Historical pre-reconstruction ownership/contract references require registry comparison. P0-07 implementation state must not be treated as accepted architecture. Exact implementation HEAD must always be re-read before verification claims.

## 15. Proposed technical decisions
None closed. Open: authorization composition, runtime application, rollback/partial application, persistence, observability/privacy.

## 16. Contract impacts
Potential future impact only; no current registry modification. Most relevant are CTR-001/002/003 and the operational contracts listed above.

## 17. Invariant impacts
No change proposed. Existing invariants are preserved and strengthened by the MH-07 contour.

## 18. Dependency impacts
No dependency edge change proposed. MH-07 spans security_core, runtime_core, command/automation/scheduling, device/configuration, lifecycle/recovery, data/storage, assistant/plugin and verification boundaries.

## 19. Verification requirements
Targeted P0-07 tests, full regression, security/capability/forbidden-call scans, persistence scan, exact-head evidence, authorization-composition tests, lifecycle/mode tests, stale-update tests, runtime application/failure evidence, privacy/observability evidence and clean/synchronized repository state.

## 20. Acceptance evidence
Current P0-07 PR #17 is open/draft. Its stated verification gate requires targeted/full regression plus security/persistence scans before merge. Current GitHub PR snapshot reports head `83ccb0d4993761ffcd43146d982ff9781116c7db`. Available commit-status surface returned no statuses. Therefore P0-07 is not VERIFIED/ACCEPTED/FROZEN.

## 21. Acceptance authority
Explicit governance/human acceptance after evidence and central reconciliation.

## 22. Remaining OPEN items
Historical corpus completeness; authorization composition; implementation verification; runtime semantics; persistence; observability/privacy; governance acceptance/freeze.

## 23. Anti-loss confirmation
PASS. No CAP is removed, retired or reassigned. UNKNOWN/EVIDENCE_GAP remains explicit. All CAP-001…CAP-058 remain preserved.

## 24. Suggested canonical registry changes
No mandatory change. Optional central proposals: explicit cross-cutting Configuration/Policy architecture boundary; dedicated authorization-composition contract if approved; traceability references from affected capabilities/contracts.

## 25. Authority statement
MH-07 has no unilateral authority to apply any registry, architecture, ownership, invariant, decision or production-gate change.
