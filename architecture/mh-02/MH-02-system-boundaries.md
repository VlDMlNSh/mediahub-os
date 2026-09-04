# MH-02 — System Boundaries

## Boundaries
B-01 Presentation: UI/API creates requests and observes state; no direct mutation.
B-02 Intelligence: AI/RAG/KG/analytics produce analysis/proposals; no authority.
B-03 Authorization: policy and authorization gate mutation-capable actions.
B-04 Integration: external devices/protocols pass adapters, normalization and consumer contracts.
B-05 State Authority: sole canonical mutation boundary.
B-06 Persistence: State Authority → Persistence Contract → future implementation; current physical persistence NOT AUTHORIZED.
B-07 OS/Hardware: Runtime → OS Services → Drivers/Kernel → Hardware.
B-08 Cloud: controlled interface to external compute; no State Authority, unrestricted shell/filesystem/credentials or direct critical device control.

Network reachability ≠ trust. VPN ≠ authorization.
