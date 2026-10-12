"""G1 — reject PlatformShipPushed for offline / push-disabled orders."""

from __future__ import annotations

OFFLINE_PREFIX = "OFFLINE_"
ERR_OFFLINE_PUSH = "ERP_V1_OFFLINE_PUSH_FORBIDDEN"


def is_offline_channel(channel_type: str | None) -> bool:
    return bool(channel_type) and str(channel_type).startswith(OFFLINE_PREFIX)


def assert_platform_push_allowed(
    channel_type: str | None,
    requires_platform_push: int | bool | None,
) -> None:
    """Raise if offline channel_type OR requires_platform_push == 0."""
    offline = is_offline_channel(channel_type)
    push_flag = int(requires_platform_push or 0)
    if offline or push_flag == 0:
        msg = (
            f"{ERR_OFFLINE_PUSH}: 线下渠道禁止平台发货回传 "
            f"(channel_type={channel_type!r}, requires_platform_push={push_flag})."
        )
        _raise(msg)


def guard_platform_ship_push(doc, method=None):
    """Hook entry: call before enqueueing / submitting a platform ship push.

    Expects custom fields on linked Sales Order (or on doc itself):
      channel_type, requires_platform_push
    """
    channel_type = _get(doc, "channel_type")
    requires = _get(doc, "requires_platform_push")
    # If DN / Shipment: resolve from against_sales_order when fields absent
    if channel_type is None and hasattr(doc, "get"):
        so_name = doc.get("against_sales_order") or doc.get("sales_order")
        if so_name:
            channel_type, requires = _load_so_channel(so_name)
    assert_platform_push_allowed(channel_type, requires)


def _get(doc, key):
    if doc is None:
        return None
    if isinstance(doc, dict):
        return doc.get(key)
    if hasattr(doc, "get"):
        return doc.get(key)
    return getattr(doc, key, None)


def _load_so_channel(so_name: str):
    try:
        import frappe

        so = frappe.db.get_value(
            "Sales Order",
            so_name,
            ["channel_type", "requires_platform_push"],
            as_dict=True,
        )
        if not so:
            return None, None
        return so.get("channel_type"), so.get("requires_platform_push")
    except ImportError:
        return None, None


def _raise(msg: str) -> None:
    try:
        import frappe

        frappe.throw(msg, title=ERR_OFFLINE_PUSH)
    except ImportError:
        raise PermissionError(msg) from None
