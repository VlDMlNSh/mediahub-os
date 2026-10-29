# MediaHub OS — Mature Project Source Screening, Wave 434

- Date: 2026-10-23
- Status: PARTIAL SOURCE SCREEN / CANDIDATE INVENTORY OPEN / COMPARISON NOT STARTED
- MediaHub baseline target: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Research branch: `research/mature-ai-project-landscape-wave431-20261023`
- Candidate register: [machine-readable register](MEDIAHUB-MATURE-PROJECT-CANDIDATE-REGISTER-WAVE-432-2026-10-23.json)
- Human-readable overview: [candidate register](MEDIAHUB-MATURE-OPEN-SOURCE-AI-CANDIDATE-REGISTER-2026-10-23.md)
- Prior source screen: [Wave 433](MEDIAHUB-MATURE-PROJECT-SOURCE-SCREENING-WAVE-433-2026-10-23.md)
- Parent research PR: https://github.com/VlDMlNSh/mediahub-os/pull/585
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Scope

Wave 433 pinned eight agent framework/orchestration sources. Wave 434 adds eight sources across durable workflow execution, model routing/gateway, coding-agent runtime, model evaluation, observability, sandboxing, memory and authorization policy.

Commit SHA selection comes from repository-scoped GitHub commit search. The chosen SHAs are immutable code identifiers, but the connected tools in this pass did not provide an authoritative current refs/heads/default-branch pointer read for each repo. Therefore the record status is **COMMIT PINNED / DEFAULT-REF EQUIVALENCE NOT VERIFIED**, not “latest default branch verified”.

No dependencies were installed, no local environment modified, no provider inference run, no Gemini or other agent dispatch started, no secrets read, and no production changes made.

## 2. Wave 434 pinned source evidence

| Component candidate | Immutable upstream commit | License file blob / observed text | Primary manifest blob | Lockfile evidence |
|---|---|---|---|---|
| Temporal | [8a40a2663e304a79b07779ae08108648ccbc797d](https://github.com/temporalio/temporal/commit/8a40a2663e304a79b07779ae08108648ccbc797d) | MIT; `LICENSE` blob `3349f76795f4409cba6ae18ea56adf9fbd8346f3` | `go.mod` blob `b58f656dc5fb62f7e1c9fc6d9d8aa2b871af4a23` | `go.sum` blob `7bb84062f0806238f63f3a71ccc70375a98f8968`, 67,329 chars retrieved; dependency analysis NOT RUN |
| LiteLLM | [f2118fc7670ba3fa736d9b8f4deef9077a45a720](https://github.com/BerriAI/litellm/commit/f2118fc7670ba3fa736d9b8f4deef9077a45a720) | Mixed/subtree review required; `LICENSE` blob `3bfef5bae9b48c334acf426d5b7f21bc1913aab9` indicates enterprise-directory exceptions | `pyproject.toml` blob `3aefd9119375172be6f7d312952d8153b442b77d`, version 1.108.0 | `uv.lock` blob SHA `8d2a38c180661f7298dbf4b87721452013ad55b0` found, but file API returned empty content; NOT AUDITED |
| OpenHands Software Agent SDK | [dd0892c80fffb1e59bac77242adafbd8b1168649](https://github.com/OpenHands/software-agent-sdk/commit/dd0892c80fffb1e59bac77242adafbd8b1168649) | MIT; `LICENSE` blob `b0bd86a6335a564bd3766666bebbf014fd6a8013` | `openhands-sdk/pyproject.toml` blob `9de3ff9a3f657e417779f9a969f6b5f3dcd350cd`, version 1.58.1 | workspace `uv.lock` blob SHA `488396553564ddcf27790a7c89b41ef2c7ab5063` found, but file API returned empty content; NOT AUDITED |
| Promptfoo | [c2f6a848aca5f7e01491d2533f3fb1122bc63c50](https://github.com/promptfoo/promptfoo/commit/c2f6a848aca5f7e01491d2533f3fb1122bc63c50) | MIT; `LICENSE` blob `af3fa111d9303b3041d225fb851534e50a4bbec2` | `package.json` blob `973377dfd97e01d2a9890bcd38fdedad3f69ce11`, version 0.124.1 | `package-lock.json` blob SHA `0df53ae4741246203b20850aea29f68b53ebe096` found, but file API returned empty content; NOT AUDITED |
| Langfuse | [bb85692102a005470c3a02ccb9ebc1609ae25461](https://github.com/langfuse/langfuse/commit/bb85692102a005470c3a02ccb9ebc1609ae25461) | Mixed/subtree review required; `LICENSE` blob `eaa2e5e444c8634f35b2a1137f7ea06e8353f475` contains path exceptions including enterprise-related folders | `package.json` blob `9899d13e4a45711cfcc47e7a37ec22f67d9ba082`, version 4.69.0 | `pnpm-lock.yaml` blob `07f2c3a17dd5f08783102c71816d98aeeac60089`, 901,824 chars retrieved; dependency analysis NOT RUN |
| OpenSandbox | [f3f4a7f419e526de4c3deb250d72fc034986fc28](https://github.com/opensandbox-group/OpenSandbox/commit/f3f4a7f419e526de4c3deb250d72fc034986fc28) | Apache-2.0; `LICENSE` blob `b09cd7856d58590578ee1a4f3ad45d1310a97f87` | Python SDK `sdks/sandbox/python/pyproject.toml` blob `ef4e53e88faa0497e2500e177d1c23b90e1f85a2`, version dynamic via hatch-vcs | SDK `uv.lock` blob `9e15c612151e927edd344554501242730352be12`, 161,381 chars retrieved; dependency analysis NOT RUN |
| Mem0 | [2c81af3bbe27d9bccb09c772d583df9e9be72ee5](https://github.com/mem0ai/mem0/commit/2c81af3bbe27d9bccb09c772d583df9e9be72ee5) | Apache-2.0; `LICENSE` blob `d20d5102c3cf97ecbee54afd65893de4a11d26fe` | `pyproject.toml` blob `c6c1f38d39598cc0c40afbff6ce07c276a44ef92`, version 2.2.1 | `poetry.lock` blob `ee07e1dbe3af7521ddf1fa77a84eac26a18f5821`, 914,250 chars retrieved; dependency analysis NOT RUN |
| Open Policy Agent (OPA) | [83a65784cbc60c8bbf73d46fd4b4489c5b0e2d76](https://github.com/open-policy-agent/opa/commit/83a65784cbc60c8bbf73d46fd4b4489c5b0e2d76) | Apache-2.0; `LICENSE` blob `8f71f43fee3f78649d238238cbde51e6d7055c82` | `go.mod` blob `bb894fcce89f7f52f72d2a174711172a660451e0` | `go.sum` blob `75cd170afff5bff8e63c3b113d95ae17cf9acd2c`, 29,407 chars retrieved; dependency analysis NOT RUN |

All file SHAs above are file/blob IDs at the pinned commit, not release signatures or supply-chain attestations.

## 3. Screening implications

- **Conditional licensing:** LiteLLM and Langfuse remain CONDITIONAL until the exact proposed source subtree is checked against applicable license exceptions. Do not infer that the entire repo is covered by the root SPDX badge or first section.
- **Strong potential subsystems to retain for further screening:** Temporal for durable execution; OpenHands SDK for sandboxed coding-agent execution; Promptfoo for eval/red-team test harness; OpenSandbox for isolation; OPA for policy-as-code; Langfuse for telemetry; Mem0 for memory. This is a research relevance judgement, not a ranking, qualification or choice of implementation.
- **Provider gateway comparison:** LiteLLM remains useful for analysis, but its mixed licensing boundary and the security fix subject of the pinned commit require careful review. No gateway is qualified for MediaHub and no paid fallback may be enabled by default.
- **Lockfiles:** Eight lockfile paths/blobs were identified. Five lockfile contents were retrieved (Temporal, Langfuse, OpenSandbox SDK, Mem0, OPA); three file endpoints produced a blob SHA but empty content (LiteLLM, OpenHands SDK, Promptfoo). None have been dependency-audited.
- **Release and security status:** zero pinned stable release tags, zero advisory reviews and zero upstream exact-head CI checks for these eight candidates.
- **Default ref:** current default-branch pointer equivalence is not verified. The selected SHAs are pinned immutable commits only.

## 4. Candidate register consistency

The Wave 434 update corrected the machine-readable register status counts to match 89 entries:
- CANDIDATE: 70
- CONDITIONAL: 12
- REFERENCE_ONLY: 2
- EXCLUDED_FROM_ACTIVE_SHORTLIST: 5
- Total: 89

The same register now records 16 immutable source commit IDs and 16 license/manifest readbacks. Lockfile audit, advisories, release/tag pins, default-branch-pointer checks and exact upstream CI audits remain incomplete. Inventory stays OPEN_NOT_FROZEN; comparative evaluation and adoption remain NOT STARTED.

## 5. MediaHub governance and current PR

- Main target: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open with issuer/ingress/lease/cancel/recovery, audit/privacy, accepted runner/workspace/network manifest, standards-compliant schema validation and workflow hardening gates.
- Research PR [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585) remains open/Draft/unmerged. The Wave 434 machine-register and documentation commits require exact-head CI refresh; formal independent review has not been recorded.
- Controller hardening PR [#583](https://github.com/VlDMlNSh/mediahub-os/pull/583) remains independently blocked by the known brittle concurrency-group assertion failure. Do not mix a controller fix into the research PR.
- The canonical map body was recoverable in Wave 433 through a blob fallback, but the current branch remains noncanonical. Do not edit the canonical map from the research branch without verified read/edit/write/read-back on its proper documentation branch.
- No Gemini or Claude dispatch, provider inference, secret access, local installation, deployment, merge, qualification or acceptance occurred in Wave 434.

## 6. Next bounded work

1. Extend exact source/license/manifest/lockfile screening to the remainder of the 89-entry register, prioritizing durable workflow, gateway, coding-agent, eval/observability, guardrail, memory, sandbox and protocol subsystems.
2. Retrieve lockfile content where connectors only returned blob IDs; run or document a versioned dependency/advisory scan only after reproducible access is available.
3. Pin stable tags/releases and verify upstream default-ref pointers where a reliable API result is available.
4. Complete the category-level query evidence and reconcile Markdown/JSON candidate lists, duplicates, renamed repositories and license status; only then freeze the candidate pool.
5. Start identical-workload comparison and component assembly only after the freeze gates pass. A full orchestrator replacement remains allowed if demonstrated better with tests and without violating MediaHub authority boundaries.

**Disposition: 8 ADDITIONAL IMMUTABLE SOURCE PINS / LICENSES AND MANIFESTS READ / LOCKFILE AUDIT INCOMPLETE / INVENTORY NOT FROZEN / COMPARISON NOT STARTED / NO COMPONENT ADOPTED / CONTOUR A NOT ACCEPTED.**
