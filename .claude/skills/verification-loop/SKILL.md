---
name: verification-loop
description: MediaHub verification loop adapted from ECC prior art.
license: MIT
metadata:
  origin: ECC/affaan-m/ECC
---

# MediaHub Verification Loop

Use after every significant change and before a checkpoint.

1. Inspect `git status`, diff and exact SHA/TREE.
2. Run repository functional tests.
3. Run Ruff and mypy.
4. Run Semgrep, Bandit, pip-audit and the repository security scan.
5. Run negative/failure-injection tests for the changed boundary.
6. Review the diff for secrets, authority escalation and architectural drift.
7. Report exact results; never claim a gate passed without tool evidence.

If any gate fails: STOP, diagnose, make the smallest safe fix, and requalify.

ECC source attribution: https://github.com/affaan-m/ECC/tree/main/skills/verification-loop
