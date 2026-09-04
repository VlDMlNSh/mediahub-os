# MH-17 — Firmware Architecture

**Status:** PROPOSED / CANDIDATE

Firmware is a lifecycle/security plane, not an ordinary Device command. Firmware operations require explicit authorization, artifact identity, integrity/authenticity verification, compatibility checks, rollback/security-floor checks, bounded execution, audit, and post-update health evidence.

Device-reported firmware version is evidence, not authority. A firmware update MUST NOT bypass Device Trust, Policy, Authorization, State Authority, or lifecycle gates.

Unknown update outcome MUST remain `UNKNOWN` and MUST NOT be converted to success by timeout assumptions. Rollback is permitted only when security policy and device capabilities establish that the target version is allowed.

No specific firmware protocol, bootloader, vendor mechanism, signing infrastructure, or rollback technology is selected by this architecture.
