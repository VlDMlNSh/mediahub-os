# MH-09 — Error Semantics

**Status:** PROPOSED / REQUIRES VERIFICATION

Presentation-facing error classes: validation, authentication required, authorization denied, policy denied, stale, conflict, unavailable, timeout, cancellation, dependency failure, degraded, quarantine, recovery required and unknown result.

Errors are classified without exposing sensitive internal details. UI must not convert an error into success, silently retry indefinitely, alter authorization, or infer canonical state from a transport/UI outcome.
