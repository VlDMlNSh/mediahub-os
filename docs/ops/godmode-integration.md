# MediaHub Godmode integration

MediaHub uses the upstream Godmode coding-agent discipline as a bounded engineering layer.

- Upstream: `https://github.com/arbazkhan971/godmode`
- Pinned commit: `18bfc31d669804856ba232f04cdbd172afbdc379`
- Native agent definitions: `.codex/agents/godmode_*.toml`
- OpenRouter profile: `.codex/godmode-openrouter.toml`
- Launcher: `ops/ai/godmode_openrouter_codex.sh`

## Boundary

Godmode agents are subordinate engineering workers. They must not mutate State Authority, release or production state, obtain or persist secrets, bypass verification, or merge changes.

## Activation

The launcher requires `OPENROUTER_API_KEY` to be supplied out-of-band. It sets the OpenAI-compatible endpoint to OpenRouter and invokes the installed Codex CLI. The repository never stores the credential.
