# MH-01 Scope

Status: PROPOSED / REQUIRES VERIFICATION.

## In scope

- Local runtime and canonical runtime state.
- Capability/command execution through authorized boundaries.
- Device/protocol integration.
- Policy, authorization and automation.
- Media/content capabilities.
- UI/presentation surfaces.
- Diagnostics and observability.
- Security, privacy and trust lifecycle.
- Recovery, maintenance and lifecycle control.
- AI, RAG, Knowledge Graph and Digital Twin as non-authoritative subsystems.
- Controlled external/cloud integrations.

## Out of scope for the core product

- Mandatory cloud operation.
- Cloud ownership of canonical runtime state.
- Unrestricted autonomous AI.
- Implicit trust from discovery/presence.
- UI/plugin/database/cache as alternate mutation authorities.
- Automatic HA guarantees.
- Production qualification of historical hardware without evidence.

## Future scope

- Qualified distributed local cluster.
- Controlled external GPU/cloud compute.
- Advanced digital twin/knowledge capabilities.
- Qualified persistence architecture.
- Advanced recovery/update mechanisms.
- HA only if separately designed, verified and accepted.

## Forbidden scope

- Alternate canonical mutation path.
- AI/LLM direct mutation authority.
- Cloud direct State Authority access.
- Security bypass via plugin/integration.
- Undocumented breaking changes.
- Irreversible architectural changes without governance.
- Treating backup, mirroring or replication as proof of HA.

## Scope rule

A capability can be added without becoming an authority. Every new capability must declare owner, trust boundary, authorization path, mutation path, data class, failure behavior and verification gate.