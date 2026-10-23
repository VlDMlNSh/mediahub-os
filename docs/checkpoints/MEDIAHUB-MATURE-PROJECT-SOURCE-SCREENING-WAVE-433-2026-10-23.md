# MediaHub OS — Mature Project Source Screening, Wave 433

- Date: 2026-10-23
- Status: PARTIAL SOURCE SCREEN / CANDIDATE INVENTORY OPEN / FORMAL COMPARISON NOT STARTED
- MediaHub base target SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Working branch: `research/mature-ai-project-landscape-wave431-20261023`
- Parent research PR: [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585)
- Prior discovery report: [Wave 432](MEDIAHUB-MATURE-PROJECT-DISCOVERY-WAVE-432-2026-10-23.md)
- Machine-readable candidate register: [Wave 432 register](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Canonical checkpoint: [continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Governing objective: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Scope and result

Wave 433 performs the first pinned source-screening batch for eight cross-cutting agent framework/orchestration candidates. For each one, the exact repository HEAD was retrieved through GitHub commit search, then the LICENSE and primary package manifest were fetched by that immutable commit SHA. License and manifest blob SHAs are recorded in the candidate JSON.

This is **not** a complete maturity/security qualification. No dependencies were installed. No provider inference, secret access, agent dispatch, deployment, or runtime code change occurred.

## 2. Pinned source evidence

| Candidate | Immutable upstream HEAD | License (file blob SHA) | Manifest (file blob SHA) | Version evidence |
|---|---|---|---|---|
| LangGraph | `eb066bd31a2bf01fc0cd58256df4800a3695c233` | MIT — `fc0602feecdd6748623c852ab534e1ca612673c7` | `libs/langgraph/pyproject.toml` — `6aac18d6162e9f516e3f66113ce064f5da698b9a` | 1.2.16 |
| Microsoft Agent Framework | `4982e4c61ec81cc4f9ba0cbdb5594ed530dbbcfe` | MIT — `9e841e7a26e4eb057b24511e7b92d42b257a80e5` | `python/packages/core/pyproject.toml` — `bbcdc3c84a8022c1e4d50d476f4b4ce0464b4555` | 1.23.0 |
| CrewAI | `0656245f0787347f0110c4d85dc5d5c2432aea3c` | MIT — `a6ee25527ec07201e4373fcbf89f128f304a6f2e` | `pyproject.toml` — `401cea493010475f5aaa5443267725f1d7a4099d` | Not extracted |
| Ruflo | `88349655ebc2de8f9bf702aaf31d6be768e1ea11` | MIT — `5c4718198a4156beacc780980077043a98b0dd6a` | `package.json` — `00adf9205546dd88762d96ea2a264b45a567a11c` | 3.59.17 |
| Pydantic AI | `5f7c0ccdaf6e37c993902a2ef7fe68210bf46130` | MIT — `1bf1f55e6d1736b499ded961ec6b94bfebb17aec` | `pyproject.toml` — `75a5cc1cd0c74219675bc0e3292547fd81dba9e4` | Not extracted |
| OpenAI Agents SDK | `0dc4cf152bff1f50bdc0e41f28808563406545b2` | MIT — `e5ad2c5aa30343f143a5c418004ca1a8d2cfaff4` | `pyproject.toml` — `5596912c09e314c4445cc7cf910402fea104abce` | 0.24.0 |
| Google ADK | `c31856d17ab54d82dbe89b4e511d34395ffc977b` | Apache-2.0 — `d645695673349e3947e8e5ae42332d0ac3164cd7` | `pyproject.toml` — `2acaae84a8120ed6aa3b03d6fdb986fadbaacdfa` | Not extracted |
| Agno | `6d5af04a72f7b152f433394b1bd4ab740fde8aed` | Apache-2.0 — `51032f045aafc8732c072ed31aa96f2994f29081` | `libs/agno/pyproject.toml` — `6b4f86141b09ad0ec932969fa460ef5a4af515fc` | 3.1.10 |

Direct source links are commit-pinned in the JSON register's `screening.license.url` and `screening.manifest.url` fields. These are root/component manifest checks, not a complete legal opinion or dependency audit.

## 3. Additional discovery sweep

Executed GitHub repository searches for:
- `AI agent orchestration framework stars:>1000 archived:false`
- `multi agent framework`
- `durable workflow engine`
- `LLM proxy gateway`
- `agent orchestration`
- `durable workflow orchestration open source stars:>1000 archived:false`
- `LLM gateway model routing open source stars:>500 archived:false`

The connector returned incomplete repository metadata for these broad queries (not enough to create a defensible complete query-result inventory). Therefore this sweep is recorded as **DISCOVERY ATTEMPTED / QUERY RESULT EVIDENCE INCOMPLETE**, not as a completed census of GitHub. Keep the discovery phase open and continue with focused searches that capture each returned repository, exact HEAD, archived state, license and release evidence.

## 4. What is still not audited

For all eight candidates:
- release/tag and release cadence: NOT PINNED;
- lockfiles and transitive dependency inventory: NOT AUDITED;
- vulnerability advisories / supply-chain provenance: NOT AUDITED;
- exact-head upstream CI/test status: NOT AUDITED;
- security boundaries, permission model, persistence/recovery and integration contracts: NOT AUDITED;
- MediaHub interface compatibility and subsystem qualification: NOT STARTED.

The JSON register now reports `pinned_heads=8`, `license_files_read_at_pinned_heads=8`, and `manifest_files_read_at_pinned_heads=8`; lockfile, advisory, exact-CI and release-tag audit counts remain zero.

## 5. Governance and branch status

- Main HEAD was refreshed as `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- PR #585 is open, Draft, unmerged, based on that immutable target.
- On the immediately preceding PR head `41774807278c27ae497416c4af01ce69113cbe88`, Astra Cloud Runtime Validation run `39976776998` and Astra Verify run `39976776769` completed successfully. The current documentation update requires its own exact-head checks.
- Formal independent PR review remains NOT VERIFIED (zero formal reviews observed).
- The canonical map's Contents API response was empty, but its returned blob SHA `78fa7dfa02357fe9e95645843e583f8802867d78` was successfully read using the blob endpoint (1,177,267 characters). The map is now readable; its newest top pointer is Wave 392, and the current research branch is not canonical. Do not treat this draft discovery as accepted canonical state.
- Issue #301 admission gates remain separate and open; no Gemini dispatch was attempted. SentinelX inventory still shows only `Voktors-Mini.Dlink` as connected; it is not a confirmed third server for Claude Code, so no local Claude task was launched.

## 6. Next bounded package

1. Extend pinned source screening to durable workflow engines, model gateways/routing, coding executors, observability/evaluation, guardrails, memory/RAG, sandbox/browser automation and protocols.
2. For each active candidate, pin exact HEAD, release/tag, license blob, component manifest and lockfile; check CI/tests, release cadence and security advisories.
3. Record all focused GitHub query results and explicit exclusions, then decide whether the inventory meets freeze gates.
4. Only after an evidence-backed freeze, begin formal side-by-side comparison and component selection. No adoption decisions are made in Wave 433.

**Disposition: 8 SOURCE HEADS PINNED / 8 LICENSES VERIFIED AT PINNED HEAD / 8 MANIFESTS READ / MATURITY SCREEN INCOMPLETE / INVENTORY OPEN / COMPARISON NOT STARTED / CONTOUR A NOT ACCEPTED.**
