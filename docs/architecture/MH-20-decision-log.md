# MH-20 Decision Log

| ID | Decision | Alternatives | Rationale / Evidence | Status |
|---|---|---|---|---|
| D-20-001 | Automation is orchestration, not authority | Separate automation authority | Preserves P0-03/P0-04 | ACCEPTED AS ARCHITECTURAL CONSTRAINT |
| D-20-002 | Every mutation reaches Policy → Authorization → Consumer Boundary → State Authority | Direct automation/device mutation | Preserves P0-03/P0-05 | ACCEPTED AS ARCHITECTURAL CONSTRAINT |
| D-20-003 | Architecture chats remain non-development workspaces | Mixed architecture/development chat | Repository governance record | ACCEPTED |
| D-20-004 | GitHub is durable external architecture record | Chat-only history | Long-term traceability | ACCEPTED |
| D-20-005 | SINGLE NODE / NO HA remains canonical | Distributed automation workers | Explicit MH-20 baseline | ACCEPTED |
| D-20-006 | Critical/destructive automation requires explicit gates | Autonomous execution | Safety/security boundary | ACCEPTED |

These decisions do not constitute implementation authorization.