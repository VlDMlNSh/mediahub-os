# Astra authorized execution schemes

This registry records execution schemes explicitly authorized by Astra qualification policy. A scheme is not marked PASS until fresh runtime evidence and qualification gates pass on the exact target SHA.

| Scheme | Nodes | Executor | Model | Max active claims | Status |
|---|---|---|---|---:|---|
| Three-Claude distributed local | mh-dev-01, Voktors-Mac-mini.local, mh-dev-02 | Claude x3 | qwen2.5-coder:1.5b, qwen2.5-coder:1.5b, qwen2.5-coder:3b | 3 | AUTHORIZED / QUALIFICATION PENDING |

## G-5

The three permanent executor lanes are one claim each. The queue MUST NOT exceed three simultaneous active claims.

## PASS rule

Change QUALIFICATION PENDING to PASS only after all three executor lanes produce fresh PASS evidence, evidence is target-SHA bound, independent verification passes, aggregate qualification passes, and the 24/7 controller soak has a fresh PASS result.

No synthetic or prefilled evidence is accepted.
