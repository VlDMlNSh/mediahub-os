# MediaHub OS — Contour A WB-14P: launcher-family and bootstrap-contract reconciliation

- Date: 2026-10-16
- Status: **BOUNDED SOURCE RECONCILIATION / CONTRACT GAPS FOUND / RECOMMENDATION ONLY / NO SOURCE OR RUNTIME CHANGES**
- Parent: WB-14O Legacy Artifact Reverse-References and Retirement Provenance.
- Main HEAD/tree at pass start: `ab36db009d034db8dca723691e23b331322287e7`; recursive tree 800 entries / 723 blobs, `truncated=false`.
- Documentation branch HEAD at pass start: `fe601dc26da08a11f0239027606f018806d1c2c3`.
- Live comparison `main...docs/mediahub-chat-tree-map-20261012`: **DIVERGED**, docs branch ahead 1473 / behind 4; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Boundary: no tests, workflow dispatch, credentials, provider/model calls, host/runtime inspection, installation, infrastructure, deployment, migration, source-code changes, branch integration, or ref movement.

## 1. Executive finding

The launcher family is not a single coherent implementation. The repository contains at least two different generations of launch templates plus a shared bootstrap helper:

1. `deploy/` templates start `astra_github_agent.py` directly from `/opt/mediahub/astra`.
2. `ops/` templates start the agent through `ops/astra-github-bootstrap.sh`, but use fixed old host identities and paths.
3. The documentation describes the helper-driven launch path as canonical, while the direct-execution templates remain in both main and the documentation branch.
4. The old systemd template was deleted only on the documentation branch, but a different old systemd template remains under `deploy/` on both refs. Thus the deletion did not remove the complete checked-in systemd launch surface.
5. The shared helper and agent have useful engineering-control concepts, but the agent couples transport polling, old-node HMAC key selection, command admission, broad operation dispatch, claim/journal behavior, and result publication. They are not a clean, already-qualified greenfield Contour A controller.
6. The health evidence verifier documents “fresh health” as a precondition but does not itself enforce freshness, correlate a health result to a requested command/nonce, require a readiness status, or compare the returned node ID to an explicitly supplied expected node ID. That is a contract-verification gap in the current static checker.

**Recommendation:** do not deploy or inherit any existing launcher template for the clean-slate system. Harvest useful abstract requirements only after contract review. Keep host-bound launch files classified as RETIRE candidates; keep the shared bootstrap helper and agent as SHARED-OR-UNKNOWN/HISTORICAL until the owner settles whether Contour A needs a GitHub-polling adapter at all and the exact command, identity, workspace, result and health contracts are approved.

The target architecture continues to separate Jarvis mission coordination, ASTRA A0 engineering lifecycle, and MediaHub Product State Authority. Executors/transports have no implied product-state authority. None of the legacy files is promoted to target acceptance by this report.

## 2. Launcher inventory and incompatibilities

### 2.1 `deploy/mediahub-astra-github.service`

- Main and docs ref blob SHA: `e1962e4afe5db7ac1fcb901344d9f88205de0689`.
- Path history on main includes `6f0e348c3b3a7b8e3c101360b80fcd36ca46d5fd` (2026-09-27) and `5dc4569732e76a49d2390b92852d47b6a3b4bd39` (2026-10-08).
- Directly launches `/usr/bin/python3 /opt/mediahub/astra/astra_github_agent.py`, with `WorkingDirectory=/opt/mediahub/astra` and `PYTHONPATH=/opt/mediahub/astra/runtime:/opt/mediahub/astra`. It uses a separate optional environment file `/etc/mediahub/astra-github.env` not present in the repository, and allows writes to `/var/lib/mediahub-astra` and `/opt/mediahub/astra`.
- It does not invoke the documented bootstrap helper.

**Static mismatch:** the checked-in agent source defaults `ASTRA_WORKTREE`/its operational `ROOT` to `/opt/mediahub/astra-worktree` if that variable is not set, distinct from the service's executable and working directory `/opt/mediahub/astra`. The optional host environment file could override the variable, but its actual contents were not available or inspected. Therefore this is a configuration conflict/unknown, not a claim that a live service necessarily fails.

Classification: **LEGACY-OPERATIONAL / RETIRE CANDIDATE** pending full launcher-family disposition.

### 2.2 `deploy/com.mediahub.astra.github-agent.plist`

- Main and docs ref blob SHA: `2cca029b502fd911ec38272871c823a8717ed8fd`.
- Path history: `2657304749f8855e1f02c207ecae26f48b742d65` (2026-09-27).
- Directly launches `/usr/bin/python3 /opt/mediahub/astra/astra_github_agent.py`, with `RunAtLoad=true` and `KeepAlive=true`. It sets `ASTRA_GITHUB_REPO` but does not set `ASTRA_WORKTREE`, `ASTRA_STATE_DIR`, or a target node identity in the checked-in plist.
- As the agent's default `ROOT` is `/opt/mediahub/astra-worktree`, the direct executable path and default operational worktree diverge unless external environment or launch context supplies the missing value.

Classification: **LEGACY-OPERATIONAL / RETIRE CANDIDATE**; no deployment or live process was inspected.

### 2.3 `ops/systemd/mediahub-astra-github-bootstrap.service`

- Main blob SHA: `bb88eb20bd2127c9c70a223bc07025ee9c150916`.
- Present on main; absent from the documentation branch after commit `d27962f9c69e4a7a8f2c2cc17cbd16ee61410ea1`.
- Hard-codes `ASTRA_NODE_ID=mh-dev-02`, `/home/mediahub/astra-work`, `/var/lib/mediahub-astra`, and starts the bootstrap script from that old worktree.

Classification: **LEGACY-OPERATIONAL / RETIRE CANDIDATE**. This branch-local deletion is not live-host shutdown evidence and is not in main.

### 2.4 `ops/launchd/com.mediahub.astra.github-agent.plist`

- Main and docs ref blob SHA: `d1d8aea99c2303c26e542a3d1c5e54b4596521d0`.
- Hard-codes `/Users/voktor/astra-work`, `/Users/voktor/astra-state`, and `ASTRA_NODE_ID=Voktors-Mini.Dlink`, with launch-at-load and keep-alive behavior.
- Runs through the bootstrap helper, but remains tied to an old host identity and user-specific paths on both refs.

Classification: **LEGACY-OPERATIONAL / RETIRE CANDIDATE**. Preserve only the historical evidence needed for provenance; do not treat as a target launch configuration.

### 2.5 Separate old mesh service

- `ops/systemd/mediahub-mesh.service` SHA: `bfa8b075229385ac14b8ba34dccad84275d1c474`.
- `ops/systemd/mediahub-mesh.env.example` SHA: `4ee40c945cbbd33fe38d603fe26d1a5de634526b`.
- The service uses `WorkingDirectory=/home/mediahub/astra-work` and reads `/etc/mediahub/node-profile.env` and `/etc/mediahub/mediahub-mesh.env`, external files not inspected. The checked-in example binds `MEDIAHUB_MESH_NODE_ID=mh-dev-02`.
- This is not the ASTRA transport launcher itself, but it is an adjacent service template tied to the same old worktree. It needs a separate source/dependency review before any target use.

Classification: **LEGACY-OPERATIONAL / REUSE-UNKNOWN**. Do not equate checked-in service definitions with installed/running services.

## 3. Bootstrap helper and ASTRA agent are compound control components

### 3.1 Bootstrap helper

- `ops/astra-github-bootstrap.sh` SHA: `5f36f35ea85f55e5f49af6d3dabb5e876fffa09b`, same across the two refs.
- Its stated contract is to synchronize `main` and execute the agent from the synchronized worktree.
- It defaults to repository `VlDMlNSh/mediahub-os`, branch `main`, and worktree `$HOME/astra-work`.
- If a worktree exists, it fetches the configured branch, resets the local branch to `origin/$BRANCH`, and executes `git reset --hard origin/$BRANCH`. There is no dirty-worktree preflight in this script before the reset.
- It is referenced by the old ops systemd unit, the old ops launchd plist, and both operator-facing bootstrap/launcher documents.

Disposition: **SHARED-OR-UNKNOWN**. Do not delete it merely because one systemd template was removed. Its synchronization and executable-path identity concepts can be requirements for review; its main-branch hard-reset implementation is not automatically accepted as the target mechanism.

### 3.2 `astra_github_agent.py`

- SHA on both refs: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`, 60,305 bytes / 926 lines.
- It is more than an inert transport: it polls the command record, authenticates signed commands, checks command schema/target commit SHA and idempotency, manages claims for some operations, executes an operation dispatcher, and publishes results to `astra-node/<node-id>` result branches.
- It combines process synchronization/self-reexec, node identity, node-specific HMAC environment key mapping, command admission, execution and evidence publication. The embedded key map explicitly names `mh-dev-01`, `mh-dev-02`, and `Voktors-Mac-mini.local`.
- Its allowed operation set includes health/reporting, research/document/coding flows, qualification/evidence paths and autonomous queue/mission operations. This is a wide execution/control surface, not a minimal health-only agent.
- Its normal loop synchronizes the worktree to `origin/main` and may re-exec the agent if the checked-in file's SHA-256 differs from the running file's SHA. Commands separately pin `target_sha` to the current Git HEAD.
- The agent source is identical on the two refs, but this proves source identity only, not that it is deployed, qualified or approved for the new target.

Disposition: **SHARED-OR-UNKNOWN + LEGACY-NODE COUPLING**. Do not promote the entire script into the new Contour A architecture as-is. First extract and govern the requirements for command identity/signature, issuer/key lifecycle, target revision binding, scoped paths/actions, idempotency, task/claim lifecycle, result provenance and health identity. The replacement might be a new adapter or an explicitly requalified implementation, subject to owner decision.

### 3.3 Command signer

- `ops/control/sign_command.py` SHA: `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`.
- It derives required HMAC environment variable names from a static legacy node-ID mapping and fails closed if the selected key is absent. This behavior is a real security seam but its current identity mapping is not a new-target registration contract.

Disposition: retain the security requirement, not the old identity vocabulary by implication. New issuer/principal/receiver identities and key provisioning/rotation/revocation must be defined by the accepted security/capability contracts before implementation.

## 4. Health-evidence contract gap

Relevant source pins:

- `ops/qualification/verify_transport_health.py` — `55dca778bcc1019ba2e2bd93f877ce15442b5bab`.
- `docs/qualification/ASTRA-TRANSPORT-HEALTH-GATE.md` — `f577be6e6643bf8250bf1bebbdf5a87b55e90cb2`.
- `evidence/transport-health-current.json` — `c1d63bb5fa5b4d6be0763eff2893fb157324999a`.
- `qualification/transport-gate-2026-09-27.json` — `7ea00906db3774468e3a320fd516a9d5e7084696`.

The document says the gate must use a fresh result and that PASS proves only the transport identity contract. The code requires the node ID to be non-empty, a hard-coded transport version, agent path/worktree identity and a matching hash of the local agent file. However:

- there is no required capture timestamp or maximum-age check;
- there is no request/command ID or nonce correlation to the health request;
- it does not require `status=ready`;
- it does not accept an explicit expected node ID to compare with the returned `node_id`;
- it does not check a target commit SHA or a target capability/admission state.

Consequently, **freshness is a caller precondition, not a machine-enforced property of this verifier**, and a matching but stale health payload could satisfy the listed identity checks if the source file and paths remain unchanged. This is a static inspection finding; the verifier was not run.

The checked-in evidence snapshot has aggregate `status=BLOCKED` / `qualification=NOT_PASS` and old-node records. It is historical source evidence, not current new-hardware status, and must not be used to promote target acceptance.

Recommended contract candidates (not adopted/implemented here):
1. explicit expected executor/node identity;
2. result/request correlation ID or nonce;
3. capture/issued-at timestamp and maximum freshness window;
4. required readiness state and schema version;
5. exact expected revision plus agent-source identity;
6. distinguish transport identity PASS from scheduler, fencing, recovery, runtime and qualification PASS.

## 5. Operator documentation consistency

- `docs/operations/ASTRA-GITHUB-TRANSPORT-BOOTSTRAP.md` SHA `e87cf363dc6fa0c88207ab9fbb6b72f6dcb75d28` says persistent transport should start through `ops/astra-github-bootstrap.sh` or an equivalent that implements its contract. It describes `origin/main` synchronization and the transport-version/source-SHA health check.
- `docs/operations/ASTRA-TRANSPORT-LAUNCHER-MANIFESTS.md` SHA `d25d413abce67a01c402394a15304c5398b7ad53` tells operators to install both Linux/systemd and macOS/launchd templates, and reiterates that committing manifests alone does not change live systems.

Conflicts/gaps:
- `deploy/` launchers bypass the documented bootstrap boundary.
- The docs branch removed `ops/systemd/mediahub-astra-github-bootstrap.service`, but the installation guide still says install a systemd unit, and a separate `deploy/mediahub-astra-github.service` still exists.
- The launchd guide does not distinguish the two separate plist implementations: `deploy/com.mediahub.astra.github-agent.plist` (direct static agent) vs `ops/launchd/com.mediahub.astra.github-agent.plist` (bootstrap and old host paths).
- Neither guide establishes greenfield approval for any of these paths.

These docs contain potentially reusable intent, but should not be used as target installation instructions until their old host-specific mechanics and current launcher contradictions are explicitly reconciled.

## 6. Disposition matrix

| Artifact | Classification | Recommended handling |
|---|---|---|
| `deploy/mediahub-astra-github.service` | LEGACY-OPERATIONAL / RETIRE CANDIDATE | Do not install; resolve duplicate launch family and path/worktree conflict first. |
| `deploy/com.mediahub.astra.github-agent.plist` | LEGACY-OPERATIONAL / RETIRE CANDIDATE | Do not install; direct-launch path is old and lacks explicit worktree/state/node configuration. |
| `ops/systemd/mediahub-astra-github-bootstrap.service` | LEGACY-OPERATIONAL / RETIRE CANDIDATE | Already removed on the documentation ref only; keep main-vs-docs discrepancy explicit. |
| `ops/launchd/com.mediahub.astra.github-agent.plist` | LEGACY-OPERATIONAL / RETIRE CANDIDATE | Old host ID/path; include in coordinated launcher retirement proposal. |
| `ops/systemd/mediahub-mesh.service` + env example | LEGACY-OPERATIONAL / REUSE-UNKNOWN | Separate review required; current example/path are old-host-bound. |
| `ops/astra-github-bootstrap.sh` | SHARED-OR-UNKNOWN | Preserve until transport synchronization and worktree safety contracts are resolved. |
| `astra_github_agent.py` | SHARED-OR-UNKNOWN + LEGACY-NODE COUPLING | Do not reuse wholesale. Extract requirements; review identity, authority, operations, revision binding and result publication. |
| `ops/control/sign_command.py` | SHARED-OR-UNKNOWN | Preserve security semantics; replace fixed legacy identity mapping only under accepted identity/key contract. |
| `ops/qualification/verify_transport_health.py` | REUSE-CANDIDATE / CONTRACT GAP | Keep as historical comparator; do not use as new-target gate without explicit freshness, request-correlation and expected-identity rules. |
| Old transport-health JSON snapshots | HISTORY / LEGACY-QUALIFICATION EVIDENCE | Preserve provenance; never treat old node PASS rows as target proof. |
| Two launcher documentation files | HISTORY + REQUIREMENT-CANDIDATE | Keep lineage; revise only through controlled documentation work after contract decisions. |

## 7. Owner decision packet

The current evidence does not establish whether the greenfield Contour A design should retain persistent GitHub polling as its command ingress. This decision should not be inferred from the existence of the legacy agent.

- **Option A — retain the pattern but replace the implementation:** define a versioned, scoped command/health/result contract, then build a new minimal transport adapter. Benefit: preserves a pull-based control path. Cost: demands fresh identity, credential lifecycle, polling, idempotency and operational qualification.
- **Option B — select a different admitted Contour A command ingress:** define an interface adapter between ingress and ASTRA A0; the selected ingress does not own ASTRA queue/claim/gate state or MediaHub Product State Authority. Benefit: explicit separation. Cost: requires interface and security review of the replacement.
- **Option C — retain existing launcher/agent only as historical evidence:** do not operate it in the greenfield Contour A target. Benefit: avoids importing old topology. Cost: all needed behavior must be re-specified and built elsewhere.

**Recommendation for owner review:** Option B as the design posture, with a contract-first interface to ASTRA A0; carry over only independently reviewed requirements from the old transport. Do not treat this recommendation as an accepted decision. Option A remains viable if the owner explicitly chooses to preserve the pull model and the security, workspace, and command contracts can be reconciled.

## 8. Scope and verification

- Source-only read of pinned files and path history; no code changes or runtime actions.
- Current main tree is complete within the returned 800-entry tree; the launcher-specific reverse-reference review remains bounded and is not a proof of all dynamic imports or external triggers.
- External environment files, installed/loaded launchd or systemd services, workflow enablement/run histories and host filesystems are UNKNOWN.
- No test, qualification, launch, model/provider call, credentials access, host/runtime inspection, install, deployment, migration, merge, rebase, cherry-pick or ref movement occurred.

## 9. Next justified step — WB-14Q

Prepare a **contract-only target ingress decision and requirements matrix** for Contour A:

1. translate the abstract capabilities identified here into requirements and failure cases, cross-referenced to accepted A0 ingress, capability/security, identity lifecycle, command/task/result contracts;
2. explicitly separate target requirements from source reuse candidates and legacy assumptions;
3. specify a proposed health-response schema that enforces freshness and request/identity correlation, without implementing or running it;
4. leave owner decision on ingress A/B/C explicit and do not touch main source until the target choice and branch integration strategy are resolved.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
