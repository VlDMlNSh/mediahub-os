# MH-06 — Dependency Model

Status: PROPOSED

Dependency classes: hard, soft, optional, runtime. Relationship semantics include control dependency and data dependency.

Critical dependencies require explicit startup, failure, degraded-mode and recovery behavior. Critical cycles are prohibited unless explicitly justified by ADR and evidence.

Dependency readiness must not imply authorization or trust. Dependency failure must remain contained within its defined failure domain.
