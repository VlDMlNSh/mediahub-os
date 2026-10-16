# MediaHub Master Roadmap — Cloud-Agent Fabric Execution Addendum, Wave 35

- Date: 2026-10-17
- Parent plan: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Architecture packet: [Cloud-Agent Autonomous Queue Reference Architecture, Wave 35](MEDIAHUB-CLOUD-AGENT-AUTONOMOUS-QUEUE-REFERENCE-ARCHITECTURE-WAVE-35-2026-10-17.md)
- Status: **ROADMAP ADDENDUM / PROPOSED / EXISTING COMPONENTS CROSSWALKED / IMPLEMENTATION AND QUALIFICATION BLOCKED**

## Owner direction preserved

The developer fabric must combine the existing three-server topology with authorized cloud agents. Provider credentials must be associated with provider/account/project and a scoped secret reference, rather than permanently attached to one host. Authorized agents should be admitted through one governed registry and routed into a durable, auditable development queue. Cloud agents are complementary workers; they do not replace Jarvis coordination, ASTRA/A0 queue authority, or MediaHub Product State Authority.

This addendum places that direction into the single master execution plan. It does not select an unreviewed provider, alter accepted authority boundaries, or grant automatic permission to call a provider.

## Confirmed current baseline

- Main HEAD observed through GitHub API: `99e7c0598bdc2f69201958aeb983f64c04504990`.
- Documentation branch compare: DIVERGED; ahead by 1,944, behind by 12; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Existing Agent Fabric claim/lease primitive: `runtime/mediahub_runtime/agent_fabric.py`, blob `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd`.
- Existing 23-lane execution manifest: `ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json`, blob `b948f0beb510f24399d82aaefcb7f95584e99cab`.
- Current ASTRA qualification truth: `docs/qualification/CURRENT-TRUTH.generated.md`, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`; G0–G11 are BLOCKED and overall status is NOT_PROVEN / BLOCKED.
- Existing provider secret-flow/egress review identifies task-scoped credential and destination controls as open; see Wave 30, blob `28a5152b60b0809a90a0c938b81439b8a19852b7`.

## Updated execution order

| Priority | Roadmap item | Required work | Exit criteria |
|---|---|---|---|
| P0 | A0, R-06, MH-12 and target-manifest reconciliation | Resolve issuer lifecycle, ingress/API contract, data-class/purpose/destination policy, credential resolution and current target manifest from exact primary sources | Source-to-requirement crosswalk; unresolved decisions explicitly listed; no assumed API/issuer contract |
| P0 | Distributed claim authority | Decide whether existing persistence or GitHub-backed coordination can supply atomic claim, fencing, lease, heartbeat, cancellation and recovery across separate ephemeral runners | Accepted contract and collision/recovery evidence plan at an immutable revision |
| P0 | Agent/provider admission registry | Version a non-secret registry of integration identity, credential reference, route permissions, data classes, capabilities, terms evidence, quotas, review expiry and revocation | Schema, collision check and offline validator plan; secret values absent |
| P1 | Task envelope and evidence manifest | Bind task ID, immutable source SHA, allowlisted paths, agent admission revision, provider route, capabilities, budget, deadline, dependencies, cancellation and output digest | Schema references existing queue state; versioned mapping to the 23-lane manifest |
| P1 | Workflow and worker adapter hardening | Inspect existing cloud/local workflows; use least privilege, full-SHA action pins, isolated workspaces, sanitized artifacts and downstream validated writes | Reviewed diff and exact target manifest; no default ambient write token or broad secret fan-out |
| P1 | Offline and read-only verification | Validate schemas and policy checks before any provider is invoked; use synthetic context first | Test evidence bound to exact commit; no production mutation |
| P2 | Per-agent enrollment | Owner authorizes one integration/account/repository in its own UI; add reference metadata; run only the specifically authorized admission probe | Auth, route and data-policy evidence; read-only admission passed |
| P2 | Patch-worker admission | Add narrow branch/write capability after read-only admission and independent review | Path guard, source-SHA fencing, PR-only output, independent verifier and revocation proof |
| P3 | Expansion and soak | Increase concurrency by lane only after atomic shared claims and G0–G11 gates are evidenced | Frozen-SHA integrated results, recovery/rollback evidence and independent acceptance |

## Operational rule for automatic onboarding

When an owner-authorized agent becomes available, the controller may automatically:
1. detect its non-secret registration record;
2. validate required metadata, source permissions and policy evidence;
3. set it to `WAITING_AUTH`, `BLOCKED_POLICY` or `READY_FOR_PROBE`;
4. enqueue a synthetic/read-only task only after an explicit probe authorization exists;
5. allow production task claims only after the admission record has valid evidence and the task route is pre-authorized.

The controller must never infer that a credential exists from a hidden secret value, print secret material, or initiate model work solely because a secret was added. Auth, quota and terms failures stop admission; they do not trigger account switching or an unapproved fallback.

## Network and credential invariant

No always-on owner-operated server is required if a permitted hosted agent or GitHub-hosted runner can authenticate directly. The credential remains account/project/repository/environment scoped. However, every remote request has a real network origin; cloud provider IP and region signals remain observable. The design removes a fixed host dependency, not network-origin or regional policy. Choose a permitted egress region rather than spoofing location.

## Acceptance status

This addendum updates the roadmap sequence and links the Wave 35 architecture. It does not change the master baseline, canonical component manifest, runtime workflows or code. Main/docs branch divergence remains untouched. No provider was invoked, no credentials inspected, no tests run, no host or infrastructure changed, and no deployment or branch integration occurred in this pass.
