# MH-17 — Compatibility Testing

**Status:** PROPOSED / CANDIDATE

Compatibility testing covers protocol versions, vendor variants, capability versions, firmware versions, transport changes, endpoint changes, device replacement, malformed/partial feature declarations, and backward/forward compatibility where claimed.

A device is not considered compatible solely because discovery succeeds. Compatibility requires identity, capability, command/event semantics, security properties, lifecycle behavior, and resource constraints to satisfy the applicable contract.

Unsupported variants MUST fail closed or remain explicitly unsupported rather than silently degrading into unsafe semantics.
