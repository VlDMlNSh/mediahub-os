# MH-7 — CONFIGURATION / POLICY ARCHITECTURE

Status: CANDIDATE ARCHITECTURE — NOT FROZEN

## 1. Canonical principle
Configuration describes desired behavior. Policy describes admissibility under declared conditions. Authorization determines whether a principal may perform a concrete operation. Runtime State describes what is actually effective. P0-04 State Authority remains the sole canonical mutation authority.

No configuration, policy, AI proposal, plugin proposal, or external source may acquire mutation authority.

## 2. Authority chain
MH-7 is a domain architecture above the frozen chain:

P0-07 domain validation/policy evaluation
→ P0-05 controlled consumer/integration boundary
→ P0-04 State Authority transaction
→ atomic commit
→ runtime application
→ observed state

P0-07 MUST NOT directly invoke P0-04. P0-05 MUST remain the controlled ingress.

## 3. Domain objects
Configuration and Policy are bounded, immutable, transient v1 domain objects. They are not persistence, checkpoints, recovery sources, or alternate state stores.

Configuration fields: identity, namespace, schema version, scope, metadata, desired value, revision/publication metadata when governed. Policy fields: identity, namespace, version/revision, scope, bounded declarative rules.

v1 scope is device-local only.

## 4. Configuration lifecycle
Absent → Candidate → Validated → Authorized → Published → Applied → Superseded; Reset/Delete are explicit terminal domain operations with separate semantics.

A Candidate is not authoritative. Validated does not mean Authorized. Authorized does not mean Published. Published does not mean Applied. Applied requires runtime evidence.

## 5. Policy lifecycle
Absent → Candidate → Validated → Authorized → Published → Active/Disabled/Dry-run/Recommendation/Supervised. Superseded, Reset, Delete and Quarantined are explicit states/modes. Emergency-disabled is a fail-safe mode, not an authority bypass.

Mode changes require explicit authorization and auditability.

## 6. Validation pipeline
Syntax → schema → semantic → policy admissibility → principal authorization → runtime applicability.

These are distinct gates. Failure is fail-closed unless a frozen lower-level contract explicitly defines another safe outcome.

## 7. Policy evaluation
Evaluation is deterministic and observational:

input → validation → normalization → exact applicable rules → decision → bounded diagnostics.

v1 semantics: malformed/unsupported/no-match/ambiguity/conflict → DENY; explicit DENY → DENY; explicit ALLOW without conflict → ALLOW. No wildcard, priority, inheritance, merge, LWW, hidden retry, or hidden conflict resolution.

## 8. Authorization boundary
P0-07 authorization is conjunctive with policy evaluation and the independently required P0-04/P0-05 authorization. P0-07 capabilities are never translated into P0-04 capabilities and cannot self-grant authority.

Current mutation publication is BLOCKED by the documented P0-07→P0-05 governance/API gap. The approved choices remain: existing-context model, explicit governance-approved authorization bridge, or revised P0-05 contract. No frozen P0-03…P0-06 contract may be changed merely to remove this blocker.

## 9. Revision/concurrency
Every authoritative configuration/policy publication requiring concurrency control must bind to the lower State Authority generation/state version. Stale candidates fail closed. No second P0-07 transaction authority, hidden merge, rebase, retry, or LWW is introduced. Cross-document atomicity is not authorized.

## 10. Runtime interaction
Canonical application:
Configuration Candidate → validation → policy → authorization → P0-05 → P0-04 transaction → atomic commit → runtime application → observed state.

Runtime consumes only validated/authorized representations. Configuration never directly mutates runtime state.

## 11. Proposals / AI / plugins / external sources
All are inert proposal sources. They may recommend, validate, analyze, or detect conflicts. They cannot publish policy, change capabilities, self-authorize, directly mutate state, or execute arbitrary code.

AI path: AI → Proposal → Validation → Policy → Authorization → Consumer Boundary → State Authority.
Plugin path is equivalent and remains bounded by the inert proposal/plugin boundary.
External/cloud policy is non-canonical in v1 and must enter through the same local validation/policy/authorization path.

## 12. Persistence boundary
Physical persistence is NOT AUTHORIZED. MH-7 specifies logical ownership only. No database, file format, cache, KV store, cloud policy service, or policy engine is selected by this architecture.

## 13. Defaults
No undocumented security-affecting default. Critical behavior defaults to fail-safe. Every future default requires owner, rationale, security impact, version semantics and evidence.

## 14. Failure semantics
Malformed configuration/policy, unsupported schema, conflicting policy, stale revision, unauthorized operation, missing capability, policy-engine failure, and runtime incompatibility fail closed: DENY / NO APPLY / transaction abort as applicable. Application failure must not be represented as successful publication.

Partial application and rollback semantics require an explicit runtime contract; they are UNKNOWN until verified. Restart recovery is also UNKNOWN while persistence is unauthorized.

## 15. Safety hierarchy
Hard Safety > Manual Emergency > Explicit Admin Policy > Local Automation > Optimization > Recommendation.

Critical operations require stronger authorization, explicit policy, stronger audit and bounded execution. AI-only approval is prohibited.

## 16. Security invariants
1. Configuration is not authority.
2. Policy is not authority.
3. Policy Engine is not State Authority.
4. Policy cannot self-grant capability.
5. AI cannot publish without authorization.
6. Plugins cannot publish without authorization.
7. Configuration/policy cannot bypass P0-05.
8. No wildcard or inheritance.
9. No hidden merge/LWW/retry/rebase.
10. Ambiguity, malformed and unsupported policy fail closed.
11. Stale revision fails closed.
12. Inputs are bounded and immutable.
13. Credentials are rejected.
14. Opaque references are inert and not dereferenced.
15. No hidden persistence/network/plugin execution.
16. P0-04 remains canonical mutation authority.

## 17. Current implementation reconciliation
The current P0-07 branch implements bounded immutable configuration/policy primitives, exact capability authorization, deterministic policy evaluation, operation validation, and inert proposal/plugin boundaries. The implementation is explicitly non-persistent, non-executable, credential-resolution-free, network-free, and does not mutate State Authority.

The evaluator implements deterministic deny-by-default semantics, including conflict denial and no wildcard/priority/inheritance/merge/retry.

The mutation adapter remains blocked because the current P0-05 surface authorizes its supplied context against P0-04 directly and no approved mechanism exists to compose P0-07 domain authorization with independently required P0-04 authorization.

## 18. Acceptance state
MH-7 architecture: CANDIDATE.
P0-07 implementation: IMPLEMENTATION IN PROGRESS / NOT VERIFIED by this architecture review.
P0-07 mutation publication: BLOCKED — GOVERNANCE/API GAP.
P0-03…P0-06: preserved as frozen baseline per supplied governance record; MH-7 does not authorize modifications.

## 19. Required verification before freeze
- repository test evidence for all P0-07 tests;
- security/persistence/capability scans;
- reconciliation of all 24 MH-7 artifacts;
- explicit decision on P0-07→P0-05 authorization composition;
- validation of lifecycle/mode semantics;
- revision and stale-update evidence;
- runtime application and failure evidence;
- privacy/observability evidence;
- governance acceptance.
