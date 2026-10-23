# MediaHub OS — Mature Project Source Screening, Wave 439

- Date: 2026-10-23
- Status: SOURCE SCREEN RECORDED / 10 EXISTING RECORDS ENRICHED / INVENTORY OPEN
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- MediaHub baseline SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Machine register: [candidate register](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Previous source screen: [Wave 438](MEDIAHUB-MATURE-PROJECT-SOURCE-SCREENING-WAVE-438-2026-10-23.md)
- Parent research PR: https://github.com/VlDMlNSh/mediahub-os/pull/585
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Scope and disposition

Wave 439 covers durable workflows, Kubernetes workflows, telemetry, LLM observability/evaluation, model gateway, typed agent framework, RAG pipelines, policy-as-code and programmable builds. The machine register already contained all ten repositories, so this pass enriched their existing records rather than creating duplicate rows. Counts remain 118 records: 91 CANDIDATE, 20 CONDITIONAL, 2 REFERENCE_ONLY, 5 EXCLUDED_FROM_ACTIVE_SHORTLIST.

## 2. Pinned source evidence

All source SHAs below were the latest repository-scoped commit-search results observed in this pass. They are immutable commit references, but equivalence to default branch HEAD or a supported release tag remains NOT VERIFIED.

| Project | Source commit | License file blob | Manifest and blob | Screening disposition |
|---|---|---|---|---|
| [Temporal](https://github.com/temporalio/temporal) | [8a40a2663e304a79b07779ae08108648ccbc797d](https://github.com/temporalio/temporal/commit/8a40a2663e304a79b07779ae08108648ccbc797d) | MIT; `3349f76795f4409cba6ae18ea56adf9fbd8346f3` | `go.mod` `b58f656dc5fb62f7e1c9fc6d9d8aa2b871af4a23`; `go.temporal.io/server` | Durable retries/workflows reference; operational footprint needs comparison against GitHub-native design |
| [Argo Workflows](https://github.com/argoproj/argo-workflows) | [82ad6f109df41c5a0fc25cc1cefba69adc67bb5a](https://github.com/argoproj/argo-workflows/commit/82ad6f109df41c5a0fc25cc1cefba69adc67bb5a) | Apache-2.0; `67e99b065bcd6ac93d93c8fe8e0a72c6296a5614` | `go.mod` `c261bdfa09a096413a00ee6f7d87cdf304a59923`; `github.com/argoproj/argo-workflows/v4` | Kubernetes-native workflow engine; fit is conditional on actual Kubernetes scope |
| [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | [42ee5d39b18f24c206cca3f91f8b0877424bdfee](https://github.com/open-telemetry/opentelemetry-collector/commit/42ee5d39b18f24c206cca3f91f8b0877424bdfee) | Apache-2.0; `d645695673349e3947e8e5ae42332d0ac3164cd7` | `go.mod` `1790f8ef4d615afc21d071486972823ad2201536`; `go.opentelemetry.io/collector` | Standard telemetry pipeline candidate |
| [Langfuse](https://github.com/langfuse/langfuse) | [8aedbccf805d7c7baf7aeaadd8fc4907fe0e312d](https://github.com/langfuse/langfuse/commit/8aedbccf805d7c7baf7aeaadd8fc4907fe0e312d) | `eaa2e5e444c8634f35b2a1137f7ea06e8353f475`; mixed/path-specific terms | `package.json` `9899d13e4a45711cfcc47e7a37ec22f67d9ba082`; v4.69.0 | CONDITIONAL: audit exact proposed paths and terms before reuse |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | [c0b88a324175c60019cc80de1b2e32b4c849d4c3](https://github.com/promptfoo/promptfoo/commit/c0b88a324175c60019cc80de1b2e32b4c849d4c3) | `af3fa111d9303b3041d225fb851534e50a4bbec2`; custom terms require legal review | `package.json` `6593940624d1a5a7acb245a21d90e141a5f1c7c4`; v0.125.0 | Candidate for evaluation/red-team test patterns; no code reuse until license review |
| [LiteLLM](https://github.com/BerriAI/litellm) | [f2118fc7670ba3fa736d9b8f4deef9077a45a720](https://github.com/BerriAI/litellm/commit/f2118fc7670ba3fa736d9b8f4deef9077a45a720) | `3bfef5bae9b48c334acf426d5b7f21bc1913aab9`; mixed/path-specific terms | `pyproject.toml` `3aefd9119375172be6f7d312952d8153b442b77d`; v1.108.0 | CONDITIONAL model gateway candidate; audit provider allowlists, secret handling and paid-fallback prevention |
| [PydanticAI](https://github.com/pydantic/pydantic-ai) | [332d3011d1a1bada4ae7210d5416ed5b31be3346](https://github.com/pydantic/pydantic-ai/commit/332d3011d1a1bada4ae7210d5416ed5b31be3346) | MIT; `1bf1f55e6d1736b499ded961ec6b94bfebb17aec` | `pyproject.toml` `75a5cc1cd0c74219675bc0e3292547fd81dba9e4`; dynamic version | Typed schemas/tool contract patterns candidate |
| [Haystack](https://github.com/deepset-ai/haystack) | [76fc2d3d7492ec243eed40eb939a836f2a8b29da](https://github.com/deepset-ai/haystack/commit/76fc2d3d7492ec243eed40eb939a836f2a8b29da) | Apache-2.0; `6fb66d8d5fa55912ee80f4fdab94cab99140c448` | `pyproject.toml` `2a61e110757e7dc31a18f95f0c53e7cf7f0ca804`; version not extracted | RAG/pipeline candidate only if retrieval is in scope |
| [Open Policy Agent](https://github.com/open-policy-agent/opa) | [83a65784cbc60c8bbf73d46fd4b4489c5b0e2d76](https://github.com/open-policy-agent/opa/commit/83a65784cbc60c8bbf73d46fd4b4489c5b0e2d76) | Apache-2.0; `8f71f43fee3f78649d238238cbde51e6d7055c82` | `go.mod` `bb894fcce89f7f52f72d2a174711172a660451e0`; `github.com/open-policy-agent/opa` | Policy-as-code candidate; must preserve current issuer/capability authority |
| [Dagger](https://github.com/dagger/dagger) | [930485687df5c9a7ed521f5585a17b2a36936b17](https://github.com/dagger/dagger/commit/930485687df5c9a7ed521f5585a17b2a36936b17) | Apache-2.0; `17b2ba29b525453b46b0311d202b63044d3aa5cb` | `go.mod` `44cb897774abde54c5a6fef33c4a6b84a3ede71d`; `github.com/dagger/dagger` | Reproducible build/test candidate; compare with GitHub Actions and workspace constraints |

## 3. Research controls and unresolved gates

- License and root manifest files were read for all ten projects at the pinned commits.
- Root license presence is not enough to clear mixed/path-specific licensing. Promptfoo, Langfuse and LiteLLM remain gated for legal review before any component reuse.
- No lockfile or transitive dependency audit, security advisory review, exact upstream CI audit, release-tag pin, default-branch equivalence check, or threat-model review was performed in this pass.
- No repository code was installed, vendored or executed. No secrets read; no model/provider calls; no agent dispatch.
- No formal score or component selection is authorized. The candidate inventory remains NOT READY TO FREEZE.

## 4. MediaHub status snapshot

- Research PR #585 was OPEN, DRAFT and NOT MERGED at review. Its head at that check was `de185f0e1f0ef4065bc051d8fca97b005a2765bc`; the Wave 439 register update creates a new head and requires fresh exact-head CI.
- PR #585 formal reviews were empty in the previous check; empty review/status results are NOT VERIFIED, not PASS.
- PR #583 remains a separate open draft; do not conflate its controller patch or CI with this research register.
- Canonical map remains on `docs/mediahub-chat-tree-map-20261012`; its Contents API body was empty and prior recovery used blob SHA `78fa7dfa02357fe9e95645843e583f8802867d78`. The research branch is not canonical.
- Issue #301 remains the governing Contour A qualification contract. This source screen does not pass its gates or authorize controller dispatch.

## 5. Next bounded pass

Continue source discovery and deduplication only while new mature categories or materially different implementations remain uncovered. In parallel, begin evidence closure for existing records: supported release tags, upstream default-ref equivalence, lockfiles and advisory results, exact upstream CI, ownership/maintenance, path-level licensing and documented security boundaries. Keep comparison and component assembly blocked until inventory-freeze criteria are met.

**Disposition: 10 EXISTING RECORDS ENRICHED / 118 RECORDS RECONCILED / INVENTORY NOT FROZEN / FORMAL COMPARISON NOT STARTED / NO COMPONENT ADOPTED / CONTOUR A NOT ACCEPTED.**
