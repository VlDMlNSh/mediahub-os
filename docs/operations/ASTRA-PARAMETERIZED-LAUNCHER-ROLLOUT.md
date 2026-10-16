# Parameterized launcher rollout

The canonical systemd launcher is intentionally split into a reusable template and
node-specific deployment values.

## Template

Use `ops/systemd/mediahub-astra-github-bootstrap.template.service`.

Required node-specific values:

- `ASTRA_NODE_ID`
- `ASTRA_WORKTREE`
- `ASTRA_STATE_DIR`
- `User` / `Group` if the node differs from the standard Linux account

The template pins the canonical repository, remote, and `main` branch and invokes
the bootstrap from the synchronized worktree.

## Controlled rollout

For each Linux node:

1. Create the node-specific systemd unit from the template.
2. Ensure the service manager, not an old copied agent, owns the long-running process.
3. Start the canonical launcher during a controlled migration window.
4. Issue a fresh read-only GitHub health command.
5. Require `transport_version=self-reexec-v1`.
6. Require `agent_path` to be inside the configured canonical worktree.
7. Compare `agent_source_sha` with the SHA of `astra_github_agent.py` in that
   synchronized worktree.
8. Only after those checks pass, proceed to runtime and scheduler qualification.

Committing this template does not migrate any live node. A live process-manager
change remains an explicit deployment boundary.

## Node mapping

Current known Linux mappings:

- `mh-dev-01`: `/home/mediahub/astra-work`,
  `/var/lib/mediahub-astra`
- `mh-dev-02`: use its existing Astra worktree/state paths after verifying them
  during controlled rollout.

Do not infer that a node is migrated from repository state alone.
