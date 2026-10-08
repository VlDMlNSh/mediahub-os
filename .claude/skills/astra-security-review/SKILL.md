# Astra security review

A bounded security-review gate inspired by ECC security scanning patterns.

## Check every task diff for
- credentials, API keys, bearer tokens, private keys, cookies, or connection strings;
- accidental changes to workflow files, controller state, production infrastructure, or user-data paths when outside the declared boundary;
- debug dumps, temporary files, generated caches, and local environment files;
- commands that disable validation, bypass admission, or write directly to main;
- changes that weaken target-SHA, claim, verifier, or fail-closed guarantees.

## Decision
Any suspected secret or policy bypass is BLOCKED until removed or explicitly authorized. Security review is evidence-producing and never a qualification PASS by itself.
