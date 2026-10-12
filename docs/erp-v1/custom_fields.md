# Custom Fields — ERP v1 D5

All fields are **Custom Field** stubs (or DocType Property Setter later).  
Naming: `snake_case` fieldnames; Chinese labels optional in UI translation.

Channel enum (shared):

```
EC_TAOBAO
EC_JD
EC_PDD
EC_DOUYIN
EC_KUAISHOU
EC_SELF
EC_MOCK
OFFLINE_POS
OFFLINE_DEALER
OFFLINE_PHONE
OFFLINE_MOCK
```

Offline set (for guards): any `channel_type` starting with `OFFLINE_`.

---

## 1. Sales Order

| fieldname | fieldtype | options / default | req | notes |
|-----------|-----------|-------------------|-----|-------|
| `channel_type` | Select | channel enum above | yes | drives platform-push policy |
| `requires_platform_push` | Check | default 0 | yes | boolean fallback if enum missed; set 1 for EC_*, 0 for OFFLINE_* |
| `platform_order_no` | Data | — | EC yes / offline **forbid** | unique with shop + channel; offline must be empty |
| `shop_id` | Data | — | EC yes / offline empty | shop / store identifier |

Suggested section: insert after `customer` (or new tab「履约渠道」).

**Unique key (B2)**: `(channel_type, shop_id, platform_order_no)` for ecommerce.  
Offline SO: `platform_order_no` must be blank; reject if filled.

---

## 2. Pick List

| fieldname | fieldtype | options / default | req | notes |
|-----------|-----------|-------------------|-----|-------|
| `picker_id` | Link | User | yes when assigned | PRD `picker_id` |
| `wave_no` | Data | — | optional | wave / batch id for B6 |

Suggested: insert after `purpose` / warehouse fields.

---

## 3. LabelPrinted / Shipment extension

Prefer extending native **Shipment** (AWB/carrier). If Shipment is unused in a flow, use a lightweight **DocType** `ERP Label Print Log` (Child or standalone) linked to Sales Order / Delivery Note.

### On Shipment (preferred)

| fieldname | fieldtype | options / default | req | notes |
|-----------|-----------|-------------------|-----|-------|
| `template_version` | Data | e.g. `mock-v1` | yes | face-sheet template evidence |
| `reprint_count` | Int | default 0 | yes | increment on explicit reprint |
| `printer_id` | Data | e.g. `MOCK_PRINTER_1` | yes | mock printer id in phase 1 |

### Optional DocType stub: `ERP Label Print Log`

If engineers prefer a note DocType instead of cluttering Shipment:

| fieldname | fieldtype | notes |
|-----------|-----------|-------|
| `sales_order` | Link → Sales Order | |
| `delivery_note` | Link → Delivery Note | optional |
| `shipment` | Link → Shipment | optional |
| `tracking_no` | Data | |
| `express_company` | Data | |
| `template_version` | Data | |
| `reprint_count` | Int | default 0 |
| `printer_id` | Data | |
| `print_status` | Select | `SUCCESS` / `FAILED` |
| `failure_reason` | Small Text | required when FAILED |

Idempotency: same `doc_no + tracking_no` keeps one SUCCESS; explicit reprint bumps `reprint_count`.

---

## 4. Implementation notes

1. Prefer Custom Field fixtures over editing core JSON of Sales Order / Pick List / Shipment.
2. Client Script: when `channel_type` changes, auto-set `requires_platform_push` (EC→1, OFFLINE→0).
3. Server validate: offline + non-empty `platform_order_no` → throw.
4. Fixture file: `fixtures/erp_v1/custom_fields.json`.
