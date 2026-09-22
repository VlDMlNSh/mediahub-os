# P6.1 Voice Provider Order Reconciliation

Status: VERIFIED_LOCAL_SUBSCOPE / P6.1 NOT CLOSED

## Queue requirement

`P6.1 Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml` — declares the canonical voice provider order.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — preserves the voice/platform governance boundary and does not authorize provider bypass.
- `ops/verify_functional_baseline.sh` — repository-native baseline verification gate.

## Classification

- Canonical provider order declaration: PRESENT.
- Provider adapters/runtime integrations: NOT qualified by this evidence.
- External provider execution/account access: not performed.

## Gate

This verifies only the repository-declared order. It does not close provider implementation, consent, authorization, replay protection, outage handling or production voice qualification.
