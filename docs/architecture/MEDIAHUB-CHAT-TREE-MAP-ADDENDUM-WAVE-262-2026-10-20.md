# MediaHub Chat Tree Map — Addendum Wave 262 (2026-10-20)

## Owner-confirmed infrastructure boundary
- The cloud agent pool must operate exclusively on GitHub-hosted cloud infrastructure for orchestration, dispatch, ephemeral worker execution, artifacts, evidence and coordination.
- No dedicated physical hardware, VPS, self-hosted runner, local workstation, NAS, always-on listener or customer-managed server is a cloud-pool dependency.
- External model-provider APIs are permitted only as explicitly authorized model endpoints called from GitHub-hosted jobs; they are not an approved alternate orchestration plane.
- Servers are reserved exclusively for later local-compute/Jarvis needs and must not be required by Contour A's cloud pool.
- Local executor/Jarvis design and deployment remain sequenced after cloud-pool deployment and independent operational acceptance. Contour B remains blocked until Contour A acceptance.

## Existing evidence
- Issue #301 remains open and describes GitHub-hosted ephemeral workers, outbound HTTPS and runtime-only secret injection; schema validation and negative fixtures remain open; CAF-Q-001…015 are documentary rather than a live scheduler.
- Existing provider registry `ops/qualification/provider_model_registry.json` on `main`, blob `62328126fd2cd8879a73bb6812adcacd3e2abe84`, has 25 records; these are not proof of active access/qualification.
- Controller workflow blob on `main`: `99e5a87825aeb239568f96ecef004a102ff3e53b`. Source inspection does not authorize dispatch. PR #421 remains OPEN/Draft at the last checked state.
- Full evidence and consequences: [Wave 262 report](../checkpoints/MEDIAHUB-GITHUB-CLOUD-ONLY-POOL-AND-LOCAL-JARVIS-BOUNDARY-WAVE-262-2026-10-20.md).

## Hard implementation filter
Reuse ready-made multi-agent frameworks only inside GitHub-hosted jobs and behind the existing controller/capability boundaries. Prefer GitHub-native coordination first. Any requirement that would force an external hosted database, queue, router or dedicated server must be recorded as a capability gap and routed through explicit governance/change control; no silent architectural expansion.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
