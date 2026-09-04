# MH-17 — Threat Model

**Status:** PROPOSED / CANDIDATE

Primary assets: device identity, credentials, protocol sessions, commands, capability declarations, telemetry, topology, canonical state, safety controls, firmware, and audit evidence.

Threats include rogue discovery, identity spoofing, endpoint takeover, credential theft, protocol downgrade, malformed input, replay, command injection, unauthorized capability use, adapter compromise, plugin escalation, AI prompt/control confusion, cloud compromise, firmware compromise, denial of service, and stale/ambiguous state.

Required controls: authenticated identity where supported, least privilege, default deny, capability validation, replay/idempotency protection, input validation, bounded resources, quarantine, revocation, auditability, fail-closed authorization, and explicit unknown-state handling.

Concrete protocol-specific threat claims remain subject to technology evaluation and security evidence.
