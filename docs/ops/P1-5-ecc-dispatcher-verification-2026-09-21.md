# P1.5 ECC Adapter / Dispatcher Verification

Date: 2026-09-21
Lane: engineering/mh21-sandbox-lifecycle-20260910

## Scope

Machine-readable acceptance evidence for the existing bounded ECC advisory policy and target-gated hybrid dispatcher. No live cloud-agent execution, credential acquisition, State Authority mutation, release, or production operation is performed.

## Verification surface

- `ops/ai/ecc_policy.py`
- `ops/ai/hybrid_dispatcher.py`
- `tests/ai/test_ecc_policy.py`
- `tests/ai/test_hybrid_dispatcher.py`

## Deterministic acceptance

The acceptance surface requires provenance-bound advisory ECC admission, allowlisted roles and capabilities, fail-closed denial of State Authority, production, release, secrets, credential-access and network-write capabilities, non-advisory scope rejection, target-gated dispatcher authorization, session/conversation/generation identity binding, bounded timeout validation, egress/endpoint identity matching, and reconciliation-required handling after uncertain agent outcomes.

## Evidence

Combined ECC policy / hybrid dispatcher suite: `23 passed`.

`ruff` was not available as a Python module on the development host; this is recorded as an environment limitation rather than a fabricated PASS. `git diff --check` was requested as part of the verification command but the command sequence stopped at the unavailable ruff executable, so formatting/diff evidence remains pending for this change.

No live cloud-agent qualification is claimed. Credentials were not acquired or materialized.

## Disposition

`P1.5 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS`

The evidence is sufficient to encode the existing deterministic local acceptance surface. It does not authorize cloud execution, production routing, release, credential use, or State Authority mutation.
