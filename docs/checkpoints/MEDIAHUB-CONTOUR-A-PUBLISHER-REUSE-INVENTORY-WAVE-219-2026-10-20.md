# MediaHub OS Contour A — publisher reuse inventory (Wave 219)

- Date: 2026-10-20
- Status: **DESIGN INPUT / NOT IMPLEMENTATION / NOT ACCEPTANCE**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Working PR: https://github.com/VlDMlNSh/mediahub-os/pull/396

## 1. Existing components inspected on main

| Component | Blob SHA | Verified behavior | Not established |
|---|---|---|---|
| `ops/mesh/artifacts.py` | `a5dddf3b58a35e21385e3c9f9049a6e538c2e71b` | Computes SHA-256, verifies an expected digest, and checks required manifest keys/schema version/digest/size consistency. | No source-bound check of task issuer, capability, lease/cancel state, target SHA, allowed output paths, path traversal, or trusted publisher authority is performed by this small module. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Three checkout steps, upload of `astra-distributed-worker-result.json`. | Workflow currently declares `contents: write` and all three checkout steps persist credentials. Worker code can also perform git add/commit/push. |
| `.github/workflows/astra-node-result-publication.yml` | `087a373fe113d11a81be4d349e4c3d330a22f33c` | Separate workflow consumes a named controller/GOLD node-result artifact and publishes a sanitized controller result. | Its artifact contract and controller-result semantics are not proof of a worker-source-artifact publisher; do not reuse it by assumption. |
| `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Requires identity/trust/authorization/State Authority path before canonical mutation; insufficient capability must deny. | Does not, by itself, prove the worker workflow enforces a publisher-specific issuer/capability check. |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Defines lease TTL, required execution metadata, candidate cloud executor paths, and preserves mandatory paths until qualified. | Not a complete worker artifact envelope or publisher authorization implementation. |

## 2. Existing hardening candidate

PR #375, [Draft: minimize distributed worker checkout credential exposure](https://github.com/VlDMlNSh/mediahub-os/pull/375), proposes changing worker workflow `contents: write` to `contents: read`, disabling persisted checkout credentials on three checkout steps, and adding dependency-free static regression tests. Its description explicitly says its test suite was not executed in that pass and that issuer/capability governance, FCC token propagation, OS/network isolation, and publisher provenance remain unresolved.

A previous map/checkpoint snapshot says the PR was two commits ahead and zero behind at an older point, but current exact PR head/base SHA and current branch divergence were not independently recovered in this pass. The recorded successful runs `39295373907` and `39295373833` were queried by SHA `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`; that SHA was not established here as the current PR #375 head. Therefore these runs are **not accepted as exact-head evidence for PR #375**.

## 3. Safe design decision

Reuse `ops/mesh/artifacts.py` as a digest-verification primitive only after adding higher-level validation; do not treat it as the trust boundary. Do not repurpose the node-result publisher until its trigger, artifact schema, identity binding, and authorization model are proven to match worker task outputs.

The next implementation candidate should:
1. Keep the worker workflow read-only and remove persisted checkout credentials, if current exact-head review confirms the existing PR #375 change remains correct and based on a safe current ref.
2. Remove worker-side Git publication from the worker execution path rather than relying only on environment scrubbing.
3. Emit an artifact manifest bound to immutable task ID, source SHA, allowed paths, digest, size, result metadata, lease/cancellation state, and provenance.
4. Let a separate trusted publisher validate the manifest and A0 issuer/capability before creating a branch/PR.
5. Include negative tests for unexpected paths, traversal, digest mismatch, target SHA mismatch, stale/replayed task, missing evidence, and unauthorized publisher invocation.

## 4. Verification status

- GitHub source read-back completed for all five components above; blob SHAs are recorded.
- No local tests were executed and no workflow was dispatched in this wave.
- No code or workflow was modified; this is reuse research and sequencing.
- No PR was merged and no deployment or qualification gate was promoted.
- Current generated truth remains NOT_PROVEN / BLOCKED, with G0–G11 BLOCKED and G11 HUMAN_ONLY.

## 5. Next concrete action

Recover PR #375's exact head/base, changed-file list, current divergence, review submissions and exact-head CI. If it is stale, do not merge or rebase blindly; compare its two-file diff against current main and create a fresh bounded candidate only after checking for intervening changes. In parallel, design the worker-specific artifact manifest/publisher capability contract.
