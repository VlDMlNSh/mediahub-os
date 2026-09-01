# P0-04 Data Handling and Privacy Boundary v1.0

## Status

Prepared for the P0-04 implementation gate. Documentation only; implementation remains blocked until explicit P0-03 governance authorization.

## Purpose

Define minimum data-handling controls for the deterministic in-memory State Authority so that implementation and later execution evidence do not introduce unnecessary personal-data exposure or sensitive-state leakage.

## Data classes

### D0 — synthetic/non-sensitive test data

Preferred class for unit, adversarial, and execution tests. Examples must be fabricated and must not contain real credentials, tokens, personal identifiers, private messages, or production state.

### D1 — operational metadata

Non-sensitive identifiers required to prove invariants, such as transaction identity, generation identity, schema version, state version, lifecycle status, and test-case identifiers.

### D2 — sensitive state

Credentials, authentication material, tokens, secrets, private content, raw voice/audio content, API keys, and other sensitive payloads. P0-04 tests must not require real D2 data.

### D3 — personal data

Names, contact details, unique identifiers, user-generated private content, location information, or other data relating to an identifiable person. P0-04 verification should use synthetic substitutes whenever possible.

## Mandatory controls

1. **Data minimization:** tests and diagnostics use the smallest data necessary to prove the invariant.
2. **Synthetic-by-default:** no production personal or secret data is required for P0-04.
3. **No sensitive diagnostic payloads:** exceptions and diagnostics must not expose secrets, credentials, tokens, API keys, raw voice, or unnecessary personal data.
4. **Recursive sanitization:** nested containers must be sanitized, not only top-level fields.
5. **Untrusted-state boundary:** serialized/checkpoint material is treated as untrusted until structural, size, schema, generation, authenticity/integrity checks pass.
6. **No implicit external transmission:** P0-04 contains no network transport or telemetry path.
7. **No AI mutation path:** AI/external proposals remain non-authoritative data and cannot mutate canonical state directly.
8. **Evidence hygiene:** execution evidence records commands, results, versions, and invariant outcomes without copying sensitive payloads.
9. **Retention minimization:** temporary test artifacts should contain no unnecessary personal or secret data and should be removable without affecting canonical state.
10. **Fail closed:** inability to validate authorization, integrity, generation, schema, structure, or bounds results in rejection rather than best-effort acceptance.

## Privacy-specific negative tests

P0-04 verification must include evidence that:

- nested sensitive diagnostic fields are redacted;
- sensitive values inside lists/tuples/dictionaries do not escape sanitization;
- malformed input cannot force disclosure through exception text;
- hostile strings remain data and are never interpreted as commands or executable code;
- checkpoint metadata does not contain unnecessary payload data;
- failed restore/commit paths do not leak candidate state;
- rejected authorization attempts do not expose sensitive state;
- execution logs contain no real secrets or personal data.

## Security boundary

This document does not authorize encryption, key management, production identity, mTLS, external storage, cloud processing, hardware-backed protection, or persistent audit infrastructure. Those require separate architecture and security gates.

## Acceptance evidence

The P0-04 evidence package must identify the exact implementation commit and execution environment and must include privacy/security inspection results. A source-level assertion without execution evidence is insufficient for final acceptance.

## Historical boundary

No historical MH-02…MH-16 responsibility is inferred by this document.
