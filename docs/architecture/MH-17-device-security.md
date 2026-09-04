# MH-17 — Device Security

**Status:** CANDIDATE

Threat classes: spoofed/rogue/compromised devices, cloned identities, replay, MITM, credential theft, certificate compromise, downgrade, malicious firmware, malformed packets, parser exploits, command/event injection, fake or stale telemetry, resource exhaustion and network pivoting.

Security controls are protocol/device specific. Candidate mechanisms include mutual TLS, certificates, pre-shared keys and scoped tokens, but none is canonical until concrete evidence exists.

Required principles:
- authentication ≠ authorization;
- TLS ≠ application authorization;
- VPN ≠ trust;
- reachability ≠ permission;
- credential possession ≠ unlimited capability.

Revocation and quarantine must be enforceable independently of device availability.