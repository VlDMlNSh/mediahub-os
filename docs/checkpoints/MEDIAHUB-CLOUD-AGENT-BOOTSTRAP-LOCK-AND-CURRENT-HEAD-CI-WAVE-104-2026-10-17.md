# MediaHub OS — bootstrap supply-chain hardening and exact-head CI, Wave 104

- Date: 2026-10-17
- Status: **BOOTSTRAP HASH-LOCK IMPLEMENTED / EXACT-HEAD CI PASS / INDEPENDENT REVIEW AND CONTOUR A ACCEPTANCE OPEN**
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Candidate: https://github.com/VlDMlNSh/mediahub-os/pull/338
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Live source snapshot

- `main` HEAD observed: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical documentation branch HEAD observed before this report: `8e214ea8030c6c49b390b17cbb8548a8326c7d00`.
- Compare: diverged; documentation branch 2,151 commits ahead and 27 behind `main`; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. This count is directionally reported by the compare API; it does not authorize whole-branch integration.
- Bootstrap instruction blob: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Current continuation checkpoint blob before this update: `775763b0f82106a87c31ec992aa4c621bb3adcc5`; its recorded latest wave was Wave 101.
- Master Development Roadmap blob before this update: `89fc7df39f3b9661a08a232f0a7679ba22df367e`; its last continuation record was older than the current cloud-agent runs.
- The map Contents API returned an empty body; its full content was read from blob `e6a75b574c74a6bd7106e5cb010d9bf76b328f7a` (1,033,947 characters). It ended at section 20.353/Wave 98 and did not index Waves 102–103.
- Functional authority remains Baseline 2.0 on `main`; Baseline 1.0 remains historical provenance.

## 2. Bootstrap integrity update

- Candidate branch: `contour-a-schema-validation-consolidation-wave98-20261017`.
- Candidate HEAD at this report: `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`.
- Bootstrap file: `requirements/cloud-agent-lock-generation-bootstrap.lock`.
- Bootstrap lock blob SHA: `2cb89e822dabbe54a11e6b718ec8443b8891c926`.
- Lock-generation workflow blob SHA: `22ed52a9252630bfa62b5fbb7d37ea79c84f8b82`.
- Schema-validation workflow blob SHA: `f58add06b86b9f816e641ca1aea7d343e9662765`.
- The bootstrap pins eight distributions using exact versions and one universal-wheel SHA-256 per package; installation is restricted to hashes and wheels using `--require-hashes --only-binary=:all:`.
- Pinned set: `build==1.3.0`, `click==8.3.3`, `packaging==26.3`, `pip==26.2`, `pip-tools==7.6.2`, `pyproject-hooks==1.2.0`, `setuptools==84.0.0`, `wheel==0.48.0`.
- Hashes were checked against official PyPI release-file metadata: [build 1.3.0](https://pypi.org/project/build/1.3.0/), [click 8.3.3](https://pypi.org/project/click/8.3.3/), [packaging 26.3](https://pypi.org/project/packaging/26.3/), [pip 26.2](https://pypi.org/project/pip/26.2/), [pip-tools 7.6.2](https://pypi.org/project/pip-tools/7.6.2/), [pyproject-hooks 1.2.0](https://pypi.org/project/pyproject-hooks/1.2.0/), [setuptools 84.0.0](https://pypi.org/project/setuptools/84.0.0/), [wheel 0.48.0](https://pypi.org/project/wheel/0.48.0/).
- The file header was corrected from “Independent, reviewed” to explicitly say the independent review remains pending. Hashes pin bytes to published digests; hashes alone are not independent approval or a guarantee of publisher trust.
- Residual provenance risk: the official PyPI record for setuptools 84.0.0 says Trusted Publishing was not used. Retain as an open supply-chain review finding; do not misstate its status as independently trusted.

## 3. Exact-head GitHub Actions evidence

### Lock generation — latest candidate HEAD

- Run [39058422263](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39058422263), lock-generation workflow run #18, event `push`, head `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`: **completed / success**.
- Job: `117471074334`, `generate`, success. All steps succeeded: install hash-locked bootstrap toolchain; verify installed tool versions; compile the runtime lock; capture diff; publish artifact; require byte-for-byte reproducibility.
- Log evidence: `pip check` reported no broken requirements; the eight pinned tool versions passed verification; `LOCK_REGENERATION_MATCH=true`; `git diff --check` and `git diff --exit-code -- requirements/cloud-agent-schema-validation.lock` passed.
- Artifact ID `12110905625`; ZIP size 7,034 bytes; GitHub digest `sha256:c94ead52345eba9d652a0107c611eb67dca46e39f0ce0b49b40d1938e54ad224`. Artifact metadata confirms it belongs to the current candidate HEAD and expires 2026-10-24.
- Runtime lock was not changed by the regeneration. This is exact-run reproducibility evidence for the pinned toolchain/runner/index inputs, not a promise of identical output after future package-index or environment changes.

### Schema and semantic fixtures — latest PR run

- PR run [39058425661](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39058425661), schema-validation workflow run #207, event `pull_request`, candidate head `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`: **completed / success**.
- Job: `117471084337`, `validate`, success. GitHub's PR test merge SHA checked out by the job was `dce0bc01c04020560b2842de6ab5cf190348f0fa`; the PR source head remains `fd12ee3...`. Keep those identities distinct.
- Results in job log: 3/3 Draft 2020-12 schemas meta-validated; 3/3 positive schema fixtures passed; 179/179 negative schema cases rejected, including 166 generated missing-required nested cases; 26/26 semantic negatives rejected; zero reported failures. The positive cross-artifact fixture also passed.
- The workflow parsed all three machine-readable report files as JSON and confirmed validation reports have `status=PASS`.
- Artifact ID `12110676230`; size 8,798 bytes; GitHub digest `sha256:7957517179ce91c469e851996d2141410640c008da90c6f0c35f879ac185bb3c`.
- Report file SHA-256 values emitted by the job:
  - `cloud-agent-ci-provenance.json`: `b4f4c81be3eaf0ddbc9b57cea06333998219353f9907469235de7e69a92f1ac3`
  - `cloud-agent-schema-validation-report.json`: `43848675f28cc0e57a7a576ef48dbfdf65476219a1dcceccf6b26908d19685ee`
  - `cloud-agent-semantic-validation-report.json`: `ba86d3bdcfcc1827eac5c0f1fd54877c6235538bff4ab54994a4a023220ae896`

## 4. Workflow maintenance and status

- Both workflows use explicit `ubuntu-24.04`; Node.js 24-compatible full-SHA pins are now used for checkout `3d3c42e5aac5ba805825da76410c181273ba90b1`, setup-python `5fda3b95a4ea91299a34e894583c3862153e4b97`, and upload-artifact `bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`.
- The latest lock-generation and PR-schema logs confirm those exact action SHAs were downloaded; there was no previous Node.js 20 forced-runtime warning in these latest runs.
- The schema-validation push run [39058422253](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39058422253), job `117471074171`, also succeeded on the current candidate head.
- PR #338 remains OPEN / DRAFT / UNMERGED. GitHub currently reports `mergeable=true`, but the PR base SHA is stale (`2bd41b5f71006597a7669a4b7154abc58f87af5d`) and the branch compares as diverged from the current documentation branch: 20 ahead / 20 behind, merge base `2bd41b5f71006597a7669a4b7154abc58f87af5d`.
- No independent PR reviews or review threads were returned by the available GitHub review APIs. The successful CI does not replace independent review or authorize merge.
- Issue #301 remains OPEN. Unclosed acceptance gates include A0 issuer/verifier/ingress and lifecycle, R-06 audit/privacy authority, accepted runner/workspace/network target manifest, independent schema/authority review, and bounded worker/queue qualification.
- No model/provider call, secret read, cloud-agent dispatch, merge, deployment or Contour A acceptance occurred in this wave.

## 5. Interpretation and next bounded step

**Verified:** bootstrap runtime install is now hash-required and wheel-only; pinned tool versions match expected versions; runtime lock regeneration was byte-for-byte reproducible on the current candidate HEAD; exact-head schema/semantic CI passed with machine-readable reports; runner and Actions runtime pins are current to the reviewed candidate workflow.

**Not established:** independent supply-chain/security review, setuptools publisher provenance acceptance, independent schema/governance review, branch-base reconciliation, live issuer/capability lifecycle, R-06, accepted target manifest, durable queue behavior, runtime qualification or Contour A acceptance.

Next:
1. Obtain an independent source/security review of the bootstrap lock, with explicit disposition for setuptools 84.0.0 provenance and necessity of every direct bootstrap entry.
2. Reconcile PR #338 with the moving canonical docs base using a clean/lossless comparison; inspect conflicts and keep historical records intact. Do not force-update or merge merely because CI passes.
3. Independently review schema/semantic validation coverage and references.
4. Continue Issue #301 A0/R-06/target-manifest and bounded queue-worker admission gates. Keep Contour A **NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED**.

## 6. Sources

- [Wave 102 lock regeneration evidence](MEDIAHUB-LOCK-REGENERATION-VERIFIED-WAVE-102-2026-10-17.md)
- [Wave 103 runner pin evidence](MEDIAHUB-RUNNER-PIN-QUALIFICATION-WAVE-103-2026-10-17.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #338](https://github.com/VlDMlNSh/mediahub-os/pull/338)
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
