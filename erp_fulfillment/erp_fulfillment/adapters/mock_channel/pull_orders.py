"""B1 — Mock pull → OrderSynced / Sales Order draft fields.

No network. Returns deterministic sample payloads for EC_MOCK / OFFLINE_MOCK.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def pull_mock_orders(channel_type: str = "EC_MOCK", limit: int = 1) -> list[dict[str, Any]]:
    """Return mock OrderSynced-shaped dicts (not yet inserted as SO)."""
    now = datetime.now(timezone.utc).isoformat()
    out: list[dict[str, Any]] = []
    for i in range(max(1, limit)):
        offline = channel_type.startswith("OFFLINE_")
        out.append(
            {
                "event_id": str(uuid4()),
                "event_type": "OrderSynced",
                "schema_version": "1.0",
                "occurred_at": now,
                "source": f"mock:{channel_type}",
                "actor_type": "BOT",
                "actor_id": "bot:B1",
                "idempotency_key": f"mock-{channel_type}-{i}-{now}",
                "correlation_id": str(uuid4()),
                "channel_type": channel_type,
                "requires_platform_push": 0 if offline else 1,
                "stock_effect": "NONE",
                "doc_no": None,  # filled by B2 / SO naming
                "platform_order_no": None if offline else f"MOCK-PO-{i+1:04d}",
                "shop_id": None if offline else "mock-shop-1",
                "customer_id": "CUST-MOCK-1",
                "order_lines": [
                    {"sku_id": "SKU-DEMO-1", "qty": 1, "price": 99.0},
                ],
                "warehouse_id": "Stores - Mock",
                "lock_stock": offline,
            }
        )
    return out
