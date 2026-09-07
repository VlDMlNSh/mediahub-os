#!/usr/bin/env bash
set -euo pipefail

# MediaHub reference development host bootstrap.
# This script is intentionally fail-closed: privileged package installation is
# explicit and interactive; it never accepts or stores a password or secret.

readonly VENV="${HOME}/.venvs/mediahub-dev"
readonly CONFIG_DIR="${HOME}/.config/mediahub"
readonly TOOLCHAIN_FILE="${CONFIG_DIR}/dev-toolchain.env"

need_root() {
  if ! sudo -n true 2>/dev/null; then
    echo "BLOCKED: one-time administrator authentication is required for system packages." >&2
    echo "Run this script interactively on the host; do not provide a sudo password to an agent." >&2
    exit 20
  fi
}

install_system_packages() {
  need_root
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends \
    python3.12-venv python3-pip pipx \
    jq ripgrep fd-find shellcheck shfmt pre-commit age
}

install_python_stack() {
  python3 -m venv "${VENV}"
  "${VENV}/bin/python" -m pip install --upgrade pip setuptools wheel
  "${VENV}/bin/pip" install pytest pytest-cov bandit pip-audit
}

configure_user_environment() {
  install -d -m 700 "${CONFIG_DIR}"
  cat > "${TOOLCHAIN_FILE}" <<'EOF'
export MEDIAHUB_DEV_VENV="${HOME}/.venvs/mediahub-dev"
export PATH="${MEDIAHUB_DEV_VENV}/bin:${HOME}/.local/bin:${PATH}"
EOF
  chmod 600 "${TOOLCHAIN_FILE}"
}

verify() {
  source "${TOOLCHAIN_FILE}"
  python --version
  pytest --version
  bandit --version
  pip-audit --version
  jq --version
  rg --version | head -1
  shellcheck --version | head -2
  shfmt --version
  pre-commit --version
  age --version
}

install_system_packages
install_python_stack
configure_user_environment
verify
printf '%s\n' "REFERENCE_DEV_BOOTSTRAP=PASS"
