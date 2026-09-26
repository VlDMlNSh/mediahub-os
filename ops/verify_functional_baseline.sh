#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
BASE="specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md"
GOV="specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml"
INV="specification/invariant-registry.yaml"

[ -f "$BASE" ]
[ -f "$GOV" ]
[ -f "$INV" ]
grep -Fq '**Status:** NORMATIVE / SINGLE SOURCE OF TRUTH' "$BASE"
grep -Fq 'status: NORMATIVE_SINGLE_SOURCE_OF_TRUTH' "$GOV"
grep -Fq 'baseline_id: MEDIAHUB-FUNCTIONAL-BASELINE-1.0' "$GOV"
grep -Fq 'INV-036: Functional Baseline 1.0 is the normative single source of truth' "$INV"
grep -Fq 'MediaHub State Authority' "$BASE"
grep -Fq 'Home Assistant Core' "$BASE"
grep -Fq 'Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI' "$BASE"
grep -Fq 'exact_application_count: 2' "$GOV"
grep -Fq 'release: LOCKED' "$GOV"
grep -Fq 'production: NOT_AUTHORIZED' "$GOV"

R4_SHA='471f709f5633feab7aeb62dd3ea52effad6d2bc4'
R4_TREE='2279612908135418b2b5448d598274ea6741deaa'
git merge-base --is-ancestor "$R4_SHA" HEAD
test "$(git rev-parse "$R4_SHA^{tree}")" = "$R4_TREE"

printf '%s\n' 'FUNCTIONAL_BASELINE=PASS'
printf '%s\n' 'STATUS=NORMATIVE_SINGLE_SOURCE_OF_TRUTH'
printf '%s\n' "BASELINE_SHA256=$(sha256sum "$BASE" | cut -d' ' -f1)"
printf '%s\n' "GOVERNANCE_SHA256=$(sha256sum "$GOV" | cut -d' ' -f1)"
printf '%s\n' "HEAD=$(git rev-parse HEAD)"
printf '%s\n' "R4_SHA=$R4_SHA"
printf '%s\n' "R4_TREE=$R4_TREE"
