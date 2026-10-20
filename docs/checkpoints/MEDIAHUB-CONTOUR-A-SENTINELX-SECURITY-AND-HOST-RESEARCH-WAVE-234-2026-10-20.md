# MediaHub OS — SentinelX security and host research (Wave 234, 2026-10-20)

## Purpose and status

This record consolidates two investigations requested for Contour A:
1. assessment of the SentinelX product/capability claims against its public security documentation;
2. a fresh, read-only inventory of the SentinelX account currently connected to this ChatGPT session.

This is research evidence, not an endorsement, security certification, accepted architecture decision, or Contour A qualification. No host configuration was changed, no disabled host was re-enabled, no agent update was performed, and no workflow was dispatched.

## Current MediaHub repository refs

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Functional development ref `main` HEAD observed by recent-commit search: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`.
- Live compare `main...docs/mediahub-chat-tree-map-20261012`: **DIVERGED**, docs ref 2,535 commits ahead and 33 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. Do not merge these histories wholesale.
- Bootstrap blob SHA read from canonical ref: `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`.
- Canonical map blob SHA: `2187b4ca50792fe073f0979442c0f73432a2f6f9`; Contents API returned empty content even when requesting a line range. Per the prior Wave 233 record, the blob was readable through a separate Git-data read, but that path is not available in this pass. Therefore the map was not modified.
- Checkpoint blob SHA read from canonical ref: `437a8747db22d8ac39d7f4856122727357de05a2`.
- Master Roadmap blob SHA read from canonical ref: `beef785c787702dc174cf9a5515bac8c9f4b292f`.
- Prior Contour A research reconciliation: [Wave 233](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-DEEP-RESEARCH-WAVE-233-2026-10-20.md).
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).

## Study A — SentinelX product and security-documentation review

### Source set

Public project sources read on 2026-10-20:
- [sentinelx-cloud-core README](https://github.com/pensados/sentinelx-cloud-core/blob/main/README.md)
- [SECURITY.md](https://github.com/pensados/sentinelx-cloud-core/blob/main/SECURITY.md)
- [THREAT_MODEL.md](https://github.com/pensados/sentinelx-cloud-core/blob/main/THREAT_MODEL.md)
- [sentinelx-cloud-protocol](https://github.com/pensados/sentinelx-cloud-protocol)
- [sentinelx-core-mcp](https://github.com/pensados/sentinelx-core-mcp)

The public pages identify `main` but an immutable upstream commit/blob SHA could not be obtained through the connected GitHub Contents API in this pass (the external repository request returned 404). Treat the links as mutable source references, not pinned-source evidence. This report does not claim a full code audit.

### Findings grounded in published documentation

- The public documentation describes an outbound-WebSocket agent with no inbound listener; a hub operated by Pensa; a host-side command allowlist; separate path allowlists for structured filesystem operations; per-host enrollment identity; and SSRF/path-traversal protections for the documented upload paths.
- The project explicitly says the hub is trusted for message contents. A compromised hub can invoke any operation the operator has allowed. The agent has no sandbox, and the documented command boundary is only as strong as the allowlist: allowing a shell such as `bash`/ `sh -c` can effectively remove the intended restriction.
- The documentation acknowledges that legitimate allowlisted operations can expose data to the hub/LLM, the agent does not currently rate-limit requests, and its local mutation log is best-effort rather than tamper-resistant. The threat model recommends an append-only external audit sink for higher-assurance use.
- The README describes `script_run` as a supported operation. Therefore, enabling it is not equivalent to granting a constrained declarative task API; the effective allowlist, script interpreter rules, file-path policy, sudoers rules, hub trust, and audit retention must be reviewed together.
- The separate `sentinelx-core-mcp` project describes OAuth/OIDC scopes at the MCP bridge and a second internal bearer-token layer. That is a different deployment topology from the currently connected SentinelX cloud hub and must not be assumed to protect this account's hub route.
- The published docs are vendor-authored security claims. This pass did not independently execute adversarial tests or verify every linked implementation and test. No claim of verified exploit resistance is made.

### Contour A disposition

SentinelX can be considered a **temporary, policy-constrained remote operations surface** for read-only inventory and narrowly scoped diagnostics. It is not, by itself, the Contour A task issuer, capability authority, isolated cloud worker, artifact publisher, immutable provenance mechanism, or independent acceptance authority.

Before any use for project mutation or autonomous execution, require:
1. exact upstream source commit, release/version, license, and dependency provenance;
2. exported effective policy/config with secrets redacted, including commands, paths, services, sudo, and URL-fetch hosts;
3. explicit operation-to-task capability mapping, with deny-by-default and no broad shell escape hatch;
4. independent, append-only audit and correlation to task ID, issuer, target SHA, actor, operation, result, and evidence digest;
5. tests for replay/revocation, policy changes, hub compromise, path/symlink traversal, command-prefix ambiguity, secret exposure, timeout/cancellation, and output integrity;
6. clear separation between worker output and any GitHub write/publish credential;
7. a documented rollback and decommission plan for temporary hosts.

## Study B — live SentinelX account/host inventory

The connected SentinelX integration was queried read-only on 2026-10-20.

| Item | Observed state |
|---|---|
| Plan | Free |
| Enforced active-host limit | 1 |
| Active / parked / available slots | 1 / 0 / 0 |
| Active host | `Voktors-Mac-mini.local`, host ID `host_5f7264034bdf0b51` |
| Active agent | `sentinelx-cloud-core 0.22.0`; kernel `Darwin 23.6.0`; architecture `arm64` |
| Update notice | Integration reports `0.23.28` as latest; no update performed |
| Disabled host 1 | `mh-dev-01`, ID `host_58114817a6ab4dd0`, version `0.19.3`, disabled by user on 2026-10-17 |
| Disabled host 2 | `mh-dev-02`, ID `host_5bda3b5006655e9e`, version `0.22.0`, disabled by user on 2026-10-01 |

The two disabled hosts remain enrolled but are refused by the service until manually re-enabled through the SentinelX dashboard. The free-plan active-host limit is enforced at one; therefore the desired three-agent/three-host arrangement is **not currently available under this connected plan state**. No attempt was made to re-enable hosts or change plan/billing.

The active host capability summary reported 95 allowed commands, one service, one location, nine playbooks, two file-operation paths (both writable), two trusted fetch hosts, a 60-second default execution timeout, and a 600-second maximum. This is a count-only summary, not an exported review of the actual policy entries; the actual allowlist contents remain unreviewed in this pass.

## Reconciled conclusion

- SentinelX's documented design includes useful guardrails, but it trusts the hub to choose among allowed operations and does not provide a sandbox. The security boundary depends heavily on the actual host policy and operator choices.
- The live account currently offers one active host, not three. Do not describe three SentinelX hosts/agents as active or ready.
- Use the currently active host only for bounded, non-destructive diagnostics unless the exact operation is separately authorized and its policy reviewed. Do not use it as a substitute for GitHub-hosted ephemeral workers.
- The connected tool's ability to run scripts, edit files, manage services, or create cloud compute does not itself grant architectural or product-state authority.
- Contour A remains **NOT PROVEN / BLOCKED**. This study does not close issuer/capability/replay/revocation, accepted target manifest, R-06 audit/privacy, publisher separation, branch-protection evidence, or independent acceptance gates.

## Checks and limitations

- Re-read the report source (Wave 233), bootstrap, checkpoint, and Master Roadmap from the canonical documentation ref; recorded blob SHAs above.
- Re-checked `main` HEAD through recent commit search and compared `main` with the canonical documentation ref.
- Re-queried live SentinelX hosts and capability summary. No mutation was issued.
- Public SentinelX source pages were read via the web interface; exact upstream commit/blob SHAs and a full implementation/test audit remain **UNKNOWN**.
- The canonical map and large continuation checkpoint were not rewritten in this pass. The map endpoint returned empty content for the requested line slice; a safe Git-data update was not available through the currently exposed action set. This report is on the canonical documentation ref and is linked from Issue #301 instead.

## Next bounded action

1. Continue the Contour A source-bound review on the current `main` SHA, prioritizing the worker/publisher credential boundary and A0 issuer/capability lifecycle.
2. In a separate SentinelX-only read-only pass, retrieve the exact effective allowlist and path/service policy (redacted), then pin the upstream release/commit and run source-linked tests before deciding whether it is suitable for any mutating project task.
3. Keep the two disabled hosts disabled unless a separate capacity/authorization decision changes; do not make a three-host plan from the current Free-plan inventory.
4. Update the canonical map only through a verified Git-data write against the live documentation branch tree; do not use a large Contents API replacement or merge the diverged docs branch into `main` as a shortcut.
