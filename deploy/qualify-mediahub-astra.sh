#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/mediahub/astra"

[[ -f "$ROOT/runtime/mediahub_runtime/astra_gateway.py" ]]
python3 "$ROOT/tools/validate_contracts.py"
python3 "$ROOT/tools/validate_connectors.py"
python3 -m compileall -q "$ROOT/runtime" "$ROOT/tools"

systemctl is-active --quiet ollama.service
curl -fsS http://127.0.0.1:11434/api/tags >/dev/null
systemctl is-active --quiet sentinelx-cloud-core.service
systemctl is-active --quiet mediahub-astra.service

grep -q 'Environment=MEDIAHUB_RUNTIME_MODE=autonomous'   /etc/systemd/system/mediahub-astra.service

[[ -f /etc/sentinelx/config.yaml ]]
grep -q '^disabled_ops:' /etc/sentinelx/config.yaml
grep -q '^  - script_run$' /etc/sentinelx/config.yaml
grep -q '^exec_strict: true$' /etc/sentinelx/config.yaml
grep -q '/home/mediahub/mediahub-os' /etc/sentinelx/config.yaml

echo "QUALIFICATION=PASS"
echo "AUTONOMOUS_RUNTIME=READY"
echo "LOCAL_OLLAMA=READY"
echo "SENTINELX=READY"
