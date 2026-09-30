# MH-02 — Contradiction Register

## C-01 — Compute Contribution
Historical Section 1 described Compute Contribution as intended for every deployment.
Current explicit decision rejects user Compute Contribution into Developer Fabric.
**Resolution:** current decision supersedes the historical proposal; preserve historical provenance and keep the capability disabled.

## C-02 — R4 identifier supplied in continuation prompt
The continuation prompt contains a malformed R4 string with extra trailing characters.
GitHub-confirmed project provenance uses the valid 40-character SHA `471f709f5633feab7aeb62dd3ea52effad6d2bc4`.
**Resolution:** use the GitHub-confirmed 40-character SHA; retain malformed form only as untrusted prompt text.

## C-03 — Current branch vs architecture checkpoint provenance
The active engineering branch resolves to a different head than the 2026-09-30 Section 4 checkpoint lineage.
**Resolution:** MH-2 checkpoint work is based on the latest explicitly relevant Section 4 commit `863e61783272e0107ce74ab1620212285946aca8` and is isolated on a dedicated architecture branch. No force-push/reset/rewrite is performed.

## C-04 — HA Core vs MediaHub State Authority
The two authorities govern different scopes.
**Resolution:** HA Core owns operational Smart Home state; MediaHub State Authority owns canonical platform state, identity/lifecycle/policy references and cross-domain consistency. They are not competing authorities.
