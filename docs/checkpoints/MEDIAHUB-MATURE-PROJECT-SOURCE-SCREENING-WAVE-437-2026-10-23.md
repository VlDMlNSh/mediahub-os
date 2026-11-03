# MediaHub OS — Mature Project Source Screening, Wave 437

- Date: 2026-10-23
- Status: PARTIAL SOURCE SCREEN / 7 ADDITIONAL REPOSITORIES RECORDED / INVENTORY OPEN / COMPARISON NOT STARTED
- MediaHub baseline SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Machine register: [candidate register (latest Wave 437)](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Prior screen: [Wave 436](MEDIAHUB-MATURE-PROJECT-SOURCE-SCREENING-WAVE-436-2026-10-23.md)
- Parent PR: https://github.com/VlDMlNSh/mediahub-os/pull/585
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. New candidate screen

| Project | Pinned source | Role to evaluate | License / manifest / dependency evidence | Current disposition |
|---|---|---|---|---|
| [mcp-use](https://github.com/mcp-use/mcp-use) | [`f877f789e7b4979e62e5cbe221bfb29ebb86d1bd`](https://github.com/mcp-use/mcp-use/commit/f877f789e7b4979e62e5cbe221bfb29ebb86d1bd) | MCP client and agent integration | MIT LICENSE blob `083b7c012ba392a98e59534cb51439a4b0c67874`; root `package.json` and `pnpm-lock.yaml` not found at tested paths | CANDIDATE; monorepo workspace and lockfile path unresolved |
| [Neo4j GraphRAG Python](https://github.com/neo4j/neo4j-graphrag-python) | [`123964634f213fde8e2a5fd29b45bea4d0391d5d`](https://github.com/neo4j/neo4j-graphrag-python/commit/123964634f213fde8e2a5fd29b45bea4d0391d5d) | Graph retrieval / GraphRAG | Root LICENSE not found; `pyproject.toml` blob `6efe2038e0204c879a32d195a19d7d0b9905f75f` includes Apache license header; `uv.lock` blob reported as `c545f3eda0de0048be8d3e3fb16e72a11727fb65`, but returned content was empty | CANDIDATE with license/dependency evidence gaps |
| [LanceDB](https://github.com/lancedb/lancedb) | [`a9535684cc1d9901c54c852f103dd0d492d61c3f`](https://github.com/lancedb/lancedb/commit/a9535684cc1d9901c54c852f103dd0d492d61c3f) | Vector retrieval / multimodal data | Apache-2.0 LICENSE blob `7a4a3ea2424c09fbe48d455aed1eaa94d9124835`; workspace manifest `Cargo.toml` blob `870ef5d07091d042cfa703ad2f657926fb9e1de0`; `Cargo.lock` blob `8bad6ca926c64490356804862758616773b089fd` (282,765 characters read; audit NOT RUN) | CANDIDATE |
| [ToolHive](https://github.com/stacklok/toolhive) | [`7970d588230120ee88dd20d9d7f2308a7ba12093`](https://github.com/stacklok/toolhive/commit/7970d588230120ee88dd20d9d7f2308a7ba12093) | Managed / isolated MCP server runtime | Apache-2.0 LICENSE blob `5d19730a604c467f93437238d205f8e793dddb40`; `go.mod` blob `d982221745ab54116e59bc71241a0b30b7817b1e`; `go.sum` blob `8933fb182ccecd5593cd59be7272ce1dac3ff091` (97,411 characters read; audit NOT RUN) | CANDIDATE; compare with MediaHub issuer/capability gates |
| [MCP Registry](https://github.com/modelcontextprotocol/registry) | [`f13bdd6d11e98bf63f074f289b98a8c6aef12bc9`](https://github.com/modelcontextprotocol/registry/commit/f13bdd6d11e98bf63f074f289b98a8c6aef12bc9) | MCP server discovery / registry | LICENSE blob `4a93985763241755401a10678395303de4e720ba` explicitly states a transition from MIT to Apache-2.0 is underway; `go.mod` blob `5023f23cd830449e1ab17a6ef6d26b897b87cf1a`; `go.sum` blob `c9fd26ccf9ecc6fe165da519df0ae74fab10759f` (19,098 characters read; audit NOT RUN) | CONDITIONAL pending exact license terms |
| [Kagent](https://github.com/kagent-dev/kagent) | [`6401bd1e8da1d49d9a5d8778fca77ad451a7bc5c`](https://github.com/kagent-dev/kagent/commit/6401bd1e8da1d49d9a5d8778fca77ad451a7bc5c) | Kubernetes-oriented agent orchestration | Apache-2.0 LICENSE blob `f7b5e615693b3618c2d10228851355921fc4656e`; root `go.mod`/`go.sum` not found at tested paths | CANDIDATE; module path and deployment footprint unresolved |
| [AgentOps](https://github.com/AgentOps-AI/agentops) | [`f8e907b92dabe47232978023fdcb01e2a7d4b752`](https://github.com/AgentOps-AI/agentops/commit/f8e907b92dabe47232978023fdcb01e2a7d4b752) | Agent observability | Latest commit returned by repository-scoped search was dated 2026-06-25; license, current HEAD and lockfile not verified in this pass | CONDITIONAL; refresh current source and maintenance evidence |

## 2. Findings and limitations

- ToolHive is the clearest new candidate for isolated MCP server lifecycle/security. It is not granted MediaHub product-state authority, issuer authority, or permission to bypass the approved GitHub controller.
- MCP Registry's pinned LICENSE text says the project is undergoing a license transition. Do not copy code until the effective terms for the exact files and commit are confirmed.
- Neo4j GraphRAG has an Apache license header in `pyproject.toml`, but no root LICENSE file was returned. This is partial evidence, not a complete licensing sign-off.
- mcp-use is a monorepo: tested root package/lockfile paths were not found. Locate the correct package workspace before dependency audit.
- LanceDB and ToolHive lockfile contents were retrieved; their dependency/advisory audits were not run. MCP Registry's lockfile was also retrieved but not audited.
- Kagent's tested root Go module paths were not found. Resolve the real build module before deciding whether it is a component candidate.
- The repository lookup for `meta-llama/llama-stack` resolved to `ogx-ai/ogx`, an identity mismatch. It was deliberately **not** added as Llama Stack. Confirm canonical repository transfer/name before screening that project.
- No repository was installed, no provider inference or agent dispatch was executed, no secrets were accessed, and no runtime/deployment changed.

## 3. Register totals after Wave 437

- Total records: 108
- CANDIDATE: 83
- CONDITIONAL: 18
- REFERENCE_ONLY: 2
- EXCLUDED_FROM_ACTIVE_SHORTLIST: 5

Counts reconcile to 108. The register records 39 pinned commits, 35 readable license files at pinned commits, and 36 manifest files read. Sixteen lockfile contents are recorded as retrieved but not audited. The cumulative source screen still has zero completed dependency/advisory audits, zero stable release-tag pins, zero upstream exact-CI audits, and zero verified equivalences between selected commits and default branch tips. Inventory status remains NOT_READY.

## 4. Governance and next work

- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains the controlling issue. Issuer/ingress/lease/cancel/recovery, R-06 audit/privacy, runner/workspace/network manifest, schema validation and workflow hardening remain gates.
- Parent PR [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585) is open, Draft, and unmerged. This wave's writes occurred after prior CI runs; prior success does not qualify the new exact head. Formal review is NOT VERIFIED.
- Do not begin comparative scoring or component assembly until candidate discovery is broad enough and inventory freeze gates are evidenced. Next pass should resolve source identity/path gaps, pin release tags, inspect dependency advisories, and expand the candidate landscape across serving, evaluation, policy, identity/provenance and workflow engines.

**Disposition: 7 REPOSITORIES ADDED / 2 CONDITIONAL FOR LICENSE OR FRESHNESS / DEPENDENCY AUDITS NOT RUN / INVENTORY NOT FROZEN / COMPARISON NOT STARTED / NO COMPONENT ADOPTED / CONTOUR A NOT ACCEPTED.**
