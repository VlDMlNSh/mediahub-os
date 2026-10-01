# Agent Roles

| ID | Role | Persistent profile | Runtime | Write authority |
|---|---|---|---|---|
| A0 | Astra / Coordinator | yes | task/session | coordination + bounded integration |
| A1 | Architect | yes | task-scoped | proposal/contract; bounded implementation if assigned |
| A2 | Builder | yes | task-scoped | assigned owned paths |
| A3 | Verifier | yes | task-scoped | verification artifacts only |

Dynamic workers reuse A1/A2/A3. Do not create permanent Storage/UI/Network/ML/etc. roles without a later architecture-change stage proving necessity.
