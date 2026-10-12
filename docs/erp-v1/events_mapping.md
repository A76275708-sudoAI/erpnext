# Events → DocType mapping — ERP v1 D5

Short table from PRD §3 / Spike D4. Full narrative: `/workspace/proto-bot/erpnext-spike-d4.md`.

| PRD event | Primary DocType(s) | Key custom fields / notes |
|-----------|--------------------|---------------------------|
| `OrderSynced` | **Sales Order**; optional Stock Reservation Entry (offline `lock_stock`) | `channel_type`, `requires_platform_push`, `platform_order_no`, `shop_id` |
| `StockIn` | **Purchase Receipt**; **Stock Entry** (Material Receipt / Transfer / Other) | map `in_type`; GOOD/DEFECTIVE via Rejected WH or QI |
| `PickAssigned` | **Pick List** | `picker_id`, `wave_no` |
| `LabelPrinted` | **Shipment** (+ Print Format); optional `ERP Label Print Log` | `template_version`, `reprint_count`, `printer_id` |
| `Shipped` | **Delivery Note** (Submit → SLE OUT); may link Shipment | guard: default **no Cancel** |
| `PlatformShipPushed` | Adapter / custom push log (not core DocType); optional Unicommerce later | **forbid** when offline / `requires_platform_push=0` |
| `ReturnRequested` | Draft return DN or Issue-like stub (no stock move) | keep `channel_type` |
| `ReturnReceived` | **Delivery Note** `is_return` + optional **Quality Inspection** | SLE IN; Good/Defective WH |
| `RefundSettled` | Sales Invoice Credit Note / Payment Entry **placeholder only** | `accounting_placeholder=true`; no GL in phase-1 |
| `InventoryAdjusted` | **Stock Reconciliation** (or Stock Entry by delta) | initiator ≠ approver fields later |

## Ecommerce happy path (docs)

```
Sales Order (OrderSynced)
  → Pick List (PickAssigned)
  → Shipment / Label log (LabelPrinted)
  → Delivery Note Submit (Shipped)
  → Mock push (PlatformShipPushed)  [EC only]
```

## Offline happy path

```
Sales Order (OrderSynced, OFFLINE_*, requires_platform_push=0)
  → Delivery Note Submit (Shipped)
  → PlatformShipPushed MUST NOT fire
```
