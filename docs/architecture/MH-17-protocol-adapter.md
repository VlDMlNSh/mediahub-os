# MH-17 — Protocol Adapter

**Status:** CANDIDATE

Adapter responsibilities: connection management, protocol authentication, encoding/decoding, validation, normalization, bounded retries, timeouts, protocol-specific errors, capability mapping and transport/resource limits.

Adapter non-responsibilities: canonical authority, global policy, authorization issuance, unrestricted persistence, AI decisions, security bypass, arbitrary network access or command invention.

Adapter inputs and outputs must be typed, size-bounded and versioned. Credentials are references to approved secret mechanisms, not arbitrary plugin-accessible material.

A protocol binding associates a normalized device with an adapter and endpoint. The repository already models binding with protocol, adapter, endpoint, priority and status. fileciteturn12file0L2-L5