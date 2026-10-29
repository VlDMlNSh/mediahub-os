# MediaHub OS — Upstream Latest Release, Lockfile and Advisory Screen (Wave 448)

- Date: 2026-10-29
- Status: **SOURCE REFS VERIFIED / STRUCTURAL LOCKFILE SCREEN RECORDED / TRANSITIVE ADVISORY AUDIT NOT RUN / PR #585 CURRENT-HEAD CI NOT YET VERIFIED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Map addendum: [Wave 448 addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-448-2026-10-29.md)
- Continuation checkpoint: [current checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Research source report: [Wave 448 candidate source screen](https://github.com/VlDMlNSh/mediahub-os/blob/research/mature-ai-project-landscape-wave431-20261023/docs/checkpoints/MEDIAHUB-MATURE-PROJECT-SOURCE-SCREENING-WAVE-448-2026-10-29.md)
- Candidate register: [machine-readable register](https://github.com/VlDMlNSh/mediahub-os/blob/research/mature-ai-project-landscape-wave431-20261023/docs/checkpoints/MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json), blob `f17b26b804b934ed624cf5fe70fba151e2b25cd1`
- Governing Issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. MediaHub source refs and governance

- `main` HEAD at verification: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Canonical docs branch: `docs/mediahub-chat-tree-map-20261012`; map blob before this update: `f7e0f186a63a56102e917da3a4dec67b3569badd`.
- Issue #301 remains OPEN (last reported update `2026-10-23T14:55:53Z`, 196 comments).
- PR #583 remains OPEN / DRAFT / UNMERGED at head `265a6116874739d1826fc5c7dda84b5b8b8f9eeb`. Six observed exact-head workflows succeeded: Astra Verify [39984638744](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39984638744); controller contract validation [39984638700](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39984638700); non-launching controller probe [39984638718](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39984638718); provider contract [39984638939](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39984638939); AI Factory verification [39984638905](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39984638905); Cloud Runtime Validation [39984639019](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39984639019). The probe was non-launching; this is not a Gemini batch.
- PR #585 research head at this report check: `fe57a19e189e3dd3f95c0d40747685349ffbeb23`. After the initial in-progress read, exact-head recheck confirmed Astra Verify [40832270154](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832270154) and Astra Cloud Runtime Validation [40832270170](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40832270170) both completed **success** on the same immutable SHA `fe57a19e189e3dd3f95c0d40747685349ffbeb23`. This evidence is exact-head CI only; the combined-status API remains pending with zero contexts. Earlier head `bf1c6d86a308aeeeb02480ae6c168fe55c83c99a` had both observed workflows succeed (runs [40831988237](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40831988237), [40831988194](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40831988194)); those results do not prove the newer head.
- Formal PR review submissions: zero for #583 and #585 at the check. Combined status APIs returned pending/zero contexts for #585. An authoritative effective branch-protection/required-check read remains unavailable (branch-protection endpoint returned HTTP 403; empty ruleset list is not proof of no protection). Integration eligibility remains **NOT VERIFIED**.

## 2. Latest release and exact-source evidence

The candidate register was re-read as valid JSON: 128 records / 128 unique repositories; declared status counts 99 CANDIDATE / 22 CONDITIONAL / 2 REFERENCE_ONLY / 5 EXCLUDED_FROM_ACTIVE_SHORTLIST. No candidate was added or removed. Discovery remains OPEN_NOT_FROZEN, comparison NOT_STARTED, adoption NONE.

| Candidate | Latest release ref → exact commit | Current default-branch HEAD | File evidence |
|---|---|---|---|
| [zizmor](https://github.com/zizmorcore/zizmor) | [v1.31.1](https://github.com/zizmorcore/zizmor/releases/tag/v1.31.1) → `effdb35fa7868863f11655db256d9008922fa427` | [`bf9ccabc03ca255c8ac3ac43329335d0524e3dd7`](https://github.com/zizmorcore/zizmor/commit/bf9ccabc03ca255c8ac3ac43329335d0524e3dd7) | LICENSE blob matches release/head: `491f2b2c09f25968b9554948aa7f9b33708aa23a`; `pyproject.toml` matches: `96d1af120771d767fbf750b0fe4c8c3e13e62521`; `uv.lock` differs (release `c68a7e33664ae40b6e013730f4180e0c831ecf9f`, head `27a9fc3b2eb5bf0e70eb315c985238547519e742`), while both are 415 lines and contain 22 package records. |
| [Trivy](https://github.com/aquasecurity/trivy) | [v0.76.1](https://github.com/aquasecurity/trivy/releases/tag/v0.76.1) → `e713f67f7d54decdcd9b3132c9751833dcced698` | [`4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77`](https://github.com/aquasecurity/trivy/commit/4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77) | LICENSE matches: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`; release/head `go.mod` blobs `9f2eb69c8a64d1097706a55ada38055d8e17d833` / `64bd58c933f83ee4133861a72538e6e0131e4a19`; `go.sum` blobs `672990d988b1177ccc56c83fc223d233b270d24d` / `1beb295a3a0ba30ebecf1c918ce93c7981ae7d52` (1,300 vs 1,299 lines). |
| [gVisor](https://github.com/google/gvisor) | [release-20261026.0](https://github.com/google/gvisor/releases/tag/release-20261026.0) → `e8a2a28891ba41f3fb737dee8bb7120745d75826` | [`ac7b4e0fdc7dc4674453438e5e15fc069895620c`](https://github.com/google/gvisor/commit/ac7b4e0fdc7dc4674453438e5e15fc069895620c) | LICENSE matches: `f7a006d10464cfe9724b5d687c0013bf982cc66a`; `go.mod` matches: `d063558784be716b06f65140063c6be8afd6cd28`; `go.sum` matches: `7835f843768bb04feaadb125707099d71e15b67b`. Annotated tag object `61bae0ec902c13cf5ec4128759cd64062ad52848` resolves to the release commit but is reported unsigned; artifact provenance remains NOT VERIFIED. |

Source blob identity checks and structural lockfile counts do not establish dependency safety. No dependency installation or full dependency resolution was performed.

## 3. Upstream CI and advisory evidence

### zizmor — sampled CI SUCCEEDED; advisory state NOT VERIFIED

Release runs [38820769929](https://github.com/zizmorcore/zizmor/actions/runs/38820769929), [38820769942](https://github.com/zizmorcore/zizmor/actions/runs/38820769942), [38820769919](https://github.com/zizmorcore/zizmor/actions/runs/38820769919), [38820810412](https://github.com/zizmorcore/zizmor/actions/runs/38820810412) and current-head runs [40828282626](https://github.com/zizmorcore/zizmor/actions/runs/40828282626), [40828282582](https://github.com/zizmorcore/zizmor/actions/runs/40828282582), [40828282674](https://github.com/zizmorcore/zizmor/actions/runs/40828282674), [40828282675](https://github.com/zizmorcore/zizmor/actions/runs/40828282675), [40828282632](https://github.com/zizmorcore/zizmor/actions/runs/40828282632) completed success. The public advisory page was not retrievable in this pass.

### Trivy — release checks SUCCEEDED; current default-head CI MIXED / NOT QUALIFIED

Release tests/build evidence: [Test 39586330639](https://github.com/aquasecurity/trivy/actions/runs/39586330639), [Release 39586330915](https://github.com/aquasecurity/trivy/actions/runs/39586330915), [Test 39586309315](https://github.com/aquasecurity/trivy/actions/runs/39586309315), all success. Current-head merge-group run [40695092936](https://github.com/aquasecurity/trivy/actions/runs/40695092936) has an Ubuntu GoReleaser job failure: [job 122839625090](https://github.com/aquasecurity/trivy/actions/runs/40695092936/job/122839625090) logs `disk quota exceeded` while writing Go build artifacts and GoReleaser exits 1. In that run, unit tests, integration, E2E, VM, module and Kubernetes tests plus Windows build succeeded; macOS build was cancelled. Separate push runs [40695091513](https://github.com/aquasecurity/trivy/actions/runs/40695091513) and [40698250775](https://github.com/aquasecurity/trivy/actions/runs/40698250775) emitted “No test required”, so they are not test-pass proof. Current-head CI is MIXED until the resource-limited build is explained or rerun successfully.

Published project advisories include [GHSA-69fq-xp46-6x23](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23), a critical supply-chain compromise affecting the Trivy v0.69.4 binary and unsafe/historical action/setup versions; consumers must use safe versions and immutable SHA-pinned actions. Other version-range advisories include [GHSA-q3fv-x8vg-qqm4](https://github.com/aquasecurity/trivy/security/advisories/GHSA-q3fv-x8vg-qqm4) (fixed in 0.71.0), [GHSA-mcj4-mphf-j9ff](https://github.com/aquasecurity/trivy/security/advisories/GHSA-mcj4-mphf-j9ff) (fixed in 0.71.1), and [GHSA-8rc5-4fr6-64pw](https://github.com/aquasecurity/trivy/security/advisories/GHSA-8rc5-4fr6-64pw) (fixed in 0.72.0). v0.76.1 is newer than those root-project patch floors, but this is not a transitive lockfile audit. The v0.76.1 release notes discuss mitigation related to the eMudhra intermediate CA incident: [release notes](https://github.com/aquasecurity/trivy/releases/tag/v0.76.1).

### gVisor — sampled CI SUCCEEDED; release-tag artifact provenance pending

Release staging/mirror [40603410346](https://github.com/google/gvisor/actions/runs/40603410346), [40606990389](https://github.com/google/gvisor/actions/runs/40606990389); release-commit checks [40276747920](https://github.com/google/gvisor/actions/runs/40276747920), [40276748007](https://github.com/google/gvisor/actions/runs/40276748007), [40276748129](https://github.com/google/gvisor/actions/runs/40276748129); and current-head checks [40828608584](https://github.com/google/gvisor/actions/runs/40828608584), [40828608600](https://github.com/google/gvisor/actions/runs/40828608600), [40828608638](https://github.com/google/gvisor/actions/runs/40828608638), [40828608655](https://github.com/google/gvisor/actions/runs/40828608655) completed success. The [public advisory listing](https://github.com/google/gvisor/security/advisories) showed no published advisories at check time, which is not proof of no vulnerabilities. The release tag object is unsigned, so verify the release artifact provenance before adoption.

## 4. Qualification disposition

- Latest release pointers, exact upstream HEADs, and selected file-at-ref blobs: **VERIFIED for these three candidates**.
- Structural lockfile inspection: **VERIFIED**, limited to file SHA/line/package counts.
- Full lockfile and transitive dependency/OSV advisory audit: **NOT RUN / NOT VERIFIED**.
- Upstream CI: zizmor sampled runs **SUCCEEDED**; Trivy release CI **SUCCEEDED** but current-head aggregate **MIXED / NOT QUALIFIED**; gVisor sampled runs **SUCCEEDED** but release artifact provenance **NOT VERIFIED**.
- Candidate inventory remains OPEN_NOT_FROZEN; formal comparison NOT_STARTED; adoption NONE.
- No dependency installs, model/provider calls, secret access, Gemini controller dispatch, child agent run, local executor task, merge, deployment, qualification or production changes were performed.
- PR #583/#585 reviews and effective required-check/branch protection policy remain **NOT VERIFIED**. Controller dispatch remains blocked by governance/readiness gates. Contour A: **NOT ACCEPTED**; Contour B remains gated.

## 5. Next bounded step

Run a reproducible advisory/lockfile audit against exact `uv.lock`, `go.mod` and `go.sum` source blobs; verify gVisor release artifact provenance; resolve/re-run Trivy's quota-limited GoReleaser job; and obtain formal independent reviews plus authoritative branch policy evidence before any inventory freeze or controller dispatch.
