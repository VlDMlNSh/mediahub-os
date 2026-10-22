# Astra Cloud API Contract v0

POST /v1/tasks

Request fields: request_id, command, context, requested_capabilities.

Response fields: task_id and state. State is one of queued, running, blocked, succeeded, failed, cancelled.

GET /v1/tasks/{task_id}

Status exposes state, plan summary, agent executions, artifacts and audit references. Secrets and provider credentials are never returned.

Agent jobs contain task_id, capability, scoped context, allowed tools and policy constraints. Agents return structured output plus artifact references. Raw credentials are prohibited.
