# MediaHub OS — Cloud-Agent Schema Semantic Review, Wave 15

- Date: 2026-10-16
- ID: MH-CAF-SCHEMA-REVIEW-15
- Status: **STATIC REVIEW FINDINGS / REMEDIATION PROPOSAL / NO SCHEMA PATCH APPLIED**
- Contour: A — autonomous development fabric
- Scope: Wave 11 task envelope, Wave 13 agent registry and execution evidence manifest
- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Exact source revisions

| Artifact | Blob SHA | Review scope |
|---|---|---|
| [Task Envelope Schema v0.1](MEDIAHUB-CLOUD-AGENT-TASK-ENVELOPE-SCHEMA-V0.1-WAVE-11-2026-10-16.json) | `64148c96c056e8c1fc7a79072862a79cb1c837eb` | Admission authority, source binding, route authorization, budget, review and promotion |
| [Agent Registry Record Schema v0.1](MEDIAHUB-CLOUD-AGENT-REGISTRY-SCHEMA-V0.1-WAVE-13-2026-10-16.json) | `449a38bc84283f720fe723ea8e3587e6082fdbb4` | Identity, capability, provider route, authorization and lifecycle fields |
| [Execution Evidence Manifest Schema v0.1](MEDIAHUB-CLOUD-AGENT-EVIDENCE-MANIFEST-SCHEMA-V0.1-WAVE-13-2026-10-16.json) | `9714fd2dd04d401a9a3d1a800cb19d7b69e7e73f` | Task/run/source/input/agent/policy/artifact and review provenance |
| [Activation Queue](MEDIAHUB-CLOUD-AGENT-ACTIVATION-QUEUE-WAVE-11-2026-10-16.json) | `0d751edc2b52085781eddb8e2e5ce638d93e5f88` | CAF-Q-001…CAF-Q-012 current documentary queue |

This is a static source review. It did not run a standards-compliant JSON Schema validator, workflow, provider request or runtime worker.

## 2. Findings

| ID | Priority | Finding | Risk | Recommended disposition |
|---|---|---|---|---|
| CAS-01 | P0 | Evidence-manifest `execution.status` includes `verified` and `qualified` alongside runtime execution states | Collapses execution, verification and qualification into one field, conflicting with the project’s lifecycle distinction | Remove those values from execution status in a versioned schema revision; represent verification/qualification as separate evidence-linked decisions with reviewer identity, scope, criteria revision and result |
| CAS-02 | P0 | Registry `status=authorized` and manifest review `decision=approved` are representable data values | Consumers could mistake syntactic validity for an actual grant or approval | Keep schema values descriptive only; admission service must verify issuer signature/record, scope digest, revocation, expiry, reviewer authority and exact target/task binding against accepted A0/MH-12 contracts |
| CAS-03 | P1 | Cross-field lifecycle invariants cannot be enforced by the current simple schema: `issued_at < expires_at`, freshness of `last_reviewed_at`, and revocation state consistency | A syntactically valid record can be temporally invalid or stale | Add a mandatory semantic-validation contract and negative test cases; evaluate timestamps against an approved clock source and bounded skew |
| CAS-04 | P1 | Manifest `source.action_shas` is represented as an array but lacks a strict per-item 40-hex SHA constraint and explicit uniqueness/bounds in the inspected schema | Provenance can contain malformed or duplicated action identities | Add `minItems`/bounded `maxItems`, `uniqueItems: true`, and item pattern `^[a-f0-9]{40}$`; require action identities when workflow execution uses third-party actions |
| CAS-05 | P1 | Input and artifact arrays require stronger explicit cardinality/byte-bound semantics at the schema/runtime boundary | Oversized manifests or unbounded evidence lists may complicate review and processing | Add array bounds, field length bounds and total manifest byte ceiling; enforce aggregate input/output/artifact budgets in runtime code as well |
| CAS-06 | P1 | Registry capability effects include patch/PR/test effects, while the schema does not by itself prove that the selected task, agent class, authorization grant and effect are mutually compatible | Over-broad registry records could pass structural validation | Add conditional constraints where feasible; always enforce capability intersection at admission: task grant ∩ agent class ∩ allowed paths ∩ data class ∩ effect ∩ target policy |
| CAS-07 | P1 | `provider_routes` contain policy and authorization references as strings, but schema validation cannot prove the referenced records exist, are current, or cover the same data class and model | Stale or mismatched route references can appear valid | Resolve every reference against the accepted policy/authorization source; bind provider, model, purpose, data class, quota bucket, expiry and task ID in a semantic route check |
| CAS-08 | P1 | `format: date-time` only has the intended effect when the chosen JSON Schema validator enables format assertion | Invalid timestamps may pass some validator configurations | Require a declared Draft 2020-12 validator profile with format assertion enabled and record validator/version/digest in qualification evidence |
| CAS-09 | P1 | Schema URLs identify mutable documentation-branch paths | A stable schema name may resolve to changed bytes over time | Bind each execution to schema version plus immutable source commit/blob SHA and schema digest; use an immutable release ref for normative publication once accepted |
| CAS-10 | P2 | Provider identity fields are mandatory even for potential local/no-provider executor classes, while route arrays can be empty | Future mixed local/cloud scheduling may require an explicit executor kind and clear route semantics | Decide through the component contract whether local executors are in scope; if so, introduce a versioned discriminated executor union instead of weakening provider requirements implicitly |

## 3. Remediation order

1. **P0:** Separate execution status from verification/qualification; make the authorization-consumption contract explicit.
2. **P1:** Harden action SHA and evidence-list bounds; define semantic validators for time, reference resolution, capability intersection and provider route matching.
3. **P1:** Pin validator profile and immutable schema digests in every execution manifest.
4. **P2:** Resolve whether local/no-provider executors share this registry schema or use a separate versioned record.
5. After review, create v0.2 schema candidates rather than silently changing v0.1 semantics. Preserve all historical IDs and include a migration/compatibility table.

## 4. Acceptance gates

- A standards-compliant Draft 2020-12 validator validates each schema itself.
- Valid and invalid fixtures cover unknown properties, malformed SHAs, missing evidence, stale/expired grants, inconsistent timestamps, mismatched provider/model/data class, disallowed effects and empty/oversized arrays.
- Semantic validation binds every authorization and policy reference to exact source revisions and an accepted authority.
- Execution, verification, qualification, release, deployment and acceptance remain distinct records.
- Independent reviewer evidence names the exact schema and validator revisions.
- Runtime use remains blocked until accepted A0 issuer/lifecycle, MH-12 authority, R-06 disposition and target manifest are available.

## 5. Disposition

Wave 15 records ten actionable source-level findings. The v0.1 schemas remain unchanged. Existing 15/15 Wave 13 structural assertions and the Wave 14 bounded cross-artifact checks are useful smoke evidence only; they are not full JSON Schema validation, semantic qualification or proof of a live registry/scheduler.

Next: review the findings, create versioned v0.2 schema candidates, then validate with an approved standards-compliant validator and independent review after the relevant execution authorization is in place.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
