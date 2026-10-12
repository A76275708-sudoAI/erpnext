#!/usr/bin/env bash
# ERP v1 D7 — start frappe_docker pwd-v15 stack on the agent box (no systemd).
# Requires: docker.io installed; passwordless sudo; ~4–8G swap recommended.
set -euo pipefail
export PATH="/sbin:/usr/sbin:$PATH"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="${COMPOSE_FILE:-$REPO_ROOT/docker-compose.frappe-pwd-v15.yml}"
# Prefer frappe_docker checkout if present (volumes project name)
PROJECT_DIR="${PROJECT_DIR:-/workspace/frappe_docker}"
if [[ -d "$PROJECT_DIR" ]]; then
  COMPOSE_FILE="$PROJECT_DIR/pwd-v15.yml"
  # keep pwd-v15.yml in sync with repo copy
  cp "$REPO_ROOT/docker-compose.frappe-pwd-v15.yml" "$COMPOSE_FILE"
fi

# 1) swap
if ! swapon --show | grep -q /swapfile; then
  if [[ ! -f /swapfile ]]; then
    sudo dd if=/dev/zero of=/swapfile bs=1M count=8192 status=progress
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
  fi
  sudo swapon /swapfile || true
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# 2) dockerd (box has no systemd)
if ! docker info >/dev/null 2>&1; then
  sudo pgrep -x containerd >/dev/null || sudo containerd >/tmp/containerd.log 2>&1 &
  sleep 1
  sudo dockerd --host=unix:///var/run/docker.sock >/tmp/dockerd.log 2>&1 &
  sleep 3
  sudo chmod 666 /var/run/docker.sock || true
fi

# 3) bridge FORWARD fix (iptables-legacy DROP vs nft conflict on this box)
sudo iptables-legacy -P FORWARD ACCEPT 2>/dev/null || true
sudo iptables -P FORWARD ACCEPT 2>/dev/null || true

# 4) up
cd "$(dirname "$COMPOSE_FILE")"
docker compose -f "$(basename "$COMPOSE_FILE")" up -d
echo "Waiting for site..."
for i in $(seq 1 60); do
  code=$(curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/login || true)
  if [[ "$code" == "200" ]]; then
    echo "OK http://127.0.0.1:8080  (Administrator / admin)"
    # Re-link erp_fulfillment desk theme assets (sites/assets is per-container, not on volume)
    LINK_SCRIPT="$REPO_ROOT/erp_fulfillment/scripts/link_desk_assets.sh"
    if [[ -x "$LINK_SCRIPT" ]]; then
      COMPOSE_FILE="$COMPOSE_FILE" "$LINK_SCRIPT" || true
    fi
    exit 0
  fi
  sleep 5
done
echo "Stack up but /login not 200 yet; check: docker compose -f $COMPOSE_FILE logs create-site"
exit 0
