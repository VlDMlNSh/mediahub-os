# MH-03 Command Execution

Canonical path:
`Input → Integration/Capability Boundary → Validation → Policy/Authorization → P0-05 Consumer Boundary → State Authority → Canonical Mutation → Event → Observers`.

Commands are requests to change. Every executable operation must carry explicit context and bounded inputs.

Forbidden:
- UI/API direct State Authority mutation;
- AI proposal direct execution;
- plugin direct state mutation;
- device direct canonical mutation;
- cloud direct canonical mutation;
- event/telemetry as implicit command.

Stale or malformed commands are rejected. Missing authorization is denied. Runtime may coordinate execution but may not bypass P0-05.
