# P6.4 Home Assistant Smart Home Mutation Boundary Reconciliation

Status: VERIFIED_LOCAL_SUBSCOPE / P6.4 NOT CLOSED

## Queue requirement

`P6.4 Route Smart Home mutations through Home Assistant Core.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — identifies Home Assistant Core as the Smart Home authority and forbids bypass.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml` — declares `smart_home: Home Assistant Core`.
- `specification/invariant-registry.yaml` — records Home Assistant Core as sole Smart Home authority.
- `specification/decision-registry.yaml` — records Home Assistant as internal Smart Home integration/automation source of truth.
- `ops/verify_functional_baseline.sh` — validates the repository baseline authority declarations.

## Classification

- Canonical Smart Home authority declaration: IMPLEMENTED at repository governance level.
- Direct MediaHub UI/AI bypass prohibition: PRESENT in normative baseline.
- Operational Home Assistant mutation adapter: ABSENT in inspected repository.
- Runtime end-to-end mutation proof: ABSENT; no Home Assistant runtime was accessed.

## Gate

This verifies the declared authority boundary only. It does not mutate Smart Home state, access Home Assistant, or close P6.4 globally.
