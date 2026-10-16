# MediaHub OS — Gemini Trust and Configuration Source Reconciliation, Wave 34

- Date: 2026-10-17
- ID: MH-GEMINI-TRUST-CONFIG-RECONCILIATION-34
- Contour: A — Developer Fabric
- Status: SOURCE REVIEW / DESIGN ONLY / WORKFLOW UNCHANGED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- MediaHub main HEAD reviewed: `149f5af85962a7a1219a4012e1f4b0b8b335a0a3`
- Workflow blob: `b81e9cf829d1272fe7ea0db8ce8e4b48adcc272a`
- Prior packet: [Wave 33](MEDIAHUB-GEMINI-WORKFLOW-HARDENING-PACKET-WAVE-33-2026-10-17.md), blob `6d063a2bbceb177a2469571ef6f705aed8e4a3fb`

## 1. Scope and outcome

This pass reconciles the exact Gemini CLI trust setting, the Google Action's own trust guidance, the action's project-settings contract and the pinned CLI settings schema. It also rechecks the unresolved target-manifest authority. This is a public-source/documentation pass only.

No workflow edit, dispatch, provider/model invocation, credential access, test, qualification, host/runtime inspection, installation, infrastructure change, deployment or branch integration occurred.

## 2. Source-bound findings

### 2.1 Trust environment variable: CLI source and Action guidance disagree

The MediaHub workflow sets `GEMINI_CLI_TRUST_WORKSPACE: 'true'`.

At Gemini CLI tree commit `ed96faedfd5571f055c44f2c9509d62321d1138d`, the primary file `docs/cli/trusted-folders.md` explicitly documents `GEMINI_CLI_TRUST_WORKSPACE=true` as a headless trust-check bypass for the session. The same document states that untrusted workspaces ignore project settings and do not connect MCP servers, while trusting the folder unlocks project configuration and MCP functionality.

At Google Action commit `f77273f4c914e4bf38440cf36a0369cb64a37489`, `docs/trust-guidance.md` instead instructs users to set `GEMINI_TRUST_WORKSPACE=true`. This conflicts with the CLI's exact source documentation. Treat the Action guide as inconsistent/stale for this setting; the MediaHub variable name is supported by the CLI source reviewed here. Preserve the trust bypass as a material risk decision, rather than treating it as an incidental environment setting.

Sources:
- CLI trusted-folders: https://github.com/google-gemini/gemini-cli/blob/ed96faedfd5571f055c44f2c9509d62321d1138d/docs/cli/trusted-folders.md
- CLI trust implementation wrapper: https://github.com/google-gemini/gemini-cli/blob/ed96faedfd5571f055c44f2c9509d62321d1138d/packages/cli/src/config/trustedFolders.ts
- Action trust guide: https://github.com/google-github-actions/run-gemini-cli/blob/f77273f4c914e4bf38440cf36a0369cb64a37489/docs/trust-guidance.md

### 2.2 Project settings are written into the checked-out workspace

The Action's `action.yml` at commit `f77273f4c914e4bf38440cf36a0369cb64a37489` declares input `settings` as a JSON string written to `.gemini/settings.json` for project-level configuration.

The MediaHub workflow supplies its MCP server configuration through that input. Therefore the project settings file is an active part of the agent's trust boundary. The exact action commit and the exact CLI settings schema must remain part of the evidence record for any future workflow change.

Action source:
https://github.com/google-github-actions/run-gemini-cli/blob/f77273f4c914e4bf38440cf36a0369cb64a37489/action.yml

### 2.3 `tools.core` is a valid CLI settings key

At CLI tree commit `ed96faedfd5571f055c44f2c9509d62321d1138d`, `packages/cli/src/config/settingsSchema.ts` defines `tools.core` as an array that restricts built-in tools through an allowlist. Thus the workflow's `"tools": { "core": [] }` shape is recognized by this schema. This is only a schema/source confirmation; runtime semantics and effective tool availability have not been tested.

Schema source:
https://github.com/google-gemini/gemini-cli/blob/ed96faedfd5571f055c44f2c9509d62321d1138d/packages/cli/src/config/settingsSchema.ts

### 2.4 Write-capable MCP boundary remains the highest direct risk

The workflow grants the job `contents: write` and `pull-requests: write`, then exposes MCP tools for branch creation, repository file writes and PR creation. A model instruction to create one branch/PR is a behavioral prompt, not an independent enforcement boundary.

Before admission, the write path needs a trusted validator or broker outside model-controlled settings, including:
- allowlisted paths and protected-path policy;
- base commit pinning and branch namespace constraints;
- diff-size/file-count limits and symlink/path traversal rejection;
- secret-like content filtering and deterministic evidence manifest;
- PR creation only after policy validation;
- independent review, branch protection and merge/deployment separation.

### 2.5 MCP image digest remains unresolved

The MediaHub workflow currently names `ghcr.io/github/github-mcp-server:v0.27.0`. Public source evidence resolves the tag to source commit `2b352ab0b914cde8c16d44200a7cace9f400be71`, while the tag metadata is unsigned. The public package evidence collected in this pass did not establish a registry manifest digest specifically bound to that exact tag and platform.

**Decision:** keep the digest/provenance gate BLOCKED. Do not substitute the digest of the current/latest package or another version.

### 2.6 Exact clean target remains unknown

Wave 10's clean-target reconciliation remains authoritative for this question: no owner-accepted exact target manifest was identified. Hardware, OS, network, storage and worker-isolation facts remain unresolved. The proposed Gemini workflow hardening does not close that admission gate.

Source:
https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CLEAN-TARGET-MANIFEST-AUTHORITY-RECONCILIATION-WAVE-10-2026-10-16.md

## 3. Decisions and gates

| Gate | Evidence | Status |
|---|---|---|
| CLI trust variable | Pinned CLI documentation confirms `GEMINI_CLI_TRUST_WORKSPACE`; Action guidance uses a conflicting name | Source discrepancy recorded; trust bypass still requires explicit design treatment |
| Project settings | Action writes `.gemini/settings.json`; pinned CLI schema recognizes `tools.core` | Source confirmed; effective runtime behavior unverified |
| MCP image | Exact source tag known; exact OCI digest/provenance unbound | BLOCKED |
| Write boundary | Model-facing MCP has write-capable operations; no independent path validator evidenced | BLOCKED |
| CLI version | Action defaults to mutable `latest`; `v0.64.0` remains candidate only | BLOCKED pending accepted pin and provenance |
| Target manifest | Wave 10 identifies target as UNKNOWN/BLOCKED | BLOCKED |
| A0 / MH-12 / R-06 | Existing issuer, secret-lifecycle and governance decisions remain open | OPEN |

## 4. Next bounded pass

1. Continue read-only upstream package/provenance reconciliation for the exact MCP `v0.27.0` image; retain BLOCKED if exact binding cannot be established.
2. Prepare a minimal workflow diff proposal that pins immutable Action refs and a reviewed CLI version, keeps the model's MCP allowlist narrow, and introduces trusted diff/path validation before PR creation.
3. Define a versioned evidence-manifest schema with workflow run, action commits, CLI version, model ID, MCP image digest, base SHA, task authority, diff digest, validator result and PR/review state.
4. Reconcile the change proposal against A0, MH-12, R-06 and the clean-target manifest before seeking any separate change authority.
5. Keep dispatch, model/provider calls, testing, qualification, host/runtime work, infrastructure changes, deployment and branch integration outside this pass.

## 5. Status

Source discrepancy and configuration contracts are documented. No executable workflow changes or runtime verification were performed. All blocked gates remain explicit.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
