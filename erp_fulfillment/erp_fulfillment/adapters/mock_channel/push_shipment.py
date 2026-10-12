"""B7 — Mock PlatformShipPushed. Must call G1 before any push."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from erp_fulfillment.guards.platform_push import assert_platform_push_allowed


def push_platform_shipment(
    *,
    channel_type: str | None,
    requires_platform_push: int | bool | None,
    doc_no: str,
    tracking_no: str,
    carrier: str = "MOCK_CARRIER",
) -> dict[str, Any]:
    """Reject offline; otherwise return a mock PlatformShipPushed envelope."""
    assert_platform_push_allowed(channel_type, requires_platform_push)
    now = datetime.now(timezone.utc).isoformat()
    return {
        "event_id": str(uuid4()),
        "event_type": "PlatformShipPushed",
        "schema_version": "1.0",
        "occurred_at": now,
        "source": f"mock:{channel_type}",
        "actor_type": "BOT",
        "actor_id": "bot:B7",
        "idempotency_key": f"push-{doc_no}-{tracking_no}",
        "correlation_id": doc_no,
        "channel_type": channel_type,
        "requires_platform_push": int(requires_platform_push or 0),
        "stock_effect": "NONE",
        "doc_no": doc_no,
        "tracking_no": tracking_no,
        "carrier": carrier,
        "push_status": "MOCK_OK",
        "retry_count": 0,
    }
