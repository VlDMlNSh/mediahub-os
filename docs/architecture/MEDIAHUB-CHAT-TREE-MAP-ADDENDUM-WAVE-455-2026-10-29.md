# MediaHub OS — Canonical Map Addendum, Wave 455 (2026-10-29)

- Status: **PINNED VERSION-RANGE OVERLAP VERIFIED / REACHABILITY NOT VERIFIED / NO ADOPTION**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Detailed report: [gVisor/containerd advisory intersection](../checkpoints/MEDIAHUB-GVISOR-CONTAINERD-ADVISORY-INTERSECTION-WAVE-455-2026-10-29.md)
- Prior evidence: [Wave 453 gVisor release provenance](../checkpoints/MEDIAHUB-GVISOR-RELEASE-PROVENANCE-AND-CURRENT-GATES-WAVE-453-2026-10-29.md)
- Current checkpoint: [mediahub-next-continuation-checkpoint-2026-10-12-current.md](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Result

- gVisor release commit e8a2a28891ba41f3fb737dee8bb7120745d75826 has go.mod blob d063558784be716b06f65140063c6be8afd6cd28, which declares github.com/containerd/containerd/v2 v2.1.5.
- GitHub advisory [GHSA-pg57-6jwg-q645 / CVE-2026-53493](https://github.com/advisories/GHSA-pg57-6jwg-q645) places v2.1.5 inside the published affected range >=2.1.0 and <2.2.9.
- containerd branch 2.1 is marked End of Life in the [upstream release policy](https://github.com/containerd/containerd/blob/main/RELEASES.md).
- The advisory describes image-pull resource exhaustion. This pass did not establish gVisor runtime reachability or exploitability.
- Release provenance remains NOT VERIFIED; the full transitive dependency/advisory audit remains NOT RUN.
- No runtime change, provider call, controller dispatch, merge, deployment, qualification or adoption occurred. Contour A NOT ACCEPTED; Contour B GATED.

Next: source-review the pinned gVisor path that consumes containerd v2.1.5; keep the candidate unqualified pending patched dependency evidence or reviewed reachability analysis.
