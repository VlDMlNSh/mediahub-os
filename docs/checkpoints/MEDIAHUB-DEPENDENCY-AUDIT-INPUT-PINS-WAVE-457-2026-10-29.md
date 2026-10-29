# MediaHub OS — Pinned Inputs for Dependency/Advisory Audit (Wave 457, Step 1)

- Date: 2026-10-29
- Scope: **STEP 1 ONLY — SELECT AND PIN SOURCE INPUTS AND SCANNER**
- Status: **SOURCE COMMITS/BLOBS PINNED / LOCKFILE SCAN NOT RUN / TOOL PROVENANCE NOT QUALIFIED / NO ADOPTION**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Map addendum: [Wave 457](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-457-2026-10-29.md)
- Continuation checkpoint: [current checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Previous governance evidence: [Wave 454](MEDIAHUB-PR-HEAD-GOVERNANCE-RECHECK-WAVE-454-2026-10-29.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. MediaHub immutable target

- `main` target HEAD: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Canonical documentation branch at start of input pinning: `cf552c0b0f5617360c41dbb4bb6a0834248a9723`.
- Bootstrap blob: `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- The map's Contents API returned its full content (1,192,761 characters) and its effective blob SHA was read via the Git/contents path as `0ad0532a2a6c8ac749add31438a9de2e8003600e`; the separate fetch-file wrapper returned empty content for this large file. Do not treat the empty wrapper content as the map's actual body.

## 2. Exact upstream release snapshots and current HEADs

These are separate source snapshots, intentionally not interchangeable.

| Project | Selected latest release as of 2026-10-29 | Release commit | Current default-branch HEAD | Release metadata |
|---|---|---|---|---|
| [zizmor](https://github.com/zizmorcore/zizmor) | [v1.31.1](https://github.com/zizmorcore/zizmor/releases/tag/v1.31.1) | `effdb35fa7868863f11655db256d9008922fa427` | `bf9ccabc03ca255c8ac3ac43329335d0524e3dd7` (`main`) | Published 2026-10-15; release API `immutable=true`; tag ref resolves directly to a commit |
| [Trivy](https://github.com/aquasecurity/trivy) | [v0.76.1](https://github.com/aquasecurity/trivy/releases/tag/v0.76.1) | `e713f67f7d54decdcd9b3132c9751833dcced698` | `4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77` (`main`) | Published 2026-10-21; release API `immutable=true`; tag ref resolves directly to a commit |
| [gVisor](https://github.com/google/gvisor) | [release-20261026.0](https://github.com/google/gvisor/releases/tag/release-20261026.0) | `e8a2a28891ba41f3fb737dee8bb7120745d75826` | `ac7b4e0fdc7dc4674453438e5e15fc069895620c` (`master`) | Published 2026-10-28; release API `immutable=false`; annotated tag object `61bae0ec902c13cf5ec4128759cd64062ad52848` reports `verified=false / unsigned` |

The gVisor tag object dereferences to the recorded release commit. Its unsigned status and mutable release metadata remain open provenance gaps, not reasons to silently substitute the current branch head.

## 3. Exact input file blob identities

### zizmor — Python lockfile plus project manifest

| Snapshot | Commit | File | Git blob SHA | API-returned characters / lines |
|---|---|---|---|---|
| Release v1.31.1 | `effdb35fa7868863f11655db256d9008922fa427` | `uv.lock` | `c68a7e33664ae40b6e013730f4180e0c831ecf9f` | 76,189 / 441 |
| Current `main` | `bf9ccabc03ca255c8ac3ac43329335d0524e3dd7` | `uv.lock` | `27a9fc3b2eb5bf0e70eb315c985238547519e742` | 76,190 / 441 |
| Release and current `main` | respective commits above | `pyproject.toml` | `96d1af120771d767fbf750b0fe4c8c3e13e62521` (identical both refs) | 644 / 25 |

| Release v1.31.1 | `effdb35fa7868863f11655db256d9008922fa427` | `Cargo.lock` | `576fedeeb4bb26439aa0fcb9f7a8d4fc68d10d91` | 110,171 / 4,420 |
| Current `main` | `bf9ccabc03ca255c8ac3ac43329335d0524e3dd7` | `Cargo.lock` | `fce6a87d7caeb0b47df419497dd168664b745bed` | 110,675 / 4,438 |

The `uv.lock` and Rust `Cargo.lock` blobs differ between release and current head, so scans must be separate result sets. Wave 456 separately recorded a narrow rustls advisory overlap; it is not a complete SCA result.

### Trivy — Go module manifest and checksum file

| Snapshot | Commit | File | Git blob SHA | API-returned characters / lines |
|---|---|---|---|---|
| Release v0.76.1 | `e713f67f7d54decdcd9b3132c9751833dcced698` | `go.mod` | `9f2eb69c8a64d1097706a55ada38055d8e17d833` | 25,287 / 489 |
| Current `main` | `4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77` | `go.mod` | `64bd58c933f83ee4133861a72538e6e0131e4a19` | 25,532 / 494 |
| Release v0.76.1 | `e713f67f7d54decdcd9b3132c9751833dcced698` | `go.sum` | `672990d988b1177ccc56c83fc223d233b270d24d` | 123,446 / 1,301 |
| Current `main` | `4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77` | `go.sum` | `1beb295a3a0ba30ebecf1c918ce93c7981ae7d52` | 123,341 / 1,300 |

Both Trivy file blobs differ between release and current head. `go.mod` is the supported OSV-Scanner input; `go.sum` is retained as input identity/integrity evidence and must not be described as a separate supported lockfile scan.

### gVisor — Go module manifest and checksum file

| Snapshot | Commit | File | Git blob SHA | API-returned characters / lines |
|---|---|---|---|---|
| Release release-20261026.0 | `e8a2a28891ba41f3fb737dee8bb7120745d75826` | `go.mod` | `d063558784be716b06f65140063c6be8afd6cd28` | 6,374 / 137 |
| Current `master` | `ac7b4e0fdc7dc4674453438e5e15fc069895620c` | `go.mod` | `d063558784be716b06f65140063c6be8afd6cd28` (identical both refs) | 6,374 / 137 |
| Release and current `master` | respective commits above | `go.sum` | `7835f843768bb04feaadb125707099d71e15b67b` (identical both refs) | 46,236 / 503 |

The two gVisor Go manifest blobs are identical between the selected release commit and current `master`; the commits themselves remain distinct.

## 4. Scanner selection and tool provenance

Selected first-pass scanner: [Google OSV-Scanner](https://github.com/google/osv-scanner), release `v2.7.0`.

- Git tag object: `7ef17deffedb9e9b751fe6c6c328a88de29d9cf4`.
- Tag dereferences to source commit `bfe2f84abd2f09fe0b83ba7f6dad40d296762f40`.
- Release published 2026-10-12; release metadata `immutable=false`.
- Linux x86_64 executable asset API digest: `sha256:160c6253e2922e9e0a6a9771c5c4c40a4b3c6090b34a3cdd5e80c96cc2e4218b` (57,725,088 bytes).
- Linux arm64 executable asset API digest: `sha256:4061ef4c021ed3c47f203b818f337e351336cc5cd67c0274fc36bd1dfc728dd7` (53,870,752 bytes).
- Release checksum asset `osv-scanner_SHA256SUMS` API digest: `sha256:95d69019bcfe0586eb8f07aad4c56e2f734ee969e8e3e209591f259a1bfde88c`.
- Attestation bundle `multiple.intoto.jsonl` API digest: `sha256:f76e4c6fe6c5f12cb209978418ac42de3da63251bdbef16417645c7660f10ea8`.
- GitHub tag-object signature verification: `verified=false / reason=unknown_key`. This is not an accepted signature. Artifact digest metadata was observed, but the downloaded executable, checksum contents, and attestation have **not** been independently verified. Tool qualification remains **NOT VERIFIED**.

Official scanner documentation lists `uv.lock` and `go.mod` among supported lockfile/manifests: [supported lockfiles](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/). Scan commands/options must be checked against the pinned v2.7.0 documentation/source before execution; do not silently rely on moving `main` docs.

## 5. Bounded scan matrix for Step 2

Run each exact input separately and retain JSON output plus raw output digest.

1. zizmor release `v1.31.1`: `Cargo.lock` blob `576fedeeb4bb26439aa0fcb9f7a8d4fc68d10d91`.
2. zizmor release `v1.31.1`: `uv.lock` blob `c68a7e33664ae40b6e013730f4180e0c831ecf9f`.
3. zizmor current `main`: `Cargo.lock` blob `fce6a87d7caeb0b47df419497dd168664b745bed`.
4. zizmor current `main`: `uv.lock` blob `27a9fc3b2eb5bf0e70eb315c985238547519e742`.
5. Trivy release `v0.76.1`: `go.mod` blob `9f2eb69c8a64d1097706a55ada38055d8e17d833`; matching `go.sum` evidence blob `672990d988b1177ccc56c83fc223d233b270d24d`.
6. Trivy current `main`: `go.mod` blob `64bd58c933f83ee4133861a72538e6e0131e4a19`; matching `go.sum` evidence blob `1beb295a3a0ba30ebecf1c918ce93c7981ae7d52`.
7. gVisor release `release-20261026.0`: `go.mod` blob `d063558784be716b06f65140063c6be8afd6cd28`; matching `go.sum` evidence blob `7835f843768bb04feaadb125707099d71e15b67b`.
8. gVisor current `master`: same `go.mod` and `go.sum` blobs, independently labeled with its current commit for provenance.

For Go projects, this matrix only specifies the source snapshots to audit. It does not claim that a `go.mod` scan alone represents all selected/transitive modules or source-reachability; that limitation and any needed reproducible module-graph/source scan must be addressed in Step 2.

## 6. Step 1 exit criteria and disposition

- Release refs and default-branch HEADs: **PINNED / API-RECHECKED**.
- Six relevant source blobs across release/current snapshots: **PINNED**; differences/identical pairs recorded above.
- OSV-Scanner version and published asset digests: **PINNED AS CANDIDATES**.
- Scanner binary checksum verification, attestation verification, execution environment and exact command validation: **NOT VERIFIED / NOT RUN**.
- Dependency scan/advisory results: **NOT RUN**.
- Trivy quota-failure recovery: **NOT RUN**.
- gVisor official checksum-file content comparison and independent provenance: **NOT VERIFIED**.
- Formal reviews and effective branch governance for PR #583/#585: **NOT VERIFIED**.
- No Gemini dispatch/child runs, provider inference, secret access, local executor task, merge, deployment, runtime qualification or component adoption occurred during Step 1.

## 7. Next bounded step

Step 2 will validate the pinned OSV-Scanner v2.7.0 command/output contract and executable checksum/attestation in a controlled, reproducible environment, then scan exactly the eight pinned lockfile snapshots listed above. If tool integrity or the execution environment cannot be established, record the scan as **BLOCKED / NOT RUN**, not PASS. Preserve separate release-vs-current result sets and keep component comparison/adoption gated.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
