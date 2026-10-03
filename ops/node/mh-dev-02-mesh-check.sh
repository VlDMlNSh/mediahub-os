#!/usr/bin/env bash
set -euo pipefail
source /etc/mediahub/node-profile.env
printf 'node_id=%s\n' "$MEDIAHUB_NODE_ID"
printf 'role=%s\n' "$MEDIAHUB_NODE_ROLE"
command -v codex || true
command -v claude || true
command -v ollama || true
command -v bwrap || true
command -v ffmpeg || true
command -v transmission-cli || true
command -v ipfs || true
test -x /home/mediahub/llama.cpp/build/bin/llama-cli && echo 'llama_cli=present' || echo 'llama_cli=missing'
test -x /home/mediahub/llama.cpp/build/bin/llama-server && echo 'llama_server=present' || echo 'llama_server=missing'
test -x /home/mediahub/.local/bin/fcc-codex && echo 'fcc_codex=present' || echo 'fcc_codex=missing'
test -x /home/mediahub/.local/bin/fcc-claude && echo 'fcc_claude=present' || echo 'fcc_claude=missing'
test -x /opt/OmniRoute/omniroute-desktop && echo 'omniroute_embedded=present' || echo 'omniroute_embedded=missing'
printf 'mesh_fail_closed=1\n'
printf 'astra_gold_autolaunch=0\n'
