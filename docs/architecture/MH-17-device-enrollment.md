# MH-17 — Device Enrollment

**Status:** CANDIDATE

Enrollment is a security transition, not discovery and not configuration convenience.

Candidate gate:
`candidate identity → proof/evidence → collision check → trust decision → explicit authorization scope → capability validation → configuration binding → audit → enrolled`

Required evidence can be protocol- or device-specific: cryptographic proof where available, authenticated pairing, validated out-of-band proof, or approved manual evidence. No single method is assumed canonical.

Re-enrollment must preserve audit history and explicitly handle credential rotation. Device replacement must not copy identity automatically. Stolen, cloned, expired or revoked identities are denied and may be quarantined.

Enrollment must not imply unlimited authorization. Capability authorization remains separate and can be reduced independently.

**UNKNOWN:** concrete enrollment protocol, certificate provisioning, credential storage and revocation workflow are not implemented/verified in the current repository.