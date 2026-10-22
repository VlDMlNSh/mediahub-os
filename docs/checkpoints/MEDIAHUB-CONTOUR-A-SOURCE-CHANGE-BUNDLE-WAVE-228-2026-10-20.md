# MediaHub Contour A — Source-change bundle boundary (Wave 228)

- Date: 2026-10-20
- Status: **PROPOSED CONTRACT + STRUCTURAL VALIDATOR; NOT AUTHORIZATION / NOT QUALIFICATION**
- Work branch: work/contour-a-source-change-bundle-wave228
- Base SHA: 25033753415fcbecdc7b2fe53085ed1bf2e4b8b4
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Work completed

1. Added architecture/mesh/source-change-bundle.schema.json, a Draft 2020-12 candidate manifest that binds task/command/node IDs, base and target revisions, patch SHA-256/size, changed paths, and explicit issuer/capability/policy/signed-command references. The state is constrained to PROPOSED_UNVERIFIED; the schema description explicitly says schema conformance is not authorization or permission to publish.
2. Added ops/qualification/source_change_bundle.py, a standard-library-only structural/binding validator. It fails closed for unexpected fields, missing/mismatched task-command-node context, revision mismatch, malformed digests/sizes, missing or mismatched issuer/capability/policy/command-digest references, unsafe paths (absolute, traversal, backslash, colon, .git, empty segments), duplicate paths, and paths outside the caller-provided exact owned_paths list.
3. Added tests/qualification/test_source_change_bundle.py with a positive structural-bound case and negative cases for path escape, unauthorized paths, identity/revision mismatch, missing authorization context, unknown fields, invalid digests/sizes, and attempts to promote the state to VERIFIED.

## Verification

- Focused tests: **12 passed**.
- JSON Schema Draft 2020-12 meta-validation via jsonschema.Draft202012Validator.check_schema: **PASS**.
- py_compile: PASS.
- git diff --check: PASS.
- Initial full unittest discovery without PYTHONPATH=runtime: 420 tests attempted, 7 import errors because existing mediahub_runtime imports were not on the path. This was an invocation/environment error, not test assertion failures. Reran with PYTHONPATH=runtime: **438 tests passed, 0 failures/errors**.
- Temporary dependencies were installed through uv run; no project dependency/lockfile changed.

## Trust and scope limits — explicit

- validate_bundle_binding() is **not** a publisher admission gate. expected and owned_paths must come from a separate, authenticated, authorized context; caller-supplied/model-controlled values do not establish trust.
- No signature/HMAC verification, issuer authentication, capability policy evaluation, revocation check, replay ledger, expiry/freshness validation, patch-content hash recomputation, diff parsing, symlink resolution, OS/network sandbox, or publication was implemented in this wave.
- The current run_distributed_local_worker.py still accepts task JSON from ASTRA_MICRO_TASK_JSON and directly commits/pushes changes. This remains the previously identified SEV-1 blocker. This wave does not alter that worker and does not grant a trusted publisher capability.
- The existing control-command schema does not yet provide a fully accepted issuer/capability envelope. The new fields are references/claims to be bound to a separately accepted authority decision, not proof that the decision occurred.
- No worker was dispatched; no secrets were read or changed; no PR was merged; no gate was promoted. Contour A remains NOT_PROVEN / BLOCKED, G0–G11 blocked and G11 human-only.

## Next bounded step

Have governance accept the exact issuer/capability/policy/command-digest contract and identify the trusted admission component. Then add independent cryptographic verification and replay/freshness checks at that boundary, recompute the patch digest and inspect archive/path/symlink semantics, and design a separate publisher with narrowly scoped authority. Keep model execution credentials separate from publication credentials. Only then consider wiring the worker to upload a bundle artifact instead of performing git push.
