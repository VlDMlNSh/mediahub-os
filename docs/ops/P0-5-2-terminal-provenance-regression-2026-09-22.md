# P0.5.2 Terminal Provenance Regression Verification

Status: VERIFIED_LOCAL_SUBSCOPE / P0.5.2 NOT CLOSED

## Repository-observed behavior

Source: `ops/ai/hybrid_development_daemon.py`
Tests: `tests/ai/test_hybrid_development_daemon.py`

The daemon only accepts a terminal checkpoint as a clean stop when session identity, baseline SHA, R4 SHA and terminal state all match. A mismatch in baseline or R4 provenance is re-raised as `HybridDevelopmentDenied` rather than silently reviving or replacing the session identity.

## Verification

Command: `pytest -q tests/ai/test_hybrid_development_daemon.py`

Acceptance: the deterministic mismatch regression passes while the exact-identity terminal-stop test remains passing.

## Boundary

This evidence qualifies only local terminal provenance reconciliation. It does not authorize production execution, release, credentials, external providers, State Authority mutation, or identity replacement.
