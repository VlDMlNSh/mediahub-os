# MediaHub Mature Project Source Screening — Wave 448

- Date: 2026-10-29
- Status: **LATEST RELEASE REFERENCES REFRESHED / SOURCE BLOBS VERIFIED / STRUCTURAL LOCKFILE SCREEN COMPLETE / TRANSITIVE ADVISORY AUDIT NOT COMPLETED**
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Parent PR: https://github.com/VlDMlNSh/mediahub-os/pull/585
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Candidate register: [machine-readable candidate register](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json), blob `f17b26b804b934ed624cf5fe70fba151e2b25cd1`
- Register update commit: `9b0c0cdd394886838f2531bcc83a3583005c0b11`
- Prior canonical Wave 447 upstream-ref report: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-NEXT-UPSTREAM-HEAD-VERIFICATION-AND-PR-STATUS-WAVE-447-2026-10-29.md

## 1. Scope, invariant and limits

This pass refreshed the latest public release references, exact release-target commit IDs, current default-branch HEADs, LICENSE/manifest/lockfile blob identities, selected exact-commit CI runs, and a bounded project-version advisory screen for three existing candidates: zizmor, Trivy and gVisor.

Candidate register read-back: **128 records / 128 unique repositories**; declared counts remain 99 CANDIDATE / 22 CONDITIONAL / 2 REFERENCE_ONLY / 5 EXCLUDED_FROM_ACTIVE_SHORTLIST. No records were added or removed. Discovery remains OPEN_NOT_FROZEN; comparison NOT_STARTED; adoption NONE.

The pass did not install dependencies, run a package scanner, resolve all transitive versions against OSV/GHSA, build upstream projects, qualify a MediaHub subsystem, or approve adoption. Lockfiles were read at exact release and default-head refs and structurally inspected for blob identity/line counts only.

## 2. Exact release refs and source blobs

| Candidate | Latest release tag and exact target commit | Current default-branch HEAD | LICENSE / manifest / lockfile |
|---|---|---|---|
| [zizmor](https://github.com/zizmorcore/zizmor) | [v1.31.1](https://github.com/zizmorcore/zizmor/releases/tag/v1.31.1) → `effdb35fa7868863f11655db256d9008922fa427` | [`bf9ccabc03ca255c8ac3ac43329335d0524e3dd7`](https://github.com/zizmorcore/zizmor/commit/bf9ccabc03ca255c8ac3ac43329335d0524e3dd7) | LICENSE identical at release/head: `491f2b2c09f25968b9554948aa7f9b33708aa23a`. `pyproject.toml` identical: `96d1af120771d767fbf750b0fe4c8c3e13e62521`. `uv.lock` differs: release `c68a7e33664ae40b6e013730f4180e0c831ecf9f`, HEAD `27a9fc3b2eb5bf0e70eb315c985238547519e742`; both observed at 415 lines and 22 package records. |
| [Trivy](https://github.com/aquasecurity/trivy) | [v0.76.1](https://github.com/aquasecurity/trivy/releases/tag/v0.76.1) → `e713f67f7d54decdcd9b3132c9751833dcced698` | [`4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77`](https://github.com/aquasecurity/trivy/commit/4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77) | LICENSE identical: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`. `go.mod`: release `9f2eb69c8a64d1097706a55ada38055d8e17d833`, HEAD `64bd58c933f83ee4133861a72538e6e0131e4a19`. `go.sum`: release `672990d988b1177ccc56c83fc223d233b270d24d` (1,300 lines), HEAD `1beb295a3a0ba30ebecf1c918ce93c7981ae7d52` (1,299 lines). |
| [gVisor](https://github.com/google/gvisor) | [release-20261026.0](https://github.com/google/gvisor/releases/tag/release-20261026.0) → `e8a2a28891ba41f3fb737dee8bb7120745d75826` | [`ac7b4e0fdc7dc4674453438e5e15fc069895620c`](https://github.com/google/gvisor/commit/ac7b4e0fdc7dc4674453438e5e15fc069895620c) | LICENSE identical: `f7a006d10464cfe9724b5d687c0013bf982cc66a`. `go.mod` identical: `d063558784be716b06f65140063c6be8afd6cd28` (133 lines). `go.sum` identical: `7835f843768bb04feaadb125707099d71e15b67b` (502 lines). Annotated release tag object `61bae0ec902c13cf5ec4128759cd64062ad52848` resolves to the commit but GitHub reports the tag object as unsigned; artifact provenance remains unverified.

These checks establish which exact refs/files were read. They do not show that current HEAD is interchangeable with the latest release, nor that transitive dependency risk is acceptable.

## 3. Upstream CI sampled on exact refs

### zizmor — sampled runs SUCCEEDED

Release-ref workflows: [CI 38820769929](https://github.com/zizmorcore/zizmor/actions/runs/38820769929), [security analysis 38820769942](https://github.com/zizmorcore/zizmor/actions/runs/38820769942), [wheel build 38820769919](https://github.com/zizmorcore/zizmor/actions/runs/38820769919), [release 38820810412](https://github.com/zizmorcore/zizmor/actions/runs/38820810412) all completed success. Current default-head CI [40828282626](https://github.com/zizmorcore/zizmor/actions/runs/40828282626), security analysis [40828282582](https://github.com/zizmorcore/zizmor/actions/runs/40828282582), wheel build [40828282674](https://github.com/zizmorcore/zizmor/actions/runs/40828282674), docs deploy [40828282675](https://github.com/zizmorcore/zizmor/actions/runs/40828282675), CodSpeed [40828282632](https://github.com/zizmorcore/zizmor/actions/runs/40828282632) also completed success. Public advisory lookup for zizmor was not retrieved; advisory status is **NOT VERIFIED**.

### Trivy — release checks SUCCEEDED, current-head CI MIXED / NOT QUALIFIED

Release checks [39586330639](https://github.com/aquasecurity/trivy/actions/runs/39586330639) and [39586330915](https://github.com/aquasecurity/trivy/actions/runs/39586330915) completed success. On current main HEAD, merge-group run [40695092936](https://github.com/aquasecurity/trivy/actions/runs/40695092936) has an Ubuntu GoReleaser build failure in [job 122839625090](https://github.com/aquasecurity/trivy/actions/runs/40695092936/job/122839625090): repeated `disk quota exceeded` errors while writing Go build artifacts; GoReleaser exited 1. In that same workflow, Ubuntu unit tests, integration, E2E, VM, module and Kubernetes tests, and the Windows build succeeded; the macOS build was cancelled. Separate push jobs [40695091513](https://github.com/aquasecurity/trivy/actions/runs/40695091513) and [40698250775](https://github.com/aquasecurity/trivy/actions/runs/40698250775) reported “No test required,” so they are not test-pass evidence. Aggregate current-head CI remains **MIXED** until the resource-limited build is resolved or rerun successfully.

### gVisor — sampled runs SUCCEEDED; tag provenance pending

Release staging [40603410346](https://github.com/google/gvisor/actions/runs/40603410346) and release mirror [40606990389](https://github.com/google/gvisor/actions/runs/40606990389) completed success. Sampled release-commit checks [40276747920](https://github.com/google/gvisor/actions/runs/40276747920), [40276748007](https://github.com/google/gvisor/actions/runs/40276748007), [40276748129](https://github.com/google/gvisor/actions/runs/40276748129), and current-head Go/Gazelle/Lint/CI [40828608584](https://github.com/google/gvisor/actions/runs/40828608584), [40828608600](https://github.com/google/gvisor/actions/runs/40828608600), [40828608638](https://github.com/google/gvisor/actions/runs/40828608638), [40828608655](https://github.com/google/gvisor/actions/runs/40828608655) all completed success. The release tag object itself is reported unsigned; verify artifact provenance before any adoption.

## 4. Public advisory screen

- Trivy [GHSA-69fq-xp46-6x23](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23) documents a critical supply-chain compromise associated with the Trivy v0.69.4 binary and affected/unsafe historical action/setup tags. It calls for safe versions and immutable SHA pinning. Trivy v0.76.1 is above the advisory's listed root-binary affected version, but consumers must still avoid floating or compromised historical action tags.
- Trivy also has [GHSA-q3fv-x8vg-qqm4](https://github.com/aquasecurity/trivy/security/advisories/GHSA-q3fv-x8vg-qqm4), fixed in 0.71.0; [GHSA-mcj4-mphf-j9ff](https://github.com/aquasecurity/trivy/security/advisories/GHSA-mcj4-mphf-j9ff), fixed in 0.71.1; and [GHSA-8rc5-4fr6-64pw](https://github.com/aquasecurity/trivy/security/advisories/GHSA-8rc5-4fr6-64pw), fixed in 0.72.0. Version v0.76.1 is newer than these root-project patch floors. This is not a transitive lockfile audit.
- gVisor's [public advisory listing](https://github.com/google/gvisor/security/advisories) showed no published advisories at check time; this is not proof of zero vulnerabilities. zizmor advisory status remains NOT VERIFIED because the page response could not be retrieved.
- Trivy v0.76.1 release notes discuss mitigations related to the eMudhra intermediate-CA incident: [release notes](https://github.com/aquasecurity/trivy/releases/tag/v0.76.1).

## 5. Register and MediaHub PR state

- Register blob read-back: `f17b26b804b934ed624cf5fe70fba151e2b25cd1`; 128 records and 128 unique repositories; status counts unchanged. Candidate rows preserved.
- PR #585 research HEAD at this write is expected to move because this report is being committed. On the previously checked head `bf1c6d86a308aeeeb02480ae6c168fe55c83c99a`, Astra Verify [40831988237](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40831988237) and Astra Cloud Runtime Validation [40831988194](https://github.com/VlDMlNSh/mediahub-os/actions/runs/40831988194) completed success. Recheck the final PR head after this write; do not carry CI conclusions to another SHA.
- PR #585 remains OPEN / DRAFT / UNMERGED; formal review submissions = 0. Combined status API returns pending with zero contexts; effective branch protection/required checks remain NOT VERIFIED. PR #583 is also open/Draft/unmerged, has six observed successful workflows on head `265a6116874739d1826fc5c7dda84b5b8b8f9eeb`, but no formal reviews and no verified effective branch policy.
- No Gemini controller dispatch, child agent run, provider inference, secret read, local executor task, merge, deployment, qualification or component adoption occurred. Contour A remains **NOT ACCEPTED**; Contour B remains gated.

## 6. Next bounded step

Run a reproducible dependency/advisory audit against the exact `uv.lock`, `go.mod` and `go.sum` blobs for these candidates; verify the gVisor release artifact provenance; and obtain a successful rerun or root-cause closure for Trivy's quota-limited GoReleaser job. Keep candidate inventory OPEN_NOT_FROZEN until evidence is inspectable. In parallel, PR #583/#585 still need independent review and authoritative required-check/branch-protection evidence; do not dispatch Gemini or merge before those gates are satisfied.

Canonical map:
https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
