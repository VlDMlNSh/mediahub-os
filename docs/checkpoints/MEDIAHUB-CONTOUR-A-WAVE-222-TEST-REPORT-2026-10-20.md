# Contour A Wave 222 — test and branch report

Date: 2026-10-20. Status: local candidate only; not accepted.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
Prior PR: https://github.com/VlDMlNSh/mediahub-os/pull/375
Evidence PR: https://github.com/VlDMlNSh/mediahub-os/pull/396

## Exact refs

- Current main observed: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- Prior PR #375 head: `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`.
- Prior PR #375 base: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- `git rev-list --left-right --count origin/main...origin/pr-375-wave220`: `6 12`. The old PR must not be merged or rebased directly.
- Old PR diff touches the worker workflow, Astra Verify workflow and one semantic YAML regression test.

## Test results

A disposable venv at `/tmp/mediahub-contour-a-wave220-venv` was populated from `requirements-dev.txt`; shared environments were not changed.

- Exact PR #375 head: credential-policy suite — **11 passed in 0.10s**.
- Local current-main-based refresh branch `security/contour-a-worker-credential-refresh-wave222`: credential-policy + worker security gate + distributed workflow suites — **32 passed in 0.17s**.
- Refresh branch's CI-style unittest invocation — **11 tests passed**.
- Separate schema-validator checkout `4a131acf6484f6e370625b0ebc454ee7b4b5116c`: three targeted suites — **28 passed in 0.49s**. Do not attribute these to the refresh branch.
- `git diff --check origin/main...HEAD` passed; refresh branch diff is three files only.
- Local refresh commit: `1cffd325323a41fd706a0c2fcbd8b833241e1f19`.

## Decision

The local candidate reduces the worker workflow's token scope, disables persisted checkout credentials for the three checkout steps, and adds semantic YAML regression tests. The candidate does not remove worker-side Git publication or prove issuer/capability enforcement, artifact-only publishing, OS/network isolation or complete provenance.

The refresh branch has not been published to GitHub; no new PR, merge, deployment, branch-protection change or credential change is claimed. Contour A remains NOT_PROVEN / BLOCKED; G0–G11 BLOCKED and G11 HUMAN_ONLY.

## Next action

Publish the current-main-based local candidate to a Draft PR if repository write actions are available, verify exact remote head and CI, and obtain independent security review. Do not merge based on targeted test results alone.
