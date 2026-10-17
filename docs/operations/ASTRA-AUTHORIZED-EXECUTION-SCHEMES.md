# Astra PASS-certified execution schemes

This is the **certification registry**, not a candidate list. Only schemes that passed authorization, fresh exact-target-SHA runtime qualification, independent verification, artifact/evidence validation, aggregate qualification, and the mandatory 24-hour soak may appear here.

## Certified schemes

| Scheme | Nodes | Executor | Model | Max active claims | Target SHA | Evidence bundle | Certified at | Status |
|---|---|---|---|---:|---|---|---|---|
| _No scheme currently satisfies all certification gates._ | — | — | — | — | — | — | — | **NONE CERTIFIED** |

## Admission requirements

A row may be added only when all of the following are supported by immutable, inspectable evidence for the same target SHA:

1. All three permanent executor lanes are healthy and each executed a real task with Claude: `mh-dev-01` (`qwen2.5-coder:1.5b`), `Voktors-Mac-mini.local` (`qwen2.5-coder:1.5b`), and `mh-dev-02` (`qwen2.5-coder:3b`).
2. Every task has exactly one live claim per physical executor lane; the queue never exceeds three concurrent active claims.
3. Evidence binds `command_id`, `task_id`, `node_id`, `target_sha`, worker run, executor/verifier identity, artifact digest, branch/head and independent verifier result.
4. Recovery, timeout, stale lease and duplicate-dispatch tests pass. Missing, stale, malformed or mismatched evidence is BLOCKED.
5. Security gate, complete regression suite and aggregate queue qualification pass.
6. The separate real 86,400-second (24-hour) soak passes on the same admitted SHA with no unapproved duplicate controller, critical finding, or evidence gap.

A passing unit suite, a single successful worker, a GitHub Actions workflow result, a candidate topology, or an open pull request is not sufficient.

## Candidate/reference designs

Proposed patterns and their implementation status are tracked separately in [Astra reference-architecture synchronization](ASTRA-REFERENCE-ARCHITECTURE-SYNCHRONIZATION.md). A design stays out of this certification registry until all admission requirements above have passed. Do not pre-populate a PASS row or treat a pending scheme as authorized.
