# MediaHub Chat Tree Map — Wave 494 addendum (2026-10-31)

- Reference architecture: [Wave 494 — Twenty-slot GitHub-hosted Cloud Agent Pool](../checkpoints/MEDIAHUB-20-SLOT-GITHUB-HOSTED-CLOUD-AGENT-POOL-REFERENCE-WAVE-494-2026-10-31.md).
- Defines 20 logical concurrent job slots, dynamically allocated across agent execution, build/test, independent review, research, integration/evidence and control/recovery.
- Default candidate remains `ubuntu-24.04` x64; ARM/Windows/macOS are specialist profiles on demand. Hosted VMs are ephemeral per job; no shared filesystem or peer-network bandwidth is assumed.
- Uses weighted fair scheduling, per-provider quota controls, immutable SHA handoff, sequential dependent A1→A2→A3 review, and pool-wide parallelism for independent tasks.
- The 20-slot design is a target ceiling, not proof of effective account entitlement or reserved concurrency. Effective plan, concurrency, usage and artifact retention remain NOT VERIFIED.
- A0 issuer/capability/lifecycle, R-06, egress enforcement, schema validation and independent review remain controlling gates. No dispatch/runtime changes or acceptance.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Working branch: `docs/wave494-twenty-slot-cloud-pool-reference-20261031`; not canonical and not integrated.

## Architecture reconciliation — three pools and Jarvis (2026-10-31)

Wave 494's 20 logical slots apply only to pool 1, the GitHub-hosted cloud pool. The owner-directed Wave 283 topology remains three separate pools: (1) GitHub-hosted ephemeral workers, (2) separately admitted MediaHub user machines, and (3) the Alamo-only local Claude executor subject to a verified zero-cost route. Jarvis submits delegated missions to ASTRA GOLD A0; A0 owns DAG decomposition, dispatch, claims/leases, retry/cancel/recovery and evidence reconciliation. Jarvis is not one of the 20 worker slots and must not create a competing queue or bypass A0. This does not prove Jarvis has already been migrated/deployed in GitHub cloud; that remains NOT VERIFIED.

Repository is public and GitHub Free official documentation currently lists 20 concurrent standard GitHub-hosted jobs, maximum 5 macOS jobs; public-repository standard runner use is free. Free-plan artifact storage is 500 MB; private repository allowance is 2,000 minutes/month. These limits do not grant model-provider quota. Avoid larger runners and enforce per-provider free quota / no paid fallback independently.

Provider candidates researched (not admitted): Gemini API, Groq, Cerebras, Cloudflare Workers AI, OpenRouter free models; optional time-limited Alibaba Model Studio new-user quota. Hugging Face's $0.10 monthly credits are not a strict free-only route without a hard stop. GitHub Models retired July 30, 2026. See Wave 494 report for constraints and official sources.


## Additional cloud worker runtimes (research only)

Wave 494 report now includes a bounded candidate shortlist: Gemini CLI (existing), mini-SWE-agent (issue-to-patch), Aider (small diffs), OpenHands Software Agent SDK (general sandboxed coding), and Goose CLI (general research/MCP worker, higher tool-surface risk). These are runtimes, not free model providers; inference quotas remain separate. Ruflo remains evaluation-only under Issue #568 and must not replace Astra/A0. No candidate was installed or dispatched. See §13 of the report for source links and qualification order.
