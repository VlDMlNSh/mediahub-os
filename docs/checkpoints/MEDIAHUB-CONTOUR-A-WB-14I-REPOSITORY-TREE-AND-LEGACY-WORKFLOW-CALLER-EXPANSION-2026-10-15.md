# MediaHub OS — Contour A WB-14I: Repository Tree and Legacy Workflow Caller Expansion

- Date: 2026-10-15
- Status: **READ-ONLY TREE ENUMERATION + TARGETED STATIC SOURCE TRACE / NOT A COMPLETE CONTENT SEARCH**
- Parent: WB-14H repository search-surface blocker and WB-14G reverse-reference trace.
- Functional source ref: `main`; documentation written only to `docs/mediahub-chat-tree-map-20261012`.

## 1. Result

A reliable GitHub Git Trees API route is now available. The recursive tree for `main` resolved to commit/tree SHA `ab36db009d034db8dca723691e23b331322287e7`, contained 800 entries / 723 blobs, and reported `truncated=false`. The documentation branch tree resolved to SHA `54eb579ecf8e28ea30d905d4645520ef57e43c1d`. This removes WB-14H's *tree-enumeration* blocker.

It does **not** yet provide a complete repository content search: GitHub code search reports the repository is not indexed and targeted code-search results are non-diagnostic. The pass therefore expanded the direct workflow/caller graph using a bounded set of individually fetched, SHA-pinned source files. It does not claim all 283 non-documentation code/config files or all 720 text-like files were content-scanned.

## 2. Newly proven direct edges and operational references

| Source | Blob SHA on `main` | Finding |
|---|---|---|
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Lines 307–316 call `gh workflow run .github/workflows/astra-distributed-local-worker.yml` with command/task/node/executor inputs. Lines 325–328 poll runs for that workflow. This proves the queue is a direct dispatcher/caller, not merely a file with a matching string. |
| `.github/workflows/astra-autonomous-supervisor.yml` | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | Paths trigger includes the distributed worker workflow; source pins and steps hard-code `mh-dev-01`, `control/commands/mh-dev-01.json`, signer invocation, and result/host checks. Direct relationship to the old controller path is proven. |
| `.github/workflows/astra-stale-supervisor-run-reaper.yml` | `c15df23b85c7b943593383038805d301007db771` | Push path filters include worker, supervisor, qualification workflow, `ops/agent-fabric/**`, and the queue. Its cancellation allowlist explicitly includes the distributed worker workflow. This is an operational dependency for run lifecycle management. |
| `.github/workflows/astra-chat-control.yml` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Issue-comment entry point; `/astra run-gold` dispatches the supervisor. `run-worker` calls the worker script, but its parser/host/executor constraints are internally inconsistent for some accepted input combinations. This is a separate source-level concern; no workflow was executed. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Workflow-dispatch entry point; node-conditioned self-hosted jobs bind old node IDs, runner labels, host/user checks, local model checks, and the worker script. |
| `.github/workflows/astra-distributed-verification.yml` | `648f56badd2b919b822b4fe4b61f285cca99ed93` | Contains old node IDs/host assertions and emits per-node attestation artifacts. |
| `.github/workflows/astra-queue-recovery.yml` | `5d9e0db244429ba44a433f69cf2ff816df0f9824` | Runner label `mh-dev-01-canonical` binds recovery work to the legacy topology. |
| `.github/workflows/astra-node-result-publication.yml` | `087a373fe113d11a81be4d349e4c3d330a22f33c` | Publishes `control/results/mh-dev-01.json` to `astra-node/mh-dev-01` branch and builds old node command IDs. |
| `.github/workflows/astra-runner-admission-probe.yml` | `acbc9e6b73f5854b87fb053c538f675ed8bcae5f` | Host assertion hard-codes `mh-dev-01`. |
| `.github/workflows/astra-g4-115-qualification.yml` | `1edfd7f574cd50cf9004d8d2e826725167fa46c8` | Multiple qualification jobs bind old Linux nodes and `Voktors-Mini.Dlink`. |
| `.github/workflows/astra-gold-24h-soak.yml` | `598b462e2cbfe4ca96db21ec55aed06f72d10545` | Reads old node result branch and asserts `mh-dev-01` hostname/identity. |
| `.github/workflows/astra-gold-unified-qualification.yml` | `e965a648718502d41d62518a6164b03a99bc403c` | Signs and checks `control/commands/mh-dev-01.json`, and consumes `control/results/mh-dev-01.json`. |
| `.github/workflows/astra-local-claude-qualification.yml` | `7f7dc2d65481e2cc80a1db94b41a1e60ed117ffd` | Hard-codes the `mh-dev-02` executor lane. |
| `.github/workflows/astra-provider-qualification.yml` | `d3160088fbef4fce152ed7335f0acaa3bb440378` | Hard-codes expected node `mh-dev-02`. |
| `.github/workflows/mh25-dual-local-23wave.yml` | `6f36cee0cc83886df5a70a393a4e4061dab3f2c1` | Contains old Linux and Mac host checks. |
| `.github/workflows/mh25-first-24h-autonomous-queue.yml` | `8f1cdd61b5ab540344ce4600b66182e0765f22c0` | Contains a `mh-dev-01` host assertion. |
| `astra_github_agent.py` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Contains old-node HMAC environment-key mapping and required-node set. This is security-sensitive control logic; do not remove blindly. |
| `ops/qualification/produce_distributed_node_attestation.py` | `d2d423325558e877845f848314ceaf583a71fd8e` | Hard-coded old hostnames/users in node attestation configuration. |
| `ops/qualification/produce_distributed_verification_evidence.py` | `ee3a1fa1d364da5a6d57a47ab0cfdbd3d0897a6f` | Canonical node and old HMAC environment-key names embedded in evidence generation. |
| `ops/qualification/verify_execution_backends.py` | `31a8c1887c9506dc2eb1d4e2587f81fa531ff859` | Verifies old `mh-dev-01` node identity in execution evidence. |
| `ops/agent-fabric/distributed-local-development-plan.json` | `d49d9d9dbab241fe8878fb63aa8adf3db2134a18` | Repeated old node identities across development plan entries. |
| `tests/test_astra_topology_consistency.py` | `cc5410f631a161b3e3bfb4bae198340f905da6e4` | Test source asserts the three-node permanent executor pool and its topology; it is source evidence of an existing assumption, not a test result (no tests run). |

## 3. Manifest-reader status

The manifests remain pinned to WB-14F:
- `ops/agent-fabric/providers/node-role-map.yaml`: `6fab2a8513ad32ed5bb15be819ad74cc2365214b`
- `ops/agent-fabric/providers/local-executor-routing-v2.yaml`: `af3d96fe91055af6ba79eded9c800d28d8c0c5c9`

No direct literal filename reference to either manifest was found in the bounded content inspection. This is **not** proof that they are unused: indirect readers, generated paths, external automation, and unscanned repository files remain possible. Do not delete or edit either manifest based on this result.

## 4. What is established vs unknown

Established:
- The repository tree can be enumerated without truncation through Git Trees API.
- The queue directly dispatches the old distributed worker workflow and polls its runs.
- Several additional workflows and source files encode old topology assumptions, evidence formats, runner labels, node identities, and run-lifecycle behavior.
- These are source-level facts, not evidence of live hosts, active runners, currently executing workflows, or accepted target topology.

Unknown:
- Complete inbound references/readers for both YAML manifests.
- Complete callers of the worker script and signer; external dispatchers and workflow enablement/live usage.
- Whether the legacy workflows can safely be retired independently or share useful security/evidence semantics with greenfield work.
- Correct owner-approved replacement contract and target topology.

## 5. Safe disposition and next bounded step

- No source/config/workflow/test file was changed; no workflow, test, qualification, provider, credential, host/runtime or infrastructure action was performed.
- Preserve security-sensitive code and all old operational files pending a complete reference closure and owner decision.
- Next: use the now-working recursive tree to drive a deterministic content scan of remaining source/config/test files for the two manifest names, worker-script references, signer references, workflow dispatch identifiers, and legacy node strings; record every scanned file SHA and any scan omissions. Then produce an owner decision packet without treating any option as accepted.

## 6. Navigation

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous blocker report: [WB-14H](MEDIAHUB-CONTOUR-A-WB-14H-REPOSITORY-SEARCH-SURFACE-BLOCKER-2026-10-15.md)
- Previous workflow trace: [WB-14G](MEDIAHUB-CONTOUR-A-WB-14G-REVERSE-REFERENCE-WORKFLOW-ENTRY-TRACE-2026-10-15.md)
