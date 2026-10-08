# Astra / Everything Claude Code integration

## Decision
MediaHub does not adopt Everything Claude Code (ECC) as a dependency or second controller. Astra remains the sole control plane, source of truth, claim authority, promotion gate, and qualification authority.

ECC-derived patterns are used selectively inside the executor workflow because they improve development quality without changing Astra authority:

- bounded plan -> implement -> test -> review loop;
- explicit verification gates and evidence-first reporting;
- security review of diffs for secrets and policy bypasses;
- focused regression testing before broader testing;
- context and token discipline with small-scope edits.

## Deliberately not imported

- ECC's own controller/orchestration layer;
- configuration that can change Astra admission or promotion policy;
- independent MCP/tool authority that bypasses Astra claims;
- learning or memory mechanisms that become an alternative source of truth;
- unbounded hooks or plugins with write access to production infrastructure.

## Placement

The selected workflow guidance lives under `.claude/skills/` in the repository. It is versioned, reviewable, target-SHA bound, and available to every executor checkout. The worker remains responsible for executable gates; skill text never replaces validation.

## Expected effect

Executors should produce smaller, better-scoped changes, run relevant tests earlier, perform security and scope review before verification, and provide stronger evidence to the independent verifier. This integration does not imply Astra Gold PASS; fresh runtime evidence, independent verification, aggregate qualification, and soak remain mandatory.
