# Astra Cloud Architecture

Astra Cloud is the cloud orchestration plane for MediaHub OS. It complements the existing local orchestrator and does not replace the MediaHub Control Plane.

## Request flow
MediaHub iOS -> Astra API -> Task Compiler -> Agent Router -> Agent Runtime -> Tool Gateway -> provider adapters -> reconciliation -> MediaHub iOS

## Boundaries
- iOS never receives an OpenAI API key.
- Provider credentials remain server-side.
- Agents are execution workers; Astra owns orchestration, policy, state and reconciliation.
- Local/dev operations use an authenticated host gateway.
- Task and agent transitions are auditable.

## Components
- astra-api: authenticated command/status API
- task-compiler: converts commands into typed execution plans
- agent-registry: capabilities, versions, health and policy bindings
- agent-router: selects eligible agents
- agent-runtime: executes bounded jobs
- tool-gateway: controlled access to external and host tools
- provider-openai: server-side OpenAI adapter
- reconcile: validates outputs and artifacts
- audit: append-only execution events

## Hybrid execution
Cloud reasoning and orchestration may delegate privileged filesystem/build/deployment work to an enrolled MediaHub host. The host is an execution boundary, not a source of cloud credentials.
