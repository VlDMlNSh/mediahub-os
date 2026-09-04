# MH-15 — Dependency Map

Status: ARCHITECTURE WORK IN PROGRESS

## Upstream

- MH-1 — product/governance/system charter
- MH-2 — reference architecture and system boundaries
- MH-3 — runtime foundation
- MH-4 — security/trust/authorization foundation
- MH-5 — consumer/integration boundary
- MH-6 — core runtime services
- MH-7 — configuration/policy architecture
- MH-8 — plugin/extension architecture
- MH-9 — presentation/UI architecture
- MH-10 — AI/intelligence architecture
- MH-11 — diagnostics/observability architecture
- MH-12 — security architecture
- MH-13 — privacy/data governance architecture
- MH-14 — persistence architecture
- P0-03 State Authority; P0-04 In-Memory State Authority; P0-05 Consumer Boundary; P0-06 Core Runtime; P0-07 Configuration/Policy

## Downstream

- MH-16 — installer/recovery/update architecture
- Development implementation and host qualification

## Non-negotiable dependency rules

1. Host OS, filesystem, supervisor, kernel and container runtime remain subordinate infrastructure.
2. MH-12 remains the security enforcement authority; MH-15 defines host boundaries and controls.
3. MH-14 persistence remains subordinate to State Authority.
4. MH-11 observes host/runtime events but does not become authority.
5. MH-8/MH-10 consumers cannot obtain arbitrary shell, host secrets or unrestricted device/filesystem access.
6. MH-16 installer/update/recovery mechanisms cannot become State Authority.
7. Any conflict with frozen upstream architecture requires explicit governance; no silent reconciliation.

## Current dependency verdict

No dependency has sufficient evidence to authorize host implementation. MH-15 remains WIP.
