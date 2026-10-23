# MediaHub OS — Mature Project Source Screening, Wave 436

- Date: 2026-10-23
- Status: PARTIAL SOURCE SCREEN / INFRASTRUCTURE CANDIDATES ADDED / INVENTORY OPEN / COMPARISON NOT STARTED
- MediaHub baseline: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Machine-readable candidate register: [Wave 432 register, latest Wave 436 data](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Prior screen: [Wave 435](MEDIAHUB-MATURE-PROJECT-SOURCE-SCREENING-WAVE-435-2026-10-23.md)
- Parent PR: https://github.com/VlDMlNSh/mediahub-os/pull/585
- Governance issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Scope and evidence boundary

Wave 436 expands the corpus with AI-adjacent infrastructure for repeatable execution, messaging, secret handling, telemetry and policy support. Selected commits were sourced through repository-scoped GitHub commit search. The identifiers are immutable commits; current default-branch pointer equivalence has not been independently confirmed, so they are not described as “latest main” or “current release”.

No software was installed, no secret was accessed, no provider inference or agent dispatch was run, and no runtime or deployment changed.

## 2. Source-pinned candidates

| Candidate | Immutable commit | License evidence | Manifest evidence | Lockfile evidence |
|---|---|---|---|---|
| [Agent Router](https://github.com/theagentrouter/agent-router) | [6d63a4f71f56e9cc370ced2da862787d8d04f06c](https://github.com/theagentrouter/agent-router/commit/6d63a4f71f56e9cc370ced2da862787d8d04f06c) | Apache-2.0; `LICENSE` blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `8dd62d965d6408bd8d24b6f8981b30e724352940`; module remains `github.com/envoyproxy/ai-gateway` | `go.sum` blob `8e7ed239eaefd743c7f1dff2a87875a93eda8683`, 62,934 characters retrieved; audit NOT RUN |
| [Dagger](https://github.com/dagger/dagger) | [930485687df5c9a7ed521f5585a17b2a36936b17](https://github.com/dagger/dagger/commit/930485687df5c9a7ed521f5585a17b2a36936b17) | Apache-2.0; `LICENSE` blob `17b2ba29b525453b46b0311d202b63044d3aa5cb` | `go.mod` blob `44cb897774abde54c5a6fef33c4a6b84a3ede71d`, module `github.com/dagger/dagger` | `go.sum` blob `96da71bed5c9fc302c53a7cdc298c3ba4b6e6371`, 96,406 characters retrieved; audit NOT RUN |
| [NATS Server](https://github.com/nats-io/nats-server) | [f8f6db894528640b27311353e874ac62c3a47af5](https://github.com/nats-io/nats-server/commit/f8f6db894528640b27311353e874ac62c3a47af5) | Apache-2.0; `LICENSE` blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `b8a7ccdfbaca27c053847a7babfc440bec6d0359`, module `github.com/nats-io/nats-server/v2` | `go.sum` blob `32d8014a1a4834a42131ec4131b543088f9981b0`, 1,973 characters retrieved; audit NOT RUN |
| [SOPS](https://github.com/getsops/sops) | [453e7e6ab01b1340dca9f9025fd8430229320f97](https://github.com/getsops/sops/commit/453e7e6ab01b1340dca9f9025fd8430229320f97) | Mozilla Public License 2.0; `LICENSE` blob `a612ad9813b006ce81d1ee438dd784da99a54007` | `go.mod` blob `811f12b2cd3c882ff3ab162109ecd6c2d16310b9`, module `github.com/getsops/sops/v3` | `go.sum` blob `24b7aeb953031c7e495037cf146b10e7b17ae923`, 46,516 characters retrieved; audit NOT RUN |
| [External Secrets Operator](https://github.com/external-secrets/external-secrets) | [e932f3a3f6f274e8e269c01aa1f5fb3d1322e3c9](https://github.com/external-secrets/external-secrets/commit/e932f3a3f6f274e8e269c01aa1f5fb3d1322e3c9) | Apache-2.0; `LICENSE` blob `7a4a3ea2424c09fbe48d455aed1eaa94d9124835` | `go.mod` blob `3b7e0a0aff2396057ef329d84d00f0aa782190cb`, module `github.com/external-secrets/external-secrets` | `go.sum` blob `45c09077846dd375c8f03eb56bcca6be8320ff28`, 154,291 characters retrieved; audit NOT RUN |
| [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | [42ee5d39b18f24c206cca3f91f8b0877424bdfee](https://github.com/open-telemetry/opentelemetry-collector/commit/42ee5d39b18f24c206cca3f91f8b0877424bdfee) | Apache-2.0; `LICENSE` blob `d645695673349e3947e8e5ae42332d0ac3164cd7` | `go.mod` blob `1790f8ef4d615afc21d071486972823ad2201536`; file comments state root go.mod is not used to build | Root `go.sum` NOT FOUND at tested path; monorepo module-specific dependency evidence needed |
| [OpenTelemetry Collector Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) | [0b7da3787f9dd1d72e3e25e4d46f921bb4481e07](https://github.com/open-telemetry/opentelemetry-collector-contrib/commit/0b7da3787f9dd1d72e3e25e4d46f921bb4481e07) | Apache-2.0; `LICENSE` blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `396f250318906632f18c61bddb0bf886404bf84d`, module `github.com/open-telemetry/opentelemetry-collector-contrib` | Root `go.sum` NOT FOUND at tested path; component/module-specific dependency evidence needed |
| [HashiCorp Vault](https://github.com/hashicorp/vault) | [b63ab2722fbb565bece8e6a438adf58921e772b9](https://github.com/hashicorp/vault/commit/b63ab2722fbb565bece8e6a438adf58921e772b9) | Business Source License 1.1; `LICENSE` blob `9017076a38c37bb82914e0cd75bae2930a535d87` | `go.mod` blob `bb61d20db44fe5a0bc2e744c78d77597234111ba`, module `github.com/hashicorp/vault` | `go.sum` blob `5a5d1e835eb6a05bca806672c0dab7602a266a1e`, 171,143 characters retrieved; audit NOT RUN |

## 3. Identity and licensing concerns

- **Agent Router rename/transfer:** querying `envoyproxy/ai-gateway` returned `theagentrouter/agent-router`; the selected repository's Go module still says `github.com/envoyproxy/ai-gateway`. The register marks it CONDITIONAL until transfer/rename history and canonical ownership are reconciled.
- **Vault:** Business Source License 1.1 is not OSI-approved open source. It remains CONDITIONAL/source-available pending legal/business terms review; it is not an assumed code donor.
- **SOPS:** MPL-2.0 is a file-level copyleft license. Its use and any modifications/distribution need a compliance review even though the license is OSI-approved.
- **Dagger/NATS/External Secrets/OpenTelemetry:** all are infrastructure candidates only. They do not become new MediaHub authority or secret-storage authorities by being on this list. Use only if a specific architectural need justifies their operational footprint.
- **OpenTelemetry:** root go.sum could not be found at the tested paths; repository layout is module-oriented. The dependency audit must resolve exact module/collector distributions rather than infer a monorepo-wide lockfile.
- **Lockfiles:** six lockfile contents were retrieved (Agent Router, Dagger, NATS, SOPS, External Secrets, Vault); none were dependency-audited. Two root lockfile paths were not found (OpenTelemetry Collector and Contrib).
- **Default ref, stable tags, advisories and upstream exact CI:** none of the eight has a verified default-branch-pointer equivalence, stable release tag audit, dependency advisory audit or exact-head CI evidence in this pass.

## 4. Candidate register after Wave 436

- Total records: 101
- CANDIDATE: 78
- CONDITIONAL: 16
- REFERENCE_ONLY: 2
- EXCLUDED_FROM_ACTIVE_SHORTLIST: 5

Counts reconcile to 101. The screening summary now records 32 immutable commit IDs, 30 readable license files at pinned commits, 32 manifest reads, 20 lockfile blobs identified, 13 lockfile contents retrieved but not audited, 7 lockfile IDs with empty content responses, and 8 tested lockfile filenames not found. Dependency/advisory audits, stable release pins, upstream exact-CI audits and default-ref equivalence are still zero.

## 5. MediaHub governance

- Main target SHA remains `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open. Its issuer/ingress/lease/cancel/recovery, R-06 audit/privacy, accepted runner/workspace/network manifest, schema-validation and workflow-hardening gates remain prerequisites.
- PR [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585) remains open / Draft / unmerged; exact-head CI must be refreshed after Wave 436 report and checkpoint commits. Formal independent review remains NOT VERIFIED.
- PR [#583](https://github.com/VlDMlNSh/mediahub-os/pull/583) remains a separate controller test repair.
- No provider inference, agent dispatch, secret access, install, deployment, merge, inventory freeze, formal comparison, component assembly or Contour A acceptance occurred in Wave 436.

## 6. Next step

Continue candidate screening in missing areas and reconcile the Markdown and JSON registers. Pin stable release tags and audit exact lockfile/dependency data, CI/test health and security advisories for the 32 pinned source commits. Freeze the inventory only after the source, licensing, maturity and security gates are evidenced. Only then run equal-workload comparison and assemble selected components on an isolated branch.

**Disposition: 8 INFRASTRUCTURE SOURCES PINNED / VAULT & AGENT ROUTER CONDITIONAL / LICENSES AND MANIFESTS READ / DEPENDENCY AUDITS NOT RUN / INVENTORY NOT FROZEN / COMPARISON NOT STARTED / NO COMPONENT ADOPTED / CONTOUR A NOT ACCEPTED.**
