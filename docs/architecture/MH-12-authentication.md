# MH-12 Authentication

Authentication answers who the principal is; it does not grant authorization. Required domains: local, service-to-service, device, API, administrator, plugin, cloud and recovery.

Session/credential lifecycle must define issuance, binding, expiration, refresh, revocation, replay resistance, failed-auth handling, rate limits/quarantine and recovery. Exact technology stack remains non-canonical until evidence and ADR.

Invalid, expired, unverifiable or replayed authentication context fails closed.
