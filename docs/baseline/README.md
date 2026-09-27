# MediaHub OS — Baseline

This directory contains the authoritative MediaHub OS baseline
artifacts used to drive factual implementation.

Rules:

- No new product features are introduced here.
- No architectural concepts are invented here.
- Implementation must remain traceable to the approved baseline.
- Changes to the baseline require an explicit project decision.


## Normative authority

The canonical functional authority is:
`specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`

Governance manifest:
`specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml`

These artifacts establish Functional Baseline 1.0 as the **NORMATIVE SINGLE SOURCE OF TRUTH**.
Capability, contract and architecture artifacts are subordinate implementation/detail layers.
A contradiction must be reconciled before the affected implementation can qualify.
Baseline 1.0 is not edited in place; approved functional changes require a new baseline version.

The immutable R4 technical anchor remains unchanged. Any SHA discrepancy is a separate
technical reconciliation item and cannot be resolved by rewriting R4.
