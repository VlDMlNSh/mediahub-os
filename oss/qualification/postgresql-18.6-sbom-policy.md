# PostgreSQL 18.6 SBOM Qualification Policy

Status: target-gated

## Rule

PostgreSQL 18.6 MUST NOT become `active` until a reproducible SBOM is generated from the exact upstream source artifact selected by the qualification manifest and the resulting SBOM digest is recorded in qualification evidence.

## Required evidence

- exact upstream artifact identity: `postgresql-18.6.tar.gz`
- exact SHA-256 of the downloaded artifact, independently verified against the official PostgreSQL checksum
- SBOM generated from that exact artifact using the approved MediaHub supply-chain tooling
- SBOM format and tool version recorded
- SBOM digest recorded
- vulnerability evidence evaluated against the exact qualified artifact/build inputs

## Fail-closed rule

An unavailable, synthetic, inferred, or manually asserted SBOM is not valid evidence. `sbom=true` MUST NOT be set in `qualification.json` until the artifact and generated SBOM have been independently verified.

## Authority boundary

PostgreSQL is a persistence implementation under MediaHub State Authority. It is not a State Authority and MUST NOT introduce an alternate state authority, shadow state, or bypass of the governed command path.
