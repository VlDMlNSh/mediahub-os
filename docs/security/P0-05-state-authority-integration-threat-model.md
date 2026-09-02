# P0-05 — State Authority Integration Threat Model v1.0

## Status

DRAFT SECURITY ARTIFACT — GOVERNANCE REVIEW REQUIRED

## Scope

Threat model for integrating runtime services, UI, plugins/extensions, diagnostics, and AI/proposal producers with the P0-04 frozen State Authority. Persistence and production integration are excluded.

## Primary assets

- canonical runtime state;
- state generation and version metadata;
- authorization decisions/context;
- checkpoint identity within the in-memory scope;
- integrity-validation results;
- privacy-sensitive diagnostic/error information.

## Trust assumptions

Consumers are not trusted with direct canonical-state mutation. UI, plugins, AI and external inputs are untrusted at the data boundary. State Authority remains the trusted mutation authority.

## Threats and controls

| ID | Threat | Required control |
|---|---|---|
| P05-T01 | Consumer bypasses State Authority | No direct canonical mutation primitive; architecture inspection and negative tests |
| P05-T02 | Mutable read alias changes canonical state | Immutable read boundary; alias/mutation tests |
| P05-T03 | Stale consumer overwrites newer state | Generation/version binding; stale transaction rejection |
| P05-T04 | Plugin obtains unintended mutation capability | Default-deny capability/authorization boundary |
| P05-T05 | AI proposal becomes executable authority | Inert proposal contract; no execute/commit primitive |
| P05-T06 | Malformed external data causes unsafe state mutation | Structural validation, bounds and fail-closed rejection |
| P05-T07 | Consumer learns sensitive internal details from failures | Sanitized consumer-facing errors/diagnostics |
| P05-T08 | Integration introduces arbitrary execution/network/filesystem side effects | Capability scan plus negative tests; explicit API exclusion |
| P05-T09 | Personal data crosses an unapproved durable boundary | P0-05 has no persistence; future durable boundary requires separate governance |
| P05-T10 | Concurrency creates inconsistent canonical revision | State Authority serialization and atomic publication contract |

## Security invariants

- State Authority is the sole canonical mutation authority.
- Authorization precedes mutation.
- External/AI proposals are data, never authority.
- Failure preserves canonical state.
- No implicit persistence exists.
- Consumer-facing diagnostics remain sanitized.

## Exit requirement

Before implementation acceptance, every threat must map to a concrete contract invariant, negative-path test or capability inspection, with execution evidence against the exact reviewed commit.
