# MediaHub OS — Wave 377: third-server runner identity check

- Date: 2026-10-22
- Scope: read-only verification of GitHub Actions runner inventory and local runner service on the explicitly designated third server only.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- SentinelX host: `host_5f7264034bdf0b51`, hostname `Voktors-Mini.Dlink`, connected and operational; macOS kernel 23.6.0, arch arm64, agent 0.22.0.

## Direct evidence from the third server

Read-only command:
`launchctl list | grep -Ei 'actions.runner|runner|github' ; gh api repos/VlDMlNSh/mediahub-os/actions/runners --jq '.runners[] | select(.name=="Voktors-Mini-Astra-Control") | {id,name,status,labels:[.labels[].name]}'`

Observed launchd rows:
- `1509  128  com.mediahub.astra.github-agent`
- `797   0    actions.runner.VlDMlNSh-mediahub-os.Voktors-Mini-Astra-Control`

GitHub Actions runner inventory returned:
- `mh-dev-01`: `offline`; labels `self-hosted`, `Linux`, `X64`, `mediahub-control`, `mh-dev-01`.
- `mh-dev-02`: `offline`; labels `self-hosted`, `Linux`, `X64`, `mediahub-provider`, `mh-dev-02`.
- `Voktors-Mini-Astra-Control`: `online`; runner ID 24; labels `self-hosted`, `macOS`, `ARM64`, `astra-control`.

## Finding

The third server has its own online GitHub Actions runner service, but that runner does **not** match the Linux/x64/`mediahub-control` qualification runner contract. The required `mh-dev-01` runner is explicitly `offline` in GitHub's API.

SentinelX also lists `mh-dev-01` as disabled in SentinelX (disabled by user at 2026-10-22T12:42:27+00:00). This is a separate SentinelX host-enrollment state; it is consistent with the target being unavailable, but it does not alone prove why the GitHub runner is offline.

## Disposition

- Third server identity and its local runner service: `OBSERVED`.
- Third-server runner online in GitHub: `CONFIRMED`, but only with macOS/ARM64/`astra-control` labels.
- Required `mh-dev-01` runner online: `NO — OFFLINE`.
- FreeLLMAPI qualification: `BLOCKED / NOT VERIFIED`.
- No labels changed; no runner service restarted; no other server was contacted or operated; no secret was read; no workflow dispatch, provider call, merge, deployment, qualification or acceptance occurred.

## Next step

Continue working only from `Voktors-Mini.Dlink`. Investigate the approved, existing mechanism for bringing the intended `mh-dev-01` Actions runner back online only if explicitly permitted by its governance. Do not relabel the third server's macOS runner as Linux/x64 and do not bypass the qualification workflow's runner/hostname assertions.

