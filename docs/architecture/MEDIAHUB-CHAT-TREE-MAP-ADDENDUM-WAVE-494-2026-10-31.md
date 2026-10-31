# MediaHub Chat Tree Map — Wave 494 addendum (2026-10-31)

- Reference architecture: [Wave 494 — Twenty-slot GitHub-hosted Cloud Agent Pool](../checkpoints/MEDIAHUB-20-SLOT-GITHUB-HOSTED-CLOUD-AGENT-POOL-REFERENCE-WAVE-494-2026-10-31.md).
- Defines 20 logical concurrent job slots, dynamically allocated across agent execution, build/test, independent review, research, integration/evidence and control/recovery.
- Default candidate remains `ubuntu-24.04` x64; ARM/Windows/macOS are specialist profiles on demand. Hosted VMs are ephemeral per job; no shared filesystem or peer-network bandwidth is assumed.
- Uses weighted fair scheduling, per-provider quota controls, immutable SHA handoff, sequential dependent A1→A2→A3 review, and pool-wide parallelism for independent tasks.
- The 20-slot design is a target ceiling, not proof of effective account entitlement or reserved concurrency. Effective plan, concurrency, usage and artifact retention remain NOT VERIFIED.
- A0 issuer/capability/lifecycle, R-06, egress enforcement, schema validation and independent review remain controlling gates. No dispatch/runtime changes or acceptance.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Working branch: `docs/wave494-twenty-slot-cloud-pool-reference-20261031`; not canonical and not integrated.