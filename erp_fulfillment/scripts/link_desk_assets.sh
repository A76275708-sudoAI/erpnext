#!/usr/bin/env bash
# Link erp_fulfillment public assets into each container's /home/frappe/frappe-bench/assets
# (sites/assets is a symlink to that path and is NOT on the shared sites volume).
set -euo pipefail
COMPOSE="${COMPOSE_FILE:-/workspace/frappe_docker/pwd-v15.yml}"
PROJECT_DIR="$(dirname "$COMPOSE")"
for svc in frontend backend queue-short scheduler websocket; do
  cid=$(docker compose -f "$COMPOSE" ps -q "$svc" 2>/dev/null || true)
  [[ -z "$cid" ]] && continue
  docker exec -u root "$cid" bash -c '
    APP_PUB=/home/frappe/frappe-bench/apps/erp_fulfillment/erp_fulfillment/public
    ASSETS_ROOT=/home/frappe/frappe-bench/assets
    if [[ -d "$APP_PUB" ]]; then
      mkdir -p "$ASSETS_ROOT"
      ln -sfn "$APP_PUB" "$ASSETS_ROOT/erp_fulfillment"
      echo "linked erp_fulfillment assets in $(hostname)"
    fi
  '
done
