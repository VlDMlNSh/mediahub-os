# MH-7 — Privacy

Status: CANDIDATE / EVIDENCE REQUIRED

Configuration and policy must not carry credentials or hidden sensitive payloads. Opaque references remain inert and are not dereferenced by MH-7.

Diagnostics and observability must be bounded and avoid unnecessary sensitive values. Physical persistence and cloud policy synchronization are not authorized in v1.

Any future persistence, remote synchronization or sensitive-data handling requires explicit data-flow evidence, minimization rationale, security/privacy review and governance acceptance.
