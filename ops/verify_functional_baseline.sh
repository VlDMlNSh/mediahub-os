#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
TOOLCHAIN_ROOT="${TOOLCHAIN_ROOT:-"$ROOT/.mh05-toolchain-source"}"
BASE="$TOOLCHAIN_ROOT/specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md"
GOV="$TOOLCHAIN_ROOT/specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml"
INV="$TOOLCHAIN_ROOT/specification/invariant-registry.yaml"

check() {
  local name="$1"; shift
  if "$@"; then
    printf '%s\n' "BASELINE_CHECK=PASS:$name"
  else
    rc=$?
    printf '%s\n' "BASELINE_CHECK=FAIL:$name:rc=$rc" >&2
    exit "$rc"
  fi
}

check "file:BASE" test -f "$BASE"
check "file:GOV" test -f "$GOV"
check "file:INV" test -f "$INV"
check "status:BASE" grep -Fq '**Status:** NORMATIVE / SINGLE SOURCE OF TRUTH' "$BASE"
check "status:GOV" grep -Fq 'status: NORMATIVE_SINGLE_SOURCE_OF_TRUTH' "$GOV"
check "baseline_id:GOV" grep -Fq 'baseline_id: MEDIAHUB-FUNCTIONAL-BASELINE-1.0' "$GOV"
check "INV-036" grep -Fq 'INV-036: Functional Baseline 1.0 is the normative single source of truth' "$INV"
check "authority:BASE" grep -Fq 'MediaHub State Authority' "$BASE"
check "ha-core:BASE" grep -Fq 'Home Assistant Core' "$BASE"
check "ai-chain:BASE" grep -Fq 'Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI' "$BASE"
check "application-count:GOV" grep -Fq 'exact_application_count: 2' "$GOV"
check "release:GOV" grep -Fq 'release: LOCKED' "$GOV"
check "production:GOV" grep -Fq 'production: NOT_AUTHORIZED' "$GOV"

R4_SHA='471f709f5633feab7aeb62dd3ea52effad6d2bc4'
R4_TREE='2279612908135418b2b5448d598274ea6741deaa'
check "r4-commit" git cat-file -e "$R4_SHA^{commit}"
check "r4-ancestor" git merge-base --is-ancestor "$R4_SHA" HEAD
check "r4-tree" test "$(git rev-parse "$R4_SHA^{tree}")" = "$R4_TREE"

printf '%s\n' 'FUNCTIONAL_BASELINE=PASS'
printf '%s\n' 'STATUS=NORMATIVE_SINGLE_SOURCE_OF_TRUTH'
printf '%s\n' "BASELINE_SHA256=$(sha256sum "$BASE" | cut -d' ' -f1)"
printf '%s\n' "GOVERNANCE_SHA256=$(sha256sum "$GOV" | cut -d' ' -f1)"
printf '%s\n' "HEAD=$(git rev-parse HEAD)"
printf '%s\n' "R4_SHA=$R4_SHA"
printf '%s\n' "R4_TREE=$R4_TREE"
