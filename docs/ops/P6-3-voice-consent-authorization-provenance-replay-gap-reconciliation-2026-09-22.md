# P6.3 Voice Consent / Authorization / Provenance / Replay Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P6.3 NOT CLOSED

## Queue requirement

`P6.3 Enforce consent, authorization, command provenance and replay protection.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — requires voice/appearance authorization, provenance, audit and revocation at the broader platform level.
- `docs/architecture/MH-12-authentication.md` — requires authentication lifecycle, revocation and replay resistance.
- `docs/architecture/MH-12-authorization.md` — requires explicit operation-specific, identity/context/policy-aware, auditable and fail-closed authorization.
- `docs/architecture/MH-21-device-interaction.md` — constrains remote commands through validation, policy, authorization and Consumer Boundary.
- `tests/security/test_mh05_bypass_audit.py` — provides negative generic command-boundary coverage, not voice-specific acceptance.

## Classification

- Voice-specific consent contract: ABSENT.
- Voice-specific authorization contract: ABSENT.
- Voice command provenance contract: ABSENT.
- Voice replay-protection tests: ABSENT.
- Generic platform security boundaries: PRESENT/PARTIAL, but insufficient for voice-specific closure.

## Gate

No voice provider was executed and no voice-specific protocol semantics were invented. P6.3 remains open.
