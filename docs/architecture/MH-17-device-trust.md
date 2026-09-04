# MH-17 — Device Trust

**Status:** CANDIDATE

Trust is independent from availability and health. The repository already models trust as a separate object with status `TRUSTED`, `PENDING`, `UNTRUSTED`, or `BLOCKED`, plus source and timestamp. fileciteturn10file0L2-L5

Target lifecycle:
`Discovered → Untrusted → Identified → Verified → Enrolled → Authorized → Configured → Active → Degraded → Quarantined → Revoked/Removed`

Trust transitions require explicit evidence and fail closed. A device can be reachable while untrusted, trusted while temporarily offline, or authenticated while lacking a requested capability authorization.

Quarantine is a security state, not merely a health state. Revocation must remove ordinary control authority without requiring physical disappearance.

**Compatibility note:** the existing schema is narrower than the target lifecycle and therefore requires an explicit versioned contract migration/ADR before implementation.