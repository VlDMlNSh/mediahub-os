# MediaHub OS — Mature Project Source Screening, Wave 444

- Date: 2026-10-29
- Status: THREE EXISTING RECORDS ENRICHED / RELEASE REFS PINNED / MANIFEST AND LOCKFILE AUDIT STILL OPEN
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Parent PR: [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585)
- Candidate register: [Wave 432 machine-readable register, updated by Wave 444](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Canonical continuation checkpoint: [current checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Scope and invariant

This pass enriched three already-present candidate records: zizmor, Trivy and gVisor. **No candidate rows were added or removed.** The register remains 128 records / 128 unique repositories: 99 CANDIDATE, 22 CONDITIONAL, 2 REFERENCE_ONLY, 5 EXCLUDED_FROM_ACTIVE_SHORTLIST. Formal comparison remains NOT STARTED; inventory freeze remains NOT READY; no component was adopted.

## 2. Release-tag and source evidence

| Candidate | Release ref observed in public listing | Exact tag commit SHA | Default branch | License blob SHA at release and default ref | Release manifest blob SHA | Default-ref manifest blob SHA | Release lockfile blob SHA | Default-ref lockfile blob SHA |
|---|---|---|---|---|---|---|---|---|
| [zizmor](https://github.com/zizmorcore/zizmor) | [`v1.30.1`](https://github.com/zizmorcore/zizmor/releases/tag/v1.30.1) | `99a054ed9283c90abdd2d5b9fb5101d27dde9783` | `main` | `491f2b2c09f25968b9554948aa7f9b33708aa23a` | `pyproject.toml` `7b31b5ffd53a7de427a1dfb09c34da98c58e6cc7` | `pyproject.toml` `96d1af120771d767fbf750b0fe4c8c3e13e62521` | `uv.lock` `4c8652a412372ba5b1fdcb70da99a989f3ca7f03` | `uv.lock` `27a9fc3b2eb5bf0e70eb315c985238547519e742` |
| [Trivy](https://github.com/aquasecurity/trivy) | [`v0.76.0`](https://github.com/aquasecurity/trivy/releases/tag/v0.76.0) | `531360e5d2a88e732373f1614ba99a38738538b8` | `main` | `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` `1b94feb298f88964d3fb1d19b02a0a411774b138` | `go.mod` `64bd58c933f83ee4133861a72538e6e0131e4a19` | `go.sum` `a07b63dfa1badfa034ebb9c078d6a2c32cbcebd8` | `go.sum` `1beb295a3a0ba30ebecf1c918ce93c7981ae7d52` |
| [gVisor](https://github.com/google/gvisor) | [`release-20261019.0`](https://github.com/google/gvisor/releases) | `760b80785dc53311d4c87bd2de167525a99709c1` | `master` | `f7a006d10464cfe9724b5d687c0013bf982cc66a` | `go.mod` `294ae28a2e67c7f556cbab16b789afd0ff06c531` | `go.mod` `d063558784be716b06f65140063c6be8afd6cd28` | `go.sum` `4370b95ac74ab0cc579d848b9ecd5505084d963f` | `go.sum` `7835f843768bb04feaadb125707099d71e15b67b` |

### Interpretation

- A specific release tag and full commit SHA were recorded for all three candidates. Public releases listings observed on 2026-10-29 showed zizmor `v1.30.1`, Trivy `v0.76.0` and gVisor `20261019.0` (tag ref `release-20261019.0`).
- License blobs are identical between each selected release ref and its current default ref at the observed paths.
- Manifest and lockfile blob SHAs differ between release and current default ref in all three candidates. This is concrete evidence not to collapse a release ref and default-branch state into one assumed dependency snapshot.
- The exact current default-branch HEAD SHA was **NOT VERIFIED** by the available repository metadata. File-blob comparisons are not proof of branch-head equivalence.
- Lockfile blobs and contents were retrieved, but the lockfiles have **NOT BEEN AUDITED**. Dependency advisories, upstream CI qualification, transitive-license evaluation and subsystem tests remain NOT STARTED.

## 3. Source references

- zizmor [release listing](https://github.com/zizmorcore/zizmor/releases), [release commit](https://github.com/zizmorcore/zizmor/commit/99a054ed9283c90abdd2d5b9fb5101d27dde9783), [release manifest](https://github.com/zizmorcore/zizmor/blob/v1.30.1/pyproject.toml), [release lockfile](https://github.com/zizmorcore/zizmor/blob/v1.30.1/uv.lock), [current default manifest](https://github.com/zizmorcore/zizmor/blob/main/pyproject.toml), [current default lockfile](https://github.com/zizmorcore/zizmor/blob/main/uv.lock).
- Trivy [release listing](https://github.com/aquasecurity/trivy/releases), [release commit](https://github.com/aquasecurity/trivy/commit/531360e5d2a88e732373f1614ba99a38738538b8), [release manifest](https://github.com/aquasecurity/trivy/blob/v0.76.0/go.mod), [release lockfile](https://github.com/aquasecurity/trivy/blob/v0.76.0/go.sum), [current default manifest](https://github.com/aquasecurity/trivy/blob/main/go.mod), [current default lockfile](https://github.com/aquasecurity/trivy/blob/main/go.sum).
- gVisor [release listing](https://github.com/google/gvisor/releases), [release policy and cadence](https://gvisor.dev/release/), [release commit](https://github.com/google/gvisor/commit/760b80785dc53311d4c87bd2de167525a99709c1), [release manifest](https://github.com/google/gvisor/blob/release-20261019.0/go.mod), [release lockfile](https://github.com/google/gvisor/blob/release-20261019.0/go.sum), [current default manifest](https://github.com/google/gvisor/blob/master/go.mod), [current default lockfile](https://github.com/google/gvisor/blob/master/go.sum).

## 4. Register update and validation

- Candidate register before this pass: blob `a84c3d9cdfd3b596b5d8bf382c361aac90944eea`.
- Updated register blob: `be836e92203f6ce137f12fa87e1cb18e803ad71c`.
- Register update commit: `b11c17c1ed5bce016ac0e625a2e9e804fb2a2042`.
- The machine-readable register update preserved all 128 unique records and the existing 99/22/2/5 status counts. Three records gained a release tag/commit, release manifest and lockfile blob evidence, current-default-ref blob comparison, and explicit NOT VERIFIED / NOT AUDITED states.

No dependencies were installed, no candidate was executed, no provider call or secret access occurred, and no production workflow, deployment or runtime path was changed.

## 5. Disposition and next step

- Source refs and selected release blobs: **RECORDED / READ BACK VERIFICATION PENDING**.
- Latest default-branch HEAD equivalence, lockfile audit, dependency advisories, exact upstream CI, formal candidate comparison and inventory freeze: **NOT VERIFIED / NOT STARTED**.
- PR #585: remains a Draft research proposal; integration eligibility is not implied by this evidence. Exact-head CI must be rechecked after all documentation commits advance the research branch.
- Contour A: **NOT ACCEPTED**; Contour B remains gated.

Next: read the register back and validate the 128-record invariant; after the final report commit, recheck PR #585's new exact head and all checks. Continue with exact upstream HEAD/release parity and lockfile/advisory evidence before freezing the inventory.
