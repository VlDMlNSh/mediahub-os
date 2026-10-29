# MediaHub OS — Mature Project Source Screening, Wave 445

- Date: 2026-10-29
- Status: THREE EXISTING RECORDS ENRICHED / RELEASE REFS PINNED / MANIFEST AND LOCKFILE AUDIT STILL OPEN
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Parent PR: [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585)
- Candidate register: [Wave 432 machine-readable register, updated by Wave 445](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Canonical continuation checkpoint: [current checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Scope and invariant

This pass enriched three already-present candidate records: zizmor, Trivy and gVisor. **No candidate rows were added or removed.** The register remains 128 records / 128 unique repositories: 99 CANDIDATE, 22 CONDITIONAL, 2 REFERENCE_ONLY, 5 EXCLUDED_FROM_ACTIVE_SHORTLIST. Formal comparison remains NOT STARTED; inventory freeze remains NOT READY; no component was adopted.

The screen was first prepared under the next sequence identifier, then renumbered after discovering that the canonical continuation checkpoint already uses Wave 444 for the PR #583 CI/governance recheck. The misnumbered working report was removed in commit `6646b97cd92622c3b45a01534f5382a4f76aa113`. This report is the canonical research-sequence record for the candidate-release screening.

## 2. Release-tag and source evidence

| Candidate | Release ref observed in public listing | Exact tag-target commit SHA | Default branch | Current default-branch HEAD SHA | License blob SHA at release and current HEAD | Release manifest blob SHA | Exact-HEAD manifest blob SHA | Release lockfile blob SHA | Exact-HEAD lockfile blob SHA |
|---|---|---|---|---|---|---|---|---|
| [zizmor](https://github.com/zizmorcore/zizmor) | [`v1.30.1`](https://github.com/zizmorcore/zizmor/releases/tag/v1.30.1) | `99a054ed9283c90abdd2d5b9fb5101d27dde9783` | `main` | [`bf9ccabc03ca255c8ac3ac43329335d0524e3dd7`](https://github.com/zizmorcore/zizmor/commit/bf9ccabc03ca255c8ac3ac43329335d0524e3dd7) | `491f2b2c09f25968b9554948aa7f9b33708aa23a` | `pyproject.toml` `7b31b5ffd53a7de427a1dfb09c34da98c58e6cc7` | `pyproject.toml` `96d1af120771d767fbf750b0fe4c8c3e13e62521` | `uv.lock` `4c8652a412372ba5b1fdcb70da99a989f3ca7f03` | `uv.lock` `27a9fc3b2eb5bf0e70eb315c985238547519e742` |
| [Trivy](https://github.com/aquasecurity/trivy) | [`v0.76.0`](https://github.com/aquasecurity/trivy/releases/tag/v0.76.0) | `531360e5d2a88e732373f1614ba99a38738538b8` | `main` | [`4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77`](https://github.com/aquasecurity/trivy/commit/4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77) | `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` `1b94feb298f88964d3fb1d19b02a0a411774b138` | `go.mod` `64bd58c933f83ee4133861a72538e6e0131e4a19` | `go.sum` `a07b63dfa1badfa034ebb9c078d6a2c32cbcebd8` | `go.sum` `1beb295a3a0ba30ebecf1c918ce93c7981ae7d52` |
| [gVisor](https://github.com/google/gvisor) | [`release-20261019.0`](https://github.com/google/gvisor/releases) | `760b80785dc53311d4c87bd2de167525a99709c1` | `master` | [`ac7b4e0fdc7dc4674453438e5e15fc069895620c`](https://github.com/google/gvisor/commit/ac7b4e0fdc7dc4674453438e5e15fc069895620c) | `f7a006d10464cfe9724b5d687c0013bf982cc66a` | `go.mod` `294ae28a2e67c7f556cbab16b789afd0ff06c531` | `go.mod` `d063558784be716b06f65140063c6be8afd6cd28` | `go.sum` `4370b95ac74ab0cc579d848b9ecd5505084d963f` | `go.sum` `7835f843768bb04feaadb125707099d71e15b67b` |

### Interpretation

- The public release listings observed during this pass showed zizmor `v1.30.1`, Trivy `v0.76.0` and gVisor `20261019.0` (source ref `release-20261019.0`). Exact target commit SHAs for those release refs are recorded above.
- License blobs are identical between each selected release ref and its current default ref at the inspected paths.
- Manifest and lockfile blob SHAs differ between each release and current default ref. This is concrete evidence not to collapse a release ref and default-branch state into one assumed dependency snapshot.
- Exact current default-branch HEAD SHAs were resolved by GitHub to full commit SHAs, then LICENSE, manifest and lockfile were fetched again at those exact commits: zizmor `bf9ccabc03ca255c8ac3ac43329335d0524e3dd7`, Trivy `4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77`, gVisor `ac7b4e0fdc7dc4674453438e5e15fc069895620c`. Each exact default-branch HEAD differs from the observed latest release commit. Manifest and lockfile blob SHAs in the table were verified at those exact current HEAD SHAs; this establishes source identity but does not audit dependencies.
- Lockfile blobs and contents were retrieved, but lockfiles have **NOT BEEN AUDITED**. Dependency advisories, upstream CI qualification, transitive-license evaluation and subsystem tests remain NOT STARTED.

## 3. Source references

- zizmor [release listing](https://github.com/zizmorcore/zizmor/releases), [release commit](https://github.com/zizmorcore/zizmor/commit/99a054ed9283c90abdd2d5b9fb5101d27dde9783), [release manifest](https://github.com/zizmorcore/zizmor/blob/v1.30.1/pyproject.toml), [release lockfile](https://github.com/zizmorcore/zizmor/blob/v1.30.1/uv.lock), [current default manifest](https://github.com/zizmorcore/zizmor/blob/main/pyproject.toml), [current default lockfile](https://github.com/zizmorcore/zizmor/blob/main/uv.lock).
- Trivy [release listing](https://github.com/aquasecurity/trivy/releases), [release commit](https://github.com/aquasecurity/trivy/commit/531360e5d2a88e732373f1614ba99a38738538b8), [release manifest](https://github.com/aquasecurity/trivy/blob/v0.76.0/go.mod), [release lockfile](https://github.com/aquasecurity/trivy/blob/v0.76.0/go.sum), [current default manifest](https://github.com/aquasecurity/trivy/blob/main/go.mod), [current default lockfile](https://github.com/aquasecurity/trivy/blob/main/go.sum).
- gVisor [release listing](https://github.com/google/gvisor/releases), [release policy and cadence](https://gvisor.dev/release/), [release commit](https://github.com/google/gvisor/commit/760b80785dc53311d4c87bd2de167525a99709c1), [release manifest](https://github.com/google/gvisor/blob/release-20261019.0/go.mod), [release lockfile](https://github.com/google/gvisor/blob/release-20261019.0/go.sum), [current default manifest](https://github.com/google/gvisor/blob/master/go.mod), [current default lockfile](https://github.com/google/gvisor/blob/master/go.sum).

## 4. Register update and validation

- Candidate register before the initial Wave 444-labelled edit: blob `a84c3d9cdfd3b596b5d8bf382c361aac90944eea`.
- Evidence-enriched register blob before sequence correction: `be836e92203f6ce137f12fa87e1cb18e803ad71c`.
- Register blob after sequence correction: `0a3394115ef4f0d1d04fd92b96e783ed23ba1efa`.
- Exact current default-branch HEAD verification commit: `3587855f20f53a1831e4e88b77b35997dfbaa014`.
- The machine-readable register validates at 128 records / 128 unique repositories, with unchanged 99/22/2/5 status counts. Three existing records contain release tag-target SHAs plus exact current default-branch HEAD SHAs and license, manifest and lockfile blob evidence. Original Wave 440 source-head parity remains NOT VERIFIED; lockfile and advisory audits remain NOT AUDITED.

No dependencies were installed, no candidate was executed, no provider call or secret access occurred, and no production workflow, deployment or runtime path was changed.

## 5. Disposition and next step

- Release refs and selected blobs: **RECORDED; register read-back passed**.
- Exact current default-branch HEAD SHA and file-at-HEAD references: **VERIFIED FOR THESE THREE REPOSITORIES**. Original candidate source-head equivalence, lockfile audit, dependency advisories, exact upstream CI, formal candidate comparison and inventory freeze: **NOT VERIFIED / NOT STARTED**.
- PR #585 remains a Draft research proposal. Final exact-head CI is rechecked separately after all branch commits.
- Contour A: **NOT ACCEPTED**; Contour B remains gated.

Next: finalize the map/checkpoint evidence record, recheck PR #585's final exact head and statuses, then continue exact upstream HEAD/release parity and lockfile/advisory evidence before considering an inventory freeze.
