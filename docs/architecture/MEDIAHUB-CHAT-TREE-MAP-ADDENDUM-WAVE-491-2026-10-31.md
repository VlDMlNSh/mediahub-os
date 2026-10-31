# Wave 491 — Dev Container toolchain inventory

- [Wave 491 inventory and implementation gate](../checkpoints/MEDIAHUB-DEVCONTAINER-TOOLCHAIN-INVENTORY-WAVE-491-2026-10-31.md)
- Main snapshot: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Main CI uses Python 3.12 for core Astra, Mesh/P2P, Agent Fabric and Gemini contract validation; a specialized Claude FCC worker uses Python 3.14.7.
- `requirements-dev.txt` declares only `PyYAML>=6.0` and `pytest>=8.0`, with no transitive lock. Astra/Mesh tests additionally install apt `transmission-cli`; Gemini workflow contract checks use Go/actionlint v1.7.7.
- Disposition: Dev Container config deliberately NOT CREATED until dependency locking, immutable base-image digest/provenance, OS/package baseline, extension allowlist and optional test-tools profile are resolved.
- No code/configuration, secret, Codespaces, provider, agent-dispatch, host, merge or deployment action occurred.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
