#!/usr/bin/env bash
set -euo pipefail
REPO="${MEDIAHUB_REPO:-/home/mediahub/mediahub-os}"
cd "$REPO"
fail=0
check(){ if eval "$2" >/dev/null 2>&1; then printf 'PREFLIGHT=%s=PASS\n' "$1"; else printf 'PREFLIGHT=%s=FAIL\n' "$1"; fail=1; fi; }
check repository 'test -d runtime/mediahub_runtime && test -f CLAUDE.md'
check python 'command -v python3 && python3 -c "import sys; assert sys.version_info >= (3,10)"'
check node 'command -v node'
check ollama 'command -v ollama'
check claude_code 'command -v claude'
check harness 'command -v harness'
check git_clean_check 'git diff --check'
check contracts 'python3 tools/validate_contracts.py'
check connectors 'python3 tools/validate_connectors.py'
check host_registration 'python3 tools/validate_host_registration.py'
check no_root_claim '! id -u | grep -qx 0'
credential_hits="$(grep -RInE --exclude-dir=.git --exclude-dir=.mediahub --exclude='preflight-mediahub-dev.sh' --exclude='*.md' --exclude='*.yml' --exclude='*.yaml' 'sk-[A-Za-z0-9_-]{20,}|OPENROUTER_API_KEY[[:space:]]*=[[:space:]]*[^$[:space:]][^[:space:]]*|TINYFISH_API_KEY[[:space:]]*=[[:space:]]*[^$[:space:]][^[:space:]]*' . 2>/dev/null || true)"
if [ -n "$credential_hits" ]; then
  printf 'PREFLIGHT=no_plaintext_credentials=FAIL\n'
  printf '%s\n' "$credential_hits" | sed -n '1,20p'
  fail=1
else
  printf 'PREFLIGHT=no_plaintext_credentials=PASS\n'
fi
if command -v ollama >/dev/null 2>&1; then ollama list | sed -n '1,12p'; fi
printf 'PREFLIGHT=COMPLETE=%s\n' "$([ "$fail" -eq 0 ] && echo PASS || echo FAIL)"
exit "$fail"
