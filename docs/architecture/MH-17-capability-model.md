# MH-17 — Capability Model

**Status:** CANDIDATE

A capability is an explicit, versioned declaration of an operation or observation surface. Capability declaration is not authorization.

Candidate shape:
`namespace + operation + target + data schema/bounds + safety class + authorization requirement + reversibility + audit level`.

Examples remain illustrative only: `power.read`, `power.control`, `temperature.read`, `temperature.set`, `media.play`, `media.stop`.

The repository already defines capability objects with id/type/version/status, properties, commands, events, constraints, dependencies, conflicts, safety class and discovery state. fileciteturn7file0L2-L5

Required security invariant: an adapter may expose only capabilities declared by its contract; runtime authorization must independently validate caller, device, operation, target, policy and safety context.

**UNKNOWN:** canonical capability ID registry, command schemas, target schemas and safety taxonomy governance are not yet established.