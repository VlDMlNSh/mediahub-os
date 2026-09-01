# P0-04 Evidence Integrity Protocol v1.0

## Status

Prepared. No implementation or acceptance authorization is implied.

## Objective

Ensure that P0-04 verification evidence is attributable to the exact implementation under test, reproducible, complete enough for security review, and free from unnecessary personal or secret data.

## Evidence chain

`authorized baseline → immutable implementation commit → execution environment → exact commands → raw result summary → test counts → security/capability inspection → adversarial review → acceptance decision`

Breaking this chain creates an evidence gap; the missing element must not be inferred.

## Required identity

Every execution record must include:

- repository and branch;
- exact implementation commit SHA;
- parent/base authorization SHA;
- execution host/environment;
- OS and architecture;
- interpreter/compiler/toolchain versions;
- UTC timestamp;
- exact command(s);
- exit code(s);
- test count and pass/fail/error counts where applicable.

## Required verification layers

1. Functional State Authority contract tests.
2. Lifecycle and terminal-state negative tests.
3. Candidate isolation and atomic publication tests.
4. Monotonic revision and stale-writer tests.
5. Generation compatibility tests.
6. Independent integrity-gate tests.
7. Operation-specific default-deny authorization tests.
8. Checkpoint and restore tests.
9. Malformed/untrusted input and resource-bound tests.
10. Diagnostics/privacy tests.
11. Capability/security inspection for prohibited execution, network, filesystem, unsafe deserialization, and AI mutation paths.
12. Failure-path preservation tests.

## Reproducibility rule

A result is valid only for the exact immutable commit that was executed. Re-running a different commit may provide useful evidence but cannot retroactively validate the original commit.

## Negative evidence rule

No match in a capability scan is evidence only for the inspected scope and command. It does not prove absence outside that scope. Security conclusions must state the inspected paths and limitations.

## Privacy rule

Use synthetic data. Do not place real secrets, credentials, tokens, raw voice/audio, private content, or unnecessary personal data into evidence. If sensitive material is discovered, stop the affected evidence flow and remediate through a controlled security process.

## Failure rule

Any failed test, unexplained skip, inconsistent result, missing command, missing exit code, or environment mismatch leaves the evidence package incomplete until resolved or explicitly dispositioned.

## Acceptance rule

Evidence integrity is necessary but not sufficient for acceptance. Final acceptance additionally requires the applicable governance authorization, security/privacy review, absence or disposition of blocking findings, and explicit acceptance authority.

## Historical boundary

This protocol does not infer historical MH-02…MH-16 responsibilities.
