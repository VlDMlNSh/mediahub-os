# P0-04 — State Authority Threat Model v1.0

## Status

**PREPARED — implementation blocked on formal P0-03 acceptance.**

This threat model constrains the future deterministic in-memory State Authority implementation. It is not implementation authorization.

## Assets

1. canonical runtime state;
2. canonical generation and state version;
3. integrity reference/status;
4. accepted checkpoint identity;
5. transaction lifecycle and authorization context;
6. diagnostic and error metadata.

## Trust boundaries

### TB-01 Caller → State Authority

All caller input is untrusted. The State Authority must not infer authority from payload content, requested revision, or caller-selected metadata.

### TB-02 Candidate → Canonical

Candidate state is non-authoritative until all validation gates succeed and publication is atomic.

### TB-03 Persistence/read material → State Authority

Future serialized/checkpoint material is untrusted until authenticity, schema, generation, integrity, and structural/resource validation succeed.

### TB-04 AI/external input → State Authority

AI output, UI input, plugin input, network input, or external proposals must not provide a direct canonical-state mutation primitive.

### TB-05 Diagnostics → Operator/logging surface

Errors and diagnostics must not disclose secrets, credentials, tokens, or unnecessary personal data.

## Threat classes

| ID | Threat | Required control |
|---|---|---|
| TM-01 | Unauthorized mutation | operation-specific default-deny authorization |
| TM-02 | Stale overwrite | observed generation/state-version binding + fail-closed commit |
| TM-03 | Partial publication | atomic complete-revision publication |
| TM-04 | Candidate leakage | isolated candidate invisible to canonical readers |
| TM-05 | Caller-selected revision | authority-owned monotonic revision assignment |
| TM-06 | Generation confusion | explicit generation compatibility gate |
| TM-07 | Integrity bypass | independent integrity validation gate |
| TM-08 | Checkpoint substitution | immutable checkpoint identity + authenticity validation |
| TM-09 | Restore corruption | restore through candidate + validation + new revision |
| TM-10 | Malformed/untrusted state | structural/schema/resource validation before acceptance |
| TM-11 | Resource exhaustion | explicit payload/transaction/resource bounds |
| TM-12 | Unsafe deserialization | no unsafe object deserialization; typed validation boundary |
| TM-13 | AI mutation | proposal/data-only boundary; no execution/mutation primitive |
| TM-14 | Command execution | no subprocess/system command capability |
| TM-15 | Filesystem mutation | no arbitrary filesystem write capability |
| TM-16 | Network mutation | no network transport or external mutation capability |
| TM-17 | Diagnostic disclosure | recursive sanitization and privacy-preserving errors |
| TM-18 | Transaction resurrection | terminal lifecycle states are irreversible |

## Security invariants

The implementation must preserve SA-001..SA-014 from the P0-03 contract. In particular:

- one authoritative mutation path;
- candidate isolation;
- atomic publication;
- authority-owned monotonic state version;
- no caller-selected revision;
- generation binding;
- integrity as a separate acceptance gate;
- restore isolation and new canonical revision;
- immutable checkpoint identity;
- default-deny authorization;
- no external mutation primitive;
- failure preservation;
- untrusted-state boundary;
- operation-specific authorization.

## Privacy requirements

The implementation must avoid requiring real personal data for tests. Test fixtures should use synthetic values. Sensitive payloads must not be copied into exceptions or diagnostics. Diagnostic sanitization must cover nested containers, not only top-level fields.

## Evidence requirements

For each threat class, evidence must include the applicable code/test inspection and, where execution is required, an exact immutable implementation commit and captured result. A design statement alone is not execution evidence.

## Residual risks deferred by scope

The following remain explicitly deferred until a separately authorized persistence/production phase:

- cryptographic checkpoint authenticity implementation;
- crash consistency and durable atomicity;
- storage corruption and recovery media;
- filesystem/ZFS/SQLite security;
- update/rollback interaction;
- production privilege boundaries;
- network/mTLS security;
- hardware-backed integrity/entropy.

## Acceptance rule

This threat model is a preparation artifact. It neither accepts P0-03 nor authorizes P0-04 implementation. Any implementation must demonstrate that no new capability silently crosses the defined trust boundaries.
