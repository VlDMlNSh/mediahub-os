# MH-03 Runtime Model

## Planes
- Control: lifecycle, orchestration, policy/authorization interaction.
- Data: canonical runtime state and events.
- Management: diagnostics, health, configuration, recovery.
- Intelligence: receives proposals/requests from AI without canonical authority.
- Integration: interacts through consumer contracts; external systems have no direct authority.

## Logical components
Runtime Coordinator; Lifecycle Manager; Dependency Manager; Service Supervisor; Command Executor; Event Dispatcher; Health Manager; Configuration Manager; Recovery Manager; Diagnostics/Observability Adapter.

Logical component does not imply separate process/package/API.

## Authority
`Runtime coordinates → governed command path → State Authority mutates → Event → observers.`
No runtime component may self-grant capability or maintain a canonical shadow store.
