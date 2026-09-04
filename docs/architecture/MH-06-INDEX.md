# MH-6 — Architecture Index

Status: HEALTH / READINESS SEMANTIC CONTRACT ACCEPTED; MH-6 OVERALL NOT FROZEN

## Canonical role
MH-6 defines Core Runtime Services as orchestration around the sole canonical mutation authority P0-04, with P0-05 as the mandatory integration/authorization boundary.

## Health / Readiness governance state
`MH-06-ADR-001-health-readiness-semantic-contract.md` is GOVERNANCE ACCEPTED at commit `1d6e9cd6ad320fff752c6ec6e1aa8a94525ef5be`.

The accepted contract separates P0-06 lifecycle, Health observation and operation-scoped Readiness. It defines bounded inputs, dependency classification, deterministic precedence, failure semantics and quarantine semantics without creating a second authority path.

## Required artifacts
- MH-06-core-runtime-services.md
- MH-06-runtime-service-model.md
- MH-06-lifecycle-model.md
- MH-06-startup-shutdown.md
- MH-06-health-readiness.md
- MH-06-ADR-001-health-readiness-semantic-contract.md
- MH-06-supervision.md
- MH-06-scheduling.md
- MH-06-resource-governance.md
- MH-06-execution-context.md
- MH-06-dependency-model.md
- MH-06-recovery-model.md
- MH-06-failure-domains.md
- MH-06-ipc-boundary.md
- MH-06-observability.md
- MH-06-security-invariants.md
- MH-06-configuration-policy-interaction.md
- MH-06-ai-runtime-interaction.md
- MH-06-persistence-boundary.md
- MH-06-update-recovery-boundary.md
- MH-06-dependency-map.md
- MH-06-evidence-register.md
- MH-06-decision-log.md
- MH-06-contradiction-register.md
- MH-06-unknowns.md
- MH-06-acceptance-criteria.md
- MH-06-final-report.md
- MH-06-ARCHITECTURE-CHAT-CHARTER.md
- MH-06-CHAT-MASTER-PROMPT.md
- MH-06-REVERSE-MASTER-PROMPT.md

## Baseline
P0-04 State Authority: ACCEPTED / FROZEN.
P0-05 Consumer Boundary: ACCEPTED / FROZEN.
P0-06 architecture/service/lifecycle contracts: ACCEPTED / FROZEN; implementation verification and production qualification remain separately evidenced.
P0-07: implementation in progress; mutation publication blocked by governance/API gap.

## Evidence control
Historical P0-06 acceptance at `d9b5c9db128d8ec75dae6fbd03b5d54950bdddf5` remains historical evidence. Current reproducible CI for that exact frozen implementation is NOT VERIFIED.

## Governance
The Health/Readiness semantic contract is accepted. MH-6 as a whole is not frozen and does not grant implementation authorization or production qualification. Development must remain separate and stopped for Health/Readiness until a distinct scoped implementation authorization is granted.
