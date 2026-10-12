# Mock adapter package layout — ERP v1 D5

No full bench required for D5. This documents where B1/B5/B7 adapters should live so engineers do not edit SLE core.

## Recommended layout (future app `erp_fulfillment`)

```
apps/erp_fulfillment/          # or repo-root package until split
  erp_fulfillment/
    __init__.py
    hooks.py                   # doc_events → guards; fixtures
    guards/
      platform_push.py         # G1
      delivery_note_cancel.py  # G2
    adapters/
      mock_channel/
        pull_orders.py         # B1 → OrderSynced / Sales Order
        push_shipment.py       # B7 PlatformShipPushed (EC only)
      mock_label/
        print_queue.py         # B5 PDF + queue state machine
    events/
      envelope.py              # common event envelope helpers
    fixtures/                  # symlink or copy from fixtures/erp_v1
```

Until the app is scaffolded, treat:

- Specs: `docs/erp-v1/*`
- Field/role JSON: `fixtures/erp_v1/*`

as the contract.

## Adapter rules (PRD)

- Adapters do protocol conversion only — no stock math.
- Rule bots write documents / ledger events, never mutate Bin directly.
- All BOT actions: `bot_id + trigger_event_id + idempotency_key`.
