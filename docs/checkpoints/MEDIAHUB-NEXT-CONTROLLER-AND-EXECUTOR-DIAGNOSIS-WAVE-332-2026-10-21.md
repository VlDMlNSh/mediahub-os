# Wave 332 — controller and executor diagnosis (2026-10-21)

Repository: https://github.com/VlDMlNSh/mediahub-os  
Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Result

Gemini Agents 1–3: NOT RUN. Claude-fcc-Ollama: NOT RUN. agent-browser: NOT RUN. E2E/failover: NOT RUN. Overall readiness: NOT QUALIFIED / NOT ACCEPTED. No workflow dispatch, issue comment, secret read, policy change, install, merge or deployment occurred.

## GitHub evidence

- Main HEAD: 5cac2f27685c88e5e5e391fcf315d07fc16c6a6b; branch metadata says protected=false.
- Controller blob: 9453403bba899a2400ee3fb874d32badd034c704.
- Agent 1 blob: 155a02159912ca371e6f826c51325ca269857aad.
- Agent 2 blob: fff1820a6b97d379b23674f36bd62227b7d4dec2.
- Agent 3 blob: 781df56e8aa7c75ba453c08378611857862b2e44.
- PR #437 remains open/draft at e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14; formal reviews=0, exact-head statuses=none reported.
- Controller run #39670089739 had four skipped jobs and no artifacts. Runs #39669722103 and #39669477347 were also skipped. No child run IDs or artifact digests exist.

## Trigger and credential findings

The source accepts a launch only for (a) trusted workflow_dispatch with mode=agents and confirm=yes, or (b) an exact /next comment on non-PR Issue #301 from an OWNER. The batch variable must resolve to true. A run name containing next-comment-<id> alone does not mean the comment body matched. The available GitHub connector exposes no workflow_dispatch operation; posting /next to Issue #301 would be a potentially live launch and was not done while gates remain open.

The workflows reference exact ASCII secret MEDIAHUB_DISPATCH_HMAC_KEY. The spellings MEDIAHUB_DISPATCH_НМАС_KEY (Cyrillic lookalikes) and MEDIAHUB_DISPATCH_NMAC_KEY are different identifiers. Effective Actions secret/variable presence and MEDIAHUB_GITHUB_TOKEN scope remain NOT VERIFIED; no secret values were read.

Issue #301 orders issuer/ingress/lease/cancel/recovery and R-06 audit/privacy gates before dispatch. No dispatch is authorized merely by the chat request. Required governance, independent review, exact-head CI and trusted-main no-secret probe remain open.

## SentinelX / Voktors-Mini

- Host: Voktors-Mini.Dlink, host_5f7264034bdf0b51, macOS kernel 23.6.0 arm64; only operational host in SentinelX.
- Read-only filesystem check found /opt/homebrew/bin/ollama, /usr/local/bin/node and /usr/local/bin/npm; agent-browser and claude were absent at checked standard paths.
- Subsequent SentinelX capability/state/ping calls returned disconnected/read-loop-ended; the version probe timed out. Ollama binary presence does not prove service health.
- Last successful allowlist snapshot excluded agent-browser, claude, ollama, fcc-claude and npx. Current allowlist could not be re-read. No allowlist change, wrapper, package install or browser action was attempted.
- agent-browser skill requires running `agent-browser skills get core` after authorized installation; this remains NOT RUN.

## Next bounded step

1. Close PR #437 exact-head CI and independent review; establish main branch governance and required checks.
2. Verify exact ASCII HMAC secret name, provider keys, batch variable and least-privilege token scope through metadata-only checks; never disclose values.
3. Record a trusted-main no-secret probe before considering a three-child batch against one immutable SHA.
4. Recover SentinelX, re-read current allowlist, then authorize and qualify agent-browser and a free-only Claude-FCC/Ollama route separately.

No dispatch, provider call, qualification or acceptance is claimed.
