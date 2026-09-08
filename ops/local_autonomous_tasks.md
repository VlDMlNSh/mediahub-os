# Local autonomous qualification queue

1. Reconcile the AI fabric order as a power-escalation path: MOBILE_AI -> LOCAL_AI -> LOCAL_CLUSTER_AI -> CLOUD_DEVELOPMENT_AI.
2. Enforce that ordinary users may reach only Mobile AI, Local AI, and Local Cluster AI; Cloud Development AI is never a user-facing endpoint.
3. Cloud Development AI is privileged MediaHub engineering infrastructure only: local/cluster AI may escalate a workload when policy determines local capacity is insufficient, with explicit authorization, data minimization, egress/residency, audit and metering.
4. Cloud Development AI never receives canonical State Authority access and never becomes runtime/home fallback authority.
5. Perform a component-gap analysis before adding dependencies. Add a component only for a demonstrated capability gap; otherwise record it as deferred and re-evaluate when the relevant wave requires it.
6. Continue contracts, invariants, negative tests, recovery/evidence and adapter boundaries for AI, cluster and iOS.
7. Treat independent review as external evidence only. The local agent may prepare qualification packages but must not self-qualify, unlock release, or authorize production.
8. Continue autonomous waves to logical completion; stop only on a hard safety/governance gate or verified absence of an actionable downstream task.
