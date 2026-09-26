# MediaHub Evidence ID Normalization Policy — 2026-09-05

STATUS: PROPOSED / NOT ACCEPTANCE

## Purpose

Legacy F-xxx identifiers are historical labels and are not assumed to be globally unique. Canonical evidence identity must be independent of legacy numbering.

## Rule

A stable evidence record should use an immutable evidence ID and may retain legacy F-xxx as an alias.

Recommended form:
`EVD-<domain>-<sequence>`

Each evidence record must identify:
- evidence ID;
- legacy identifier, if any;
- source artifact/path;
- source commit;
- capability references;
- requirement references;
- contract references;
- invariant references;
- verification/test identity;
- evidence provenance;
- acceptance authority;
- acceptance state;
- timestamp/version;
- supersession/retraction history.

## Rationale

F-007 currently occurs under two different acceptance/accepted paths with different subjects. This is treated as a historical numbering collision, not a duplicate canonical capability.

## Governance

No historical artifact is renamed or deleted solely to normalize identifiers. Normalized IDs are additive metadata until explicit governance acceptance.
