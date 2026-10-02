<!-- GENERATED FILE — do not edit by hand.
     Regenerate with: python ops/qualification/render_current_truth.py --out docs/qualification/CURRENT-TRUTH.generated.md
     Source: architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml -->

# ASTRA GOLD — Current Truth (generated)

This file is generated from the governance contract and, when present, a
gate-evidence file. It is the single readable source of current gate state.
No gate is promoted by this document.

## Gates

| Gate | Name | Status |
|---|---|---|
| G0_IDENTITY | Identity | BLOCKED |
| G1_BOUNDARY | Boundary | BLOCKED |
| G2_CONTROL_PLANE | Control Plane | BLOCKED |
| G3_EXECUTION_PATH | Execution Path | BLOCKED |
| G4_23_WAVE_QUALIFICATION | 23-Wave Qualification | BLOCKED |
| G5_CONCURRENCY | Concurrency | BLOCKED |
| G6_RECOVERY | Recovery | BLOCKED |
| G7_INTEGRATED_A3 | Integrated A3 | BLOCKED |
| G8_PRE_SOAK | Pre-Soak | BLOCKED |
| G9_24H_SOAK | 24H SOAK | BLOCKED |
| G10_LAUNCH_READY | Launch Ready | BLOCKED |
| G11_LAUNCH | Human Launch | BLOCKED |

## Truth status

- Overall: NOT_PROVEN / BLOCKED — no gate has fresh PASS evidence
- `ASTRA_GOLD_ELIGIBLE` is not asserted unless every mandatory gate has fresh PASS evidence at one frozen SHA.
- `LAUNCH_READY` requires fresh PASS of G0–G9 and a complete launch-input bundle.
- G11 is HUMAN_ONLY.

## Promotion ladder

`REGISTERED → CREDENTIAL_PRESENT → AUTH_SUCCESS → MODEL_DISCOVERY_PASS →
PROBE_PASS → EXECUTION_PASS → RESULT_VALIDATION_PASS → A3_VERIFIED →
ASTRA_GOLD_ELIGIBLE → LAUNCH_READY → LAUNCHED` — no implicit transitions.
