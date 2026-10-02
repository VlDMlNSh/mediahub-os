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


## G5 coordination attestation gate

Before any multi-node qualification wave is admitted to G5, each participating node MUST publish fresh evidence containing: node identity, running agent source SHA, declared coordination authority ID, coordination state location/transport, observed active-claim count, and the authority's reservation result. The evidence MUST demonstrate that the nodes participate in one coordination domain; matching environment-variable names or paths are not sufficient.

A node that cannot attest the shared authority MUST remain outside the autonomous qualification wave. The qualification controller MUST fail closed rather than silently falling back to node-local concurrency limits.

## G6 publication-recovery reconciliation

A recovery wave MUST exercise an interruption after remote result publication and before local processed-state finalization. Recovery is PASS only when the controller can identify the already-published result by command ID and source SHA, reconcile the remote branch tip, restore local processed state without rewriting evidence, and suppress duplicate execution.
