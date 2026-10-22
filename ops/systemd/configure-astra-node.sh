#!/usr/bin/env bash
set -euo pipefail

NODE_ID="${1:-}"
case "${NODE_ID}" in
  mh-dev-01|mh-dev-02|mh-dev-03) ;;
  *) echo "usage: $0 mh-dev-01|mh-dev-02|mh-dev-03" >&2; exit 2 ;;
esac

install -d -m 700 /etc/mediahub-astra
cat >/etc/mediahub-astra/node.env <<EOF
ASTRA_NODE_ID=${NODE_ID}
ASTRA_AGENT_ID=A0-ASTRA
ASTRA_POLL_SECONDS=30
ASTRA_CLAIM_LEASE_SECONDS=900
EOF
chmod 600 /etc/mediahub-astra/node.env
systemctl daemon-reload
systemctl enable --now mediahub-astra-github-bootstrap.service
systemctl restart mediahub-astra-github-bootstrap.service
echo "configured node identity: ${NODE_ID}"
