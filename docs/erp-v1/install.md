# ERP v1 — Bench install + fixture import (D6)

## Box feasibility (agent / this environment)

Full Frappe/ERPNext bench was **not** completed on the D6 agent box. Blockers:

| Blocker | Detail |
|---------|--------|
| No MariaDB/MySQL server | `mariadb`/`mysql` server binaries absent; no Docker to run `docker-compose.erp-v1.yml` |
| No Redis server | Only `python3-redis` client library present |
| No Docker / Podman | Cannot bring up compose services |
| Memory | ~3.3 GiB available / 16 GiB total, 0 swap — yarn + bench asset builds typically need ≥6–8 GiB free |
| Python | Box has **3.13**; Frappe v15 supports **3.10–3.11** |

Delivered instead: `erp_fulfillment` app package, hooks wiring, offline-tested guards, import script, compose + install script for a proper machine.

## On a capable machine

### Option A — script

```bash
# prerequisites: Python 3.10/3.11, Node 18+, yarn, MariaDB, Redis
docker compose -f docker-compose.erp-v1.yml up -d   # if using compose for DB/Redis
export MYSQL_ROOT_PASSWORD=erp_v1_root
./scripts/install-bench-erp-v1.sh
```

### Option B — manual

```bash
bench init --frappe-branch version-15 ~/frappe-bench-erp-v1
cd ~/frappe-bench-erp-v1
bench get-app --branch erp-v1/d6-bench https://github.com/A76275708-sudoAI/erpnext.git
ln -s /path/to/checkout/erp_fulfillment apps/erp_fulfillment
bench new-site erp-v1.localhost
bench --site erp-v1.localhost install-app erpnext
bench --site erp-v1.localhost install-app erp_fulfillment
export ERP_V1_FIXTURES_DIR=/path/to/checkout/fixtures/erp_v1
bench --site erp-v1.localhost execute erp_fulfillment.scripts.import_fixtures.run
```

## Fixture import only

```bash
# validate JSON without Frappe
python erp_fulfillment/scripts/import_fixtures.py --dry-run

# live import
bench --site <site> execute erp_fulfillment.scripts.import_fixtures.run
# or
ERP_V1_FIXTURES_DIR=/path/to/fixtures/erp_v1 \
  python erp_fulfillment/scripts/import_fixtures.py --site <site>
```

Files:

- `fixtures/erp_v1/custom_fields.json`
- `fixtures/erp_v1/roles.json`

## Hook registration

`erp_fulfillment/erp_fulfillment/hooks.py` registers:

| DocType | Event | Handler |
|---------|-------|---------|
| Sales Order | `validate` | G3a/G3b channel field checks |
| Delivery Note | `before_cancel` | G2 cancel ban |

G1 is enforced inside `adapters.mock_channel.push_shipment.push_platform_shipment` (and can be called from future DocType `validate`).

Admin override: `erp_fulfillment.admin.force_cancel.force_cancel_delivery_note(dn_name, reason)`.

## Offline verification (no bench)

```bash
cd erp_fulfillment
python scripts/check_guards_offline.py
# or: python -m pytest tests/ -q
```
