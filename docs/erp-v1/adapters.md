# Mock adapter package layout — ERP v1 (D5 spec → D6 package)

## Implemented layout (`erp_fulfillment` app)

```
erp_fulfillment/                    # repo-root Frappe app
  erp_fulfillment/
    __init__.py
    hooks.py                        # doc_events → guards; fixtures
    guards/
      platform_push.py              # G1
      delivery_note_cancel.py       # G2
      sales_order_validate.py       # G3a/G3b
    adapters/
      mock_channel/
        pull_orders.py              # B1 → OrderSynced-shaped dicts
        push_shipment.py            # B7 PlatformShipPushed (calls G1)
      mock_label/
        print_queue.py              # B5 PDF + queue state machine
    events/
      envelope.py                   # common event envelope helpers
    admin/
      force_cancel.py               # audited DN cancel override
  scripts/
    import_fixtures.py
    check_guards_offline.py
  tests/
    test_guards.py
```

Legacy stubs under `erpnext/erp_v1_stubs/guards.py` re-export the same API (fallback if app not on `PYTHONPATH`).

## Adapter rules (PRD)

- Adapters do protocol conversion only — no stock math.
- Rule bots write documents / ledger events, never mutate Bin directly.
- All BOT actions: `bot_id + trigger_event_id + idempotency_key`.
- G1 must run before any PlatformShipPushed / mock push.
