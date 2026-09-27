#!/usr/bin/env bash
set -euo pipefail

# Canonical Astra GitHub Transport bootstrap.
# The long-running process must execute this bootstrap, not a copied agent file.
# It synchronizes main and then execs the canonical agent from the synchronized
# worktree so self-reexec/update checks operate on the same source tree.

REPO="${ASTRA_GITHUB_REPO:-VlDMlNSh/mediahub-os}"
REMOTE="${ASTRA_GITHUB_REMOTE:-git@github.com:${REPO}.git}"
WORKTREE="${ASTRA_WORKTREE:-$HOME/astra-work}"
BRANCH="${ASTRA_GITHUB_BRANCH:-main}"
AGENT="${ASTRA_AGENT_PATH:-$WORKTREE/astra_github_agent.py}"

mkdir -p "$(dirname "$WORKTREE")"

if [[ ! -d "$WORKTREE/.git" ]]; then
  git clone --depth=1 --branch "$BRANCH" "$REMOTE" "$WORKTREE"
else
  git -C "$WORKTREE" fetch --depth=1 origin "$BRANCH"
  git -C "$WORKTREE" checkout -B "$BRANCH" "origin/$BRANCH"
  git -C "$WORKTREE" reset --hard "origin/$BRANCH"
fi

test -f "$AGENT"
exec /usr/bin/env python3 "$AGENT"
