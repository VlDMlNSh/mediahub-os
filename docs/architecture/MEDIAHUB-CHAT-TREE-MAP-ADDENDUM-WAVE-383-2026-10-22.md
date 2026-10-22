# MediaHub OS — chat tree map addendum, Wave 383

Date: 2026-10-22

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

Report: [Wave 383 — GitHub-hosted Astra control-plane boundary](../checkpoints/MEDIAHUB-GITHUB-HOSTED-ASTRA-CONTROL-PLANE-WAVE-383-2026-10-22.md)

- Added a least-privilege GitHub-hosted workflow to run deterministic queue transition tests on `ubuntu-latest`; no secrets or worker dispatch are used.
- Documented desired separation: Astra A0 issuer/ingress; GitHub-hosted supervisor; approved cloud-agent controller; third-server-only local executor; separate Jarvis; Product State Authority remains canonical mutation authority.
- Current `runtime/mediahub_runtime/autonomous_queue.py` still binds scheduling to a permanent executor pool containing mh-dev-01 and mh-dev-02. It is not yet a server-independent control plane.
- The existing Gemini controller does not establish that arbitrary A0 task payloads can be routed to child agents. Do not bypass it or infer task-specific dispatch support.
- Workflow CI, production queue persistence, task-specific cloud routing, local worker protocol and overall acceptance remain NOT VERIFIED / NOT IMPLEMENTED as applicable.
