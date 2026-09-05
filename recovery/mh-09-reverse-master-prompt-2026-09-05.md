# MH-09 REVERSE MASTER PROMPT — 2026-09-05

MH identifier: MH-09
Historical scope: Presentation / UI architecture.
Reconciliation status: RECONCILED WITH AVAILABLE EVIDENCE / HISTORICAL CORPUS PARTIAL.

## 1. Source evidence / provenance
- Current control point: `recovery/forensic-control-point-2026-09-05.md`.
- Redistribution master prompt and handoff prompt on `recovery/full-functional-spec`.
- Canonical projection matrix: `recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml`.
- Canonical capability registry: CAP-001…CAP-058.
- Contract registry: CTR-001…CTR-036.
- Invariant registry: INV-001…INV-030.
- Decision registry: DEC-001…DEC-012 accepted; DEC-A-001…DEC-A-004 draft.
- Master Architecture: DRAFT / NOT ACCEPTED.
- Development baseline: NOT_AUTHORIZED_FOR_IMPLEMENTATION.
- Historical MH-09 architecture evidence available in this architecture chat and persisted under `docs/architecture/MH-09-*` on branch `architecture/mh-09-presentation-ui`.

## 2. CAP mapping
Primary: CAP-045 -> ui_core; CAP-046 -> mobile_media.
Cross-cutting presentation projections preserve, without ownership transfer, all relevant device, automation, surveillance, media, mobile, engineering, cluster, assistant, lifecycle, security, privacy, notification, search/knowledge, resource and variant capabilities.

## 3. Requirement mapping
UI is a presentation/consumer layer; bounded read models; explicit user intent; authorized commands; inert proposals; operation-specific capabilities; separate UI/auth/runtime lifecycles; navigation/deep links are not security boundaries; honest freshness and offline semantics; explicit optimistic outcomes; safe stale/conflict handling; bounded retry; form/draft separation; privileged/admin/diagnostic/emergency boundaries; AI recommendation != command; plugin UI is capability-scoped; notification actions re-enter authorization; accessibility/localization/privacy are architectural concerns; platform-specific presentation does not alter canonical domain semantics.

## 4. Contract mapping
Primary/downstream contracts: CTR-002, CTR-003, CTR-006, CTR-007, CTR-008, CTR-009, CTR-010, CTR-011, CTR-012, CTR-014, CTR-016, CTR-018, CTR-019, CTR-020, CTR-021, CTR-022, CTR-024, CTR-025, CTR-026, CTR-027, CTR-028, CTR-029, CTR-030, CTR-031, CTR-032, CTR-033, CTR-034, CTR-035, CTR-036. CTR-001 remains the ultimate state-authority boundary; UI never becomes an alternate authority.

## 5. Invariant mapping
Directly reinforced: INV-001, INV-002, INV-005, INV-006, INV-007, INV-008, INV-009, INV-010, INV-014, INV-015, INV-016, INV-018, INV-019, INV-020, INV-021, INV-022, INV-023, INV-024, INV-025, INV-026, INV-027, INV-028, INV-029, INV-030.

## 6. Decision mapping
RETAIN/REMAP against DEC-001…DEC-012. MH-09 does not promote DEC-A-001…DEC-A-004.

## 7. Architecture / boundary mapping
`Human -> UI -> Presentation/Read/Interaction Model -> Consumer Boundary -> Capability/Authorization/Policy -> Command or Proposal -> State Authority/controlled subsystem -> canonical state -> event/read model -> UI`.
UI is not State, Policy, Authorization, Runtime, Persistence, Security or AI authority. Home Assistant remains internal; its UI is not the canonical MediaHub UI.

## 8. Classification
RETAIN: authority separation, MediaHub user-facing model, read/command/proposal semantics, authorization path, offline/freshness, privacy/accessibility/localization, AI/plugin/notification boundaries.
REMAP: historical presentation mechanisms to canonical ui_core/mobile_media and Consumer Boundary.
RECONCILE: any direct UI authority, persistence, device, shell, unrestricted network, plugin execution or hidden authorization/retry/merge behavior.
REPLACE: only where an accepted canonical decision supersedes an old assumption.
RETIRE: NONE.
UNKNOWN: exact historical implementation/framework/transport/component technology and inaccessible historical material.

## 9. Contradictions
No ownership contradiction established. Authority leakage remains the principal reconciliation hazard.

## 10. Missing evidence
Complete historical MH-09 corpus is not independently available on the recovery branch. This is EVIDENCE_GAP, not function loss.

## 11. Dangling / stale references
None established from available evidence. Exact implementation references remain verification items.

## 12. Proposed technical decisions
None closed. Concrete UI framework, mobile transport, rendering architecture, plugin UI technology, cache/persistence implementation and platform-specific component decisions remain OPEN / EVIDENCE-BLOCKED.

## 13. Contract / invariant impacts
No canonical registry change requested. No negative invariant impact identified.

## 14. Dependency impacts
Presentation depends on presentation models, Consumer Boundary, authorization/policy and authorized runtime read paths. No reverse dependency from State Authority into UI internals.

## 15. Verification requirements
Contract/security/integration/failure/accessibility tests must cover authorization, read-model bounds, stale generations, optimistic outcomes, offline honesty, notification actions, AI non-execution, plugin scoping, privileged UI, direct-authority shortcut detection and product variants.

## 16. Acceptance evidence / authority
MH-09 architecture package is persisted on `architecture/mh-09-presentation-ui`, but remains PROPOSED / REQUIRES VERIFICATION. Acceptance authority is central governance plus explicit human acceptance after all MH results are reconciled.

## 17. Anti-loss
FULL CANONICAL BASELINE PRESERVED: 58/58 capabilities remain accounted for. No capability was removed, retired or reassigned by MH-09.

## 18. Suggested canonical registry changes
NONE.

## 19. Explicit authority limitation
MH-09 has no unilateral authority to modify canonical registries or accepted decisions.

## 20. Production gate
BLOCKED. No production implementation, irreversible migration, technology lock-in or implementation commitment is authorized by this result.
