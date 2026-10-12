#!/usr/bin/env bash
# ERP v1 D6 — create a Frappe bench, get ERPNext v15.122.0 + erp_fulfillment, import fixtures.
# Run on a workstation/VM with: Python 3.10–3.11, Node 18+, MariaDB, Redis, yarn, ~8 GiB RAM.
# Do NOT expect this to succeed on the constrained agent box (see docs/erp-v1/install.md).
set -euo pipefail

PIN_TAG="${ERPNEXT_PIN_TAG:-v15.122.0}"
BENCH_DIR="${BENCH_DIR:-$HOME/frappe-bench-erp-v1}"
SITE="${SITE:-erp-v1.localhost}"
ADMIN_PASS="${ADMIN_PASS:-admin}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FORK_URL="${FORK_URL:-https://github.com/A76275708-sudoAI/erpnext.git}"
BRANCH="${BRANCH:-erp-v1/d6-bench}"

echo "==> preflight"
command -v python3 >/dev/null
command -v node >/dev/null
command -v yarn >/dev/null || { echo "yarn required"; exit 1; }
command -v mysql >/dev/null || command -v mariadb >/dev/null || {
  echo "MariaDB/MySQL client required; start docker-compose.erp-v1.yml first"
  exit 1
}
python3 - <<'PY'
import sys
v = sys.version_info
if v[:2] not in ((3, 10), (3, 11)):
    print(f"WARN: Frappe v15 prefers Python 3.10/3.11; found {sys.version}")
PY

echo "==> pip install frappe-bench"
python3 -m pip install --user frappe-bench

echo "==> bench init ${BENCH_DIR} (frappe ${PIN_TAG} line)"
# frappe-bench pin: use version-15 for frappe framework
if [[ ! -d "$BENCH_DIR" ]]; then
  bench init --frappe-branch version-15 "$BENCH_DIR"
fi
cd "$BENCH_DIR"

echo "==> get-app erpnext from fork @ ${BRANCH} (fallback tag ${PIN_TAG})"
if [[ ! -d apps/erpnext ]]; then
  bench get-app --branch "$BRANCH" "$FORK_URL" || \
    bench get-app --branch "$PIN_TAG" https://github.com/frappe/erpnext.git
fi

echo "==> link erp_fulfillment from fork checkout"
FULFILL_SRC="${FULFILL_SRC:-$REPO_ROOT/erp_fulfillment}"
if [[ ! -d apps/erp_fulfillment ]]; then
  if [[ -d "$FULFILL_SRC/erp_fulfillment" ]]; then
    ln -sfn "$FULFILL_SRC" apps/erp_fulfillment
  else
    echo "erp_fulfillment not found at $FULFILL_SRC"
    exit 1
  fi
fi

echo "==> create site ${SITE}"
if [[ ! -d "sites/$SITE" ]]; then
  bench new-site "$SITE" --admin-password "$ADMIN_PASS" --mariadb-root-password "${MYSQL_ROOT_PASSWORD:-erp_v1_root}"
fi

bench --site "$SITE" install-app erpnext
bench --site "$SITE" install-app erp_fulfillment

echo "==> import fixtures"
export ERP_V1_FIXTURES_DIR="${ERP_V1_FIXTURES_DIR:-$REPO_ROOT/fixtures/erp_v1}"
bench --site "$SITE" execute erp_fulfillment.scripts.import_fixtures.run

echo "==> DONE. Start with: cd $BENCH_DIR && bench start"
echo "    Site: $SITE  Admin: Administrator / $ADMIN_PASS"
