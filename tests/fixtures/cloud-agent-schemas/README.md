# Cloud-agent schema validation fixtures

These files are synthetic fixtures for the proposed v0.2 schemas, not an admitted task, provider route, agent registration, runtime record, or qualification result. Identifiers, grants, evidence references and digests are inert fixture values.

The valid folder contains one minimum positive instance per schema. `negative-cases.json` specifies deterministic mutations applied to deep copies of those positives. Each mutation must be rejected by JSON Schema Draft 2020-12 validation with format checking enabled.

Schemas are pinned by their reviewed Git blob SHA-1 in the validation script. Refresh those pins only as part of an explicit schema-review change.
