# MediaHub Chat Tree Map Addendum — Wave 509 (2026-11-02)

- Status: **OWNER-CLARIFIED TERMINOLOGY / DOCUMENTATION PROPOSED / NOT ACCEPTED**
- Owner source: [Issue #301 Wave338 clarification](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6326925941); [Wave509 reaffirmation](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6568555691).
- Detailed report: [Wave509 Ollama terminology supersession](../checkpoints/MEDIAHUB-OLLAMA-TERMINOLOGY-SUPERSESSION-WAVE-509-2026-11-02.md).
- Master continuation prompt: [Wave509 master prompt](../checkpoints/MEDIAHUB-MASTER-CONTINUATION-PROMPT-WAVE-509-2026-11-02.md).
- Canonical map remains branch-governed: docs/mediahub-chat-tree-map-20261012.

## Authoritative naming

**Ollama** is the local inference runtime/API server. A model tag (e.g. llama3.2:3b) is the model. Voktors-Mini.Dlink is a physical Mac mini 2018 host. These identities must remain distinct. The legacy term “Alamo/Allamo” is not a separate service, endpoint, hostname, host or executor. Wave364/365 wording that treated it as a distinct host is superseded by the owner clarification from Wave338.

## Affected records and changes

- Corrected active Bootstrap routing guidance; removed the Alamo/server-3 identity and separated local Ollama route from actual host verification.
- Prepended this supersession notice to the canonical map, continuation checkpoint and Master Roadmap.
- Updated architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md in PR #610 to define Ollama/runtime/model/host identities separately.
- Annotated Wave364/365/369 and WB14/Jarvis crosswalk historical records; old assertions remain visible as provenance, not current topology.
- Renamed the PR610 runner and test to .github/workflows/mediahub-ollama-fcc-claude-runner.yml and tests/test_mediahub_ollama_fcc_runner_contract.py.
- Renamed runner job to ollama-local-fcc-claude and added a regression guard against the legacy alias.
- Updated Issue #296 and current PR descriptions to use canonical Ollama naming.

## Runtime topology target

1. Runner 1: local Ollama inference candidate + FCC/ECC + Claude Code.
2. Runner 2: separate cloud-agent pool; Gemini remains exclusively controller-routed.
3. GitHub-hosted Ubuntu jobs are ephemeral; do not call them persistent VMs.
4. Physical host location does not prove inference locality. Verify Ollama endpoint, model identity, FCC upstream, auth/cost class and network egress.
5. Local-only route must fail closed: no Anthropic API, paid proxy, other cloud provider, or silent fallback.

## Evidence state

- Runner refactor is on PR #610 branch only; exact final-head CI and independent review are NOT VERIFIED.
- Documentation work is on PR #620 draft; exact-head CI/review NOT VERIFIED.
- No Gemini dispatch, no provider/model call, no secret read, no local Claude task, no merge, no deployment.
- SentinelX currently lists one operational host (Voktors-Mini.Dlink, host_5f7264034bdf0b51), Free plan one active slot / zero available; two other hosts disabled.
- Ollama live runtime/model/FCC/Claude execution remains NOT RUN / NOT QUALIFIED.
- Contour A NOT ACCEPTED; Contour B GATED.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
