# Canonical schemas moved to `schemas/`

This directory previously duplicated `ai/`, `core/` and `identity/` schemas
that also lived under `schemas/`. Two copies had drifted apart
(`core/contract-metadata.schema.json` and
`identity/identity-boundary.schema.json`), which the 2026-10-02 whole-project
audit recorded as defect **D2**.

The conflict is resolved in favour of a single canonical source:

- `schemas/` is the canonical schema tree and the only place schemas are
  authored or edited.
- `tools/validate_contracts.py` validates `schemas/` (26 files, 9 metadata
  envelope contracts).
- `tests/static/test_cross_contract.py` fails closed if a second schema tree
  reappears here.

Do not add schema files back under `contracts/`. Put them in `schemas/`
instead.
