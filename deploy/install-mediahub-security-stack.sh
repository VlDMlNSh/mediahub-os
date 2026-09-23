#!/usr/bin/env bash
set -euo pipefail

# MediaHub OS security/edge stack installer.
# Naabu + Caddy + Authelia. No credentials, paid services, or architecture changes.
# Root mode: system integration. Non-root mode: user-local binaries.

NAABU_VERSION="${NAABU_VERSION:-2.6.1}"
CADDY_VERSION="${CADDY_VERSION:-2.11.4}"
AUTHELIA_VERSION="${AUTHELIA_VERSION:-4.39.28}"
PREFIX="${MEDIAHUB_BIN_PREFIX:-$HOME/.local/bin}"
SRC="${MEDIAHUB_SRC_PREFIX:-$HOME/.local/src/mediahub-security}"
REPO="${MEDIAHUB_REPO:-/home/mediahub/mediahub-os}"

log(){ printf '[mediahub-security] %s\n' "$*"; }
fail(){ printf '[mediahub-security] ERROR: %s\n' "$*" >&2; exit 1; }

command -v curl >/dev/null || fail 'curl is required'
command -v tar >/dev/null || fail 'tar is required'
command -v python3 >/dev/null || fail 'python3 is required'
mkdir -p "$PREFIX" "$SRC"
chmod 0755 "$PREFIX" "$SRC"

install_naabu(){
  local archive="$SRC/naabu_${NAABU_VERSION}_linux_amd64.zip"
  local dir="$SRC/naabu-${NAABU_VERSION}"
  mkdir -p "$dir"
  if [[ ! -x "$PREFIX/naabu" ]]; then
    log "Installing Naabu ${NAABU_VERSION}"
    curl -fL --proto '=https' --tlsv1.2 "https://github.com/projectdiscovery/naabu/releases/download/v${NAABU_VERSION}/naabu_${NAABU_VERSION}_linux_amd64.zip" -o "$archive"
    python3 - "$archive" "$dir" <<'PY'
import sys, zipfile
archive, out = sys.argv[1:]
with zipfile.ZipFile(archive) as z:
    names = z.namelist()
    if not any(n.endswith('/naabu') or n == 'naabu' for n in names):
        raise SystemExit('Naabu binary not present in archive')
    z.extractall(out)
PY
    find "$dir" -type f -name naabu -exec install -m 0755 {} "$PREFIX/naabu" \;
  fi
  "$PREFIX/naabu" -version >/dev/null
}

install_caddy(){
  local archive="$SRC/caddy_${CADDY_VERSION}_linux_amd64.tar.gz"
  if [[ ! -x "$PREFIX/caddy" ]]; then
    log "Installing Caddy ${CADDY_VERSION}"
    curl -fL --proto '=https' --tlsv1.2 "https://github.com/caddyserver/caddy/releases/download/v${CADDY_VERSION}/caddy_${CADDY_VERSION}_linux_amd64.tar.gz" -o "$archive"
    tar -xzf "$archive" -C "$SRC"
    test -f "$SRC/caddy"
    install -m 0755 "$SRC/caddy" "$PREFIX/caddy"
  fi
  "$PREFIX/caddy" version >/dev/null
}

install_authelia(){
  local archive="$SRC/authelia-v${AUTHELIA_VERSION}-linux-amd64.tar.gz"
  local dir="$SRC/authelia-${AUTHELIA_VERSION}"
  mkdir -p "$dir"
  if [[ ! -x "$PREFIX/authelia" ]]; then
    log "Installing Authelia ${AUTHELIA_VERSION}"
    curl -fL --proto '=https' --tlsv1.2 "https://github.com/authelia/authelia/releases/download/v${AUTHELIA_VERSION}/authelia-v${AUTHELIA_VERSION}-linux-amd64.tar.gz" -o "$archive"
    tar -xzf "$archive" -C "$dir"
    find "$dir" -type f -name authelia -exec install -m 0755 {} "$PREFIX/authelia" \;
  fi
  "$PREFIX/authelia" --version >/dev/null
}

prepare_root_integration(){
  [[ "${EUID}" -eq 0 ]] || return 0
  log 'Preparing system integration; services remain disabled until configuration is supplied.'
  install -d -m 0755 /etc/mediahub/security /var/lib/authelia
  install -m 0755 "$PREFIX/naabu" /usr/local/bin/naabu
  install -m 0755 "$PREFIX/caddy" /usr/local/bin/caddy
  install -m 0755 "$PREFIX/authelia" /usr/local/bin/authelia
  id caddy >/dev/null 2>&1 || useradd --system --home /var/lib/caddy --shell /usr/sbin/nologin caddy
  id authelia >/dev/null 2>&1 || useradd --system --home /var/lib/authelia --shell /usr/sbin/nologin authelia
  chown -R authelia:authelia /var/lib/authelia
  cat >/etc/systemd/system/mediahub-caddy.service <<'UNIT'
[Unit]
Description=MediaHub Caddy edge proxy
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/caddy run --config /etc/mediahub/security/Caddyfile --adapter caddyfile
ExecReload=/usr/local/bin/caddy reload --config /etc/mediahub/security/Caddyfile --adapter caddyfile
Restart=on-failure
RestartSec=5s
User=caddy
Group=caddy
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/caddy /var/log/caddy

[Install]
WantedBy=multi-user.target
UNIT
  cat >/etc/systemd/system/mediahub-authelia.service <<'UNIT'
[Unit]
Description=MediaHub Authelia authentication gateway
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/authelia --config /etc/mediahub/security/configuration.yml
Restart=on-failure
RestartSec=5s
User=authelia
Group=authelia
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/authelia

[Install]
WantedBy=multi-user.target
UNIT
  systemctl daemon-reload
}

verify(){
  log 'Verification'
  "$PREFIX/naabu" -version
  "$PREFIX/caddy" version
  "$PREFIX/authelia" --version
  [[ ! -e "$REPO/.env" ]] || fail 'Refusing to touch repository .env'
  [[ -f "$REPO/tools/validate_connectors.py" ]] && (cd "$REPO" && python3 tools/validate_connectors.py)
  [[ -f "$REPO/tools/validate_host_registration.py" ]] && (cd "$REPO" && python3 tools/validate_host_registration.py)
  [[ -f "$REPO/tools/validate_contracts.py" ]] && (cd "$REPO" && python3 tools/validate_contracts.py)
}

install_naabu
install_caddy
install_authelia
prepare_root_integration
verify
log 'INSTALLATION=PASS'
log 'CREDENTIALS_CREATED=NO'
log 'PAID_CLOUD_ENABLED=NO'
[[ "${EUID}" -eq 0 ]] && log 'SYSTEM_SERVICES=PREPARED_DISABLED' || log 'INSTALL_MODE=USER_LOCAL'
