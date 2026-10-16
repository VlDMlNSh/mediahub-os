# MediaHub OS — Cloud-Agent Schema Coherence and Map Recovery, Wave 17

- Date: 2026-10-16
- ID: MH-CAF-COHERENCE-17
- Status: **CROSS-SCHEMA REFERENCE REPAIRED / 23 OF 23 BOUNDED ASSERTIONS PASSED / FULL VALIDATION OPEN**
- Contour: A — autonomous development fabric
- Parent: [Wave 15 Schema Semantic Review](MEDIAHUB-CLOUD-AGENT-SCHEMA-SEMANTIC-REVIEW-WAVE-15-2026-10-16.md) and [Wave 16 Schema v0.2 Candidates](MEDIAHUB-CLOUD-AGENT-SCHEMA-V0.2-CANDIDATES-WAVE-16-2026-10-16.md)
- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Cross-schema reference correction

Read-back found that the v0.2 task-envelope candidate still pinned `evidence.manifest_schema` to `mediahub.cloud-agent-evidence-manifest.v0.1`. The candidate task schema and documentary activation queue now consistently reference the v0.2 evidence manifest.

| Artifact | Commit | Current blob SHA | Disposition |
|---|---|---|---|
| Task Envelope Schema v0.2 | `8f1ccc8a3d097425cb3b87aa2d543528b42ab0dd` | `6f3cd3d40b2c5fe3f21bb6085536769fbef8322a` | Candidate schema; evidence-manifest pointer aligned to v0.2 |
| Activation Queue CAF-Q-001…CAF-Q-014 | `87ea24da664eb7855c2a84f1b530d6429370df7f` | `1ef28af318a4be6618e0d9703a3e8d208a807206` | Documentary queue now points to task-envelope v0.2 |
| Agent Registry Schema v0.2 | Earlier Wave 16 artifact | `b49b89b8fbdfc180862e3dc78f8198f35e486035` | Candidate; review and full validation open |
| Evidence Manifest Schema v0.2 | Earlier Wave 16 artifact | `40c402432fd0f3899d45fde0fa0a8af4d34c593a` | Candidate; review and full validation open |

The task envelope additionally binds a semantic-validation profile ID, immutable profile revision reference and policy-bundle digest. These fields describe the required validation profile; they do not authorize execution.

## 2. Bounded read-back checks

A read-only structural check evaluated the current GitHub read-back of the task envelope, registry schema, evidence-manifest schema and activation queue.

**Result: 23/23 assertions passed.**

Coverage:
- all three schemas declare JSON Schema Draft 2020-12;
- task envelope version and evidence-manifest version references agree;
- semantic-validation profile is mandatory in the task envelope;
- registry requires an isolated workspace, expiry/revocation references and bounded unique provider routes;
- execution states exclude `verified` and `qualified`;
- verification and qualification remain separate records;
- action SHA shape, uniqueness and cardinality are constrained;
- input, artifact and schema-reference collections are bounded;
- the queue remains documentary-only, preserves unique historical IDs and points to task-envelope v0.2;
- CAF-Q-014 tracks full validator and negative-fixture evidence.

The first assertion pass reported 22/23 because the check expected the artifact-array maximum to equal 100. Direct read-back showed the candidate uses a stricter maximum of 20, so the assertion was corrected to verify a positive bound no greater than 100. The rerun passed 23/23. This is structural evidence, not a standards-compliant schema validator.

## 3. Full validation and runtime gates

Still open:
1. Draft 2020-12 meta-validation with format assertion enabled.
2. Positive and negative fixture suite for invalid dates, expiry ordering, stale/revoked grants, provider/model/data-class mismatch, capability/effect mismatch, malformed digests, unknown properties and collection bounds.
3. Semantic resolution of every issuer, grant, policy, schema and reviewer reference against immutable accepted sources.
4. Independent review tied to exact candidate SHAs.
5. Accepted A0 ingress/issuer/lifecycle, MH-12 authority, R-06 audit/privacy disposition and authoritative runner/workspace/network target manifest.
6. Any live agent registry, scheduler, provider connection, isolated patch worker or promotion pipeline.

No schema validator was installed; no provider call, secret access, workflow dispatch, project-runtime inspection, infrastructure change, deployment or branch integration occurred in this pass.

## 4. Credential and egress invariant

The target architecture remains GitHub-centered and cloud-hosted: provider credentials are injected only into the authorized job step, and the worker calls the provider over outbound HTTPS. A user-owned always-on server and the user's phone are outside the default credential/egress path. Hosted-runner source IPs may vary; fixed-IP routing is a separately reviewed exception. Network topology does not replace provider account eligibility, terms, data handling, or regional policy.

Reference sources:
- GitHub Actions secure-use guidance: https://docs.github.com/en/actions/reference/security/secure-use
- Gemini API additional terms: https://ai.google.dev/gemini-api/terms
- Gemini available regions: https://ai.google.dev/gemini-api/docs/available-regions

## 5. Project-map integrity

The current map blob returned by GitHub contained only 23 lines and two recent entries, while the latest known complete predecessor blob `6b98de335da9fadc0f92900deff260a8bef6830a` contained 6,812 lines and the Wave 11 map state. Wave 17 restores that complete predecessor, preserves its historical sections, appends the already-created Wave 15 and Wave 16 entries, and adds this Wave 17 entry. This is a documentation-integrity repair, not branch integration.

## 6. Next queue

- **CAF-Q-014 / P0:** standards-compliant Draft 2020-12 meta-validation and negative fixtures.
- **CAF-Q-001 / P0:** accepted A0 issuer/ingress/queue/lifecycle contract.
- **CAF-Q-002 / P0:** R-06 audit/privacy governance disposition.
- **CAF-Q-012 / P1:** authoritative runner/workspace/network target manifest.
- **CAF-Q-003 / P0:** independent review of the source-bound Gemini workflow hardening proposal before any source edit.
- **CAF-Q-008 / P1:** PR promotion, required checks and independent-review governance.

The queue remains a versioned planning artifact. Activation requires the accepted A0 lifecycle and the applicable task-specific grants.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
