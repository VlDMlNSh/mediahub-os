# MH-02 — Failure Domains

| Domain | Degraded mode | Recovery authority |
|---|---|---|
| UI | Runtime continues | Runtime/operator |
| AI | Deterministic core | Runtime/operator |
| Integration | Isolate failed adapter | Runtime/operator |
| Network | Offline/local-first | Local runtime |
| Cloud | Local degraded operation | Local runtime |
| Policy | Fail closed | Authorized operator/recovery |
| Runtime service | Isolated/degraded service | Runtime supervisor/operator |
| State Authority | Critical degradation; no second mutation path | Recovery authority |
| Storage | In-memory where applicable | Recovery subsystem |
| OS | Service unavailable | Host recovery |
| Hardware | System unavailable/limited | Operator/recovery |

Observability must cover all domains without becoming an authority.
