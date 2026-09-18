#!/usr/bin/env bash
set -euo pipefail
: "${OPENROUTER_API_KEY:?OPENROUTER_API_KEY is required; credentials are never stored in the repository}"
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"
export OPENAI_API_KEY="$OPENROUTER_API_KEY"
export OPENROUTER_API_KEY
exec codex "$@"
