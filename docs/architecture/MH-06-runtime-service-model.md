# MH-06 — Runtime Service Model

Status: PROPOSED

| Capability | Responsibility | Authority | State ownership | Failure domain |
|---|---|---|---|---|
| Runtime Coordinator | sequence approved operations | orchestration only | none | runtime |
| Lifecycle | validate/publish lifecycle | P0-05 mediated | P0-04 only | service |
| Health/Readiness | bounded observation | observation | none | service |
| Supervisor | liveness/failure/restart control | approved policy | none | service/dependency |
| Scheduler | admission/priority/deadlines | scheduling only | none | task/runtime |
| Resource Governance | bounds/admission | resource control | none | runtime/host |
| Execution Context | identity/capability/deadline/cancel | context only | none | task |
| Dependency Coordinator | readiness/order | coordination | none | dependency group |
| Recovery | bounded recovery | explicitly gated | none | service/runtime |
| Startup/Shutdown | controlled orchestration | lifecycle coordination | none | runtime |
| Observability | metrics/logs/traces/audit context | observation | none | adapter |

Separate process/package/API boundaries are deferred to ADRs. P0-06 explicitly permits logical responsibilities without requiring separate deployment units.
