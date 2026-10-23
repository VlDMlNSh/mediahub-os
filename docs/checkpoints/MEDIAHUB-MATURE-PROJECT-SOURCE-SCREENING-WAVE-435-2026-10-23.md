# MediaHub OS — Mature Project Source Screening, Wave 435

- Date: 2026-10-23
- Status: PARTIAL SOURCE SCREEN / REGISTER EXPANDED / INVENTORY OPEN / COMPARISON NOT STARTED
- MediaHub baseline target: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Machine register: [MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Prior screen: [Wave 434](MEDIAHUB-MATURE-PROJECT-SOURCE-SCREENING-WAVE-434-2026-10-23.md)
- Consolidated overview: [candidate register](MEDIAHUB-MATURE-OPEN-SOURCE-AI-CANDIDATE-REGISTER-2026-10-23.md)
- Parent research PR: https://github.com/VlDMlNSh/mediahub-os/pull/585
- Governance: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Scope

Wave 435 adds source pins from agent orchestration, agent runtime, observability, browser automation, MCP protocol, vector database and guardrails. Eight immutable repository commit IDs were selected through repository-scoped GitHub commit search. For seven repositories, an exact LICENSE file was returned at the selected commit; NVIDIA NeMo Guardrails root LICENSE lookup did not resolve at the tested path, so its README's Apache claim is not treated as verified license text.

The commit identifiers are immutable, but exact equivalence to the current default-branch ref was not independently confirmed with the available branch API. State is therefore **COMMIT PINNED / DEFAULT-REF EQUIVALENCE NOT VERIFIED**.

No installation, runtime use, inference, provider invocation, dispatch, secret access, deployment or code adoption took place.

## 2. Pinned source evidence

| Candidate | Immutable upstream commit | License evidence | Manifest evidence | Lockfile evidence |
|---|---|---|---|---|
| [AG2](https://github.com/ag2ai/ag2) | [cc645f2b19f1df47629a4bb47b6522f0ddf2a13d](https://github.com/ag2ai/ag2/commit/cc645f2b19f1df47629a4bb47b6522f0ddf2a13d) | Apache-2.0; `LICENSE` blob `a40e7d03d70e094a54bcc34f67f4243b0c8a382d` | `pyproject.toml` blob `67b6748280616f5c522763a5da44b1bc9d9a580e`, version 1.2.1 | `uv.lock` blob SHA `b8dec50e6db175bcc70b5f163118543dfada7987`, content returned empty; NOT AUDITED |
| [AgentScope](https://github.com/agentscope-ai/agentscope) | [bdad647d2fee7d66597681ecd89e086b7800dd2a](https://github.com/agentscope-ai/agentscope/commit/bdad647d2fee7d66597681ecd89e086b7800dd2a) | Apache-2.0; `LICENSE` blob `2f2f2f25ea6019e5a51213c4e8a4df0c67a6ea2a` | `pyproject.toml` blob `791822f59acaefd45e33721e2d8998dfb028dc8a`, dynamic version | `uv.lock` NOT FOUND at tested path; alternative lock file search required |
| [Dapr Agents](https://github.com/dapr/dapr-agents) | [8b4cc8ddbe2845248df5892fc532dd1097298be8](https://github.com/dapr/dapr-agents/commit/8b4cc8ddbe2845248df5892fc532dd1097298be8) | Apache-2.0; `LICENSE` blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | `pyproject.toml` blob `7663826091bc04ddc104975bdbe2d225810525f0`, version not extracted | `uv.lock` blob SHA `3d10a9494d1031dcb311fadfbfd730f5480c0aca`, content returned empty; NOT AUDITED |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | [1c1eb72c60e42312289550efc2395cadba1c6685](https://github.com/Arize-ai/phoenix/commit/1c1eb72c60e42312289550efc2395cadba1c6685) | **Elastic License 2.0**; `LICENSE` blob `23d3aa7c871a4eb153186073e3d2b72d586f64be` | `pyproject.toml` blob `397ea8067cce527eb15ad748c80477890313568c`, version not extracted | `uv.lock` blob SHA `1676c9f197517d2ec6d5e814d56c90634761cbbe`, content returned empty; NOT AUDITED |
| [Browser Use](https://github.com/browser-use/browser-use) | [3df5806a0d097a1546d92c49bcf1b28c9972c3bd](https://github.com/browser-use/browser-use/commit/3df5806a0d097a1546d92c49bcf1b28c9972c3bd) | MIT; `LICENSE` blob `1ea3836ce58a4cd32c90c0b4f4e736d840d23780` | `pyproject.toml` blob `ff6f1538abb84fd8f7ceaa532d7cc1cb4a8d58db`, version 0.13.13 | `uv.lock` NOT FOUND at tested path; alternative lock file search required |
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | [2af9e3089ac66b35c1550c500aae86a82efb1e17](https://github.com/modelcontextprotocol/python-sdk/commit/2af9e3089ac66b35c1550c500aae86a82efb1e17) | MIT; `LICENSE` blob `3d48435454b105021b4f777c11b6b07d8d2ffea3` | `pyproject.toml` blob `6d7626d79b4a78c66e5dd1837b28530e677a0d34`, dynamic version/dependencies | `uv.lock` blob `fd2dcb85f9923798334ea6259522ae4ae84185f8`, 435,420 chars retrieved; dependency analysis NOT RUN |
| [Qdrant](https://github.com/qdrant/qdrant) | [222b2e44ab1c3f17e8246396ead6558e45041df7](https://github.com/qdrant/qdrant/commit/222b2e44ab1c3f17e8246396ead6558e45041df7) | Apache-2.0; `LICENSE` blob `456fb05e0e936f439cf42c517b19797dafd53ff9` | `Cargo.toml` blob `27378cb2f286f54154290873b12bd1e902c158ed`, version 1.20.0 | `Cargo.lock` blob `253aea05aaf8dea2068b2eb744f96afc7f8cc3fe`, 233,630 chars retrieved; dependency analysis NOT RUN |
| [NVIDIA NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | [a3d70b9c8e6a6ef770943ce7019f8dc59350b6a6](https://github.com/NVIDIA-NeMo/Guardrails/commit/a3d70b9c8e6a6ef770943ce7019f8dc59350b6a6) | README states Apache-2.0, but root `LICENSE` NOT FOUND at tested path; license file NOT VERIFIED | `pyproject.toml` blob `507fbccfa2939e8ea0360ea670591d0e0654b43d`, version 0.25.0.dev0 | `uv.lock` blob SHA `4668aedd6d26d59148740cde2f6f67392a9a5d78`, content returned empty; NOT AUDITED |

File/blob SHAs identify exact files at the pinned source commits, not artifact signatures or dependency integrity attestations.

## 3. Explicit screening outcomes

1. **Phoenix moved to CONDITIONAL**: the pinned root LICENSE is Elastic License 2.0. Do not treat Phoenix as OSI-approved open-source or vendor its code until legal review confirms that the intended usage is permitted. It remains a research reference for telemetry/evaluation capability only.
2. **NeMo Guardrails moved to CONDITIONAL**: the queried manifest is a development version `0.25.0.dev0` and the root license file was not found at the tested path. Find the real license path and a stable release before treating it as a mature implementation candidate.
3. **AG2, AgentScope and Dapr Agents** widen alternatives to Microsoft Agent Framework/Ruflo/LangGraph. They are candidate sources, not ranked winners.
4. **MCP Python SDK** is a protocol implementation candidate; protocol adoption itself cannot convey execution permission.
5. **Qdrant** is a data-layer candidate. It must not become a new state authority for MediaHub product state; any future selection is limited to an explicitly authorized retrieval/storage domain.
6. **Browser Use** is a browser-agent candidate only. Its cloud/hosted features, browser profile storage, and local browser sandboxing need separate data/security analysis.
7. **Lockfile and advisories** remain incomplete. Two lockfiles had retrievable content; four lockfile SHAs were returned with empty content; two tested lockfile paths were not found. There has been no dependency audit.
8. **Release/tag, security advisory and upstream exact-CI evidence** remain unaudited for all eight.

## 4. Machine register count reconciliation

The source register is now internally consistent:
- Total records: 93
- CANDIDATE: 72
- CONDITIONAL: 14
- REFERENCE_ONLY: 2
- EXCLUDED_FROM_ACTIVE_SHORTLIST: 5

The counts sum to 93. The register screening summary records:
- 24 immutable source commit IDs;
- 23 license files read at pinned commits (NeMo Guardrails license file remains unverified);
- 24 package/component manifests read;
- 14 lockfile blob SHAs identified;
- 7 lockfile contents retrieved but not audited;
- 7 lockfile SHA values returned with empty content;
- 4 lockfile paths not found by the chosen filename;
- 0 dependency advisory reviews, 0 stable release-tag pins, 0 upstream exact-CI audits, and 0 verified default-branch pointer equivalences.

## 5. MediaHub state and gates

- Main target remains `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open. Its issuer/ingress/lease/cancel/recovery, R-06 audit/privacy, accepted runner/workspace/network manifest, JSON Schema Draft 2020-12 and workflow-hardening gates take precedence over framework experimentation.
- PR #585 remains open / Draft / unmerged; exact-head CI must be checked after this report and register changes. Formal independent review has not been recorded.
- PR #583 is a separate open Draft; its controller test failure is not addressed in this research change.
- No provider inference, Gemini dispatch, secret access, install, runtime mutation, deployment, merge, formal comparison, component assembly or Contour A acceptance.

## 6. Next pass

1. Continue exact source screening for additional categories and retrieve the unavailable lockfile contents.
2. Record stable release tags, exact CI/test results and security/advisory evidence for all 24 pinned candidates.
3. Reconcile the human-readable Markdown list with all 93 machine records, including duplicates/renames and newly conditional projects.
4. Keep the inventory open until complete coverage and license/maturity/security gates are evidenced. Only then freeze it and begin equal-workload comparative tests and component assembly.

**Disposition: 8 MORE SOURCE COMMITS PINNED / PHOENIX LICENSE RISK RECORDED / NEMO VERSION+LICENSE BLOCKER RECORDED / INVENTORY NOT FROZEN / COMPARISON NOT STARTED / NO COMPONENT ADOPTED / CONTOUR A NOT ACCEPTED.**
