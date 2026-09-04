# MH-5 — Trust Boundary

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

## Trust zones

1. Trusted Core.
2. Authorized local service.
3. Local UI/CLI/management consumer.
4. Plugin/device/protocol/automation integration zone.
5. AI/external compute zone.
6. Remote/external service zone.
7. Unknown/unverified zone.

Trust requires explicit identity, authorization, scope, and lifecycle. Authentication is necessary where applicable but never sufficient for mutation authority. Localhost, LAN presence, VPN, Tailscale, WireGuard, mTLS, or encryption do not by themselves create Core trust.

Devices follow a controlled lifecycle: discovered → untrusted → verified → enrolled → configured → active. Presence is not authentication.

Administrative clients remain privileged consumers, not unrestricted authorities. Human, service, device, plugin, AI, and external-service identities are separate principal classes and are not implicitly interchangeable.
