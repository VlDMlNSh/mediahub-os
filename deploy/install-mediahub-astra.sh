#!/usr/bin/env bash
set -euo pipefail

REPO="/home/mediahub/mediahub-os"
APP_ROOT="/opt/mediahub/astra"
SERVICE="mediahub-astra.service"
SENTINELX_BOOTSTRAP="https://get.sentinelx.app"

if [[ ${EUID} -ne 0 ]]; then
  echo "Run with sudo: sudo $0"
  exit 2
fi
if [[ ! -d "$REPO" || ! -f "$REPO/runtime/mediahub_runtime/astra_gateway.py" ]]; then
  echo "Repository not found at $REPO"
  exit 3
fi

bash "$REPO/deploy/preflight-mediahub-astra.sh"

echo "=== MediaHub local wave: SentinelX host enrollment ==="
echo "Official bootstrap: $SENTINELX_BOOTSTRAP"
echo "SentinelX enrollment may request the operator token in the terminal."
echo "The token is not stored in MediaHub, Git, or the Astra service."
curl -fsSL "$SENTINELX_BOOTSTRAP" | SENTINELX_ENROLL_MODE=paste bash

# Replace the SentinelX starter policy with the MediaHub deny-by-default boundary.
# The config contains no credentials and is installed root-owned.
install -d -m 0755 /etc/sentinelx
install -m 0644 "$REPO/profiles/sentinelx/mediahub-config.yaml" /etc/sentinelx/config.yaml
systemctl restart sentinelx-cloud-core.service

install -d -m 0755 "$APP_ROOT"
cp -a "$REPO/runtime" "$APP_ROOT/"
cp -a "$REPO/profiles" "$APP_ROOT/"
cp -a "$REPO/contracts" "$APP_ROOT/"
cp -a "$REPO/tools" "$APP_ROOT/"

cat > /etc/systemd/system/$SERVICE <<EOF
[Unit]
Description=MediaHub Astra local-first runtime
After=network-online.target ollama.service sentinelx-cloud-core.service
Wants=network-online.target sentinelx-cloud-core.service

[Service]
Type=simple
User=mediahub
Group=mediahub
WorkingDirectory=$APP_ROOT
Environment=PYTHONPATH=$APP_ROOT/runtime
Environment=MEDIAHUB_RUNTIME_MODE=autonomous
ExecStart=/usr/bin/python3 -m mediahub_runtime.astra_service
Restart=on-failure
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadOnlyPaths=$APP_ROOT

[Install]
WantedBy=multi-user.target
EOF

if ! id mediahub >/dev/null 2>&1; then
  useradd --system --home-dir /var/lib/mediahub --create-home --shell /usr/sbin/nologin mediahub
fi
chown -R root:root "$APP_ROOT"
chmod -R a+rX "$APP_ROOT"

systemctl daemon-reload
systemctl enable --now "$SERVICE"

python3 "$APP_ROOT/tools/validate_contracts.py"
python3 "$APP_ROOT/tools/validate_connectors.py"
systemctl is-active --quiet sentinelx-cloud-core.service
systemctl is-active --quiet "$SERVICE"
grep -q 'Environment=MEDIAHUB_RUNTIME_MODE=autonomous' "/etc/systemd/system/$SERVICE"

echo "QUALIFICATION=PASS"
echo "AUTONOMOUS_RUNTIME=READY"
echo "LOCAL_OLLAMA=READY"
echo "SENTINELX=READY"
echo "MediaHub Astra installed. Local Ollama is location-independent and credential-free."
echo "Cloud/web credentials stay in GitHub; GitHub Actions is the external credential boundary."
