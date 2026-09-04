# MH-17 — Normalization

**Status:** CANDIDATE

Protocol adapters translate external protocol models into MediaHub canonical integration models. Protocol-specific enums, error codes, units, timestamps and addressing semantics must remain inside the adapter/contract boundary unless explicitly normalized.

Normalization must validate:
- type and schema version;
- units and conversion provenance;
- numeric ranges and precision;
- enums and unknown values;
- timestamps and clock provenance;
- identifiers and collision conditions;
- capability mappings;
- errors and status semantics.

Unknown units or ambiguous semantics are rejected/quarantined/reported as `REQUIRES_VERIFICATION`; they are never silently converted.

Normalization produces evidence; it does not become State Authority by itself.