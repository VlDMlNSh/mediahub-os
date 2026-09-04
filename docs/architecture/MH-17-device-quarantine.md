# MH-17 — Device Quarantine

**Status:** CANDIDATE

Quarantine is an explicit security state applied for unknown identity, failed authentication, malformed telemetry, protocol violation, excessive failures, suspicious behavior, expired/revoked credentials, capability mismatch, incompatible firmware or security incident.

Quarantined devices:
- do not receive ordinary control capabilities;
- cannot bypass Consumer Boundary or State Authority;
- remain observable only through bounded/sanitized telemetry and diagnostics;
- may require explicit operator/security action for release.

Quarantine must be fail-closed, auditable, rate-limited and resistant to reconnect loops. Availability/health changes alone do not imply quarantine, and quarantine does not imply physical disconnection unless separately authorized.