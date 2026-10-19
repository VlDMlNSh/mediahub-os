# MediaHub OS — bootstrap provenance scope and consumer trace — Wave 164

- Date: 2026-10-19
- Status: **SOURCE-BOUND SCOPE CORRECTION / CANDIDATE-ONLY PROVENANCE GATE / NO RUNTIME CHANGE**
- Repository: `VlDMlNSh/mediahub-os`
- Work branch: `docs/contour-a-wave-163-pypi-publisher-provenance-20261019`
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Purpose: determine whether the exact `setuptools==84.0.0` wheel with no PyPI Integrity API provenance is required by current `main`, or only by the separate Draft PR #338 candidate.

## 1. Corrected conclusion

The Wave 163 provenance result remains valid for the exact PyPI files: PyPI's Integrity API returned 404 for the wheel and source archive, and the official API contract defines 404 as no provenance object. The consumer-trace review changes the **scope of the blocker**:

- **Current `main`:** the reviewed runtime bootstrap does not install setuptools. The project tree on current `main` does not contain the candidate bootstrap-lock file, the candidate lock-generation workflow, or the candidate cloud-agent schema-validation lock/input. A direct `fetch_file` for each of those exact paths on `main` returned 404.
- **Candidate PR #338 only:** the Draft schema-consolidation candidate includes a bootstrap lock that pins `setuptools==84.0.0` and a lock-generation workflow that installs that lock and explicitly asserts the installed setuptools version. Thus the unverified publisher provenance is an adoption gate for this candidate workflow as currently authored, not evidence that the live `main` bootstrap depends on this artifact.
- The separate runtime-schema-validation lock in PR #338 does not mention setuptools; its direct input file pins `jsonschema[format]==4.23.0`. This distinguishes validation-runtime dependencies from the bootstrap toolchain used to compile that lock.

Do not describe this as a proven runtime production dependency or as proof that current `main` must be modified. Equally, do not silently ignore the provenance gap if PR #338 is to be adopted: that candidate's lock-generation path directly installs and version-checks the exact wheel.

## 2. Current repository refs and candidate state

- Current `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical docs branch `docs/mediahub-chat-tree-map-20261012` HEAD: `28816f6b523c8cbc878ebd0575b17bc419669889`.
- PR [#338](https://github.com/VlDMlNSh/mediahub-os/pull/338): OPEN / DRAFT / UNMERGED; candidate head `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`, candidate base `2bd41f5b71006597a7669a4b7154abc58f87af5d`. Comparison of current canonical docs HEAD to the candidate HEAD is DIVERGED, 20 ahead / 202 behind, merge base `2bd41f5b71006597a7669a4b7154abc58f87af5d`. No mechanical merge/rebase/cherry-pick.
- On exact PR #338 head `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`, the check-runs endpoint currently returns four completed successful runs (three `validate`, one `generate`). These validate the candidate's stated behaviour/reproducibility; they do not verify publisher identity or create a missing provenance attestation.
- PR [#373](https://github.com/VlDMlNSh/mediahub-os/pull/373) is OPEN / DRAFT / UNMERGED. Its current head `f4edec79e103a421e62609545e00ed77ea9275bd` had zero check-runs on last exact-head read. PR [#372](https://github.com/VlDMlNSh/mediahub-os/pull/372) remains OPEN / DRAFT / UNMERGED with zero check-runs observed previously.
- Functional Baseline 2.0 main blob: `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, status ACCEPTED / CANONICAL IMMUTABLE REFERENCE POINT.
- Issue #301 remains OPEN.

## 3. Source path map

| Surface | Ref / blob SHA | Observed purpose | Provenance interpretation |
|---|---|---|---|
| `ops/astra-github-bootstrap.sh` | `main` / `5f36f35ea85f55e5f49af6d3dabb5e876fffa09b` | Fetches/checks out the configured Git branch, then execs `python3 astra_github_agent.py` | No setuptools install or reference in this script |
| `requirements-dev.txt` | `main` / `241432c98a273df782c65f35b76d10593c3dea43` | Declares PyYAML and pytest for development/qualification | No setuptools pin |
| `requirements/cloud-agent-lock-generation-bootstrap.lock` | PR #338 candidate / `2cb89e822dabbe54a11e6b718ec8443b8891c926` | Eight-package locked bootstrapping toolchain | Directly pins setuptools 84.0.0 and the PyPI-listed wheel hash |
| `.github/workflows/cloud-agent-lock-generation.yml` | PR #338 candidate / `22ed52a9252630bfa62b5fbb7d37ea79c84f8b82` | Installs the bootstrap lock with `--require-hashes --only-binary=:all:`, verifies tool versions, runs pip-tools | Explicitly requires `setuptools==84.0.0` as currently authored |
| `requirements/cloud-agent-schema-validation.in` | PR #338 candidate / `46aa24e6ab56bc0bc1c69e29ffa778e7f2c74635` | Direct schema-validation input | Pins only `jsonschema[format]==4.23.0` |
| `requirements/cloud-agent-schema-validation.lock` | PR #338 candidate / `6a232e27c644ec1a46ddebc21a4a27c1d26ca781` | Transitive lock used by schema-validation workflow | No setuptools entry |
| `.github/workflows/cloud-agent-schema-validation.yml` | PR #338 candidate / `f58add06b86b9f816e641ca1aea7d343e9662765` | Installs the schema-validation lock and runs standard/semantic validation | Does not install the bootstrap lock; provenance relationship is indirect through lock generation |

The four candidate-only files above are absent at the same paths on current `main`; direct content requests returned 404. The current runtime bootstrap and development requirements were re-read at their exact SHAs above. No assumption was made that an open PR is already active production/runtime state.

## 4. Existing PyPI provenance result

- Release page: https://pypi.org/project/setuptools/84.0.0/
- Official JSON metadata: https://pypi.org/pypi/setuptools/84.0.0/json
- Exact wheel filename: `setuptools-84.0.0-py3-none-any.whl`
- PyPI-reported wheel SHA-256: `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`
- Wheel provenance route: https://pypi.org/integrity/setuptools/84.0.0/setuptools-84.0.0-py3-none-any.whl/provenance — 404.
- Source archive provenance route: https://pypi.org/integrity/setuptools/84.0.0/setuptools-84.0.0.tar.gz/provenance — 404.
- API semantics: https://docs.pypi.org/api/integrity/ — documented 404 means no provenance object is available for that exact file.

Hashes authenticate bytes against the recorded digest; they do not identify who produced/published those bytes. Source release signatures alone do not prove that the uploaded wheel was built from that source.

## 5. Safe disposition and decision options

1. **If PR #338 is rejected or superseded:** do not change current `main` merely to resolve this candidate-only issue. Keep historical evidence and ensure future candidates do not silently inherit the same unsupported provenance claim.
2. **If PR #338 remains a candidate:** keep its bootstrap-provenance subgate open. An accountable reviewer may assess whether the current bootstrap toolchain actually needs setuptools as a separately installed component, but it must not be removed solely to hide the provenance result; any lock/workflow change requires dependency-graph reasoning, reproducible lock generation, tests and fresh exact-head CI.
3. **If an alternative artifact/version is proposed:** verify its exact file digest and Integrity API provenance, plus compatibility with the pinned Python/build/pip-tools environment. Change the existing canonical lock through the normal PR/CI route, not by hand-editing generated transitive pins.
4. No governance decision or release acceptance is implied by a successful CI run on the candidate branch.

## 6. Verification boundary

This wave performed read-only GitHub source/status reads and public PyPI metadata/API checks, and prepared documentation. It did not download/install a package, recompute a local file digest, modify code/dependencies/workflows, access secrets, call a provider, dispatch a worker, change hosts, merge, deploy, qualify or independently accept Contour A.

**Disposition:** exact PyPI provenance is **unavailable for the candidate's pinned setuptools 84.0.0 wheel**. The blocking gate is **PR #338 candidate adoption**, not a demonstrated runtime dependency of current `main`. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains gated.
