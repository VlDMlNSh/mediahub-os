# MH-17 — Plugin / Device Interaction

**Status:** CANDIDATE

Plugin integrations must declare capabilities and operate through identity, authorization, Consumer Boundary and approved adapters.

Candidate path:
`Plugin → Declared Capability → Identity → Authorization → Consumer Boundary → Adapter → Device`.

Plugins do not receive arbitrary LAN access, unrestricted sockets, raw USB/serial access, device credentials, shell access or arbitrary device control. A plugin's declared capability is not permission until separately authorized.

Any future plugin-to-device transport requires explicit security review and resource isolation.