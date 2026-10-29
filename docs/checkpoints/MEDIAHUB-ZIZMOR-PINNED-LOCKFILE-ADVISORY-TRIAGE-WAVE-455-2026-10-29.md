# MediaHub OS — zizmor Pinned Lockfile Advisory Triage (Wave 455)

- Date: 2026-10-29
- Status: **UPSTREAM REFS AND LOCKFILES VERIFIED / RUSTLS ADVISORY RANGE MATCH FOUND / FULL SCA AND EXPLOITABILITY NOT VERIFIED / CANDIDATE NOT QUALIFIED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Current checkpoint: [mediahub-next-continuation-checkpoint-2026-10-12-current.md](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Candidate register / research PR: [PR #585](https://github.com/VlDMlNSh/mediahub-os/pull/585)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Scope and immutable upstream targets

This is the first narrow sub-step of the upstream dependency/advisory review. It inspects only the zizmor project at the exact release and main-head commits recorded below. It does not install or execute upstream code, alter the candidate register, qualify the project for adoption, or dispatch any MediaHub agent.

- Upstream: [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor).
- Latest observed stable release at time of check: [v1.31.1](https://github.com/zizmorcore/zizmor/releases/tag/v1.31.1), published 2026-10-15T23:16:39Z.
- Exact release commit: `effdb35fa7868863f11655db256d9008922fa427`.
- Exact upstream `main` HEAD: `bf9ccabc03ca255c8ac3ac43329335d0524e3dd7`.
- Release `Cargo.lock` blob: `576fedeeb4bb26439aa0fcb9f7a8d4fc68d10d91`, 110,171 bytes; 451 parsed package records.
- Current `main` `Cargo.lock` blob: `fce6a87d7caeb0b47df419497dd168664b745bed`, 110,675 bytes; 453 parsed package records.
- Release `uv.lock` blob: `c68a7e33664ae40b6e013730f4180e0c831ecf9f`, 76,189 bytes; current `main` `uv.lock` blob: `27a9fc3b2eb5bf0e70eb315c985238547519e742`, 76,190 bytes.
- `pyproject.toml` is byte-identical at both commits (blob `96d1af120771d767fbf750b0fe4c8c3e13e62521`). The Python lockfile differs in one package version: `zensical` 0.0.68 at the release commit versus 0.0.71 at current `main`.
- Rust `Cargo.lock` compares as 451 versus 453 package records. A name-level comparison found 26 package entries with different version/presence; this is a metadata diff, not a vulnerability scan.

Evidence links:
- [Release Cargo.lock](https://github.com/zizmorcore/zizmor/blob/effdb35fa7868863f11655db256d9008922fa427/Cargo.lock)
- [Current-head Cargo.lock](https://github.com/zizmorcore/zizmor/blob/bf9ccabc03ca255c8ac3ac43329335d0524e3dd7/Cargo.lock)
- [Release uv.lock](https://github.com/zizmorcore/zizmor/blob/effdb35fa7868863f11655db256d9008922fa427/uv.lock)
- [Current-head uv.lock](https://github.com/zizmorcore/zizmor/blob/bf9ccabc03ca255c8ac3ac43329335d0524e3dd7/uv.lock)

## 2. Concrete advisory match requiring follow-up

Both the release lockfile and current `main` lockfile pin `rustls 0.23.34` (checksum `6a9586e9ee2b4f8fab52a0048ca7334d7024eef48e2cb9407e3497bb7cab7fa7`). Public advisory data for [GHSA-c8m5-c952-6cm4](https://github.com/advisories/GHSA-c8m5-c952-6cm4) identifies affected Rustls versions as all versions below 0.23.46, with 0.23.46 as the patched 0.23 release. Therefore the pinned 0.23.34 version falls within the published affected range in both reviewed lockfiles.

The advisory describes secret exposure when a custom session store logs session values using Rust Debug formatting. This pass has **not** established that zizmor's call path instantiates such a custom store or reaches the vulnerable behavior. The defensible finding is **dependency advisory range match / exploitability and runtime reachability NOT VERIFIED**, not a claim of confirmed exploitable vulnerability in the zizmor application.

A separate public advisory, [GHSA-vp88-798v-h67f](https://github.com/advisories/GHSA-vp88-798v-h67f), describes an ECH-rejection issue affecting Rustls 0.23.44–0.23.45; the observed 0.23.34 pin does not fall within that specific version window. This does not negate the GHSA-c8m5-c952-6cm4 range match.

## 3. Exact-head CI observed on current upstream main

The first page of upstream workflow runs was checked. Four runs completed successfully at the exact current HEAD `bf9ccabc03ca255c8ac3ac43329335d0524e3dd7`:
- [GitHub Actions Security Analysis with zizmor — 40828282582](https://github.com/zizmorcore/zizmor/actions/runs/40828282582): SUCCESS.
- [CI — 40828282626](https://github.com/zizmorcore/zizmor/actions/runs/40828282626): SUCCESS.
- [zizmor wheel builds for PyPI — 40828282674](https://github.com/zizmorcore/zizmor/actions/runs/40828282674): SUCCESS.
- [Documentation deploy — 40828282675](https://github.com/zizmorcore/zizmor/actions/runs/40828282675): SUCCESS.

These successful workflows establish only that the observed runs reached success on the recorded head. They do not supersede the advisory match and do not constitute an SCA qualification.

## 4. Explicit limits and disposition

- Exact upstream release/head and lockfile blob IDs: **VERIFIED**.
- Rustls 0.23.34 is inside the published GHSA-c8m5-c952-6cm4 affected range: **VERIFIED BY VERSION-RANGE COMPARISON**.
- Whether zizmor reaches the vulnerable custom-session-store behavior: **NOT VERIFIED**.
- Full dependency graph SCA, pinned advisory database scan, license/dependency provenance review and reproducible scanner output: **NOT RUN**.
- Candidate comparison, inventory freeze and adoption: **NOT STARTED / NONE**.
- MediaHub Gemini dispatch, provider inference, secret access, merge, deployment, qualification or acceptance: **NOT RUN**.
- Contour A remains **NOT ACCEPTED**; Contour B remains gated.

## 5. Next bounded sub-step

Run a reproducible, read-only Rust dependency audit against the exact release and current-head `Cargo.lock` blobs, with scanner version and advisory-database snapshot recorded. Confirm the GHSA result in the scanner output, identify the complete dependency path to `rustls`, and record whether the vulnerable behavior is reachable. Do not change or adopt upstream components during this audit. Afterwards, take Trivy as a separate step; gVisor provenance and formal PR review/governance remain separate workstreams.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
