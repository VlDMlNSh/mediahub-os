# Agent Boundaries and Claim Policy

A claim contains:
agent, task_id, goal, paths, exclusive_actions, dependencies, status, started, updated, expiry, base_sha.

Collision rules:
- exact write collision: BLOCK
- incompatible path overlap: BLOCK
- compatible read-only overlap: allowed
- shared contracts/schemas/generated outputs: one writer
- expired claims require explicit expiry/release evidence

No worker may force-push, expose credentials, mutate production, perform destructive cleanup, or change security policy without explicit authority.

A claim grants coordination ownership only; it never grants MediaHub domain authority.
