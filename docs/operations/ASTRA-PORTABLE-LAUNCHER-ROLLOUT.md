# Portable launcher rollout

The canonical process-manager boundary is intentionally explicit. Install the parameterized systemd template on each Linux node and set ASTRA_NODE_ID to the exact node identity.

Required identities:

- mh-dev-01
- mh-dev-02

The macOS node uses ops/launchd/com.mediahub.astra.github-agent.plist and must retain the same canonical repo and bootstrap contract.

After installation, qualification must begin with a fresh health operation. The health result is accepted only when transport_version, agent_source_sha, agent_path, and worktree match the canonical synchronized worktree. Do not infer migration from the existence of the unit file.

This repository change does not install or restart services on live machines.
