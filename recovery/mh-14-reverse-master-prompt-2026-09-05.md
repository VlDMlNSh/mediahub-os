# MH-14 REVERSE MASTER PROMPT — 2026-09-05

## 1. MH identifier
MH-14 — Persistence Architecture.

## 2. Historical scope
Persistence, durable state representation, storage domains, recovery, snapshots, restore, backup, durability, consistency, atomicity, crash/power-loss semantics, integrity, encryption-at-rest boundary, retention/deletion, schema/migration/rollback, isolation, resource/capacity behavior, offline/cloud persistence and interfaces to State Authority, runtime, configuration/policy, AI, plugins, UI and observability.

Projection matrix: `development interface/persistence`; canonical projection domains: `cloud_development`, `data_core`, `ui_core`. The historical scope is cross-cutting and must not be reduced to those labels as ownership.

## 3. Source evidence / provenance
Authoritative branch evidence:
- control point SHA `203e38cfeb0282991307a32a6566c4f7f4e0e506`
- successor master prompt SHA `9972f6952e5fafd71edbb780e7fe5110ae4bd1f9`
- projection matrix SHA `d4c65f38899006b258c0a8f013d7398203e951ee`
- capability registry SHA `1f3a061ac75cedc4374f852f13fdce6ea9c7ecbb`
- contract registry SHA `84b4ecbf3150e50dd5d4fe3101b5087a272beefe`
- invariant registry SHA `b4a254eec855f3fede893f2de1fa123ad051268a`
- decision registry SHA `b66ac89287ec1b74b71b7be1465d1c3e3fab13a4`
- dependency graph SHA `a49d3df79268df5412055c5fc71f29fab0671260`
- master architecture SHA `2503f093322ce089498ac5e57b30c8c5b762d840`
- implementation map SHA `42f5ffb2d2835d7981cb275eeda4f1b7e8cbb7f6`
- current MH-14 architecture SHA `5e14084033f417722a1b04b5d5d47649dcfcda48`

Historical ChatGPT MH-14 material is treated as evidence, not canonical authority.

## 4. CAP mapping
Primary: CAP-034, CAP-036, CAP-041, CAP-042, CAP-043, CAP-039.
Cross-cutting: CAP-044, CAP-048, CAP-050, CAP-051, CAP-031, CAP-032, CAP-033.
No ownership change.

## 5. Requirement mapping
Core requirements: canonical-vs-persisted state separation; explicit durability semantics; stale-state rejection; atomic commit; crash consistency; validated recovery; authorized restore; verified backup recovery; corruption detection; integrity; retention/deletion; schema compatibility; explicit migration/rollback; storage failure/capacity handling; safe degradation; isolation; offline-first; controlled cloud boundary.

## 6. Contract mapping
Primary: CTR-001, CTR-013, CTR-014, CTR-015, CTR-023, CTR-025, CTR-026, CTR-033, CTR-035, CTR-036.
Secondary: CTR-007, CTR-010, CTR-011, CTR-012, CTR-020, CTR-021, CTR-022, CTR-024, CTR-030, CTR-032, CTR-034.

## 7. Invariant mapping
INV-001, 008, 009, 010, 018, 019, 021, 022, 023, 024, 025, 026, 027, 029 are directly implicated. MH-14's State Authority/persistence separation is an architectural guardrail derived from CTR-001 and existing authority semantics; it is not proposed here as an unapproved registry mutation.

## 8. Decision mapping
Accepted: DEC-001, DEC-003, DEC-004, DEC-005, DEC-006, DEC-007, DEC-008, DEC-009, DEC-010, DEC-012.
Draft/proposal context: DEC-A-001…DEC-A-004. None promoted.

## 9. Architecture / boundary mapping
Forward authority boundary: Consumer/Input -> Authorization -> Consumer Boundary -> State Authority -> Canonical Runtime State -> Persistence Contract -> Persistence Implementation -> Physical Storage.
Recovery boundary: Physical Storage -> validation/integrity/schema/compatibility -> Candidate State -> State Authority -> Canonical Runtime State.
Logical storage domains: System, Surveillance Recording, Personal Media Library.

## 10. Classification
RETAIN: authority separation, canonical-vs-persisted distinction, candidate-state recovery, durability semantics, atomicity prohibition, snapshots, restore authorization, backup separation, corruption model, retention/deletion, migration/rollback, isolation, safe degradation.
REMAP: persistence interfaces across runtime/data/recovery/lifecycle domains; storage implementation boundary under canonical storage ownership.
RECONCILE: projection-map wording for MH-14; relationship between persistence, data_core, storage_core, recovery_core and cloud-development interfaces.
REPLACE: none identified.
RETIRE: none; no authoritative retirement evidence.
UNKNOWN: exact historical corpus gaps and all unverified physical/technology-specific choices.

## 11. Contradictions
No canonical contradiction established. Projection-map wording may under-describe persistence's cross-cutting role; central reconciliation should decide whether to refine it.

## 12. Missing evidence / search scope
Historical corpus available to this chat plus GitHub artifacts listed above. Exact missing physical and implementation evidence is documented rather than inferred.

## 13. Dangling / stale references
No confirmed dangling registry references. Potential stale/scoping terminology exists in projection labels and requires central review only.

## 14. Proposed technical decisions
None closed. Candidates requiring evidence: storage technology, filesystem, WAL/journal, atomicity mechanism, durability semantics, backup strategy, RPO/RTO, corruption recovery, encryption/key lifecycle, migration framework, HA/replication, cloud persistence.

## 15. Contract impacts
Future concrete choices may require updates to CTR-001, CTR-013…015, CTR-023, CTR-025, CTR-026, CTR-030, CTR-033, CTR-035, CTR-036. No contract registry is modified by this prompt.

## 16. Invariant impacts
No canonical invariant changes proposed. Existing function preservation, logical storage separation, security/privacy, local/offline-first and authority boundaries remain protected.

## 17. Dependency / authority impacts
Persistence depends on State Authority, storage/recovery/migration/privacy/security and observability contracts. It must not become a second mutation authority or bypass Consumer Boundary. No dependency-graph change is requested.

## 18. Verification requirements
Require functional, crash, power-loss, corruption, stale-version, snapshot/restore, backup restore, migration/rollback, capacity/failure, security, privacy, concurrency and variant tests. Evidence must be reproducible and traceable.

## 19. Acceptance evidence / authority
Architecture acceptance and physical persistence authorization remain separate. Backup recovery capability is UNVERIFIED until successful restore plus state/runtime validation. Acceptance authority is explicit human/governance authority after central reconciliation.

## 20. OPEN items
Exact technology; filesystem; WAL/journal; durability; RPO/RTO; backup target/frequency; restore-test frequency; storage health/topology; encryption/key management; migration framework; corruption recovery; power-loss/UPS; replication/HA; cloud persistence; archival.

## 21. Anti-loss confirmation
PASS. No CAP is removed, retired or reassigned. Unknown evidence is preserved as UNKNOWN/EVIDENCE_GAP.

## 22. Suggested canonical registry changes
No mandatory change. Optional central proposal: refine MH-14 projection wording to represent persistence/storage/recovery cross-cutting relationships without changing unique capability ownership.

## 23. Authority statement
MH-14 has NO unilateral authority to apply any canonical registry change, accept Master Architecture, close technical decisions or authorize production implementation.
