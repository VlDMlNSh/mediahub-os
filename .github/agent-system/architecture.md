# MediaHub Agent Fabric Architecture

Status: CANONICAL DEVELOPMENT GOVERNANCE
Authority: MH-1…MH-25 + Functional Baseline 2.0
Date: 2026-10-01

## Topology

Human remains final authority for global architecture, production deployment, destructive migrations, security-sensitive decisions and permanent agent-governance changes.

A0 Astra is the single coordination authority and is not the single writer.
A1 Architect, A2 Builder and A3 Verifier are persistent profiles; runtime instances are task-scoped.
Additional workers are dynamic task-scoped instances of these roles.

Astra -> Architect / Builder / Verifier -> Integration Gate -> Canonical State -> Functional Baseline.

## Runtime distinction

Profile = repository role definition.
Instance = one role execution for one mission.
Session = concrete runtime context.
Coordination = Astra scheduling/reconciliation.
State = machine-readable task, claim and evidence state.
Governance = architecture, policy, limits and authority boundaries.

A profile does not imply a permanently running process.

## Adaptive topology

Small: Astra -> Builder -> Verifier.
Medium: Astra -> Architect + Builder -> Verifier.
Large: Astra -> Architect + 2-3 independent Builders -> Verifier.
Architecture conflict: Astra -> Architect -> Builder -> Verifier -> Architect -> Astra.

Parallelism is used only for genuinely independent boundaries.

## Integration

Only verified work is integrated. Astra performs post-integration verification and architecture reconciliation before close.
