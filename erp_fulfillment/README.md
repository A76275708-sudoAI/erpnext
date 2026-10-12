# erp_fulfillment — ERP v1 D6

Frappe app package for ecommerce + offline fulfillment guards and Mock adapters.

Pinned against fork base `erp-v1/base` (ERPNext `v15.122.0`).

## What this app does (D6)

| Capability | Status |
|------------|--------|
| G1 reject `PlatformShipPushed` for `OFFLINE_*` / `requires_platform_push=0` | Hook wired in `hooks.py` + pure-Python guards (importable offline) |
| G2 ban Delivery Note cancel (admin override path stub) | Hook wired + `admin.force_cancel` stub |
| Fixture import for `fixtures/erp_v1/*.json` | Script + bench path documented |
| Mock B1 / B5 / B7 adapters | Stubs only (no network) |
| Full bench site | **Not run on D6 box** — see `docs/erp-v1/install.md` + `/workspace/proto-bot/d6-status.md` |

## Install into an existing bench

```bash
# from bench root
ln -s /path/to/this/repo/erp_fulfillment apps/erp_fulfillment
# or: bench get-app /path/to/this/repo/erp_fulfillment
bench --site <site> install-app erp_fulfillment
bench --site <site> execute erp_fulfillment.scripts.import_fixtures.run
# or:
python apps/erp_fulfillment/scripts/import_fixtures.py --site <site>
```

## Offline guard smoke test (no Frappe)

```bash
cd erp_fulfillment
python -m pytest tests/ -q
# or:
python scripts/check_guards_offline.py
```

## Layout

```
erp_fulfillment/
  erp_fulfillment/
    hooks.py                 # doc_events + fixtures registration
    guards/                  # G1 / G2 / G3
    adapters/mock_channel/   # B1 pull, B7 push
    adapters/mock_label/     # B5 print queue
    events/envelope.py
    admin/force_cancel.py    # audited DN cancel override
  scripts/import_fixtures.py
  tests/test_guards.py
```
