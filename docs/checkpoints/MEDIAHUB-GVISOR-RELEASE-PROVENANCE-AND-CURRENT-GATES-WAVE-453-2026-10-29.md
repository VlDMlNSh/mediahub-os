# MediaHub OS — gVisor Release Provenance and Current Gate Recheck (Wave 453)

- Date: 2026-10-29
- Status: **CURRENT PR HEADS/OBSERVED CI VERIFIED / gVISOR RELEASE ASSET DIGEST METADATA OBSERVED / ARTIFACT PROVENANCE NOT VERIFIED / DISPATCH BLOCKED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Map addendum: [Wave 453](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-453-2026-10-29.md)
- Continuation checkpoint: [current checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Immutable MediaHub target and current PR gates

- MediaHub `main` HEAD/base target: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Canonical docs branch before this Wave 453 pass: `59157690f68e3b5cd73b6814f3fca33db27a9cc1`; the current map blob read through Contents API was empty, so its SHA was read using Git blob fallback: `11924da464a7bc52474bd938ee3dceb32d10c22b` (1,187,596 characters). Its leading index still began at Wave 451 and did not include Wave 452.
- PR [#583](https://github.com/VlDMlNSh/mediahub-os/pull/583) is OPEN / DRAFT / UNMERGED at exact head `448bcbe6b941847b993dc2675a74367cce276b3e`. Six observed check-runs completed SUCCESS on this SHA: Astra Verify [40832709532](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832709532), Cloud Runtime Validation [40832709559](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832709559), Gemini contract validation [40832709572](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832709572), provider contract [40832709553](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832709553), AI Factory verification [40832709536](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832709536), and controller probe [40832709652](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832709652). The probe was explicitly non-launching: admission and dispatch/monitor jobs were SKIPPED. This is not an agent batch.
- PR [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585) is OPEN / DRAFT / UNMERGED at exact head `8940c7f0f66c9f50e2d83659a6231aa790817221`. Astra Verify [40832496142](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832496142) and Cloud Runtime Validation [40832496196](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832496196) completed SUCCESS on that exact SHA.
- Current formal review submissions: zero for #583 and #585. Both combined-status endpoints report pending with zero contexts. `main` branch metadata reports `protected=false`; the repository rulesets listing returned empty, while direct branch-protection inspection returned HTTP 403. Effective required-check and branch governance therefore remain **NOT VERIFIED**; neither `protected=false` nor an empty visible ruleset list is used as proof of no applicable policy.
- No merge, deployment, component adoption, provider inference, secret access, local executor task or Gemini batch/child dispatch occurred. Contour A remains NOT ACCEPTED; Contour B remains gated.

## 2. Exact gVisor release and artifact evidence

- Upstream repository: [google/gvisor](https://github.com/google/gvisor).
- Releases API first page lists `release-20261026.0` as the newest observed release, published `2026-10-28T00:10:59Z`. Release API URL: [release-20261026.0](https://github.com/google/gvisor/releases/tag/release-20261026.0).
- Release tag object: `61bae0ec902c13cf5ec4128759cd64062ad52848`; GitHub verification result is `verified=false, reason=unsigned`. It points to exact commit `e8a2a28891ba41f3fb737dee8bb7120745d75826` ([commit](https://github.com/google/gvisor/commit/e8a2a28891ba41f3fb737dee8bb7120745d75826)). That differs from current `master` HEAD `ac7b4e0fdc7dc4674453438e5e15fc069895620c`.
- GitHub Release metadata reports `immutable=false`. This is an observed release-metadata property, not a statement that the commit SHA changes; it means the release record/assets have not been established as immutable by that API.
- Release assets and the API-supplied SHA-256 digests:
  - `gvisor-aarch64.tar.bz2`: `6b03c9d53f46b5ac56fd32522f38f108645e9f80a26a335e86ad1e09dcdaefda`
  - `gvisor-aarch64.tar.zstd`: `6257e49955f13e6caceb2c4181c5dc5406c460e805940c944e67ad65553f5b02`
  - `gvisor-x86_64.tar.bz2`: `096589d2d6078ba4caa26aa0200932f571aa5da9d08a5156b98ab1d93fa54468`
  - `gvisor-x86_64.tar.zstd`: `708afc62f2ee82d19930c703e85f9dab4f27a78c0aec40c0f55eb1040107f1a7`
  - `SHA256SUMS` asset: `5d295466f759f2bccc6563f099f24d7850aacab33850684571416de64d1a18b0`
  - `SHA512SUMS` asset: `f58a5fea513824771a42df15d7b5845eebdb183ae4c37c1ac5e642bc56f05784`
- The upstream [gVisor release policy](https://gvisor.dev/release/) states that the Google Cloud Storage release bucket is the canonical channel, GitHub release artifacts mirror it, and SHA256/SHA512 checksum files are provided. The [installation guide](https://gvisor.dev/docs/user_guide/install/) describes release tarballs and checksum files.
- Release Mirror workflow [40606990389](https://github.com/google/gvisor/actions/runs/40606990389) completed SUCCESS on exact release commit `e8a2a28891ba41f3fb737dee8bb7120745d75826`. This verifies that one recorded workflow concluded successfully; it does not prove independent release provenance.
- The checksum files were listed in release metadata, but their contents were not independently retrieved and compared with the asset digests in this pass. The GitHub attestation query was not available through the connected GitHub fetch integration; that is a tooling limitation, not evidence that attestations do not exist. No signed tag, verified commit signature, or successful independent artifact-attestation result was obtained.
- Therefore, release ref and GitHub asset digest metadata are **OBSERVED/VERIFIED AS API METADATA**, while gVisor artifact provenance remains **NOT VERIFIED**. Do not qualify or adopt gVisor on this evidence.

## 3. Remaining upstream qualification gaps

- The Wave 449 source screen records the zizmor `uv.lock` release blob `c68a7e33664ae40b6e013730f4180e0c831ecf9f` and current-head blob `27a9fc3b2eb5bf0e70eb315c985238547519e742`; the contents have not undergone a transitive advisory audit, and its public advisory state remains NOT VERIFIED.
- Trivy `go.mod` release/current blobs are `9f2eb69c8a64d1097706a55ada38055d8e17d833` / `64bd58c933f83ee4133861a72538e6e0131e4a19`; `go.sum` release/current blobs are `672990d988b1177ccc56c83fc223d233b270d24d` / `1beb295a3a0ba30ebecf1c918ce93c7981ae7d52`. Its sampled current-head GoReleaser job failed from runner disk quota; CI remains MIXED / NOT QUALIFIED.
- gVisor `go.mod` blob `d063558784be716b06f65140063c6be8afd6cd28` and `go.sum` blob `7835f843768bb04feaadb125707099d71e15b67b` match at the release and current head, but package-level/transitive advisories remain NOT AUDITED.
- A reproducible pinned dependency/advisory audit has not run for these source snapshots. Inventory remains OPEN_NOT_FROZEN; comparison and adoption remain NOT_STARTED/NONE.

## 4. Disposition and next bounded step

- Current PR heads and the observed exact-head CI runs: **VERIFIED** as listed above.
- Formal reviews: **NOT VERIFIED / zero submissions observed**.
- Effective branch governance: **NOT VERIFIED**.
- gVisor release-tag signature and independent artifact provenance: **NOT VERIFIED**.
- Complete pinned lockfile/transitive-advisory audit: **NOT RUN**.
- Gemini batch and child workflows: **NOT RUN**; provider/local execution, merge, deployment and qualification: **NOT RUN**.
- Next bounded step: run a reproducible, read-only dependency/advisory audit against the exact recorded lockfile/manifest blobs for zizmor, Trivy and gVisor, preserving release-vs-current-head separation. Separately resolve the Trivy quota-limited job and obtain formal independent reviews plus authoritative effective branch-policy evidence before inventory freeze, adoption, merge or controller dispatch.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
