# MH-17 — Telemetry

**Status:** CANDIDATE

Telemetry may be periodic, event-driven, polled, subscribed or heartbeat-derived. Every sample needs source, observed timestamp, ingestion timestamp, freshness/validity, sequence when supplied, unit/schema identity and provenance.

The system must distinguish stale, duplicated, out-of-order, conflicting and missing telemetry. Device clock values are evidence, not automatically trusted ordering authority; MediaHub ingestion time and monotonic sequence evidence must be retained where applicable.

No telemetry sample by itself grants authorization or proves command application. Privacy-sensitive telemetry (presence, occupancy, media behavior, location, cameras/microphones) is subject to MH-13 minimization and access controls.