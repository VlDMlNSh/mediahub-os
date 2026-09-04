# MH-12 Capability Security

Capability candidate fields: issuer, principal, operation, resource, scope, constraints, provenance, issued_at, expires_at, revocation_context.

Capabilities are bounded and operation-specific. Attenuation may only narrow authority; self-expansion is forbidden. Controls must address delegation, revocation, replay, forgery, leakage, storage, transport and confused deputy.

A capability never bypasses identity, authorization, policy, Consumer Boundary or State Authority.
