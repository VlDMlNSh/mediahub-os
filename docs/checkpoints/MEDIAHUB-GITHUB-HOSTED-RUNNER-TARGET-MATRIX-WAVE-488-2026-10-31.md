# Wave 488 — GitHub-hosted standard runner pool target matrix

- Date: 2026-10-31
- Status: **SOURCE-VERIFIED PLATFORM MATRIX / CANDIDATE TARGET DESIGN / NOT ACCEPTED / NOT QUALIFIED**
- Contour: A — GitHub-hosted cloud execution pool
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Cloud-first sequencing: [Wave 483 priority proposal / PR #595](https://github.com/VlDMlNSh/mediahub-os/pull/595)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Immutable source boundary

This is a documentation-only source audit. It does not dispatch a workflow, invoke a model/provider, inspect secrets, reserve runner capacity, or qualify a runtime.

- Documentation working parent: `72a6725dbc7c38e37805e254377d293fcb141e7e` (PR #595 head).
- Canonical documentation base: `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`.
- Runtime/source main snapshot: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Main and canonical documentation refs are **DIVERGED**: documentation branch is 3,455 commits ahead and 82 behind main; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. Do not merge or rebase these refs as part of this work.
- Repository visibility: public. The standard GitHub-hosted runner free-use rules for public repositories therefore apply to this repository; larger runners remain separately billed.

## 2. Official standard runner inventory

The following matrix is taken from GitHub's public-repository standard runner documentation, not inferred from third-party benchmarks. Storage is the documented runner SSD capacity.

| Platform / label | CPU | RAM | SSD | Architecture | Candidate MediaHub role |
|---|---:|---:|---:|---|---|
| `ubuntu-24.04` | 4 | 16 GB | 14 GB | x64 | Primary general-purpose worker |
| `ubuntu-24.04-arm` | 4 | 16 GB | 14 GB | ARM64 | ARM-native worker and multi-arch tests |
| `windows-2025` | 4 | 16 GB | 14 GB | x64 | Compatibility/build validation |
| `windows-11-arm` | 4 | 16 GB | 14 GB | ARM64 | Windows ARM compatibility |
| `macos-15` / `macos-26` | 3 (M1) | 7 GB | 14 GB | ARM64 | Apple Silicon tests; small-model experiments |
| `macos-15-intel` / `macos-26-intel` | 4 | 14 GB | 14 GB | x64 | Intel macOS compatibility |

Notes:

- GitHub's current standard public-runner table also includes `ubuntu-latest`, `windows-latest`, and `macos-latest`. Prefer explicit OS-version labels for reproducibility; requalify when changing image generation.
- `ubuntu-slim` is a 1-CPU / 5-GB shared-container option, not the same isolated VM class as the standard multi-CPU runners; exclude it from the model-worker baseline.
- macOS standard ARM64 is documented as M1 with 7 GB RAM. Do not use earlier third-party M2 Pro throughput figures as a proxy for this standard runner.
- GitHub does not advertise a GPU configuration for these standard Linux/Windows runners. The integrated Apple GPU on M1 is not a documented guaranteed accelerator entitlement for a workload; Metal/MLX availability and performance must be runtime-tested before relying on it.
- Larger runners (including large/xlarge macOS) are not part of this free pool and must not be selected under a free-only budget.

Official sources:
- [GitHub-hosted runners — public repository specifications](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Choosing the runner for a job](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [GitHub Actions limits](https://docs.github.com/en/actions/reference/limits)

## 3. Free-use and concurrency interpretation

- Standard GitHub-hosted runners are free and unlimited by minutes for public repositories.
- Private repositories consume plan-included minutes and are billed after the included quota is exhausted.
- Larger runners are always charged, including in public repositories.
- GitHub's published Free-plan concurrency baseline is 20 total concurrent standard jobs, with a maximum of 5 concurrent macOS jobs. Other plans have different limits; account-level effective plan/concurrency was not inspected in this pass.
- Concurrency is an upper bound, not a reservation. Other workflows/repositories can consume available slots, and the scheduler does not promise that all requested jobs start simultaneously.
- Do not describe the pool as a fixed 14-node or 20-node always-on cluster. It is an on-demand job capacity ceiling subject to plan, repository, and platform limits.

## 4. Network and lifecycle findings

GitHub documents that each hosted job receives a newly provisioned VM (except the single-CPU shared-container class) and that the VM is decommissioned after the job. This is not a persistent desktop or long-running worker service.

GitHub does not publish a guaranteed runner-to-runner bandwidth, latency, packet-loss, or direct-peer-connectivity SLA for standard hosted runners. Hosted runners use dynamically assigned shared-infrastructure egress addresses; Linux eligible runners use a multi-cloud compute pool. The published IP ranges are updated weekly and are not recommended as stable allowlists for internal resources.

Consequences:

1. Do not put a numeric runner-to-runner throughput into the target manifest unless MediaHub measures it on an explicitly defined path and records the measurement method, endpoints, time window, sample count, and confidence.
2. Do not assume direct inbound connectivity from one hosted runner to another, stable peer IPs, a shared LAN, shared memory, or a private low-latency fabric.
3. GitHub Actions artifacts can relay bounded files/results between jobs, but that measures the artifact service path, not raw peer-to-peer bandwidth. It is suitable for task outputs and evidence, not continuous tensor exchange or model sharding.
4. Keep workers outbound-only and use the approved controller/child workflow transport. No proxy/VPN/region-spoofing route is introduced by this proposal.
5. Do not promise a persistent VNC/remote-desktop session: the VM lifecycle ends with the job.

Official sources:
- [Using GitHub-hosted runners](https://docs.github.com/en/actions/how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners)
- [GitHub-hosted runner network requirements and IP ranges](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Private networking with GitHub-hosted runners](https://docs.github.com/en/actions/concepts/runners/private-networking)

## 5. MediaHub source crosswalk

Source refs and blob SHAs were re-read from the exact `main` snapshot `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`:

| Source | Blob SHA | What it proves |
|---|---|---|
| `control/qualification/canonical-runner-contract.json` | `32ec7bbe371b1cfd3f2f46019ee1d2671980aa26` | One canonical self-hosted Linux/x64 node contract (`mh-dev-01`); not the GitHub-hosted pool manifest |
| `control/qualification/distributed-runner-contract.json` | `993f51f07c7937165ffb3bfbe59cd0801ea71ec0` | Three self-hosted node identities and authority classes; not a GitHub-hosted target catalog |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Self-hosted local-worker workflow; uses `contents: write`, checkout credentials, and a local publisher path; separate security review required |
| `.github/workflows/gemini-autonomous-engineering.yml` | `155a02159912ca371e6f826c51325ca269857aad` | Gemini worker job currently targets `ubuntu-latest`; checkout is full-SHA pinned and `persist-credentials: false` |
| `.github/workflows/gemini-agent-2.yml` | `fff1820a6b97d379b23674f36bd62227b7d4dec2` | Agent 2 worker currently targets `ubuntu-latest` |
| `.github/workflows/gemini-agent-3.yml` | `781df56e8aa7c75ba453c08378611857862b2e44` | Agent 3 worker currently targets `ubuntu-latest` |
| `.github/workflows/gemini-batch-dispatch-controller.yml` | `0a1246f6755020faf8b7e48d07bfff790bbaece3` | Controller is a fixed-task controller; its dispatch task strings do not accept this runner-matrix research packet |

Historical source context:
- [Wave 181 runner manifest and Gemini pool readiness](MEDIAHUB-CONTOUR-A-RUNNER-MANIFEST-AND-GEMINI-POOL-READINESS-WAVE-181-2026-10-19.md), blob `993d97973db9f0fa169c4ef4b77322ff5eba7180`.
- [Wave 10 target-manifest authority reconciliation](MEDIAHUB-CLEAN-TARGET-MANIFEST-AUTHORITY-RECONCILIATION-WAVE-10-2026-10-16.md), blob `1f748bf80e08067fd85a7e1b0821cc4d12bda676`.
- [GitHub cloud-agent transport policy](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md), blob `a4e2ca4f0d4745cf54f771cf73b69afa3d0f1a06`.
- [Cloud-agent task contract](MEDIAHUB-CLOUD-AGENT-FABRIC-QUEUE-AND-TASK-CONTRACT-WAVE-11-2026-10-16.md), blob `07c8bce182c5e7c87ab963f83169f562f5543e3c`.
- [Registry and evidence schema record](MEDIAHUB-CLOUD-AGENT-REGISTRY-AND-EVIDENCE-SCHEMAS-WAVE-13-2026-10-16.md), blob `9496dca37333f6869dce4aff58226268910c3df3`.

Finding: MediaHub has self-hosted runner identity contracts and existing Ubuntu-hosted Gemini workflows, but the reviewed sources do not yet form one accepted GitHub-hosted runner/workspace/network target manifest. Do not merge self-hosted node IDs, labels, or authority classes into the hosted-worker catalog.

## 6. Candidate MediaHub pool profile (proposal only)

Recommended first qualification matrix:

1. **Primary worker:** `ubuntu-24.04` — deterministic general-purpose CI, agent work, static analysis, and CPU-compatible small-model experiments.
2. **ARM worker:** `ubuntu-24.04-arm` — architecture-native tests and ARM-compatible runtime experiments.
3. **Apple worker:** `macos-26` — MLX/Metal compatibility probes and small-model inference only after memory/performance tests. The standard runner is M1/7 GB, not an M2 Pro.
4. **Compatibility workers:** `windows-2025`, `windows-11-arm`, and `macos-26-intel` on demand; not part of the initial always-requested matrix.

The initial controller/agent path should remain Ubuntu x64 until an approved change adds and qualifies additional runner labels. macOS is a specialist qualification lane, not the default agent transport. No standard runner is assumed to have sufficient RAM/VRAM for a large model or to participate in a sharded single-model inference cluster.

## 7. Bounded qualification plan

No runtime benchmark was executed in this wave. The following is the next test plan, not a test result:

- Launch only after the existing controller, issuer/capability, A0 lifecycle, R-06, quota/budget, and review gates are satisfied.
- Use a single immutable source SHA and explicit runner labels; record the actual runner image/OS version, CPU architecture, available RAM/SSD, queue delay, job duration, and runner cleanup result.
- Run two separate measurements: (a) HTTPS download/upload to a declared neutral endpoint, and (b) GitHub-artifact upload/download between two jobs. Label the latter **artifact-relay throughput**, never runner-to-runner link speed.
- Repeat each transfer at least five times at bounded sizes (e.g. 10 MB and 100 MB initially); record median, p95, errors, and endpoint region. Do not begin with multi-GB model transfers.
- Run model tests independently on each qualified worker. Record model revision/digest, quantization, runtime version, context, prompt/output tokens, cold-load time, tokens/sec, peak RSS, OOM/exit status, and total job minutes.
- No direct P2P listener, no public inbound port, no VPN/proxy overlay, no secrets in artifacts, and no paid/larger runner fallback.
- Any model/runner combination that lacks reproducible evidence remains NOT QUALIFIED.

## 8. Decision

- **GO — parallel independent task execution** on standard GitHub-hosted runners, subject to project admission, quota, and provenance gates.
- **GO — bounded artifact-mediated exchange** of small task inputs/results/evidence between jobs.
- **NO-GO — production tensor parallelism or continuous pipeline sharding** of one large LLM across standard GitHub-hosted runners. No guaranteed peer bandwidth/latency or shared compute fabric is documented.
- **NO-GO — persistent remote desktop** on ephemeral hosted runners.
- **NOT VERIFIED — actual runner-to-runner bandwidth, live parallel capacity, model tokens/sec, MLX/Metal exposure, and account-specific effective concurrency.**

This report is a source-backed candidate matrix, not an accepted operational manifest, deployed pool, benchmark, or Contour A qualification.

## 9. Next dependencies

1. Obtain independent A3 review of the current A0 issuer/verifier candidate (PR #600) and resolve the protocol/identity/trust-anchor/audit ADRs without treating this runner matrix as a substitute.
2. Complete the authoritative hosted runner/workspace/network manifest, binding identity, immutable checkout, clean workspace, egress/data classes, publisher isolation, quota, and evidence lifecycle.
3. Close Issue #301 schema validation and negative-fixture gates.
4. Only then run the bounded GitHub-hosted worker and artifact-relay pilot through the approved controller. This research packet is not accepted as a controller task and must not be dispatched through the current fixed-task controller.

No Gemini Agents 1–3 were dispatched; no Claude/SentinelX host task, provider/model call, secret read, runner benchmark, runtime test, merge, deployment, qualification, or acceptance occurred.
