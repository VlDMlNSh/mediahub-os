# Astra UI Contract

## Status
Design contract for the future native MediaHub iOS Astra Console. The repository currently contains no Xcode project, so this step defines the boundary without fabricating an iOS implementation.

## User interaction
The UI sends a user command to Astra as a task request. The UI does not select an agent directly unless an explicit advanced-control surface is introduced later.

## Request boundary
Required concepts:
- request_id
- session_id
- user_command
- context references (not arbitrary duplicated context)
- approval state
- client metadata

The backend remains authoritative for identity, authorization, provider selection, policy, budgets, and execution.

## Streaming events
The UI should consume typed events:
- task.accepted
- task.planned
- policy.checked
- agent.selected
- execution.started
- execution.progress
- artifact.created
- validation.completed
- approval.required
- task.completed
- task.failed

Events must carry request/session/execution correlation identifiers and must not contain credentials or secrets.

## UI surfaces
1. Command composer — primary Astra interaction.
2. Execution graph — agents and execution stages.
3. Evidence/artifacts — outputs and validation evidence.
4. Approval center — explicit human approval gates.
5. Activity/audit — chronological task events.
6. Provider status — local/external availability without exposing credentials.

## Security boundary
The iOS UI is a presentation/client boundary. It must not hold provider master secrets, execute shell commands, bypass policy, or make authorization decisions.

## Local-first behavior
Astra must be able to submit tasks to Ollama without external provider credentials. External providers are opt-in and routed by the Agent Gateway.

## Token economy
The UI should send only relevant references/context. Large histories belong in persistence and are summarized before handoff according to profiles/astra-token-policy.json.

## Native implementation target
When the MediaHub iOS source becomes available, implement this contract as native Swift/SwiftUI components and a typed transport client. Do not create a parallel orchestration architecture inside the app.
