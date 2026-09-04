# MH-06 — Recovery Model

Status: PROPOSED / GOVERNANCE ENFORCEMENT REQUIRES VERIFICATION

Low-risk candidates: service restart, reconnect, cache rebuild, queue cleanup, stale-session expiration, certificate renewal, bounded retry, degraded mode.

Restricted: storage remount, pool import, reboot, policy disable, traffic isolation, rollback.

Operator-only: destructive reset, factory reset, disk replacement, compromised-key rotation, restore over existing data, firmware update, secure wipe and critical relay operations.

Every recovery action requires trigger, risk/confidence assessment where applicable, authorization, audit context, rate/attempt bounds and quarantine condition. Recovery never becomes a second mutation authority.
