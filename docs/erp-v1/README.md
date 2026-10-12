# ERP v1 — D5 Skeleton Specs

> Pin: `erp-v1/base` ← upstream ERPNext `v15.122.0` (`bfd8100`)  
> Decision (D4): fork deep + fulfillment adapters outside SLE core  
> Audience: engineers implementing Custom Fields / hooks / roles on this fork

## Contents

| File | Purpose |
|------|---------|
| [custom_fields.md](./custom_fields.md) | Field specs on Sales Order, Pick List, Shipment / LabelPrinted note |
| [guards.md](./guards.md) | Hard reject: offline PlatformShipPushed; DN cancel policy |
| [roles.md](./roles.md) | 跟单/仓管/销售/客服/运营/财务占位/管理员 → ERPNext Role mapping |
| [events_mapping.md](./events_mapping.md) | PRD event → DocType short table |
| [adapters.md](./adapters.md) | Mock adapter package layout (no full bench required) |

## Fixtures

JSON stubs for Custom Field import live under:

```
fixtures/erp_v1/custom_fields.json
```

Import later with bench (when available):

```bash
bench --site <site> import-doc fixtures/erp_v1/custom_fields.json
# or place under hooks fixtures = ["Custom Field"] once an erp_v1 app exists
```

Until then, treat the JSON as the source of truth for fieldnames/types/options.

## Out of scope for D5

- Full Frappe bench install
- Real platform keys / printers
- Workflow engine / GL posting
- Merging to `develop` or marking PRs ready
