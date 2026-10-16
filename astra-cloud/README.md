# Astra Cloud Runtime

Initial executable-boundary specification for the MediaHub Astra cloud control plane.

## Runtime modules

- api: authenticated task ingress and status retrieval
- compiler: command to typed execution plan
- registry: agent capability and policy metadata
- router: eligibility-based agent selection
- runtime: bounded agent execution
- reconcile: output/artifact validation and terminal state transition
- audit: append-only execution events
- providers/openai: server-side OpenAI adapter

## Invariants

1. Provider secrets never enter task payloads, agent context, artifacts, logs, or iOS responses.
2. Agent capability is not authorization; policy must authorize each tool/action.
3. Every execution has a stable task_id and request_id.
4. Terminal state requires reconciliation.
5. Host operations require an enrolled host identity and scoped tool authorization.

## State machine

queued -> running -> blocked -> running -> succeeded|failed|cancelled

A task may enter blocked when an approval, host, dependency, or required capability is unavailable.
