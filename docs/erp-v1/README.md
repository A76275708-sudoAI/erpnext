# ERP v1 — Specs + D6 fulfillment app

> Pin: `erp-v1/base` ← upstream ERPNext `v15.122.0` (`bfd8100`)  
> Decision (D4): fork deep + fulfillment adapters outside SLE core  
> D5: field/guard/role specs + JSON fixtures  
> D6: `erp_fulfillment` app package, hooks, fixture import path, install scripts

## Specs

| File | Purpose |
|------|---------|
| [custom_fields.md](./custom_fields.md) | Field specs on Sales Order, Pick List, Shipment / LabelPrinted note |
| [guards.md](./guards.md) | Hard reject: offline PlatformShipPushed; DN cancel policy |
| [roles.md](./roles.md) | 跟单/仓管/销售/客服/运营/财务占位/管理员 → ERPNext Role mapping |
| [events_mapping.md](./events_mapping.md) | PRD event → DocType short table |
| [adapters.md](./adapters.md) | Mock adapter package layout |
| [install.md](./install.md) | Bench install + fixture import (D6) |

## Runtime package

```
erp_fulfillment/          # Frappe app (install into bench)
  erp_fulfillment/
    hooks.py              # Sales Order validate + DN before_cancel
    guards/               # G1 / G2 / G3
    adapters/             # Mock B1 / B5 / B7
  scripts/import_fixtures.py
```

Fixtures (source of truth until site exists):

```
fixtures/erp_v1/custom_fields.json
fixtures/erp_v1/roles.json
```

## Out of scope until confirmed

- Merge to `develop` / `main`
- Mark draft PRs ready
- Full bench on agent box (see install.md blockers)
- Real platform keys / printers / GL posting
