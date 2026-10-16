# MediaHub OS — Cloud-Agent Schema v0.2 Candidates, Wave 16

- Date: 2026-10-16
- ID: MH-CAF-SCHEMA-V2-16
- Status: **V0.2 CANDIDATES CREATED / 20 BOUNDED STRUCTURAL ASSERTIONS PASSED / FULL VALIDATION OPEN**
- Contour: A — autonomous development fabric
- Parent review: [Wave 15 Schema Semantic Review](MEDIAHUB-CLOUD-AGENT-SCHEMA-SEMANTIC-REVIEW-WAVE-15-2026-10-16.md)
- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Candidate artifacts

| Artifact | Creation commit | Live blob SHA |
|---|---|---|
| [Agent Registry Schema v0.2](MEDIAHUB-CLOUD-AGENT-REGISTRY-SCHEMA-V0.2-WAVE-16-2026-10-16.json) | `d8c7be5477276d81b1dd08adb9a75f6c4ee2d950` | `b49b89b8fbdfc180862e3dc78f8198f35e486035` |
| [Execution Evidence Manifest Schema v0.2](MEDIAHUB-CLOUD-AGENT-EVIDENCE-MANIFEST-SCHEMA-V0.2-WAVE-16-2026-10-16.json) | `c16f82c30dc4ce65148dfa23ca2a76c613353036` | `40c402432fd0f3899d45fde0fa0a8af4d34c593a` |

Both files remain proposals. Wave 13 v0.1 artifacts are preserved unchanged as historical versions.

## 2. Changes in v0.2

### Agent Registry

- Makes provider-backed cloud agents the explicit scope of this registry; local/no-provider executor modeling remains a separate contract decision.
- Requires at least one authorized provider route and bounds route count.
- Bounds task types, path scopes and data-class lists; makes provider routes unique.
- Keeps expiry and revocation references mandatory and isolated workspace required.
- Expands the semantic-validation comment to require issuer/grant/reviewer resolution, scope digest, expiry/revocation, timestamp ordering, capability intersection and provider-route policy checks.
- Keeps status values descriptive; `authorized` alone never grants authority.

### Execution Evidence Manifest

- Removes `verified` and `qualified` from execution status.
- Adds distinct `verification` and `qualification` records with their own states and evidence references.
- Adds schema references and version/digest binding.
- Requires bounded, unique, 40-hex action SHAs.
- Bounds input and artifact cardinality and byte sizes.
- Allows `finished_at: null` for an explicitly represented in-progress execution record.
- Requires Draft 2020-12 format assertion in the validator profile.
- Preserves separate executor result, promotion state and independent review disposition.

## 3. Bounded structural review

A read-only check over the exact GitHub read-back content parsed both JSON files and evaluated 20 assertions:

1. Draft 2020-12 declaration and v0.2 version IDs;
2. closed top-level objects;
3. mandatory isolated workspace and expiry/revocation references;
4. at least one bounded, unique provider route;
5. execution status separated from verification and qualification;
6. separate verification and qualification records;
7. strict action SHA format and bounds;
8. bounded input/artifact lists;
9. required schema references;
10. support for an in-progress record with null finish time;
11. reviewer decision retained;
12. closed verification/qualification objects.

Result: **20/20 assertions passed**.

This is a structural smoke check, not a standards-compliant JSON Schema meta-validation, fixture suite, semantic reference-resolution test, workflow test or qualification.

## 4. Remaining issues and acceptance gates

- A full Draft 2020-12 validator must check both schemas with format assertion enabled.
- Negative fixtures must cover malformed SHAs, invalid date-time values, expiry ordering, missing/revoked grants, stale policy references, route/model/data-class mismatch, capability/effect mismatch, unknown properties and over-limit arrays.
- Cross-field time order and reference existence require semantic validation beyond JSON Schema.
- Schema-reference names must be unique by semantic key, not merely unique as whole JSON objects.
- A0 issuer/lifecycle, MH-12 authority, R-06 disposition and target runner/workspace/network manifest remain open.
- Independent review must record the exact candidate blob SHAs and validator revision.

## 5. Disposition

Wave 16 creates two versioned schema candidates and performs a bounded structural review. It does not replace v0.1, register or authorize any agent, create a live registry, connect a provider, dispatch a workflow, or qualify a runtime component.

Next: record these candidates in the activation queue, complete full validator/negative-fixture evidence under the applicable authorization, and obtain independent review before any runtime adoption.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
