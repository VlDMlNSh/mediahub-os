# MH-07 RECONCILIATION — 2026-09-05

## Status

MH-07 historical reconciliation: **UNKNOWN / EVIDENCE_GAP for exact historical corpus**.

MH-07 canonical projection: **RECONCILED AS A CURRENT CROSS-CUTTING CONFIGURATION/POLICY CONTOUR**, based on the available MH-7 architecture-chat evidence and the canonical registries. This does not reconstruct unavailable historical MH-07 material.

Production implementation: BLOCKED.
Master Architecture: DRAFT / NOT ACCEPTED.
Canonical registry mutation authority: NONE.

## 1. Historical scope

Projection matrix marks MH-07 as a historical contour whose exact corpus requires recovery. The accessible evidence surface in this chat contains a developed MH-7 Configuration/Policy architecture, its evidence/decision/contradiction/unknown artifacts, and implementation-boundary material, but not a complete export of the original historical MH-07 corpus.

Therefore historical completeness is not claimed.

## 2. Source evidence and provenance

Authoritative GitHub baseline inspected:
- recovery/forensic-control-point-2026-09-05.md
- recovery/MASTER-PROMPT-NEW-CHAT-MH01-23-REDISTRIBUTION-FINAL-2026-09-05.md
- recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml
- specification/capability-registry.yaml
- specification/contract-registry.yaml
- specification/invariant-registry.yaml
- specification/decision-registry.yaml
- specification/dependency-graph.yaml
- architecture/master-mediahub-architecture-reconstruction-2026-09-05.md
- development/implementation-map.yaml
- development/baseline.yaml
- recovery/functional-themes/chat-2026-09-05-accepted.md

Additional MH-07 evidence available in the current architecture contour includes:
- docs/architecture/MH-07-configuration-policy.md
- MH-07 evidence register, decision log, contradiction register and unknowns
- MH-07 Master Prompt / Reverse Master Prompt
- P0-07 implementation boundary and PR #17 metadata

Provenance rule: GitHub canonical baseline is authoritative; current chat material is supporting evidence and does not override canonical registries.

## 3. CAP mapping

MH-07 does not claim unique ownership of any CAP. Configuration/policy is a cross-cutting control mechanism supporting capabilities whose canonical owners remain unchanged.

Directly relevant capability families include:
- CAP-029 device discovery/identification/configuration lifecycle
- CAP-030 authenticated and authorized device commands
- CAP-040 security/trust/authentication/authorization
- CAP-044 update/firmware lifecycle
- CAP-048 resource quotas/priority/workload governance
- CAP-049 vendor/protocol/ecosystem extensibility
- CAP-052 device lifecycle
- CAP-054 contextual installation/configuration guidance
- CAP-055 privacy-governed presence context
- CAP-058 security/safety system invariant

This list is a projection of relevance, not an ownership transfer. All CAP-001…CAP-058 remain preserved.

## 4. Requirement mapping

Canonical requirements inferred from the reconciled MH-07 contour:
- configuration expresses desired behavior;
- policy expresses admissibility under declared conditions;
- authorization expresses principal/operation authority;
- runtime state expresses actual effective state;
- configuration/policy cannot become mutation authority;
- policy evaluation is deterministic and fail-closed;
- publication passes the controlled consumer boundary and State Authority;
- stale candidates fail closed;
- proposal/AI/plugin sources remain inert;
- physical persistence is not authorized by MH-7;
- critical behavior remains fail-safe;
- all configuration/policy inputs remain bounded, immutable and non-executable.

Historical requirement completeness: EVIDENCE_GAP.

## 5. Contract mapping

Relevant canonical contract families:
- CTR-001 state-authority
- CTR-002 consumer-boundary
- CTR-003 identity-authentication-authorization
- CTR-004 trust
- CTR-005 discovery-onboarding
- CTR-006 device-command
- CTR-009 automation
- CTR-010 scheduling
- CTR-012 surveillance
- CTR-013 surveillance-storage
- CTR-014 personal-media-storage
- CTR-015 storage-management
- CTR-016 network
- CTR-017 cluster
- CTR-018 cloud-development-boundary
- CTR-019 assistant-escalation
- CTR-020 health
- CTR-021 readiness
- CTR-023 recovery
- CTR-024 update-lifecycle
- CTR-025 migration
- CTR-026 privacy
- CTR-029 ecosystem-projection
- CTR-031 guidance
- CTR-032 export
- CTR-035 resource-governance
- CTR-036 verification-acceptance

MH-07 does not replace or redefine these contracts. It composes with them where configuration/policy participates in admissibility or operation authorization.

## 6. Invariant mapping

Primary relevant invariants:
- INV-001 function preservation
- INV-002 security by design
- INV-003 discovery != trust
- INV-005 authentication != authorization
- INV-006 remote access does not increase authorization
- INV-007 ordinary user has no Cloud Development access
- INV-008/009 local-first/offline-first direction
- INV-010 surveillance storage != personal media storage
- INV-014 user works with MediaHub semantics rather than protocol internals
- INV-015/016 Home Assistant internal; MediaHub user-facing authority
- INV-018 product variants preserve functional differences
- INV-020 physical connection != authorization
- INV-021 security is system-level
- INV-022 health observation-only
- INV-023 readiness operation-scoped
- INV-024 health/readiness/liveness/trust/authorization remain distinct
- INV-025 internal topology hidden from ordinary users
- INV-026 historical evidence preserved
- INV-027 unique canonical ownership
- INV-028 professional/engineering contour distinct
- INV-029 local cluster != cloud development cluster
- INV-030 direct MediaHub surveillance recording remains preserved

No MH-07 finding authorizes weakening any invariant.

## 7. Decision mapping

Directly constraining accepted decisions:
- DEC-001 functional baseline is primary product truth
- DEC-002 Home Assistant internal; MediaHub user-facing
- DEC-005 local/offline-first direction
- DEC-006 privileged Cloud Development
- DEC-008 health/readiness distinction
- DEC-009 system-level security
- DEC-010 product-variant differences
- DEC-012 deferred detail is not rejection

Architecture proposals DEC-A-001…DEC-A-004 remain DRAFT and are not promoted by this result.

## 8. Architecture / boundary mapping

Canonical MH-07 boundary:
Configuration → Validation → Policy Evaluation → Principal Authorization → Consumer Boundary → State Authority → Runtime Application.

Configuration and Policy are not State Authority, persistence, authorization issuer, runtime mutation primitives, executable extension points, or alternate state stores.

AI/plugin/external proposal sources are inert and must use the same controlled path.

## 9. Classification

| Historical/current material | Classification | Reason |
|---|---|---|
| Configuration as desired behavior | RETAIN | Semantically compatible with canonical baseline |
| Policy as admissibility | RETAIN | Compatible with authorization separation |
| Explicit principal authorization boundary | RETAIN | Reinforces CTR-003 and security invariants |
| P0-05 controlled ingress | REMAP | MH-07 composes through existing canonical boundary |
| P0-04 sole mutation authority | RETAIN | Canonical invariant |
| Deterministic deny-by-default policy evaluation | RETAIN | Fail-closed security semantics |
| AI/plugin proposal-only boundary | REMAP | Supporting mechanism; no authority transfer |
| Physical persistence selection | UNKNOWN / EVIDENCE_GAP | Not authorized by current MH-7 contour |
| Exact historical MH-07 corpus | UNKNOWN / EVIDENCE_GAP | Not accessible in complete form |
| Any proposed lower-layer contract modification solely to unblock P0-07 | REJECTED AS NON-AUTHORIZED / retain blocker | Frozen lower layers cannot be changed by MH-07 |

No RETIRE classification is justified.

## 10. Contradictions

### C-01 — P0-07 publication authorization composition
Current MH-07 implementation boundary requires policy authorization plus lower-layer authorization. Existing P0-05/P0-04 composition does not expose an already-approved bridge for translating/composing these authorization contexts.

Disposition: RECONCILE / OPEN. Do not bypass by modifying frozen P0-03…P0-06.

### C-02 — Historical contour vs developed current contour
Projection matrix marks exact historical MH-07 corpus UNKNOWN, while current architecture evidence provides a detailed MH-7 configuration/policy contour.

Disposition: RECONCILE. Current contour is usable as architecture evidence but is not asserted to be a complete historical reconstruction.

No other contradiction is evidenced from the available corpus.

## 11. Missing evidence

- complete historical MH-07 chat export/corpus;
- complete historical requirement list and original terminology;
- complete historical MH-07 test/acceptance evidence;
- authoritative resolution of P0-07→P0-05 authorization composition;
- verified runtime application/rollback/recovery evidence;
- exact persistence semantics if later authorized;
- exact observability/privacy telemetry evidence.

## 12. Dangling/stale references

Dangling/stale references requiring follow-up:
- any historical MH-07 references to pre-reconstruction ownership or contracts must be checked against current registries;
- P0-07 implementation references must not be interpreted as accepted architecture;
- exact implementation branch/HEAD is mutable and must be re-read before verification claims.

No registry reference is silently rewritten by this result.

## 13. Proposed technical decisions

No technical decision is closed here.

OPEN/EVIDENCE-BLOCKED:
1. P0-07→P0-05 authorization composition.
2. Exact runtime application semantics.
3. Partial-application and rollback semantics.
4. Physical persistence model for configuration/policy.
5. Exact observability/privacy telemetry contract.

Each requires evidence → alternatives → constraints → decision → contract update → invariant impact → verification criteria → acceptance authority.

## 14. Contract impacts

No canonical contract is changed.

Potential future impact is concentrated in CTR-001, CTR-002, CTR-003, CTR-005, CTR-006, CTR-009, CTR-010, CTR-020/021, CTR-023/024/025, CTR-026, CTR-031/032, CTR-035 and CTR-036.

## 15. Invariant impacts

No invariant change proposed.

The principal MH-07 security invariants are strengthening constraints, not new canonical registry entries at this stage.

## 16. Dependency impacts

MH-07 is cross-cutting over security_core, runtime_core, smart_home/device management, command_system, automation/scheduling, storage/data, lifecycle/recovery, assistant/plugin boundaries and verification.

No new dependency edge is proposed because the current dependency graph already contains the relevant canonical nodes and security boundaries.

## 17. Verification requirements

Before MH-07 can be accepted/frozen:
- complete P0-07 targeted test execution;
- full regression;
- security/capability/forbidden-call scans;
- persistence scan;
- exact-head evidence;
- authorization-composition tests;
- lifecycle/mode tests;
- stale revision tests;
- runtime application/failure evidence;
- observability/privacy evidence;
- clean synchronized repository state.

## 18. Acceptance evidence and authority

Acceptance authority is governance/human authority, not MH-07.

Required acceptance evidence must be tied to exact commits and reproducible tests. PR #17 is currently open/draft and its own description states execution evidence is still required before merge. The current GitHub snapshot reports head `83ccb0d4993761ffcd43146d982ff9781116c7db`; no CI statuses were returned for that commit through the available status surface.

## 19. OPEN items

- exact historical MH-07 corpus recovery;
- P0-07→P0-05 authorization composition;
- implementation verification;
- runtime application semantics;
- persistence authorization/design;
- final observability/privacy evidence;
- governance acceptance/freeze.

## 20. Anti-loss confirmation

**PASS — no function is removed.**

CAP-001…CAP-058 remain preserved. No MH-07 finding changes ownership or retires a capability. The canonical baseline explicitly requires unknown historical material to remain UNKNOWN/EVIDENCE_GAP rather than loss.

MH-07 cross-cutting configuration/policy semantics do not remove direct surveillance recording, vendor integrations, energy, networking, media, gaming, ecosystem, assistant, engineering, cluster, lifecycle, recovery, offline-first, security, privacy, automation, scheduling, events, notifications or other capabilities.

## 21. Suggested canonical registry changes

No mandatory registry change.

Optional future proposals, subject to central reconciliation only:
- add explicit Configuration/Policy cross-cutting boundary to the master architecture;
- add a dedicated authorization-composition contract only if evidence and governance approve it;
- add explicit traceability references for configuration/policy participation in affected CAP/CTR items.

These are suggestions only.

## 22. Authority statement

This MH-07 reconciliation has **NO unilateral authority** to modify CAP, CTR, INV, DEC, dependency graph, Master Architecture acceptance state, or production authorization.
