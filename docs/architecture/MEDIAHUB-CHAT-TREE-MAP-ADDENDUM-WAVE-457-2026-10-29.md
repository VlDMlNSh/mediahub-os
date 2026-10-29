# MediaHub OS — Canonical Map Addendum, Wave 457 (2026-10-29)

- Scope: **STEP 1 ONLY — PIN THE INPUTS FOR A REPRODUCIBLE DEPENDENCY/ADVISORY AUDIT**
- Status: **SOURCE RELEASES AND HEADS VERIFIED / LOCKFILES PINNED / SCAN NOT RUN / SCANNER PROVENANCE NOT QUALIFIED**
- Detailed report: [Wave 457 pinned dependency-audit inputs](../checkpoints/MEDIAHUB-DEPENDENCY-AUDIT-INPUT-PINS-WAVE-457-2026-10-29.md), blob `d82ee45893c6d0a2a68a290c2b1475cd93d117a2`
- Prior advisory triage: [Wave 456 zizmor pinned lockfile advisory triage](../checkpoints/MEDIAHUB-ZIZMOR-PINNED-LOCKFILE-ADVISORY-TRIAGE-WAVE-456-2026-10-29.md)
- Prior gVisor advisory intersection: [Wave 455](../checkpoints/MEDIAHUB-GVISOR-CONTAINERD-ADVISORY-INTERSECTION-WAVE-455-2026-10-29.md)
- Current checkpoint: [mediahub-next-continuation-checkpoint-2026-10-12-current.md](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Governing Issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Pinned snapshots

- MediaHub `main`: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- zizmor `v1.31.1` release `effdb35fa7868863f11655db256d9008922fa427`; current `main` `bf9ccabc03ca255c8ac3ac43329335d0524e3dd7`. Pinned Rust `Cargo.lock`, Python `uv.lock`, and `pyproject.toml` blobs.
- Trivy `v0.76.1` release `e713f67f7d54decdcd9b3132c9751833dcced698`; current `main` `4cdb2db63d52cfb5f6c9199e2d08196f2bb9dc77`. Pinned `go.mod` and accompanying `go.sum` blobs.
- gVisor `release-20261026.0` `e8a2a28891ba41f3fb737dee8bb7120745d75826`; current `master` `ac7b4e0fdc7dc4674453438e5e15fc069895620c`. Pinned `go.mod` and accompanying `go.sum` blobs; tag signature and release provenance remain NOT VERIFIED.
- Candidate scanner: OSV-Scanner `v2.7.0`, source commit `bfe2f84abd2f09fe0b83ba7f6dad40d296762f40`. Linux x86_64 asset metadata digest is `sha256:160c6253e2922e9e0a6a9771c5c4c40a4b3c6090b34a3cdd5e80c96cc2e4218b`; tag verification reports `unknown_key`. Executable and attestation verification remain NOT RUN, so scanner provenance/qualification is NOT VERIFIED.

## Result and next step

The source/input matrix is recorded in the detailed report with separate release-vs-current result sets. OSV-Scanner's official lockfile list supports `Cargo.lock`, `uv.lock`, and `go.mod`; `go.sum` is preserved as integrity evidence, not represented as a separate supported lockfile scan.

Step 1 did not run a vulnerability scanner, install dependencies, call a provider, access secrets, dispatch agents, merge, deploy, qualify or adopt any component. Step 2 must validate the pinned scanner binary/source contract, checksum and attestation, then execute read-only scans against each pinned lockfile; if scanner integrity cannot be established, record BLOCKED / NOT RUN.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
