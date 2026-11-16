# Wave 507 — Gemini controller and VM 2 placement audit (2026-10-31)

## Disposition

**VM 2 shared-runner design: NOT IMPLEMENTED. Controller dispatch: NOT RUN. Provider calls: NOT RUN.**

This is a source-only, non-launching audit against the immutable `main` target below. No secrets were read, no provider was invoked, no workflow was dispatched, and no infrastructure was changed.

## Immutable source snapshot

- Repository: `VlDMlNSh/mediahub-os`
- `main`: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Canonical docs branch: `docs/mediahub-chat-tree-map-20261012` at `d9a289b9113f7567711b641a7017eb814d6c259d`
- Controller `.github/workflows/gemini-batch-dispatch-controller.yml`: blob `0a1246f6755020faf8b7e48d07bfff790bbaece3`
- Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`: blob `155a02159912ca371e6f826c51325ca269857aad`
- Agent 2 `.github/workflows/gemini-agent-2.yml`: blob `fff1820a6b97d379b23674f36bd62227b7d4dec2`
- Agent 3 `.github/workflows/gemini-agent-3.yml`: blob `781df56e8aa7c75ba453c08378611857862b2e44`
- Agent registry `profiles/agent-registry.json`: blob `993cbbe1b2b2a88da7d8884a897b404f055981a8`
- Existing agent system registry `.github/agent-system/registry.yaml`: blob `0317d1e794aa80cd0fa22bd953b95921b26aafd3`
- Claim/lease simulation `ops/agent-fabric/simulations/claim-lease-simulation.md`: blob `090b96169df023781df9a98e61d285949070f578`

The source files above were read from `main`; the canonical docs refs are separately identified and were not modified by this audit.

## Findings

### 1. Current controller is a three-child-workflow fan-out, not one shared VM

The controller constructs three fixed task envelopes and dispatches these workflows through GitHub Actions API:

1. `gemini-autonomous-engineering.yml` — Agent 1
2. `gemini-agent-2.yml` — Agent 2
3. `gemini-agent-3.yml` — Agent 3

Each child has its own `workflow_dispatch` entry point and an execution job using `runs-on: ubuntu-latest`. This means the current implementation provisions separate ephemeral hosted-runner job environments. It does not provide one persistent or shared VM with three concurrent Gemini CLI roles.

### 2. Current child contracts are role-specific and source-bound, but not co-located

All three child workflows:
- accept controller-generated dispatch ID, immutable target SHA, task, base ref, scope and HMAC signature;
- verify the signature before the provider/model step;
- require trusted repository and `refs/heads/main` workflow-dispatch context;
- check out the immutable target SHA;
- use separate provider credential references: Agent 1 `GEMINI_API_KEY`, Agent 2 `GEMINI_API_KEY_2`, Agent 3 `GEMINI_API_KEY_3`.

Agent 2 and Agent 3 grant their engineering jobs `contents: write` and `pull-requests: write`; their prompt tool allowlists constrain the configured GitHub MCP operations. These rights are broader than a read-only reviewer identity and must be split into task-specific capabilities before any consolidation. Credential existence, scopes, account identity, provider eligibility and quota are **NOT VERIFIED**; secret values were not accessed.

### 3. Controller admission remains fail-closed but unresolved

The controller checks `vars.MEDIAHUB_GEMINI_BATCH_ENABLED` and requires `secrets.MEDIAHUB_GITHUB_TOKEN` plus `secrets.MEDIAHUB_DISPATCH_HMAC_KEY` before child dispatch. Issue #301 also requires A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy authority gates, authoritative runner/workspace/network manifest, schema validation and independent review before admitting workers.

The current audit did not inspect secret values or attempt dispatch. Admission readiness is **NOT VERIFIED**. No claim is made that the gates are configured or passed.

### 4. Existing repository components should be reused, not replaced

The repository already contains:
- `profiles/agent-registry.json` with provider/agent registry metadata;
- `.github/agent-system/registry.yaml` with coordinator, architect, builder and verifier role concepts, bounded dynamic workers and an independent-verification invariant;
- `ops/agent-fabric/simulations/claim-lease-simulation.md` documenting exact-path collision, parent/child collision, independent paths, heartbeat, expiry and independent verification cases.

These are useful inputs, not proof of a qualified runtime scheduler, lease service, issuer or worker admission system. The claim/lease file is explicitly a test plan requiring execution evidence.

### 5. No safe basis yet for implementing one shared worker

A shared-runner redesign must not simply move three API keys and three CLI processes into one long-lived shell. It needs:
- a single controller-authenticated worker admission envelope bound to the same immutable target SHA;
- three independent role identities/capability envelopes and non-overlapping credential scopes;
- separate worktrees/directories, environment allowlists and process boundaries;
- explicit per-role quota, timeout, cancellation, lease expiry and recovery behavior;
- no nested dispatch, no paid fallback, no credential forwarding between roles;
- auditable per-role logs/artifacts and digests with secret redaction;
- read-only Agent 2/3 review capability unless an explicitly authorized write task is assigned;
- independent negative tests for signature mismatch, stale SHA, missing issuer/capability, quota exhaustion, cancellation, workspace collision and artifact leakage.

Because Issue #301 orders A0 authority and lease/recovery gates before additional worker admission, the shared-runner implementation is **BLOCKED** pending those prerequisite contracts and evidence. This does not prevent non-secret design/test work.

## Verification matrix

| Item | Status | Evidence |
|---|---|---|
| Immutable source refs and blobs | VERIFIED | SHA list above |
| Three controller child workflow names | VERIFIED | Controller source |
| Each child uses an Ubuntu hosted runner | VERIFIED | Three child workflow sources |
| Three separate Gemini key references | VERIFIED as source references only | Agent 1/2/3 workflow sources |
| Credential presence, scopes and quota | NOT VERIFIED | No secret access |
| A0 issuer/lease/cancel/recovery qualification | NOT VERIFIED | Issue #301 prerequisites remain open |
| Shared VM 2 worker | NOT IMPLEMENTED | No such worker in inspected controller/child files |
| Gemini dispatch/provider call | NOT RUN | No dispatch performed |
| Runtime qualification/acceptance | NOT ACCEPTED | No runtime evidence |

## Next bounded step

Perform a source-only contract crosswalk for the A0 issuer, task envelope, capability registry, lease/cancel/recovery and R-06 audit/privacy requirements. Identify authoritative existing files and missing acceptance tests before drafting any shared-runner workflow. Do not dispatch agents or invoke providers. Once the prerequisites are independently verified, design a single ephemeral worker job with three isolated role sandboxes; do not describe GitHub-hosted `ubuntu-latest` as a persistent VM.

## Governance and related work

- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- PR #610 (VM 1 placement correction): https://github.com/VlDMlNSh/mediahub-os/pull/610
- PR #613 (required CI context repair): https://github.com/VlDMlNSh/mediahub-os/pull/613

