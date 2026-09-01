# P0-04 Privacy Negative Test Catalog v1.0

## Status

Prepared. No implementation authorization is implied.

## Objective

Define explicit privacy failure cases for the deterministic in-memory State Authority implementation and its verification evidence.

## Test catalog

| ID | Negative case | Expected result |
|---|---|---|
| PRIV-SA-01 | Sensitive key nested in diagnostic dictionary | Value redacted; structure remains usable |
| PRIV-SA-02 | Sensitive key nested inside list/tuple containers | Sensitive value redacted recursively |
| PRIV-SA-03 | Secret-like value embedded in hostile input | Treated as data; never executed or echoed into diagnostics unnecessarily |
| PRIV-SA-04 | Sensitive value placed in transaction error context | Error excludes secret/raw sensitive payload |
| PRIV-SA-05 | Private/user content used as a test fixture without need | Test rejected/replaced with synthetic fixture |
| PRIV-SA-06 | Raw voice/audio or credentials copied into evidence | Evidence flow stopped and sensitive material removed through controlled remediation |
| PRIV-SA-07 | Diagnostic metadata contains unnecessary personal data | Metadata minimized or redacted |
| PRIV-SA-08 | Malformed state contains sensitive fields | Rejection does not leak the sensitive fields |
| PRIV-SA-09 | Restore failure includes sensitive checkpoint material | Failure result exposes only safe metadata |
| PRIV-SA-10 | Capability/security scan output accidentally captures secrets | Evidence sanitized before publication |

## Acceptance properties

- Diagnostics are recursively sanitized for declared sensitive keys.
- Errors are safe-by-construction and do not require embedding payloads.
- Test and execution evidence uses synthetic data by default.
- Privacy failure is a blocking condition for the affected evidence path until remediated.

## Scope

This catalog covers P0-04 in-memory implementation and verification only. It does not establish production data-retention, deletion, database, filesystem, cloud, network, or hardware privacy controls.

## Historical boundary

No historical MH-02…MH-16 responsibility is inferred.
