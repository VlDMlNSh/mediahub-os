# MH-03 Service Boundaries

**Status:** PROPOSED

| Boundary | Responsibility | Authority restriction |
|---|---|---|
| Runtime Coordinator | orchestration | no canonical mutation |
| Lifecycle Manager | startup/shutdown/restart | no domain mutation |
| Dependency Manager | dependency readiness/order | no authorization inheritance |
| Service Supervisor | liveness/restart/isolation | no state authority |
| Command Executor | governed execution | must use canonical path |
| Event Dispatcher | fact propagation | events cannot imply mutation |
| Health Manager | readiness/health | observer/control only |
| Configuration Manager | load/validate config | policy-governed |
| Recovery Manager | bounded recovery | no shadow authority |
| Observability Adapter | diagnostics/telemetry | non-mutating |

Logical boundaries do not imply separate processes, containers or specific technologies.
