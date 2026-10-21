# Wave 328 — Gemini transport clarification and Voktors executor recheck

Date: 2026-10-21
Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

## Owner clarification
The owner confirms that the GitHub repository contains the batch-enable variable and HMAC-related credential. The controller's exact references are `vars.MEDIAHUB_GEMINI_BATCH_ENABLED`, `secrets.MEDIAHUB_GITHUB_TOKEN`, and `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`. The owner-provided spelling `MEDIAHUB_DISPATCH_НМАС_KEY` contains Cyrillic characters in “НМАС”; verify that the configured secret's actual name is the exact ASCII identifier `MEDIAHUB_DISPATCH_HMAC_KEY`. This is a name-only check; secret values must not be read, printed, or copied. Presence alone does not prove effective environment scope, token permissions, or successful authorization.

## Immutable state and admission
- Controller source blob on `main`: `9453403bba899a2400ee3fb874d32badd034c704`. It explicitly references the ASCII HMAC secret name, GitHub token secret, and batch-enable repository variable. Its workflow supports non-launching `probe` and explicit `agents` mode; the issue-comment path is an exact owner `/next` on Issue #301 and the dispatch job additionally requires the controller to run from `refs/heads/main`.
- PR [#437](https://github.com/VlDMlNSh/mediahub-os/pull/437) remains OPEN/DRAFT/UNMERGED at head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`, base `1a6e5a16ef9950b72dda04abd69a27f019922489`. The exact-head workflow-run query returns no runs, combined status returns no statuses, and formal reviews count is zero. Qualification is **NOT VERIFIED**.
- Branch search lists `main` and recovery/test branches, but the available connector did not return the current main HEAD SHA in this pass. No unverified SHA is invented here.
- The controller's dispatch logic requires both credential strings to be non-empty, validates the full target SHA against the GitHub API, and fails the batch if all three children cannot be correlated to successful runs. No secret values were read.

## Gemini execution
- Agent 1: **NOT RUN**. Agent 2: **NOT RUN**. Agent 3: **NOT RUN**.
- Controller run ID: none. Child run IDs/jobs: none. Artifact digests: none.
- No Issue #301 `/next` trigger comment was posted because exact-head CI, independent review, effective secret/variable metadata, branch governance, and trusted-main no-secret probe evidence remain incomplete. The user's clarification about repository configuration does not by itself clear these gates.
- Gemini execution remains strictly on the GitHub Actions/API route; no physical server is part of the Gemini transport.

## Voktors-Mini.Dlink / macOS
- SentinelX inventory still identifies only one active host: `Voktors-Mini.Dlink`, ID `host_5f7264034bdf0b51`, macOS ARM64, agent `0.22.0`. Free plan capacity is one active host, with zero additional slots.
- Current ping and capabilities calls timed out. A new bounded `script_run` timed out as well. Earlier bounded evidence found the agent-browser native ARM64 binary on disk, while the installed CLI was not in the SentinelX exec allowlist. The required `agent-browser skills get core` has not been successfully retrieved; no browser session was opened and no allowlist was modified.
- Earlier successful bounded inventory found `claude` and `ollama` absent from PATH. Claude/FCC-Ollama free route remains **NOT VERIFIED**. No Claude session started; no paid fallback used.

## Changes and acceptance
- No application code, workflow, secret, variable, host allowlist or provider configuration changed in this pass.
- PR exact-head state, reviews, controller source, SentinelX host inventory and connection were rechecked. No agent dispatch, merge, deployment, qualification or acceptance is claimed.

## Next bounded steps
1. Verify exact ASCII secret name `MEDIAHUB_DISPATCH_HMAC_KEY` and repository/environment scope metadata without revealing values; verify `MEDIAHUB_GEMINI_BATCH_ENABLED=true` at the scope read by this workflow.
2. Obtain exact-head CI and independent security review for PR #437, authoritative branch governance, and trusted-main no-secret probe evidence.
3. Only after every gate passes, dispatch all three child workflows through the approved GitHub controller against one shared immutable target SHA and record controller/child run IDs, final statuses and artifact digests.
4. Restore stable SentinelX connectivity to Voktors-Mini.Dlink, retrieve `agent-browser skills get core` through an approved invocation path, and separately verify the Claude/FCC free-only route without paid fallback.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
