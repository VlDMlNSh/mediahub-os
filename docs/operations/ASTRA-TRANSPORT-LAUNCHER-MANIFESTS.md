# Astra Transport launcher manifests

These manifests define the canonical process-manager boundary for persistent GitHub Transport.

## Linux/systemd

Install the systemd unit as the node's Astra service definition and set the node-specific
environment values before enabling it. The service must invoke
`ops/astra-github-bootstrap.sh`, never a copied `astra_github_agent.py`.

## macOS/launchd

Install the plist under the user's LaunchAgents directory with the node-specific worktree
and state paths. It invokes the same canonical bootstrap.

## Rollout contract

1. Review the manifest for the target node.
2. Stop using the legacy launcher only as part of a controlled node migration.
3. Start the canonical launcher.
4. Request a fresh read-only health command.
5. Require `transport_version`, `agent_source_sha`, `agent_path`, and `worktree`.
6. Compare `agent_source_sha` with the SHA of the canonical agent in the synchronized worktree.
7. Only then qualify the node for further execution.

These manifests are deployment artifacts; committing them does not itself change a live node.
