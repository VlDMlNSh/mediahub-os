# MH-17 — Device Lifecycle

**Status:** CANDIDATE

Lifecycle expresses operational/onboarding state and must not be used as a substitute for authorization or trust.

Target states: `Discovered, Untrusted, Identified, Verified, Enrolled, Authorized, Configured, Active, Degraded, Quarantined, Revoked, Removed`.

Transitions must be deterministic, reasoned, timestamped, auditable and fail closed. Invalid transitions produce no partial canonical mutation.

The current repository schema defines `DISCOVERED, IDENTIFIED, ONBOARDING, ACTIVE, OFFLINE, DEGRADED, RETIRED`. fileciteturn11file0L2-L5 This is a material contradiction with the target security lifecycle: quarantine/revocation/authorization cannot be represented distinctly today. This is **CONTRADICTION / REQUIRES ADR** rather than an implementation detail.

Availability (`OFFLINE`) and trust (`BLOCKED`) remain separate dimensions.