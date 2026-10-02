# Astra GitHub Transport bootstrap contract

The persistent GitHub Transport process must be launched through `ops/astra-github-bootstrap.sh` (or an equivalent launcher that implements the same contract).

## Contract

1. The launcher clones or fetches the canonical repository.
2. It checks out `origin/main` into the configured worktree.
3. It starts `astra_github_agent.py` from that same synchronized worktree.
4. The agent may then self-reexec when its source changes.
5. Health output must expose the transport version and running agent source SHA.
6. A deployment is not considered updated until a fresh GitHub health result reports the expected source SHA.

## Why this is required

A persistent process started from a separately installed copy can continue to poll GitHub while never executing the current canonical agent. In that state, GitHub command delivery can appear healthy while code updates and self-reexec are ineffective.

The bootstrap therefore makes the executable path and the synchronized source tree one boundary.

## Node-specific launcher paths

Existing nodes may use different process managers and filesystem paths. The process-manager entry point should invoke this bootstrap with the node's `ASTRA_WORKTREE` and other environment settings rather than pinning a copied `astra_github_agent.py`.

Do not perform a destructive replacement of a live process as part of routine GitHub task execution. Rollout should be controlled per node and verified with the health evidence contract above.


## Cluster coordination requirement

The node-local `ASTRA_STATE_DIR` or `ASTRA_QUEUE_STATE_DIR` is not, by itself, evidence of a cluster-wide claim authority. A qualification run involving multiple physical nodes MUST provide fresh coordination attestation showing that all participating nodes use the same declared coordination authority and that the authority enforces the canonical limit of two active autonomous claims.

Separate local state directories MUST be treated as separate coordination domains unless an external shared-state mechanism is explicitly verified. GitHub transport publication is not a substitute for atomic claim reservation.

G5 MUST remain BLOCKED until this attestation is present. No configuration value or matching path name may be treated as proof of shared storage.

## Result publication recovery evidence

For G6, a publication-recovery test MUST reconcile the immutable result identity with the remote per-node branch tip and the local processed-command state after an induced interruption. A successful push alone is insufficient evidence of complete recovery.
