# MediaHub OS — Mature Project Source Screening, Wave 440

- Date: 2026-10-23
- Status: 10 NEW REPOSITORIES SCREENED / 8 LICENSE+MANIFEST PAIRS READ / 2 PATH/LICENCE EXCEPTIONS / INVENTORY OPEN
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Baseline SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Candidate register: [MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Prior screen: [Wave 439](MEDIAHUB-MATURE-PROJECT-SOURCE-SCREENING-WAVE-439-2026-10-23.md)
- Research PR: https://github.com/VlDMlNSh/mediahub-os/pull/585
- Governance: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Scope and outcome

Wave 440 screens additional mature projects for sandbox isolation, vulnerability scanning, SBOM generation, supply-chain scoring, GitHub Actions security linting, dependency automation, static analysis and artifact-policy enforcement. Ten new upstream repositories were added; no duplicates were found in the previous 118-record register.

Updated inventory: 128 records = 99 CANDIDATE + 22 CONDITIONAL + 2 REFERENCE_ONLY + 5 EXCLUDED_FROM_ACTIVE_SHORTLIST. Count invariant verified.

## 2. Source evidence

Source commits below are immutable refs returned by repository-scoped GitHub commit search. This does not prove equality to default-branch HEAD or a supported release tag.

| Project | Source commit | License evidence | Manifest evidence | Disposition |
|---|---|---|---|---|
| [gVisor](https://github.com/google/gvisor) | [8938ebcf1c12a6266bdf5a650088e1360777aa94](https://github.com/google/gvisor/commit/8938ebcf1c12a6266bdf5a650088e1360777aa94) | Apache-2.0; blob `f7a006d10464cfe9724b5d687c0013bf982cc66a` | `go.mod` blob `d063558784be716b06f65140063c6be8afd6cd28`; module `gvisor.dev/gvisor` | Candidate sandbox isolation reference; host/runtime compatibility untested |
| [Firecracker](https://github.com/firecracker-microvm/firecracker) | [dd7c24b0d165219c9d64f58ecedd0b0328b44fa0](https://github.com/firecracker-microvm/firecracker/commit/dd7c24b0d165219c9d64f58ecedd0b0328b44fa0) | Apache-2.0; blob `d645695673349e3947e8e5ae42332d0ac3164cd7` | `Cargo.toml` blob `a1c9ad79621ecd33017cb6eaedd3630e35d10db0` | Candidate microVM isolation; host requirements must be evaluated |
| [Trivy](https://github.com/aquasecurity/trivy) | [3a0164d6cd627645220730d48d51dc71e10e7156](https://github.com/aquasecurity/trivy/commit/3a0164d6cd627645220730d48d51dc71e10e7156) | Apache-2.0; blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `72885d779cef3211370273cfd8e2ef417edeebc8`; module `github.com/aquasecurity/trivy` | Candidate vulnerability scanner |
| [Syft](https://github.com/anchore/syft) | [1c4d672b2893080704e4af40c89cdcd8a28525cc](https://github.com/anchore/syft/commit/1c4d672b2893080704e4af40c89cdcd8a28525cc) | Apache-2.0; blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `0e8c107ee85f4df035ed296736ee4a74ec29141d`; module `github.com/anchore/syft` | Candidate SBOM generator |
| [Grype](https://github.com/anchore/grype) | [64195bb4d2f060d183b98947b7fdbb5a70f6ebeb](https://github.com/anchore/grype/commit/64195bb4d2f060d183b98947b7fdbb5a70f6ebeb) | Apache-2.0; blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `e5594c560158dc727103f9a9353dcb16278e323a`; module `github.com/anchore/grype` | Candidate vulnerability matching; compare overlap with Trivy |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | [6d4113e03c0014d63613b65b26a0c5a14c98ce3f](https://github.com/ossf/scorecard/commit/6d4113e03c0014d63613b65b26a0c5a14c98ce3f) | Apache-2.0; blob `18f7f43fde86f7ef648559da1e3b2ba46c167f90` | `go.mod` blob `4e122d8b719329fb3699a053cbc506a6e1b40dd6`; module `github.com/ossf/scorecard/v5` | Candidate supply-chain evidence input, not a standalone acceptance decision |
| [zizmor](https://github.com/zizmorcore/zizmor) | [d00d411f6ebe56fa86615747ee399d0df8254c0a](https://github.com/zizmorcore/zizmor/commit/d00d411f6ebe56fa86615747ee399d0df8254c0a) | MIT; blob `491f2b2c09f25968b9554948aa7f9b33708aa23a` | `pyproject.toml` blob `96d1af120771d767fbf750b0fe4c8c3e13e62521`; package `zizmor` | Candidate GitHub Actions workflow security linter |
| [Renovate](https://github.com/renovatebot/renovate) | [a45ee254dc3a7d512f4467174fc9b5503bbf481a](https://github.com/renovatebot/renovate/commit/a45ee254dc3a7d512f4467174fc9b5503bbf481a) | Root `LICENSE` path returned 404; LICENSE UNVERIFIED | `package.json` blob `263c25ccb144dfc5758a4bf1ba621d72b0067027`; version field `0.0.0-semantic-release` | CONDITIONAL; resolve license path and terms |
| [Semgrep](https://github.com/semgrep/semgrep) | [087e93b3a1fdf44f97bc92b5b9c2ba221cb2488b](https://github.com/semgrep/semgrep/commit/087e93b3a1fdf44f97bc92b5b9c2ba221cb2488b) | GPL-family terms observed; blob `8000a6faacf471c537530805ab29523c7732e11a`; legal review required | Root `pyproject.toml` returned 404 | CONDITIONAL; locate correct build manifest and review exact reuse terms |
| [Sigstore Policy Controller](https://github.com/sigstore/policy-controller) | [f9ba304f0d1c4781ececc649d5f01667a82d78c6](https://github.com/sigstore/policy-controller/commit/f9ba304f0d1c4781ececc649d5f01667a82d78c6) | Apache-2.0; blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `e200faa911aad776e1f4ce1894cc5b993d02b7b8`; module `github.com/sigstore/policy-controller` | Candidate signed-artifact policy enforcement; deployment-scope dependent |

## 3. Evidence limitations

- Eight of ten projects had readable LICENSE and root manifest files at the pinned source commit.
- Renovate LICENSE and Semgrep `pyproject.toml` were not found at the tested paths; those gaps are explicit and do not imply missing licenses or permission to reuse.
- No release tags or default branch tips were verified; no upstream CI, lockfile, dependency advisory, or transitive-license audit was run.
- No project was installed or executed. No secret access, provider calls, controller dispatches, deployment or component adoption occurred.
- gVisor/Firecracker sandbox choices require host/runtime feasibility and threat-model review. Trivy/Grype overlap must be tested before selecting one or both. zizmor is particularly relevant to current workflow security, but enforcement remains unproven until run against the repository's workflows.

## 4. MediaHub control status

- Candidate register update commit: `b3f7011b7032201f90a1b732382ccf7fbaa0ad45`; content blob SHA `c1db91252bf67b184057b0b6b9f430a8d1c3e768`.
- Research PR #585 remains the destination for review; new commits require exact-head CI verification.
- Canonical documentation branch remains `docs/mediahub-chat-tree-map-20261012`; research branch is not canonical.
- Issue #301 remains the governing Contour A qualification issue. This screen does not satisfy or bypass its gates.

## 5. Next step

Continue closing evidence gaps, especially release/default refs, lockfiles, dependency advisories, upstream CI and legal scope. Search further for mature workflow-security and provenance components only where the register still has a genuine category gap. Inventory freeze and formal comparison remain blocked until these gates are recorded and reconciled.

**Disposition: 10 NEW REPOSITORIES / 128 TOTAL RECORDS / 2 LICENSE OR MANIFEST EXCEPTIONS / INVENTORY NOT FROZEN / COMPARISON NOT STARTED / NO COMPONENT ADOPTED / CONTOUR A NOT ACCEPTED.**
