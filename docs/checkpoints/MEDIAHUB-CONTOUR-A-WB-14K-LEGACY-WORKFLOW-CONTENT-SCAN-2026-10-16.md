# MediaHub OS — Contour A WB-14K: Legacy workflow content scan (bounded batch)

- Date: 2026-10-16
- Status: **READ-ONLY, SHA-PINNED BATCH / NOT A COMPLETE REPOSITORY SCAN / NO EXECUTION**
- Parent: WB-14J Targeted Legacy Caller Expansion.
- Source ref: `main`; this report and navigation updates are written only to `docs/mediahub-chat-tree-map-20261012`.

## 1. Result

Scanned eight workflow files identified by WB-14I/J as topology-bound, recording each source blob SHA and direct string matches for the legacy manifests, worker script, signer, worker workflow, and old node/host identifiers. The batch reconfirms that these workflow sources encode old topology assumptions. It does **not** prove those workflows are enabled, running, safe to remove, or referenced only by known callers.

No direct references to `node-role-map.yaml`, `local-executor-routing-v2.yaml`, `run_distributed_local_worker.py`, or `astra-distributed-local-worker.yml` appeared in this batch except the signer invocation in the unified qualification workflow; that is a bounded literal-string result, not manifest-reader or caller closure.

## 2. Source pins and findings

All files were fetched from `main`; blob SHA is the source revision identifier.

| Path | Blob SHA | Bounded finding |
|---|---|---|
| `.github/workflows/astra-runner-admission-probe.yml` | `acbc9e6b73f5854b87fb053c538f675ed8bcae5f` | Contains hostname assertion `mh-dev-01`. |
| `.github/workflows/astra-g4-115-qualification.yml` | `1edfd7f574cd50cf9004d8d2e826725167fa46c8` | Contains old `mh-dev-01`, `mh-dev-02`, and `Voktors-Mini.Dlink` / `Voktors-Mac-mini` host assertions across qualification lanes. |
| `.github/workflows/astra-gold-24h-soak.yml` | `598b462e2cbfe4ca96db21ec55aed06f72d10545` | Reads legacy `astra-node/mh-dev-01` result branch/path and asserts old node/hostname identity. |
| `.github/workflows/astra-gold-unified-qualification.yml` | `e965a648718502d41d62518a6164b03a99bc403c` | Invokes `ops/control/sign_command.py`; uses old `mh-dev-01` command/result paths and node identity. |
| `.github/workflows/astra-local-claude-qualification.yml` | `7f7dc2d65481e2cc80a1db94b41a1e60ed117ffd` | Labels and hostname-checks the local Claude executor as `mh-dev-02`. |
| `.github/workflows/astra-provider-qualification.yml` | `d3160088fbef4fce152ed7335f0acaa3bb440378` | Sets expected node ID and hostname to `mh-dev-02`. |
| `.github/workflows/mh25-dual-local-23wave.yml` | `6f36cee0cc83886df5a70a393a4e4061dab3f2c1` | Contains `mh-dev-01` and legacy Mac host assertions. |
| `.github/workflows/mh25-first-24h-autonomous-queue.yml` | `8f1cdd61b5ab540344ce4600b66182e0765f22c0` | Contains `mh-dev-01` hostname assertion. |

## 3. Scope and limitations

- Batch size: 8 workflow files; no claim that the other repository candidates were scanned.
- Matching method: bounded literal substring inspection of fetched file contents; not a full parser, data-flow analysis, history search, external-dispatcher search, or proof of absence.
- Exact readers of `ops/agent-fabric/providers/node-role-map.yaml` and `local-executor-routing-v2.yaml` remain UNKNOWN.
- Legacy paths remain excluded from the greenfield target baseline; this scan does not authorize deletion or migration.
- No workflow, test, qualification, model/provider, credential, host/runtime, installation, infrastructure, deployment, or branch-integration action was performed.

## 4. Disposition and next step

Keep all scanned and related legacy files unchanged. Continue a deterministic SHA-pinned scan of remaining code/config/test candidates in small batches, prioritizing likely manifest readers and indirect dispatchers. Once source coverage is sufficiently complete, prepare an owner decision packet separating (a) historical source preservation, (b) future greenfield replacement contracts, and (c) any separately authorized retirement. Do not infer a target node inventory from these old source identifiers.

## 5. Navigation

- [Project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [WB-14J parent trace](MEDIAHUB-CONTOUR-A-WB-14J-TARGETED-LEGACY-CALLER-EXPANSION-2026-10-15.md)
- [WB-14I repository tree trace](MEDIAHUB-CONTOUR-A-WB-14I-REPOSITORY-TREE-AND-LEGACY-WORKFLOW-CALLER-EXPANSION-2026-10-15.md)
