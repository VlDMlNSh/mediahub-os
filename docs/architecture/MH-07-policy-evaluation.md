# MH-07 — Policy Evaluation

Status: CANDIDATE.

Pipeline: validate input → normalize only by explicit schema rules → select applicable rules → evaluate → return bounded result/diagnostic context.

Malformed → DENY. Unsupported → DENY. No match → DENY. Explicit DENY → DENY. ALLOW without conflict → ALLOW. ALLOW+DENY conflict → DENY. Ambiguity → DENY.

No implicit precedence, retries, merge, inheritance or side effects. Evaluation cannot mutate configuration, policy, grants or State Authority.

Current evaluate_policy implementation provides exact operation/resource matching and fail-closed conflict/no-match behavior; full test verification is not established by repository inspection alone.
