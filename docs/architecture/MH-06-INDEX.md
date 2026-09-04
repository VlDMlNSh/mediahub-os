# MH-6 — Architecture Index

Status: PROPOSED / REQUIRES VERIFICATION

## Canonical role
MH-6 defines Core Runtime Services as orchestration around the sole canonical mutation authority P0-04, with P0-05 as the mandatory integration/authorization boundary.

## Required artifacts
- MH-06-core-runtime-services.md
- MH-06-runtime-service-model.md
- MH-06-lifecycle-model.md
- MH-06-startup-shutdown.md
- MH-06-health-readiness.md
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
- MH-06-ARCHITECTURE-CHAT-CHARTER.md
- MH-06-CHAT-MASTER-PROMPT.md
- MH-06-REVERSE-MASTER-PROMPT.md

## Baseline
P0-04 State Authority: ACCEPTED / FROZEN.
P0-05 Consumer Boundary: ACCEPTED / FROZEN.
P0-06 architecture/service/lifecycle contracts: ACCEPTED; implementation/production qualification remains separately evidenced.
P0-07: implementation in progress; mutation publication blocked by governance/API gap.

## Governance
This index and the referenced artifacts are architecture records, not an implementation workspace. Development must occur in a separate development chat and consume these artifacts through the master/reverse-master prompt mechanism.
