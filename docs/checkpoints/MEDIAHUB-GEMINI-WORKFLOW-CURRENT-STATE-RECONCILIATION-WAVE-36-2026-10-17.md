# MediaHub OS — Gemini Workflow Current-State Reconciliation, Wave 36

- Date: 2026-10-17
- Status: SOURCE REVIEW / DESIGN ONLY / WORKFLOW UNCHANGED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Current `main` HEAD: `6c2e8dbdee81c798b64e65546e7ded07093f100a`
- Current workflow blob: `9be13613ae79f316ca410c16c6e69e2aea7283a4`
- Prior supply-chain report: [Wave 35](MEDIAHUB-GEMINI-SUPPLY-CHAIN-ADMISSION-DESIGN-WAVE-35-2026-10-17.md), blob `4eb593154742cae57670f98a133e5e375d2ea1e0`

## 1. Scope

Reconcile the current live `main` workflow after newer commits, distinguish resolved configuration changes from remaining supply-chain and admission gaps, and refresh branch evidence. This is public source inspection and documentation only.

No workflow edit, dispatch, provider/model invocation, credential access, test, qualification, host/runtime inspection, installation, infrastructure change, deployment, merge, rebase or cherry-pick occurred.

## 2. Current branch evidence

- `main` HEAD: `6c2e8dbdee81c798b64e65546e7ded07093f100a`, commit message `fix: avoid Gemini MCP token expansion failure (#306)`.
- Documentation branch comparison: DIVERGED, ahead 1963 / behind 14.
- Merge base: `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- The branch compare is live at the time of this pass. No integration operation was performed.
- Current workflow blob SHA: `9be13613ae79f316ca410c16c6e69e2aea7283a4`.

## 3. Changes visible in the current workflow

Compared with the earlier reviewed workflow blob `b81e9cf829d1272fe7ea0db8ce8e4b48adcc272a`, the current source now:
- pins Gemini CLI input to `0.64.0`;
- disables Gemini CLI telemetry in the supplied settings;
- lowers `maxSessionTurns` from 30 to 16;
- adds `get_me` to the MCP tool allowlist and instructs the agent to call the prefixed MCP tool name;
- supplies the GitHub token through the MCP server environment interpolation `${{ github.token }}`, apparently addressing the latest commit's token-expansion issue;
- retains mutable Action refs `actions/checkout@v4` and `google-github-actions/run-gemini-cli@v0`;
- retains the mutable MCP image tag `ghcr.io/github/github-mcp-server:v0.27.0`;
- retains job-level `contents: write` and `pull-requests: write` for the model-facing worker;
- retains `GEMINI_CLI_TRUST_WORKSPACE: 'true'`.

These observations describe source configuration only. The recent commit message does not prove the workflow has been dispatched or that the change works end-to-end.

## 4. Updated disposition matrix

| Control | Current disposition | Evidence needed |
|---|---|---|
| Gemini CLI version | Explicit version now configured | Verify package provenance/integrity and action installation semantics at the pinned action commit |
| Action refs | Mutable tags remain | Full immutable commit refs and reviewed source provenance |
| MCP container | Mutable tag remains | Exact OCI index and platform manifest digest, plus verified build/source attestation |
| Token interpolation | Source now passes `${{ github.token }}` in settings | Controlled, separately authorized synthetic verification; no dispatch in this pass |
| Model-facing write authority | Broad job write permissions remain | Trusted external path/diff admission before a separate minimal publisher capability |
| Workspace trust bypass | Enabled | Explicit risk disposition plus isolation and trusted config policy |
| Evidence manifest | No trusted external admission manifest established by this source review | Trusted manifest generation, exact tree binding, policy decision and redacted secret-scan summary |
| Clean target / A0 / MH-12 / R-06 | OPEN per current documentation evidence | Canonical acceptance records and exact target/issuer/ingress evidence |
| ASTRA qualification | G0–G11 BLOCKED; overall NOT_PROVEN / BLOCKED | Gate-specific acceptance evidence |

## 5. OCI digest/provenance status

The prior source review associated MCP tag `v0.27.0` with source commit `2b352ab0b914cde8c16d44200a7cace9f400be71`. This pass still lacks authoritative evidence binding the actual OCI index and platform manifest digest to that source revision and a trusted build identity. A source commit is not an OCI digest. Status remains BLOCKED.

Required evidence: registry manifest response with digest/media type; platform-specific child digest(s); signature/attestation verification; subject digest matching the pulled image; source repository and commit; workflow identity and builder provenance. Until verified, keep the mutable image reference out of an accepted hardened baseline.

## 6. Reuse-first implementation direction

The live docs branch's Wave 35 cloud-agent records identify existing building blocks on `main`:
- 23-lane execution manifest: `ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json`, blob `b948f0beb510f24399d82aaefcb7f95584e99cab`;
- file-backed claim/lease primitive: `runtime/mediahub_runtime/agent_fabric.py`, blob `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd`;
- current generated qualification truth: `docs/qualification/CURRENT-TRUTH.generated.md`, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`, with G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED.

Do not create a second scheduler. A local file-backed claim primitive alone does not prove atomic coordination across separate ephemeral runners. Before implementation, reconcile A0, R-06, MH-12 and the target manifest, then inspect existing validator/evidence components and specify the smallest compatible admission layer.

## 7. Next bounded step

Use an authoritative OCI registry/attestation route to resolve the exact MCP digest and provenance. If unavailable, record the access/evidence gap and preserve BLOCKED. In parallel within documentation-only scope, map the external path/diff admission and sanitized evidence manifest to existing Agent Fabric, qualification and CI components. Keep runtime verification, workflow dispatch, provider calls, tests, qualification, infrastructure changes, deployment and branch integration behind separate explicit authorization.
