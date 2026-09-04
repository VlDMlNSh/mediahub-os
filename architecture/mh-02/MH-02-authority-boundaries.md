# MH-02 — Authority Boundaries

| Domain | Authority |
|---|---|
| State Authority | Canonical mutation authority |
| Policy | Determines permitted behavior |
| Authorization | Determines execution right |
| Consumer Boundary | Restricts integration interaction |
| Runtime | Lifecycle/execution coordination |
| UI | Presentation/request generation |
| AI | Recommendation/proposal |
| Persistence | Storage mechanism |
| Observability | Observation |
| Cloud | External compute |
| External devices | External systems |

Core chain: Request → Policy → Authorization → Command → Consumer Boundary → State Authority → Canonical State → Event → Observers.
