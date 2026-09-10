# W04C — FCM + ECC/Codex/Claude checkpoint

Date: 2026-09-10
Branch: `engineering/mh21-sandbox-lifecycle-20260910`

## Repository state

- HEAD at prior checkpoint: `98b9607a2bfcaecacf253db2cd47a82d1f524cff`
- TREE at prior checkpoint: `56a166d27b86634679448b7758568c3614325e9e`
- Working tree was clean before this checkpoint wave.
- R4 immutable baseline remains unchanged.

## FCM qualification

- `free-coding-models` v0.5.90 is installed for catalog intelligence.
- FCM is discovery/benchmark only; it is not MediaHub routing authority.
- FCM Router is disabled.
- FCM telemetry is disabled.
- OpenRouter is explicitly disabled in FCM local configuration.
- No provider secret was added or exposed.
## ECC / Codex / Claude

- ECC subset is present: explorer, reviewer, docs-researcher and verification-loop.
- ECC agent definitions were copied into isolated `CODEX_HOME`.
- Codex CLI: 0.151.0.
- Claude Code: 2.1.263.
- Claude native smoke reached the CLI and failed closed because the CLI is not logged in.
- Codex native smoke reached execution and failed closed because `CONTINUUM_API_KEY` is absent.
- No credential was fabricated, printed or stored.

## OmniRoute

- OmniRoute remains NOT QUALIFIED.
- Previous installation attempts were inconsistent/partial and executable validation failed.
- Runtime activation was not performed.

## Autonomous development

- Local llama.cpp remains the canonical local AI tier.
- Privileged system-service operations remain blocked by authorization.
- No privilege bypass, force-push, history rewrite, destructive reset or production cutover was performed.

## Required next wave

1. Build a MediaHub-native FCM catalog adapter.
2. Apply denylist filtering before Model Registry admission.
3. Keep every external model at CANDIDATE until live evidence exists.
4. Run targeted and full security/quality verification after changes.
5. Keep OpenRouter DENY and FCM Router non-authoritative.
6. Retry native Codex only after legitimate provider credentials exist.
7. Retry native Claude only after legitimate login/credential exists.
