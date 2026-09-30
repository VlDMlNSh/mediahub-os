# MH-7 — Configuration / Policy Architecture Decision Record

Status: DECISIONS ACCEPTED / IMPLEMENTATION AND QUALIFICATION PENDING
Date: 2026-09-30
Baseline: engineering/mh21-sandbox-lifecycle-20260910 @ ea7177ed099d3f0f436993571aac88b36f0a4cbc

## Owner decisions

All MH-7 architecture questions Q1-Q15 were answered with D.

| ID | Decision |
|---|---|
| Q1 | One logical Configuration Authority with distributed execution, versioning and policy control. |
| Q2 | One logical Policy Architecture: centralized governance/versioning with local evaluation where autonomy, security or latency requires it. |
| Q3 | Last qualified policy within TTL/validity; after expiry or invalidity, enter predefined safe degraded/fail-closed mode. |
| Q4 | Validate and reject invalid changes; if an already-active configuration is found invalid, automatically recover to last-known-good with integrity verification. |
| Q5 | Hierarchical deterministic resolution; security/safety/critical conflicts deny/fail closed. |
| Q6 | Adaptive configuration access: ordinary UI hides complexity; advanced/engineering layer exposes extended controls within policy. |
| Q7 | User-defined rules are permitted only in sandboxed user scope and cannot weaken security, safety or system policy. |
| Q8 | User-facing policy simulation is supported; full impact analysis is available in advanced/engineering scope. |
| Q9 | Policy-driven versioned history with full provenance for material changes and retention by data class. |
| Q10 | Hybrid Local First distribution: qualified local policy replica/cache plus centralized logical authority and controlled distribution. |
| Q11 | Declarative configuration is a primary mechanism for reproducibility, provisioning, qualification and migration, but is not runtime authority. |
| Q12 | Export/import is policy-controlled with data classification, secret separation, compatibility validation and rollback. |
| Q13 | Policy portability is supported after scope, capability, security and compatibility qualification. |
| Q14 | Policy-as-code is an internal/engineering mechanism with versioning, tests, simulation, provenance and controlled deployment. |
| Q15 | Hybrid distributed final model: unified logical Configuration and Policy architectures, distributed local evaluation/execution, strict hierarchy/precedence, Local First, qualification, rollback and fail-closed critical conflict handling. |

## Architectural consequences

1. Configuration, Policy, Canonical State and Runtime/Observed State remain separate classes.
2. Configuration is never State Authority.
3. Policy Engine is not a hidden State Authority.
4. Authorization and Policy Evaluation remain separate concerns:
   authorization establishes subject permission; policy evaluates contextual admissibility.
5. Policy is decision logic; Workflow remains orchestration.
6. Security and safety constraints have non-overridable precedence over user preferences and ordinary configuration.
7. Configuration and policy caches/replicas are non-authoritative and must be qualified, version-bound and validity-bound.
8. Critical policy/configuration conflicts fail closed; critical rollback is integrity-, dependency-, security- and compatibility-aware.
9. Offline operation is Local First but never permissive merely because central connectivity is unavailable.
10. Secrets remain outside ordinary configuration and are represented only through protected references/identifiers.
11. Git/declarative artifacts provide provenance and lifecycle input; they do not become runtime State Authority.
12. Developer policy/data domains cannot modify or weaken User policy/data domains.
13. AI remains advisory/subordinate and cannot alter its own policy limits or become policy authority.
14. Home Assistant Core remains Smart Home operational authority; MH-7 policy controls do not replace domain authority.
15. Distributed nodes expose explicit consistency/activation status such as current, pending, degraded, stale, incompatible or quarantined.
16. Critical configuration/policy mutation follows the controlled lifecycle:
    Request → Identity → Authorization → Scope → Schema Validation → Policy Validation → Conflict Check → Qualification → Commit → Version → Audit → Distribution → Activation → Verification.
17. Critical changes may require staged activation, transactional application, compensation or controlled rollback.
18. Policy simulation is non-mutating and must expose provenance/version/scope and affected-scope information.
19. Material changes require audit fields including actor, identity, source, previous/new version, reason, authorization, policy decision, target, result, timestamp and provenance.

## Precedence model

The selected architecture uses deterministic hierarchical precedence across:

platform → security → system → cluster → node → domain → service → workload → integration → user → session/context

This is not a blanket “lower level never overrides higher level” rule. Each policy/configuration class defines explicit merge and override semantics. Security, safety and other critical constraints are non-relaxable by lower scopes. Unresolved critical conflicts fail closed.

## Qualification boundary

This record captures the owner-approved architecture decisions. It does not by itself close MH-7.

MH-7 remains open until the repository contains and independently verifies the concrete contracts/implementation and evidence for:

- configuration and policy schemas;
- scope and precedence evaluation;
- deterministic conflict resolution;
- lifecycle/versioning;
- validation and qualification;
- distribution and local/offline behavior;
- simulation;
- rollback/recovery;
- audit/provenance;
- secret separation;
- declarative representation;
- export/import;
- policy portability;
- policy-as-code;
- security precedence;
- cross-domain authority boundaries;
- consistency with MH-1 through MH-6.

No runtime State Authority mutation, production/release authorization, credential handling, or hidden authority is introduced by this decision record.
