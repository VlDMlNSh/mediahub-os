# MH-21 Agent Limits

Status: PROPOSED.

Mandatory limits: max iterations, tool calls, execution time, context size, generated tokens, remote requests and concurrency. Circuit breakers and cancellation are required. Exhaustion ends the agent safely; it cannot expand its capabilities.