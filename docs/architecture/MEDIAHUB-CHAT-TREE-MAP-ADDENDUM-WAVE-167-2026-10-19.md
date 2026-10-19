# MediaHub OS — Project map addendum, Wave 167 (2026-10-19)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

- Report: [Wave 167 A0 model-execution credential-isolation trace](../checkpoints/MEDIAHUB-A0-MODEL-EXECUTION-CREDENTIAL-ISOLATION-TRACE-WAVE-167-2026-10-19.md); report blob SHA is pinned in the continuation checkpoint after read-back.
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Current-main sources inspected: `astra_github_agent.py` blob `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`; `runtime/mediahub_runtime/autonomous_queue.py` blob `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`; `.github/workflows/astra-distributed-local-worker.yml` blob `f650f2416c19dc75b4a0eeec037661c0c6169910`; `ops/qualification/run_distributed_local_worker.py` blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`.
- Verified source path: self-hosted worker jobs request `contents: write` and checkout `persist-credentials: true`; the model worker runs in that checkout with Git/Python tools. The worker reads the FCC env file and merges its values into the Claude process environment, including `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY`.
- Classification: high-priority credential-boundary design finding. No token value was read; no real credential access/exfiltration, malicious task, online runner, or exploitation was observed/proven.
- Prompt path boundaries and post-hoc changed-file checks are not OS-level read/process isolation. The controller HMAC command envelope is not, by itself, an issuer-bound worker capability verifier.
- Proposed remediation: separate controller/publisher credentials from model execution; read-only checkout in model workspace; remove persistent Git credentials; keep FCC credentials behind a broker; enforce OS-level filesystem/network/process isolation; add signed task capability verification after governance resolution; independent negative tests and qualification.
- No runtime code, workflow, secret, host, queue, dependency, merge or deployment changes occurred.
- Wave 149 still records GOV-CAP-01…07 and R-06 open. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains gated.
- Next: owner-authorized containment decision and source-bound design for a credential-free model execution boundary; do not dispatch additional autonomous work to the affected self-hosted path until the boundary is independently reviewed.
