# MediaHub OS — Project Map Addendum, Wave 39

- Date: 2026-10-17
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Status: **NAVIGATION ADDENDUM / SOURCE-BOUND REVIEW / RUNTIME UNQUALIFIED**

## New navigation entry

### Wave 39 — Gemini MCP PR Review and Bundled-Command Compatibility

- Primary report: [MEDIAHUB-GEMINI-MCP-PR-REVIEW-AND-COMMAND-SURFACE-RECONCILIATION-WAVE-39-2026-10-17.md](../checkpoints/MEDIAHUB-GEMINI-MCP-PR-REVIEW-AND-COMMAND-SURFACE-RECONCILIATION-WAVE-39-2026-10-17.md)
- Parent report: [Wave 38 MCP core-allowlist diagnosis](../checkpoints/MEDIAHUB-GEMINI-MCP-CORE-ALLOWLIST-DIAGNOSIS-AND-REMEDIATION-WAVE-38-2026-10-17.md)
- Related PR: [#307 — allowlist GitHub MCP tools without enabling core tools](https://github.com/VlDMlNSh/mediahub-os/pull/307)
- Review disposition: PR `validate` and `verify` checks passed; PR remains open/unmerged; provider runtime acceptance pending.
- Additional source finding: the currently resolved Google Gemini Action tag `v0` copies bundled slash-command prompts into the workspace; source-pinned prompts contain MCP tool-name/method mismatches documented in upstream issue #510. Treat this as a separate remediation lane from the direct-prompt allowlist fix.
- Credential topology: ephemeral GitHub-hosted workers remain the preferred cloud execution lane; provider/account credentials are independent of the three physical nodes. No fixed egress-IP or provider-region assumption is accepted.
- Queue status: 16 documentary items; no qualified live scheduler or active autonomous agent proven.
- Next: inspect the pinned OpenHands Agent Server route/configuration and workspace/tool enforcement against A0, MH-12 and R-06.


## Wave 40 — Gemini MCP Adapter Remediation

- Report: [Gemini MCP Adapter Remediation — Wave 40](../checkpoints/MEDIAHUB-GEMINI-MCP-ADAPTER-REMEDIATION-WAVE-40-2026-10-17.md), creation commit `a0c1e276018c5e9514bedf47386b84a7138b7022`.
- Evidence run: [39019037870](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019037870), job [117356960181](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019037870/job/117356960181), conclusion `success`; generated [PR #310](https://github.com/VlDMlNSh/mediahub-os/pull/310).
- Empirical defect: `mcp_github_list_commits` failed with `Invalid input: expected record, received array`; file reads, branch/file writes, and PR creation succeeded.
- Remediation proposed in [PR #311](https://github.com/VlDMlNSh/mediahub-os/pull/311): remove `list_commits` from the MCP allowlist and use the already successful `get_file_contents` operation for the initial connectivity check.
- Workflow file and recovery artifact were read back from the proposed branch. Runtime confirmation of the revised configuration is pending an authorized manual dispatch after review/merge.
- Free-tier quota remains provider-controlled. The current mutable `google-github-actions/run-gemini-cli@v0` reference is a separate source-pinning hardening item.
- No merge, test, provider call, installation, qualification, deployment, credential change, host/runtime inspection or infrastructure change occurred.

This addendum supplements the canonical map. It does not replace the canonical map, alter accepted Baseline 2.0, authorize runtime activation, or close acceptance gates.
