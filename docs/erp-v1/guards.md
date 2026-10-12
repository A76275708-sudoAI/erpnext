# Guards — ERP v1 D5 (hard rejects)

These are **acceptance vetoes**. Implement as server hooks / whitelisted method checks.  
Do not soft-warn and continue.

---

## G1 — Reject `PlatformShipPushed` for offline channels

**PRD**: offline channel must never produce platform ship-push (veto if any offline row appears in push logs).

### When

Before creating / submitting any document or event that means「平台发货回传」:

- Mock adapter call `push_platform_shipment(...)`
- Future Unicommerce / marketplace manifest
- Custom DocType `ERP Platform Ship Push` (if introduced)

### Rule

```
IF sales_order.channel_type startswith "OFFLINE_"
   OR sales_order.requires_platform_push == 0
THEN reject with error code ERP_V1_OFFLINE_PUSH_FORBIDDEN
```

Prefer checking **both** `channel_type` and `requires_platform_push` (boolean fallback).

### Suggested hook sites

| Site | Hook | Action |
|------|------|--------|
| Adapter B7 | before HTTP / mock push | raise |
| Custom DocType validate | `validate` | raise |
| Delivery Note `on_submit` | do **not** auto-push offline SO | only enqueue push when requires_platform_push=1 |

### Error message (zh)

> 线下渠道禁止平台发货回传（channel_type={channel_type}）。请勿对 OFFLINE_* 订单调用 PlatformShipPushed。

Log at severity **error** + alert channel for ops.

---

## G2 — Reject Delivery Note cancel (default)

**PRD**: once `Shipped` (DN submitted), business state must not roll back via cancel.  
Correction path = return Delivery Note (`is_return`) + QC, not Cancel.

### Native conflict

ERPNext allows Cancel on submitted DN → reverse SLE. That breaks「已发货不可回退」even though SLE remains auditable.

### Rule

```
ON Delivery Note before_cancel / on_cancel:
  IF not admin_override_path:
    reject with ERP_V1_DN_CANCEL_FORBIDDEN
```

### Admin override path (documented exception)

Only when **all** of the following hold:

1. Session user has Role **「ERP v1 管理员」** (or System Manager during phase-1 bootstrap).
2. Explicit flag on the cancel call, e.g. `frappe.flags.erp_v1_allow_dn_cancel = True` set only by a whitelisted admin method `erp_v1.admin.force_cancel_delivery_note(dn_name, reason)`.
3. `reason` (min 10 chars) written to Error Log / Activity Log / Comment on the DN.
4. Audit: actor_id, timestamp, dn_name, reason retained ≥ 180 days (same as BOT log retention).

UI: hide Cancel for non-admin roles via Role Permission / Client Script.  
Admin UI may show Cancel but must go through the whitelisted method (not stock Cancel button alone).

### Error message (zh)

> 已发货 Delivery Note 默认禁止取消。纠错请走退货 Delivery Note（is_return）。管理员强制取消须调用 force_cancel_delivery_note 并填写原因。

### Correction path (engineers)

1. Create return DN against original DN / SO.
2. Optional Quality Inspection → Good / Defective warehouse.
3. Stock effect via return submit (SLE IN) — never by cancelling original ship.

---

## G3 — Related soft guards (phase-1 stubs)

| ID | Rule | Severity |
|----|------|----------|
| G3a | Offline SO with non-empty `platform_order_no` | hard reject on validate |
| G3b | EC SO missing `platform_order_no` or `shop_id` | hard reject / exception pool |
| G3c | Explicit label reprint without bumping `reprint_count` | hard reject |

Hook module placeholder path (when app exists):

```
erp_fulfillment/erp_fulfillment/guards/
  platform_push.py
  delivery_note_cancel.py
```
