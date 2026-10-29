# MediaHub OS — gVisor/containerd Advisory Intersection (Wave 455)

- Date: 2026-10-29
- Status: **EXACT DEPENDENCY VERSION AND PUBLIC ADVISORY RANGE MATCH / REACHABILITY NOT VERIFIED / NO ADOPTION**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Map addendum: [Wave 455](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-455-2026-10-29.md)
- Continuation checkpoint: [current checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Upstream evidence baseline: [Wave 453](MEDIAHUB-GVISOR-RELEASE-PROVENANCE-AND-CURRENT-GATES-WAVE-453-2026-10-29.md)

## 1. Immutable targets and current gates

- MediaHub main target: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7.
- Documentation branch at start of Wave 455: cf552c0b0f5617360c41dbb4bb6a0834248a9723.
- gVisor release tag: release-20261026.0; release commit: e8a2a28891ba41f3fb737dee8bb7120745d75826.
- gVisor go.mod blob: d063558784be716b06f65140063c6be8afd6cd28. Both previously checked release and default-head go.mod/go.sum blobs are identical.
- PR #583 remains OPEN/DRAFT/UNMERGED at 448bcbe6b941847b993dc2675a74367cce276b3e. PR #585 remains OPEN/DRAFT/UNMERGED at 8940c7f0f66c9f50e2d83659a6231aa790817221.
- Formal reviews remain zero on both PRs. Effective branch policy remains NOT VERIFIED. No controller dispatch, provider inference, secret access, merge, deployment, qualification or component adoption occurred.

## 2. Narrow source-to-advisory check

The exact gVisor go.mod blob contains a direct requirement on github.com/containerd/containerd/v2 at version v2.1.5. This was retrieved from the repository's Git blob API by the recorded blob SHA; no code execution or dependency installation was performed.

The GitHub-reviewed advisory [GHSA-pg57-6jwg-q645 / CVE-2026-53493](https://github.com/advisories/GHSA-pg57-6jwg-q645) lists the containerd v2.1 line as affected for versions >=2.1.0 and <2.2.9, with v2.2.9 listed as the fixed version for the 2.2 line. The gVisor-pinned v2.1.5 lies inside that published affected range.

The advisory describes resource exhaustion during containerd image-pull processing of crafted OCI index descriptor graphs. This report establishes a dependency-version overlap only. It does not establish whether gVisor invokes an affected code path in a relevant deployment, whether the dependency is reachable in the intended build, or whether MediaHub's proposed usage is exploitable.

The upstream [containerd release policy](https://github.com/containerd/containerd/blob/main/RELEASES.md) marks branch 2.1 as End of Life since 2026-07-03. The policy's status is a separate maintenance concern from the advisory range overlap.

For context, Wave 449's exact Trivy go.mod snapshots listed containerd v2.4.1 at release and v2.4.2 at observed default HEAD; these versions are outside the affected range in this specific advisory. This does not certify Trivy as safe or qualified.

## 3. Disposition

- Exact gVisor dependency version and blob identity: **VERIFIED**.
- Public advisory affected-range overlap: **VERIFIED**.
- Affected-code reachability, runtime exploitability, and gVisor build/runtime impact: **NOT VERIFIED**.
- gVisor release-tag signature and independent artifact provenance: **NOT VERIFIED**, per Wave 453.
- Full dependency/transitive-advisory scan: **NOT RUN**.
- Candidate inventory: **OPEN_NOT_FROZEN**; comparison **NOT_STARTED**; adoption **NONE**.
- Gemini Agents 1/2/3 dispatch and child runs: **NOT RUN**. Contour A: **NOT ACCEPTED**. Contour B: **GATED**.

## 4. Next bounded step

Independently inspect the pinned gVisor source at release commit e8a2a28891ba41f3fb737dee8bb7120745d75826 to determine which build/runtime path consumes containerd v2.1.5 and whether the advisory-affected image-pull operation is reachable. Keep gVisor out of the qualified shortlist until the version is patched or a defensible source-level reachability analysis is reviewed. Do not attempt a dependency upgrade in this documentation-only step.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
