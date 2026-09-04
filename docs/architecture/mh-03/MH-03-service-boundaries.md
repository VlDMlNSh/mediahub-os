# MH-03 Service Boundaries

- Runtime Coordinator: orchestration only; no canonical mutation.
- Lifecycle Manager: lifecycle state and transitions; no domain mutation.
- Dependency Manager: dependency readiness/order; dependency does not imply authority.
- Service Supervisor: liveness/readiness/failure/restart; no self-granted capabilities.
- Command Executor: executes authorized commands through the governed path.
- Event Dispatcher: distributes facts; never converts events into implicit commands.
- Health Manager: bounded health/readiness observation.
- Configuration Manager: loads/validates runtime configuration within P0-07 scope.
- Recovery Manager: bounded recovery actions approved by policy.
- Diagnostics Adapter: observation only.

All access to canonical state remains through P0-05/P0-04.
