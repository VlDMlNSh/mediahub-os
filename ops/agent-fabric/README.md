# MediaHub Agent Fabric Runtime State

Canonical governance:
- .github/agents/
- .github/agent-system/

Runtime claims are task-scoped coordination state, not MediaHub domain authority.
Claims must be machine-readable and must not contain secrets or user data.

## Execution chain

task -> claim -> worker -> verification -> commit -> evidence -> manifest update

Authoritative queued reconciliation task:
ops/agent-fabric/tasks/MH-25-23-lane-manifest.json

Task MH25-23-LANE-MANIFEST-001 is the P0 prerequisite for lane-specific autonomous promotion.

Persistent profile != persistent runtime.
A runtime is active only with observable process/session evidence.
