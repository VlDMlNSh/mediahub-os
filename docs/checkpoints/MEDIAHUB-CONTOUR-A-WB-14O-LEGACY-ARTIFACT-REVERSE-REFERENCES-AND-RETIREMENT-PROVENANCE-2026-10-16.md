# MediaHub OS — Contour A WB-14O: legacy artifact reverse references and retirement provenance

- Date: 2026-10-16
- Status: **BOUNDED READ-ONLY REFERENCE/PROVENANCE AUDIT / RECOMMENDATION ONLY / NO SOURCE RETIREMENT**
- Parent: WB-14N, Broad Legacy Control-Plane Scan and Branch-Drift Reconciliation.
- Repository: `VlDMlNSh/mediahub-os`
- Main HEAD/tree pinned for this pass: `ab36db009d034db8dca723691e23b331322287e7`; recursive tree has 800 entries / 723 blobs; `truncated=false`.
- Documentation branch HEAD before this report: `45fc0d39020171bb7bede69ec3cc72a7ff63eaf7`.
- Live compare `main...docs/mediahub-chat-tree-map-20261012`: **DIVERGED**, docs branch ahead 1469 / behind 4; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Permissions boundary observed: no main code/config edits, no workflow dispatch, no tests, no host/runtime access, no installation/deployment/migration, no merge/rebase/cherry-pick, no ref movement.

## 1. Executive result

This pass traced the current-source relationships and path histories for the storage migration workflow, the Linux/systemd ASTRA bootstrap unit, the related bootstrap script, the macOS/launchd launcher, and their operator-facing documentation. It also scanned eight additional workflow files for direct references to the two retired paths and related dispatch/launcher strings.

The strongest result is a **partial retirement on the documentation branch, not on main**:

- The documentation branch contains deletion commit `8d9dc210b1347cc254dfa745221c1d7857ee1019` titled “retire old-server-only storage migration workflow from clean-slate target”; its diff removes the workflow file only.
- It contains deletion commit `d27962f9c69e4a7a8f2c2cc17cbd16ee61410ea1` titled “retire old-host-bound Astra bootstrap service template”; its diff removes the systemd unit only.
- The same two files still exist on main at the pinned tree. The deletion commits are not reflected in main's current tree; no merge/integration was attempted.
- The macOS launchd plist and bootstrap helper remain on both refs. The plist still embeds old host identity and old user filesystem paths. The bootstrap documentation still instructs operators to install a systemd unit and launchd plist, creating a stale/inconsistent deployment narrative relative to the two path deletions on the documentation branch.
- The bootstrap shell helper is a dependency shared by the systemd and launchd templates and two operator documents. It defaults to `main` and applies `git reset --hard origin/$BRANCH` to an existing worktree. That helper must not be deleted or promoted automatically with the old unit; its target disposition is **SHARED-OR-UNKNOWN** pending contract-level review.

No evidence was obtained about whether either service is installed/running on any host or whether the migration workflow has actually executed. GitHub Actions execution state/history was not queried. Static code search remains unindexed/non-diagnostic, and this reverse-reference pass is deliberately bounded rather than complete repository closure.

## 2. Source pins and direct observations

### 2.1 Storage migration workflow

Main path: `.github/workflows/mediahub-one-time-storage-migration.yml`  
Current main blob SHA: `b0f71f515419067c6b1508dc073b2dbce4f2ca7b`.

Current content includes:

- a `push` trigger on `main` filtered to changes to the same workflow path;
- `contents: write`;
- a self-hosted runner and old-host identity checks (`mh-dev-01`, `mediahub-runner`);
- old filesystem paths `/home/mediahub/local-ai`, `/srv/mediahub/data/local-ai`, and `/home/mediahub/local-ai.root-backup`;
- `rm -rf` against the backup path;
- self-removal of the workflow from the checked-out repository, a commit, and `git push origin HEAD:main`.

This confirms a hazardous **checked-in definition**, not that it is active or executed. The result marker path `ops/storage/mediahub-storage-migration-result.md` has no path-specific commit entries in the inspected default-branch history query; this does not prove that the workflow never ran.

### 2.2 Storage workflow provenance

Path history on main shows:

- `1299d31a6e5c93bd45f7fb5e9c46a17466b9bb13` — “ops: add one-time storage migration transport” (2026-10-01);
- `bb787115609ea8634481a2d6736304306f3b5bc3` — “Astra controller hardening and GOLD exact-SHA binding” (2026-10-05);
- `8cb9cf64343b3dd8d550566080fc0652b627667e` — “fix(astra): align storage migration runner label” (2026-10-05).

On the documentation branch, path history contains:

- `8d9dc210b1347cc254dfa745221c1d7857ee1019` (2026-10-15), parent `3fb1a328b8f4227221507b5c55be0a8300a69221).
- Commit diff is a deletion of the 157-line workflow and contains no accompanying docs, contract, marker, or replacement implementation change.
- Direct commit: https://github.com/VlDMlNSh/mediahub-os/commit/8d9dc210b1347cc254dfa745221c1d7857ee1019

Classification: **RETIRE candidate / LEGACY-OPERATIONAL / HIGH RISK if triggered**. The clean-slate direction supports excluding this old-host migration from target planning; the branch-divergence and absent dependency closure mean no claim is made here that the current-main path is safely retired.

### 2.3 Linux/systemd ASTRA bootstrap service

Main path: `ops/systemd/mediahub-astra-github-bootstrap.service`  
Current main blob SHA: `bb88eb20bd2127c9c70a223bc07025ee9c150916`.

Source properties include:

- `ASTRA_NODE_ID=mh-dev-02`;
- `ASTRA_WORKTREE=/home/mediahub/astra-work`;
- `ASTRA_STATE_DIR=/var/lib/mediahub-astra`;
- an auto-start systemd unit with `Restart=on-failure`;
- an `ExecStart` that can clone the main branch to the old worktree and then run `ops/astra-github-bootstrap.sh`.

Service-path history on main includes `de714587d69a9915f8dbab63e0b6e9dc16143b6a` (add launcher manifests) and `1ac3924e3d47690b5f00cb981b24e0cdf33a1c68` (parameterize for mh-dev-02).

On the documentation branch, the path-specific deletion is:

- `d27962f9c69e4a7a8f2c2cc17cbd16ee61410ea1` — “retire old-host-bound Astra bootstrap service template” (2026-10-15), parent `5babc50cbf230c72fec2adbdc52c8897cc8ec564`.
- Commit diff removes only the 24-line systemd unit; no companion update to the operator-facing launcher manifest documentation is included.
- Direct commit: https://github.com/VlDMlNSh/mediahub-os/commit/d27962f9c69e4a7a8f2c2cc17cbd16ee61410ea1

Classification: **RETIRE candidate / LEGACY-OPERATIONAL**. Presence in Git does not establish host installation, enablement, or liveness.

### 2.4 Remaining launchd plist

Path: `ops/launchd/com.mediahub.astra.github-agent.plist`  
Blob SHA on main and the documentation branch: `d1d8aea99c2303c26e542a3d1c5e54b4596521d0`.

The plist has been present since `de714587d69a9915f8dbab63e0b6e9dc16143b6a` (2026-09-27). The inspected history contains only that add commit; no later path-specific retirement was found in the branch history query.

Source includes:

- executable path `/Users/voktor/astra-work/ops/astra-github-bootstrap.sh`;
- worktree `/Users/voktor/astra-work`;
- state path `/Users/voktor/astra-state`;
- `ASTRA_NODE_ID=Voktors-Mini.Dlink`;
- `RunAtLoad=true` and `KeepAlive=true`.

Classification: **LEGACY-OPERATIONAL / RETIRE candidate**. It is explicitly tied to the old Mac host and user-specific paths. This is independent of the retired systemd unit and remains present in the docs ref, so Linux-only retirement did not retire the old launcher family as a whole.

### 2.5 Bootstrap helper is shared, not proven retireable with its launchers

Path: `ops/astra-github-bootstrap.sh`  
Blob SHA: `5f36f35ea85f55e5f49af6d3dabb5e876fffa09b`.

The helper is referenced by:

- the old systemd unit;
- the old launchd plist;
- `docs/operations/ASTRA-GITHUB-TRANSPORT-BOOTSTRAP.md`;
- `docs/operations/ASTRA-TRANSPORT-LAUNCHER-MANIFESTS.md`.

Source defaults include the repository `VlDMlNSh/mediahub-os`, branch `main`, and worktree `$HOME/astra-work`. If a Git worktree already exists, it fetches the selected branch, resets the branch to `origin/$BRANCH`, then uses `git reset --hard origin/$BRANCH` and executes the agent from that worktree.

That is source-level evidence of synchronization behavior and worktree overwrite potential; it is not evidence of any live side effect in this audit. Since both launcher templates and two operator docs refer to it, it is not safely classifiable as old-host-exclusive based only on the launcher names.

Classification: **SHARED-OR-UNKNOWN / do not delete automatically**. Extract any desired source-synchronization, executable-path identity, and health-evidence requirements into a reviewed target contract; do not treat the current shell script or its main-branch reset behavior as target-approved implementation.

### 2.6 Operator-facing documentation contradiction

- `docs/operations/ASTRA-GITHUB-TRANSPORT-BOOTSTRAP.md`, SHA `e87cf363dc6fa0c88207ab9fbb6b72f6dcb75d28`, says a persistent GitHub Transport process must be launched through the bootstrap helper or equivalent.
- `docs/operations/ASTRA-TRANSPORT-LAUNCHER-MANIFESTS.md`, SHA `d25d413abce67a01c402394a15304c5398b7ad53`, tells operators to install a systemd unit and a launchd plist, but does not name the deleted systemd path. It also warns that the manifests are deployment artifacts and committing them does not itself change a live node.

Both documents are still present on the documentation branch after the path deletion commits. Therefore, the docs branch contains a **documentation/source consistency gap**: a generic Linux install instruction remains although its systemd template was removed; the still-present macOS template remains old-host-bound; the generic bootstrap helper remains referenced but is not a qualified greenfield target component.

The documents may contain useful requirements (single synchronized source tree, executable path identity, health evidence). Preserve those semantics only after explicit target-contract review; do not retain the old host/path instructions as deployment steps.

## 3. Bounded reverse-reference scan

The following eight main-branch workflow files were fetched and scanned for the two exact artifact paths, bootstrap-helper/path strings, migration-marker name, and workflow-call/dispatch triggers:

| Path | Blob SHA | Relevant result |
|---|---|---|
| `.github/workflows/astra-autonomous-supervisor.yml` | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | Old mh-dev-01 runner and command signer workflow; no direct path reference to the storage workflow or systemd service was found in this file. |
| `.github/workflows/astra-chat-control.yml` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Uses `createWorkflowDispatch` for legacy node routes; no direct path reference to the two retired artifacts was found. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Defines old node-specific worker jobs; no direct path reference to either retired artifact was found. |
| `.github/workflows/astra-node-result-publication.yml` | `087a373fe113d11a81be4d349e4c3d330a22f33c` | Has a `workflow_run` trigger and publishes results for mh-dev-01; no direct path reference to the two retired artifacts was found. |
| `.github/workflows/astra-gold-unified-qualification.yml` | `e965a648718502d41d62518a6164b03a99bc403c` | Dispatchable qualification path, fixed legacy node and signer; no direct path reference to either retired artifact was found. |
| `.github/workflows/astra-g4-115-qualification.yml` | `1edfd7f574cd50cf9004d8d2e826725167fa46c8` | Old mh-dev-01/mh-dev-02 and Mac host checks; no direct path reference to either retired artifact was found. |
| `.github/workflows/astra-local-claude-qualification.yml` | `7f7dc2d65481e2cc80a1db94b41a1e60ed117ffd` | Has `workflow_call` and `workflow_dispatch`, old node binding; no direct path reference to either retired artifact was found. |
| `.github/workflows/mediahub-bridge.yml` | `6f482199af32881f42c2c418221aec66530c4b71` | Dispatchable, bound to the old mh-dev-01 runner label; no direct path reference to either retired artifact was found. |

This table is an eight-file bounded sample, not a repository-wide proof that no dynamic caller exists. The migration workflow itself has a self-path trigger and its internal self-removal/commit/push behavior. No workflow was invoked.

GitHub Code Search remains unindexed/non-diagnostic. No complete import graph, trigger-graph, or all-file literal search is claimed.

## 4. Cross-branch disposition matrix

| Artifact | Main state | Documentation-ref state | Classification | Recommendation |
|---|---|---|---|---|
| `.github/workflows/mediahub-one-time-storage-migration.yml` | Present | Deleted by `8d9dc21` | LEGACY-OPERATIONAL / RETIRE candidate / high risk if triggered | Keep excluded from the target design. Do not invoke. Review the deletion in a purpose-built, narrowly scoped source-change proposal; do not integrate the divergent branch wholesale. |
| `ops/systemd/mediahub-astra-github-bootstrap.service` | Present | Deleted by `d27962f` | LEGACY-OPERATIONAL / RETIRE candidate | Keep out of target configuration. Treat the existing docs instruction as stale until reviewed. No host-state assumptions. |
| `ops/launchd/com.mediahub.astra.github-agent.plist` | Present | Present | LEGACY-OPERATIONAL / RETIRE candidate | Include in the same launcher-family disposition; do not leave as target deployment template by default. |
| `ops/astra-github-bootstrap.sh` | Present | Present | SHARED-OR-UNKNOWN | Preserve pending decision on whether GitHub transport remains in Contour A and what safe synchronization contract replaces/retains the hard-reset behavior. |
| `docs/operations/ASTRA-GITHUB-TRANSPORT-BOOTSTRAP.md` | Present | Present | Historical/contract candidate | Retain provenance; reassess its requirements and explicitly mark old deployment mechanics as non-target before using it as an installation instruction. |
| `docs/operations/ASTRA-TRANSPORT-LAUNCHER-MANIFESTS.md` | Present | Present | Stale legacy operations guide / contract candidate | Reconcile its systemd/launchd rollout instructions against the accepted greenfield lifecycle and component contract. |
| `astra_github_agent.py`, command signer, old node registry and related evidence/contracts | Present | Present in reviewed history | SHARED-OR-UNKNOWN by component | Do not infer retireability from launcher deletions; map caller/security/evidence semantics separately. |

## 5. Branch and historical evidence

- Current main tree: `ab36db009d034db8dca723691e23b331322287e7`.
- Current documentation-ref HEAD before this report: `45fc0d39020171bb7bede69ec3cc72a7ff63eaf7`.
- Branch comparison: `DIVERGED`, docs ref 1469 ahead / 4 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Both removal commits are found in the path history queried against the documentation branch. The files remain in main's tree, confirming the removals are not reflected in main.
- No merge, rebase, cherry-pick, branch movement, or main edit was performed.

## 6. Safety and confidence boundaries

- Read-only GitHub source/history inspection only.
- No tests or qualification, no workflow dispatch, no credentials or provider/model calls, no host/runtime inspection, no install, no infrastructure edits, no deployment/migration, and no file deletion.
- Workflow run status, service enablement/liveness, live filesystem state and whether the storage workflow has ever successfully run are **UNKNOWN**.
- The direct-reference scan is bounded. “No literal match in this set” must not be restated as “unused”.
- The retirement commits are evidence of reviewed source deletion on the documentation branch, not evidence of independent runtime shutdown or target acceptance.

## 7. Next justified step: WB-14P

Perform a controlled launcher-family and bootstrap-contract reconciliation:

1. Inventory the remaining node-specific launchd/systemd templates, launcher docs, `ops/astra-github-bootstrap.sh`, `astra_github_agent.py`, old node identity maps, and health-evidence semantics.
2. Split required abstract behavior (if any) from host-bound operational values and old execution/security code.
3. Draft a recommendation-only disposition and replacement-contract matrix, with explicit UNKNOWN rows where reverse reference closure is not provable.
4. Keep all source changes out of main until a small, separately reviewable proposal can be reconciled with branch divergence and source contracts.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
