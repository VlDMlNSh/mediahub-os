# P0.5.1 Terminal Checkpoint Startup Verification

Status: VERIFIED_LOCAL_SUBSCOPE / P0.5.1 NOT CLOSED

## Repository-observed behavior

Source: `ops/ai/hybrid_development_daemon.py`
Tests: `tests/ai/test_hybrid_development_daemon.py`

The daemon treats a denied restore as a clean exit only when the journal tail exactly matches the requested session identity, baseline SHA, R4 SHA, and a terminal state (`STOPPED`, `EXPIRED`, `SAFE_STOP`, or `STOPPING`). It does not revive the terminal session or create a replacement identity on that path.

## Verification

Command: `pytest -q tests/ai/test_hybrid_development_daemon.py`

Acceptance: the exact-identity terminal restore path passes the existing deterministic test, while mismatched terminal provenance remains fail-closed under the separate regression test.

## Boundary

This evidence qualifies only the local daemon checkpoint-startup behavior. It does not authorize production daemon operation, release, external execution, credentials, State Authority mutation, or a new identity.
