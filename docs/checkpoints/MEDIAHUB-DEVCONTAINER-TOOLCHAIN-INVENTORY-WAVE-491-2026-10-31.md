# Wave 491 — Dev Container toolchain inventory and implementation gate

- Date: 2026-10-31
- Status: **INVENTORY VERIFIED AGAINST SOURCE SNAPSHOT / DEV CONTAINER NOT IMPLEMENTED**
- Workstream: Contour A developer experience; supporting tooling only
- Documentation parent: canonical docs branch commit `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`
- Runtime source snapshot: `main` commit `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Baseline: accepted Functional Baseline 2.0, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`

## 1. Decision

Do **not** add `.devcontainer/devcontainer.json` in this pass. The workflow inventory reveals multiple runtime profiles and system-tool requirements, while the repository does not yet provide a fully pinned, reproducible toolchain manifest. A single minimal container would either omit required CI tools or silently claim parity it does not provide.

The safe next action is to establish a deliberately narrow **Python 3.12 core development profile**, then add explicitly named optional tool profiles only when their dependency and version contracts are captured. The Dev Container must remain a developer workstation, not an Actions runner, provider execution authority, or persistent GUI worker.

## 2. Source inventory

All file blobs below were fetched from `main` at `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.

| Source | Blob SHA | Observed toolchain / commands |
|---|---|---|
| `.github/workflows/astra-cloud.yml` | `3cad60423311cead1ce6d1cf8eb224cb7a296844` | Python 3.12; installs `requirements-dev.txt`; `tools/validate_contracts.py`; pytest for cloud admission and orchestrator failover; `PYTHONPATH=runtime` |
| `.github/workflows/astra-verify.yml` | `ae59d954f1ca6569a8d047589a2a54fd03e47f5b` | Python 3.12; PyYAML; apt `transmission-cli`; `compileall`; unittest discovery; signed-command smoke |
| `.github/workflows/mesh-p2p-verify.yml` | `b04beecd7929c4352d0e75fbcfde007af276a95e` | Python 3.12; `requirements-dev.txt`; apt `transmission-cli`; compile mesh/P2P; 8 unittest modules; `python -m ops.mesh.verify_mesh` |
| `.github/workflows/mediahub-agent-fabric-verify.yml` | `2cec0ba1f02018f7037417363c707a13bc673117` | Python 3.12; pytest; compile runtime/tests; manifest and architecture-invariant checks |
| `.github/workflows/mediahub-ai-factory-verification.yml` | `ccad424e0d225d6f92e1e0589d3fc38ba1a37589` | Python 3 available on runner; `python3 scripts/verify_ai_factory.py`; contents:read |
| `.github/workflows/gemini-workflow-contract-validation-wave284.yml` | `0e800814cc08e1849b230ab12a2d4a92eae71a4e` | Python 3.12 + PyYAML; Go-based actionlint v1.7.7 via `go run`; six unittest contract suites; actionlint against controller/reusable workflows |
| `requirements-dev.txt` | `241432c98a273df782c65f35b76d10593c3dea43` | `PyYAML>=6.0`, `pytest>=8.0` |
| `.gitignore` | `d35ed1cb54b4b081e408a1a20d0ccb4477820021` | Python caches, build outputs, Gemini local state, GitHub App credential files |

Additional repository search surfaced a dedicated Claude FCC worker using Python 3.14.7 (setup-python pinned to that exact patch version), while most core verification workflows use Python 3.12. This is a distinct specialized workflow, not evidence that the core developer environment should silently switch to 3.14.

## 3. Toolchain conclusions

### Core profile candidate

- Linux development container.
- Python 3.12, matching the principal Astra, Mesh/P2P, Agent Fabric and Gemini contract workflows.
- Git and standard shell utilities supplied by the maintained base image.
- PyYAML and pytest from the repository's current development dependency declaration.
- Working directory mounted as the repository; no broad host filesystem mounts.
- Non-root user.
- No privileged mode, Docker socket, host networking, inbound listener, provider credentials or production secrets.

### Explicitly optional tools

- `transmission-cli`: needed only for the Astra Verify and Mesh/P2P test paths. Do not install it globally in the core image until its exact package/version and test need are justified.
- Go/actionlint: needed by the Gemini workflow contract validation. The workflow currently uses `go run ...@v1.7.7`; this is not a locked local toolchain or verified offline cache.
- Python 3.14.7: specialized Claude FCC worker contract/runtime lane; keep separate from the Python 3.12 core profile unless compatibility work explicitly unifies them.

### Reproducibility gap

`requirements-dev.txt` uses open lower bounds (`>=`) and does not lock transitive dependencies. Therefore a container installing this file today would not be bit-for-bit reproducible and might drift from a later CI execution. Do not add a container feature or lifecycle command that upgrades dependencies opportunistically and then call the environment deterministic.

The workflows also use a mix of major-version action references and full-SHA action pins. This inventory does not qualify the provenance of all base images, apt packages, Go modules or VS Code extensions.

## 4. Dev Container design constraints

A later implementation PR must:
1. Pin the base image by immutable digest after checking official image provenance and architecture support.
2. Declare a non-root user and least-privilege workspace mount.
3. Avoid `privileged`, Docker socket mounts, host networking, broad host paths and inbound listeners.
4. Avoid `postCreateCommand`/lifecycle scripts that install unpinned dependencies or access credentials.
5. Avoid embedding secrets in image layers, devcontainer metadata, environment variables, settings, logs or prebuilds.
6. Avoid automatic extension installation until the exact extension IDs, publishers and version pins are reviewed.
7. Keep Python 3.12 core separate from Python 3.14.7 specialized worker tooling.
8. Provide commands that map to existing CI steps without claiming that all CI jobs are locally reproduced.
9. Validate JSON syntax, schema, referenced image digest, feature references and command documentation in a deterministic check.
10. Keep all runtime/provider dispatch under the approved GitHub controllers and policy gates.

Codespaces is still optional and cost-gated. Do not enable prebuilds or configure repository/organization secrets for prebuild use in this workstream.

## 5. Why no config was committed

The repository does not currently establish:
- a locked Python dependency set;
- an immutable Dev Container base-image digest with verified provenance;
- a single OS/package baseline across relevant workflows;
- an approved extension allowlist;
- whether `transmission-cli` belongs in core or an opt-in profile;
- a local Go/actionlint pin/cache policy.

Creating a config before resolving these would turn assumptions into an apparently canonical developer environment. This pass therefore records the exact inputs and stops before implementation.

## 6. Acceptance and execution status

- Workflow/dependency source inventory: **VERIFIED** against the recorded main snapshot.
- Python 3.12 core profile: **PROPOSED**, not implemented.
- Python 3.14.7 specialized lane: **IDENTIFIED**, not merged into core.
- Reproducible dependency lock: **NOT PRESENT / BLOCKER**.
- Dev Container config: **NOT CREATED**.
- Container build/test: **NOT RUN**.
- Codespaces workspace/prebuild: **NOT RUN**.
- Copilot agent runtime: **NOT RUN**.
- Secrets/provider calls/Gemini dispatch/Claude execution: **NOT RUN**.
- Merge/deployment/qualification/acceptance: **NOT RUN**.

## 7. Prior-wave status

PR #604 (Wave 490) remains OPEN/DRAFT/UNMERGED. At its exact head `1b1bc26ad8ac0548a59f7930d027c706e192c60a`, combined status and PR workflow run APIs returned no checks/runs; formal reviews and comments were empty. This is **NOT VERIFIED**, not PASS. No status is inferred from the PR's mergeable flag.

## 8. Next bounded step

Resolve reproducibility before authoring the container:
- decide whether to introduce a lockfile for development dependencies without changing runtime dependency policy;
- qualify an official Python 3.12 Dev Container base image by immutable digest and provenance;
- define an opt-in test-tools profile for `transmission-cli` and Go/actionlint;
- then create a minimal config and validate it with a non-secret PR check.

Do not add Codespaces prebuilds, provider secrets, paid services, new runner authority, or any alternate agent dispatch route.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
