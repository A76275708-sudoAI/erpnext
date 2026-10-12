# D6 Status — ERP v1 bench / fulfillment package

> Date: 2026-10-12 Asia/Shanghai (CST+8)  
> Branch: `erp-v1/d6-bench` ← from `erp-v1/d5-skeleton`  
> Ask: D6 only (future phases need re-confirm)

## Bench actually runs?

**No.** Full Frappe/ERPNext bench install was **not** completed on the agent box.

### Exact blockers

| # | Blocker | Evidence |
|---|---------|----------|
| 1 | No MariaDB/MySQL server | `mariadbd` / `mysqld` missing |
| 2 | No Redis server | `redis-server` missing (only `python3-redis` client) |
| 3 | No container runtime | `docker` / `podman` missing → cannot start `docker-compose.erp-v1.yml` |
| 4 | No yarn / frappe-bench | `yarn`, `bench` missing |
| 5 | Python too new | Box **3.13.5**; Frappe v15 wants **3.10–3.11** |
| 6 | Memory headroom | ~**3335 MiB** available / 16002 MiB total, **0 swap** — insufficient for yarn + asset builds (~6–8 GiB free recommended) |

Installing MariaDB + Redis + Node toolchain + pyenv 3.11 + bench init would exceed “reasonable time” on this box and risk OOM. Offline maximal progress delivered instead.

## What works (offline)

| Item | Status |
|------|--------|
| `erp_fulfillment` Frappe app package | ✅ scaffolded at repo root |
| G1 `assert_platform_push_allowed` + mock B7 push | ✅ offline tested |
| G2 DN cancel ban + `force_cancel_delivery_note` stub | ✅ offline tested / admin path needs live site |
| G3a/G3b Sales Order validate | ✅ offline tested |
| hooks.py doc_events wiring | ✅ present (activates after `install-app`) |
| Fixture dry-run import path | ✅ `python erp_fulfillment/scripts/import_fixtures.py --dry-run` → 7 roles, 9 fields |
| `docker-compose.erp-v1.yml` + `scripts/install-bench-erp-v1.sh` | ✅ written for capable machine |
| `docs/erp-v1/install.md` | ✅ |
| `erpnext.erp_v1_stubs.guards` re-export | ✅ fallback if app not on path |

Offline smoke: `python erp_fulfillment/scripts/check_guards_offline.py` → **ALL PASSED**.

## Needs machine resources

1. Workstation/VM: Python 3.10/3.11, Node 18+, yarn, MariaDB 10.6+, Redis 6+, ≥8 GiB free RAM.
2. Run `docker compose -f docker-compose.erp-v1.yml up -d` (or native MariaDB/Redis).
3. Run `./scripts/install-bench-erp-v1.sh`.
4. Confirm site boots; create 7 role test users; smoke G1/G2 on live DN/SO.

## Next confirm-needed step (beyond D6)

- **D7 candidate (ask first):** live bench on a provisioned machine + master data + 7 login accounts + end-to-end Mock EC_MOCK / OFFLINE_MOCK path.  
- Do **not** merge to `develop`/`main`; keep PRs draft until product confirm.

## File list (D6 add/change)

```
erp_fulfillment/                         # new app
  README.md
  pyproject.toml
  setup.py
  erp_fulfillment/__init__.py
  erp_fulfillment/hooks.py
  erp_fulfillment/modules.txt
  erp_fulfillment/patches.txt
  erp_fulfillment/guards/{__init__,platform_push,delivery_note_cancel,sales_order_validate}.py
  erp_fulfillment/adapters/mock_channel/{__init__,pull_orders,push_shipment}.py
  erp_fulfillment/adapters/mock_label/{__init__,print_queue}.py
  erp_fulfillment/events/{__init__,envelope}.py
  erp_fulfillment/admin/{__init__,force_cancel}.py
  erp_fulfillment/scripts/{__init__,import_fixtures}.py
  scripts/{import_fixtures,check_guards_offline}.py
  tests/{__init__,test_guards}.py
docker-compose.erp-v1.yml
scripts/install-bench-erp-v1.sh
docs/erp-v1/install.md
docs/erp-v1/{README,adapters,guards}.md   # updated
fixtures/erp_v1/README.md                 # updated
erpnext/erp_v1_stubs/{__init__,guards}.py # re-export
```

Plus workspace notes: `/workspace/proto-bot/d6-status.md`, updated `d5-plan.md`.
