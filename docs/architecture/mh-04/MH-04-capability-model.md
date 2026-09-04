# MH-04 Capability Model

Capability is the bounded permission to request a class of operation.

Capability != command: capability authorizes a class; command is one concrete request.

Capabilities are attached to authenticated principals under policy and context. They must be explicit, least-privilege, auditable and revocable/expirable where required.

Capability assignment never grants direct State Authority access. Domain-specific capability vocabulary is deferred to MH-05..MH-23.