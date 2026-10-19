# MediaHub OS — Project map addendum, Wave 164 (2026-10-19)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

- Report: [Wave 164 bootstrap provenance scope and lock consumer trace](../checkpoints/MEDIAHUB-CONTOUR-A-BOOTSTRAP-PROVENANCE-SCOPE-AND-LOCK-CONSUMER-TRACE-WAVE-164-2026-10-19.md), blob SHA `e1382c071539215b791a56ed008527475cb623c8`.
- This pass narrows Wave 163's provenance result to the exact consumer that pins the artifact. Current main (`c06015e0b1526e0aaa6a522306052b077455aba5`) has no `requirements/cloud-agent-lock-generation-bootstrap.lock`, `.github/workflows/cloud-agent-lock-generation.yml`, or cloud-agent schema-validation requirements lock/input at those paths; direct fetches returned 404.
- Main's canonical runtime bootstrap `ops/astra-github-bootstrap.sh` blob `5f36f35ea85f55e5f49af6d3dabb5e876fffa09b` checks out the repository and execs `python3 astra_github_agent.py`; it does not install or refer to setuptools. Main `requirements-dev.txt` blob `241432c98a273df782c65f35b76d10593c3dea43` lists only PyYAML and pytest.
- The exact `setuptools==84.0.0` pin is required by the present unmerged Draft PR #338 lock-generation candidate: bootstrap lock blob `2cb89e822dabbe54a11e6b718ec8443b8891c926` and workflow blob `22ed52a9252630bfa62b5fbb7d37ea79c84f8b82`. The separate runtime schema-validation lock in that candidate has no setuptools entry.
- PR #338 is OPEN/DRAFT/UNMERGED at head `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`; four check-runs passed at that exact head, but these are functional/reproducibility tests, not publisher-provenance evidence. Canonical docs branch and candidate remain diverged 20 ahead / 202 behind at this compare.
- PyPI Integrity API returned 404 for exact wheel and source archive provenance; per https://docs.pypi.org/api/integrity/, 404 means no provenance object is available. This remains an adoption gate for PR #338 as currently authored, not a demonstrated runtime dependency of main.
- No code/dependency/workflow changed, packages downloaded/installed, secrets read, providers called, worker dispatched, branches merged or deployment/qualification/independent acceptance performed.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains gated.

Next: keep the provenance gate scoped to PR #338 adoption. Before integrating that candidate, either document an accountable alternative trust disposition or substantiate a minimal change to the existing lock-generation toolchain with reproducible lock regeneration, dependency reasoning and fresh exact-head CI. Do not silently remove or replace the pin.
