# MediaHub OS — pip package-source audit (Wave 95, 2026-10-17)

## Status

**Step 1 complete: the previously reported `--no-index` ambiguity is resolved in the current working branch.** This is a bounded configuration/evidence audit, not full Contour A qualification.

## Scope and evidence

- Repository: https://github.com/VlDMlNSh/mediahub-os
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Observed PR head before this report commit: `250214fef305f1dbd073f175f768fe275f1352cb`.
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap blob read: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Canonical checkpoint blob read: `6a2e8b04c2957827996597b74b42877da6b8f97d`.
- Master Roadmap blob read on the working branch: `89fc7df39f3b9661a08a232f0a7679ba22df367e`.
- The Contents API initially returned an empty map body; the map was then successfully read via the Contents API response for the canonical docs branch. The empty body was not treated as proof of an empty file.

## Finding: package index selection

Current generator workflow blob: `c22d820ccb59bcbdbaf4bfa40125063f2c68d8e0`.

The workflow explicitly:
- sets `PIP_CONFIG_FILE=/dev/null` to neutralize ambient pip configuration;
- sets `PIP_INDEX_URL=https://pypi.org/simple`;
- runs the compiler under `env -u PIP_NO_INDEX`;
- passes `--no-config` and `--index-url=https://pypi.org/simple` to `pip-compile`;
- emits `python -m pip config debug` output for audit.

The current lock blob is `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`. Its generated command comment contains the same explicit PyPI URL and contains no `--no-index` marker. Therefore the earlier Wave 87 warning is stale for the current branch snapshot and is superseded by this report.

## Execution evidence

- Successful generator run: [39048549631](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048549631), source commit `d493b042bdf5bb0259b84f69dc48b43875d77474`, job `117442136573`.
- Generator artifact: `12106523853`, digest `sha256:ea02c0e7433c2722edea55eb75827beb66bb822d86faaeec4a78589e426f43e4`.
- Job logs confirm `PIP_CONFIG_FILE=/dev/null`, `PIP_INDEX_URL=https://pypi.org/simple`, the unset `PIP_NO_INDEX` command, and pip resolving dependencies through the explicitly configured index.
- The lock text emitted by the log was compared to the committed lock. After accounting only for the final newline omitted by log framing, the contents match exactly. Both workflow and lock blob SHAs are the same as those read at the current PR head.
- Latest schema-validation run at the observed PR head: [39050070467](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39050070467), conclusion **success**. Job `117446667772` reports all steps successful, including hash-locked installation, Draft 2020-12 schema/fixture validation, cross-artifact semantic fixtures, machine-readable reports and evidence upload. Artifact `12107770418`, digest `sha256:b5e62b066f9f20d26100cf1799887f31ff5a96de33a17310b216a77207e83151`.

## Small-step plan

1. **Complete — audit effective pip index configuration and generated lock provenance.** Finding recorded above; the old `--no-index` concern is resolved in the current branch.
2. Inspect validation artifact contents and confirm that provenance/report files identify the exact tested source SHA and expected schema/fixture counts.
3. Review the authority and schema contracts against Baseline 2.0 and Issue #301; separate factual gaps from implementation defects.
4. Obtain independent review for schema and authority changes; keep PR #337 Draft until required review is recorded.
5. Reconcile branch divergence by file and commit provenance, then rerun checks on the exact candidate SHA. Do not merge until all governance and review gates pass.

## Remaining blockers

- PR #337 remains Draft and unmerged; merge-base comparison observed `78` commits ahead and `20` behind the canonical documentation branch before this report commit.
- Issue #301 remains open. A0 issuer/verifier lifecycle, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent schema review and bounded worker/queue qualification remain separate gates.
- This pass did not inspect or expose secrets, invoke model providers, dispatch workers, deploy infrastructure, merge branches, or declare Contour A accepted.

## Next bounded action

Perform step 2 only: inspect the current validation artifact/provenance manifest and verify its embedded source SHA and reported test counts against run `39050070467`. If artifact retrieval is unavailable through the available GitHub integration, record that limitation and use workflow logs/metadata rather than inferring artifact contents.
