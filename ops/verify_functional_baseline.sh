#!/usr/bin/env bash
set -euo pipefail

ROOT="\$(git rev-parse --show-toplevel)"
cd "\$ROOT"

BASE="specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md"
GOV="specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml"
INV="specification/invariant-registry.yaml"

R4_SHA='471f709f5633feab7aeb62dd3ea52effad6d2bc4'
R4_TREE='2279612908135418b2b5448d598274ea6741deaa'

VERIFY_REF="\${GITHUB_SHA:-HEAD}"
if [[ -n "\${GITHUB_HEAD_REF:-}" ]]; then
  git fetch --no-tags origin "refs/heads/\${GITHUB_HEAD_REF}:refs/remotes/origin/\${GITHUB_HEAD_REF}" >/dev/null 2>&1
  VERIFY_REF="refs/remotes/origin/\${GITHUB_HEAD_REF}"
fi

git rev-parse --verify "\$VERIFY_REF^{commit}" >/dev/null
git merge-base --is-ancestor "\$R4_SHA" "\$VERIFY_REF"
test "\$(git rev-parse "\$R4_SHA^{tree}")" = "\$R4_TREE"

tmp="\$(mktemp -d)"
trap 'rm -rf "\$tmp"' EXIT
for path in "\$BASE" "\$GOV" "\$INV"; do
  mkdir -p "\$tmp/\$(dirname "\$path")"
  git show "\$VERIFY_REF:\$path" > "\$tmp/\$path"
done

grep -Fq '**Status:** NORMATIVE / SINGLE SOURCE OF TRUTH' "\$tmp/\$BASE"
grep -Fq 'status: NORMATIVE_SINGLE_SOURCE_OF_TRUTH' "\$tmp/\$GOV"
grep -Fq 'baseline_id: MEDIAHUB-FUNCTIONAL-BASELINE-1.0' "\$tmp/\$GOV"
grep -Fq 'INV-036: Functional Baseline 1.0 is the normative single source of truth' "\$tmp/\$INV"
grep -Fq 'MediaHub State Authority' "\$tmp/\$BASE"
grep -Fq 'Home Assistant Core' "\$tmp/\$BASE"
grep -Fq 'Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI' "\$tmp/\$BASE"
grep -Fq 'exact_application_count: 2' "\$tmp/\$GOV"
grep -Fq 'release: LOCKED' "\$tmp/\$GOV"
grep -Fq 'production: NOT_AUTHORIZED' "\$tmp/\$GOV"

printf '%s\n' 'FUNCTIONAL_BASELINE=PASS'
printf '%s\n' 'STATUS=NORMATIVE_SINGLE_SOURCE_OF_TRUTH'
printf '%s\n' "BASELINE_SHA256=\$(sha256sum "\$tmp/\$BASE" | cut -d' ' -f1)"
printf '%s\n' "GOVERNANCE_SHA256=\$(sha256sum "\$tmp/\$GOV" | cut -d' ' -f1)"
printf '%s\n' "VERIFY_REF=\$VERIFY_REF"
printf '%s\n' "R4_SHA=\$R4_SHA"
printf '%s\n' "R4_TREE=\$R4_TREE"
