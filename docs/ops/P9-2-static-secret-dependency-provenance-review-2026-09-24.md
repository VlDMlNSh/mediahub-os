# P9.2 — Static secret, dependency, license and provenance review

Status: SECURITY_RECONCILIATION / P9.2 NOT CLOSED

## Scope

Deterministic repository-only review. Secret scanning reports locations and keyword matches without reproducing values. Dependency review is based on repository manifests; license/provenance claims are not inferred where lock or authoritative metadata is absent. This is not a substitute for a dedicated runtime scanner or supply-chain service.

## Static secret review

- Tracked text files scanned: 774
- Keyword findings (values omitted): 2
- ops/ai/godmode_openrouter_codex.sh:L5 matched a secret-related keyword; value intentionally omitted
- tests/ai/test_godmode_openrouter_launcher.py:L30 matched a secret-related keyword; value intentionally omitted

## Dependency / license review

- Declared autonomous dependencies: pip>=26.2, pip-audit==2.10.1, pytest==9.0.3
- Repository contains no dependency lockfile in the reviewed top-level inventory. Exact transitive versions and authoritative license provenance are therefore NOT established by repository manifests alone.
- `pip-audit` is declared as a review tool, but this artifact does not claim that an external advisory database scan was executed.

## Provenance

- The autonomous provenance journal is hashed as source evidence. Historical entries preserve source/tree/result fields, but this review does not treat journal content as proof of dependency integrity or secret absence.
- P9.2 remains OPEN until dependency provenance/license requirements and any material secret-scan findings are explicitly classified and accepted or remediated.

## Source evidence

### ops/requirements-autonomous.txt
SHA256: dce22dea01937bf18e4ac25464bb66fb1f2e4fe7302e117bd3d4b79fc4eed295

### docs/architecture/MH-12-secrets.md
SHA256: 4ee671f71a9b9306345503eba6f4fd0c403e72bbe91db92fd606b4f453a72346

### .gitignore
SHA256: 9267e8529342cb3a24b917b1f7092955593687cd4a55626c57080cb0476dbb30

### .autonomous/provenance.log
SHA256: 4e90bfcf0ae2badf1297bfd78918105406588c5209d2804b67bf035e662614e2
