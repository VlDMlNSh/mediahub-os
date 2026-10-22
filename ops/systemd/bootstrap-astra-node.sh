#!/usr/bin/env bash
set -euo pipefail
NODE_ID="${1:-}"
case "${NODE_ID}" in mh-dev-01|mh-dev-02|mh-dev-03) ;; *) echo "usage: $0 mh-dev-01|mh-dev-02|mh-dev-03" >&2; exit 2 ;; esac
ROOT=/home/mediahub/astra-work
STATE=/var/lib/mediahub-astra
DATA=/srv/mediahub
CFG=/etc/mediahub-astra
sudo install -d -m 0755 "${ROOT}" "${STATE}" "${DATA}" "${CFG}"
sudo install -d -m 0700 "${STATE}/queue" "${STATE}/evidence"
sudo install -d -m 0755 "${DATA}/models" "${DATA}/cache" "${DATA}/datasets" "${DATA}/backups" "${DATA}/tmp"
cat <<EOF | sudo tee "${CFG}/node.env" >/dev/null
ASTRA_NODE_ID=${NODE_ID}
ASTRA_AGENT_ID=A0-ASTRA
ASTRA_POLL_SECONDS=30
ASTRA_CLAIM_LEASE_SECONDS=900
ASTRA_WORKTREE=${ROOT}
ASTRA_STATE_DIR=${STATE}
EOF
sudo chmod 600 "${CFG}/node.env"
PKGS=(git curl ca-certificates jq python3 python3-venv python3-pip build-essential pkg-config bubblewrap ffmpeg protobuf-compiler restic sops age)
AVAILABLE=()
for p in "${PKGS[@]}"; do
  if apt-cache show "$p" >/dev/null 2>&1; then AVAILABLE+=("$p"); else echo "MISSING_FROM_APT $p"; fi
done
if (("${#AVAILABLE[@]}" )); then
  sudo apt-get update
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${AVAILABLE[@]}"
fi
case "${NODE_ID}" in
 mh-dev-01) echo CONTROL_TRANSPORT_ONLY ;;
 mh-dev-02) sudo install -d -m 0755 "${DATA}/models/ollama" "${DATA}/models/llama.cpp"; echo PROVIDER_EXECUTION_NODE ;;
 mh-dev-03) sudo install -d -m 0755 "${ROOT}/evidence" "${DATA}/backups"; echo QUALIFICATION_RECOVERY_NODE ;;
esac
if [[ ! -d "${ROOT}/.git" ]]; then
  git clone --depth=1 --branch main git@github.com:VlDMlNSh/mediahub-os.git "${ROOT}"
else
  git -C "${ROOT}" fetch origin main --quiet
  git -C "${ROOT}" reset --hard origin/main
fi
python3 -m venv "${ROOT}/.venv"
"${ROOT}/.venv/bin/pip" install --upgrade pip
"${ROOT}/.venv/bin/pip" install -r "${ROOT}/requirements-dev.txt"
"${ROOT}/.venv/bin/python" "${ROOT}/ops/qualification/inventory_local_components.py" > "${STATE}/inventory.json"
echo "Bootstrap complete: installation prepared; qualification remains a separate gate."
