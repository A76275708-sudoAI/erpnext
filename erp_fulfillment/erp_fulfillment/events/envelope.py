"""Common event envelope builder (PRD §3.1)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def build_envelope(
    event_type: str,
    *,
    channel_type: str,
    requires_platform_push: bool | int,
    stock_effect: str = "NONE",
    source: str = "erp_fulfillment",
    actor_type: str = "BOT",
    actor_id: str = "bot:unknown",
    idempotency_key: str | None = None,
    correlation_id: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    return {
        "event_id": str(uuid4()),
        "event_type": event_type,
        "schema_version": "1.0",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "actor_type": actor_type,
        "actor_id": actor_id,
        "idempotency_key": idempotency_key or str(uuid4()),
        "correlation_id": correlation_id or str(uuid4()),
        "channel_type": channel_type,
        "requires_platform_push": int(bool(requires_platform_push)),
        "stock_effect": stock_effect,
        **extra,
    }
