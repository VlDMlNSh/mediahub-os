# MediaHub OS — Mature Project Source Screening, Wave 438

- Date: 2026-10-23
- Status: SOURCE SCREEN PARTIAL / 10 IDENTITY-PROVENANCE-POLICY CANDIDATES ADDED / INVENTORY OPEN
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- MediaHub baseline SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Machine register: [candidate register (Wave 438)](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Prior infrastructure screen: [Wave 436](MEDIAHUB-MATURE-PROJECT-SOURCE-SCREENING-WAVE-436-2026-10-23.md)
- Parent PR: https://github.com/VlDMlNSh/mediahub-os/pull/585
- Governance: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Scope

Wave 438 expands the source corpus across secrets, artifact signing/provenance, workload identity, authorization policy, Kubernetes policy, certificates and developer portals. Each source was pinned to an immutable commit selected by repository-scoped GitHub commit search. This is not proof that the selected commit equals the default branch tip or a supported release tag.

## 2. Source evidence

| Project | Immutable source | License evidence | Manifest evidence | Initial fit |
|---|---|---|---|---|
| [OpenBao](https://github.com/openbao/openbao) | [1d58653b0c00e53484de5af18f20679d78b9fb28](https://github.com/openbao/openbao/commit/1d58653b0c00e53484de5af18f20679d78b9fb28) | MPL-2.0; LICENSE blob `f4f97ee5853a2b2ba9121ea21589c706edf7a1cc` | `go.mod` blob `c4690026d2353d3163db8d1173290c4bd60950ae`; module `github.com/openbao/openbao/v2` | CONDITIONAL alternative for secret-management research; not a drop-in replacement for Vault |
| [Sigstore Cosign](https://github.com/sigstore/cosign) | [a1a30f35757c5f9a484f5be8150c9c8a18bc5db3](https://github.com/sigstore/cosign/commit/a1a30f35757c5f9a484f5be8150c9c8a18bc5db3) | Apache-2.0; LICENSE blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `7873ab4b8da8143fda5129bbe0085c486e39bdb0`; module `github.com/sigstore/cosign/v3` | Candidate for signing/verifying build outputs; signature alone is not full provenance |
| [in-toto](https://github.com/in-toto/in-toto) | [e352b43ad7cb8915d84c36d791aa61346152a0a3](https://github.com/in-toto/in-toto/commit/e352b43ad7cb8915d84c36d791aa61346152a0a3) | Apache-2.0; LICENSE blob `963ee949e8e1083f7f12e685160267cae23a5ffa` | `pyproject.toml` blob `ed5939c32538e3cd155058cdc74f10e1d00b4a5c`; package metadata not extracted | Candidate for signed step/attestation provenance |
| [SPIRE](https://github.com/spiffe/spire) | [0d589ad07d7b7e7a244f5b5548bf9d2d21e9fbba](https://github.com/spiffe/spire/commit/0d589ad07d7b7e7a244f5b5548bf9d2d21e9fbba) | Apache-2.0; LICENSE blob `ce7ede043c57e70ba4930782fedf11b07615b41a` | `go.mod` blob `6ca214eaf056f1b7e957c574d8823c295ea9afb8`; module `github.com/spiffe/spire` | Candidate for workload identity; operationally heavy versus GitHub OIDC |
| [OpenFGA](https://github.com/openfga/openfga) | [22c4d5ddf4d5969bee10c24e468a5acfbcf26837](https://github.com/openfga/openfga/commit/22c4d5ddf4d5969bee10c24e468a5acfbcf26837) | Apache-2.0; LICENSE blob `4959a5e50d66e62e675d8d033d66cca0f390458d` | `go.mod` blob `d01586d0b64cd38eb66eca7ae983d4a5f249e040`; module `github.com/openfga/openfga` | Candidate for relationship-based authorization; must not create a parallel authority without a proven gap |
| [Keycloak](https://github.com/keycloak/keycloak) | [e7689b41c7a63f4dcbfc74d7eab057c3bb944911](https://github.com/keycloak/keycloak/commit/e7689b41c7a63f4dcbfc74d7eab057c3bb944911) | Root `LICENSE` path returned 404; license UNVERIFIED | `pom.xml` blob `aa47a6a6a294ed17bee9e56a361dd33fcbb2553b` read | CONDITIONAL; no license assumption until legal file is located and read |
| [Kyverno](https://github.com/kyverno/kyverno) | [e19a19643d6dcd7a1d609df42a2a05d29c4e14f7](https://github.com/kyverno/kyverno/commit/e19a19643d6dcd7a1d609df42a2a05d29c4e14f7) | Apache-2.0; LICENSE blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `490f97ebb99de034ff0060d1644ec6bf40223222`; module `github.com/kyverno/kyverno` | Candidate only if Kubernetes policy enforcement is actually in scope |
| [cert-manager](https://github.com/cert-manager/cert-manager) | [b4e42b76e09ffd8570d091d2eb23735ae7572603](https://github.com/cert-manager/cert-manager/commit/b4e42b76e09ffd8570d091d2eb23735ae7572603) | Apache-2.0; LICENSE blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `eb6b1f1335a110f064bd4232e90e32b49dbd3123`; module `github.com/cert-manager/cert-manager` | Candidate for certificate lifecycle only in Kubernetes deployments |
| [KubeVela](https://github.com/kubevela/kubevela) | [a6f4ce11663ffc32ae090efdbc030f1b3e0e2179](https://github.com/kubevela/kubevela/commit/a6f4ce11663ffc32ae090efdbc030f1b3e0e2179) | Apache-2.0; LICENSE blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `go.mod` blob `42a642e1b79d881afe4f5828ede16e369b9a1be3`; module `github.com/oam-dev/kubevela` | Broad app platform; likely excessive for GitHub-hosted Contour A |
| [Backstage](https://github.com/backstage/backstage) | [36255ddae2aa04d235dc519e937d0e93fb01e2a5](https://github.com/backstage/backstage/commit/36255ddae2aa04d235dc519e937d0e93fb01e2a5) | Apache-2.0; LICENSE blob `72ea3a85b0ee807370d34ff9bef32e0f2c7e0c92` | `package.json` blob `dbd29c05d1497f55d98b116508a606e7baeb6b13`; root package version `1.56.0` | Candidate for a future human-facing developer portal, not an orchestration engine |

## 3. Evidence limits

- Immutable commit IDs were identified, but default-ref equivalence and release tags are NOT VERIFIED.
- License text and root manifests were read for 9 of 10 candidates. Keycloak's root LICENSE path returned 404; its license remains UNVERIFIED, not implicitly accepted.
- Lockfiles, dependency advisories, exact-head CI, maintenance/release support, transitive license inventory, and threat-model reviews were not audited in this pass.
- No project was installed or executed; no secrets were read; no model/provider calls or agent dispatches occurred.
- No component is selected for production, and no architecture replacement decision is made.

## 4. Register state

After Wave 438: 118 records total — 91 CANDIDATE, 20 CONDITIONAL, 2 REFERENCE_ONLY, 5 EXCLUDED_FROM_ACTIVE_SHORTLIST. Counts reconcile. The register reports 49 pinned source commits, 44 license files read, and 46 manifests read. Formal comparison remains NOT STARTED; inventory freeze remains NOT READY.

## 5. Current MediaHub integration status

- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Canonical map contents were retrieved via blob SHA `78fa7dfa02357fe9e95645843e583f8802867d78` after Contents API returned an empty body. Bootstrap blob SHA `75f30750183efe8c6877368e9f0ada48f8e81ea7`; Master Roadmap blob SHA `21c4bf2702dbf636fa902f4f5716c6f39bb5dd1c`.
- The research branch is not the canonical documentation branch. The new register/report/checkpoint remain proposed research changes until PR acceptance.
- PR #585 was open, Draft and unmerged when checked. At the prior head `843a3370fb2c8b6cdc9679f15cb748cb75e6f2c7`, Astra Cloud Runtime Validation run `39981388995` and Astra Verify run `39981388866` completed SUCCESS. These checks precede Wave 438 writes and do not verify the new head. Formal reviews: none. Combined status API returned an empty status list, which is NOT VERIFIED.
- Issue #301 remains the governing Contour A qualification work. This source screen does not satisfy or bypass its issuer/capability, audit/privacy, runner/workspace/network manifest, schema-validation, cancellation/recovery, or workflow-hardening gates.

## 6. Next step

Continue screening the remaining mature ecosystem categories and deduplicate by upstream identity. Before inventory freeze, resolve license exceptions and repository renames, pin supported release tags, audit dependency/lockfile contents and advisories, verify upstream CI/security/maintenance signals, and reconcile the human-readable inventory against the machine register. Only after explicit freeze gates pass should equal-workload comparative evaluation begin; only after that should component adapters/prototypes be assembled on an isolated branch.

**Disposition: 10 SOURCES ADDED / 118 RECORDS / KEYCLOAK LICENSE UNVERIFIED / DEPENDENCY AND CI AUDITS NOT RUN / INVENTORY NOT FROZEN / COMPARISON NOT STARTED / NO COMPONENT ADOPTED / CONTOUR A NOT ACCEPTED.**
