# MediaHub OS Contour A — security candidate and MCP image recheck (Wave 197)

- Date: 2026-10-19
- Canonical branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous checkpoint: [Wave 196](MEDIAHUB-NEXT-CONTINUATION-CHECKPOINT-WAVE-196-2026-10-19.md)
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Scope and sources re-read

This was a bounded, read-only gate recheck. Re-read the project Bootstrap, Master Roadmap, Wave 196 checkpoint/report, canonical map by blob, Issue #301 and its full comment history, PR #374/#375/#376 summaries, `main` Gemini dispatch workflow, and generated current qualification truth.

- `main` HEAD observed: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Bootstrap blob: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Master Roadmap blob: `beef785c787702dc174cf9a5515bac8c9f4b292f`.
- Canonical map blob before this wave: `e8d9ed705c709d3d01e6238519e7a0a9178c0ce2`; Contents API returned an empty body, so the map was retrieved by exact blob SHA (1,075,873 characters).
- `docs/qualification/CURRENT-TRUTH.generated.md@main` blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` still reports G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED.

## Findings

### 1. MCP image pin remains unresolved

The official [GHCR package page](https://github.com/github/github-mcp-server/pkgs/container/github-mcp-server/) currently surfaces SHA-named package versions and manifest digests, including recent versions. The retrieved page/search result does **not** bind the workflow's `ghcr.io/github/github-mcp-server:v0.27.0` tag to one exact OCI manifest or platform manifest. A current digest or an unrelated SHA-named version cannot safely substitute for that mapping. Do not guess a digest or change the workflow based on this evidence.

Required evidence remains: exact repository/tag mapping; OCI index and platform manifest digests where applicable; registry-returned manifest identity; capture timestamp; and verifiable provenance/signature or attestation.

### 2. Existing security candidates need exact-head test evidence

- [PR #375](https://github.com/VlDMlNSh/mediahub-os/pull/375) remains open. Its recorded candidate changes reduce worker token exposure (`contents: read`) and disable persisted checkout credentials on all three checkout steps. Recorded workflow/test blob SHAs are `c24ad16ab8ed59fd4dbad9538063f63a933eab2c` and `4b3787368758f2dba4abd85325025cfbfbe59e9b`. Its own description explicitly says tests were not executed in that pass; this wave did not claim a pass or independently verify a fresh exact-head run.
- [PR #376](https://github.com/VlDMlNSh/mediahub-os/pull/376) adds static parity checks for the three Gemini workflows, but its own description likewise says tests were not executed in that session. The prior Wave 192 CI successes belong to the then-recorded exact head and are not new Wave 197 evidence.
- [PR #374](https://github.com/VlDMlNSh/mediahub-os/pull/374) records successful schema/semantic CI at candidate head `3b1fc96beeedcc6cb38c7beeb5809f0004c6ac8a`, but independent schema/semantic and bootstrap publisher-provenance review remain open. Its successful run does not close the separate A0, R-06, target-manifest or runtime qualification gates.

These candidates remain separate, open and unmerged. No merge or readiness promotion is inferred from a draft description or historical CI record.

### 3. Governance and branch protection are still blockers

Issue #301 remains open with 42 comments. The latest retrieved relevant comment is Wave 192 (`6265270600`); no later independent governance disposition was found in the reviewed history. The proposed brokered-write boundary and negative/failure-path oracle therefore remain proposals, not approved authority. Branch-protection/review requirements remain unverified because the prior integration request returned 403; no protection setting was changed.

### 4. Workflow source risk is still present on main

The source-read `.github/workflows/gemini-autonomous-engineering.yml@main` blob `09523d809530ae5b7bf528eab5fa53bc5deaf92d` still grants the job `contents: write` and `pull-requests: write`, uses mutable `actions/checkout@v4`, `google-github-actions/run-gemini-cli@v0` and MCP image tag `:v0.27.0`, and relies on prompt/tool allowlisting rather than a verified server-side branch/base/path authorization boundary. This is a source-level authority/supply-chain gap, not a claim of an observed exploit. No workflow was dispatched.

## Actions and verification boundary

- Read-only source and GitHub tracker review only; canonical documentation update is the only write planned for this wave.
- No tests were executed; no provider/model call or workflow dispatch; no secrets or credential values accessed; no host command; no infrastructure change; no merge, deployment or qualification.
- No OCI digest was guessed and no workflow pin was changed.
- Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains blocked until Contour A is deployed and independently accepted.

## Next step

First obtain authoritative tag-to-manifest/provenance evidence for the exact MCP image, or document that it cannot be reconstructed. In parallel, request a recorded independent governance/security disposition for the brokered-write boundary and verify branch protection through an authorized repository-administrator path. Then refresh PR #375/#376 exact heads and CI, and run the negative/failure-path oracle only in a disposable isolated boundary after those gates are satisfied.
