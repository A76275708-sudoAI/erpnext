"""G3a/G3b — Sales Order channel field consistency (hard reject on validate)."""

from __future__ import annotations

from erp_fulfillment.guards.platform_push import is_offline_channel

ERR_OFFLINE_PLATFORM_NO = "ERP_V1_OFFLINE_PLATFORM_ORDER_NO_FORBIDDEN"
ERR_EC_MISSING_KEYS = "ERP_V1_EC_MISSING_PLATFORM_KEYS"


def validate_sales_order(doc, method=None):
    channel_type = _get(doc, "channel_type")
    platform_order_no = (_get(doc, "platform_order_no") or "").strip()
    shop_id = (_get(doc, "shop_id") or "").strip()
    requires = _get(doc, "requires_platform_push")

    offline = is_offline_channel(channel_type)

    # Auto-align boolean fallback when channel_type is set
    if channel_type and requires is None:
        _set(doc, "requires_platform_push", 0 if offline else 1)
        requires = 0 if offline else 1

    if offline and platform_order_no:
        _raise(
            f"{ERR_OFFLINE_PLATFORM_NO}: 线下单禁止填写 platform_order_no "
            f"(channel_type={channel_type!r})."
        )

    if channel_type and str(channel_type).startswith("EC_") and (
        not platform_order_no or not shop_id
    ):
        _raise(
            f"{ERR_EC_MISSING_KEYS}: 电商单必须填写 platform_order_no 与 shop_id "
            f"(channel_type={channel_type!r})."
        )

    # Keep requires_platform_push consistent with offline prefix
    if offline and int(requires or 0) == 1:
        _raise(
            f"ERP_V1_OFFLINE_PUSH_FLAG: OFFLINE_* 渠道 requires_platform_push 必须为 0 "
            f"(channel_type={channel_type!r})."
        )


def _get(doc, key):
    if isinstance(doc, dict):
        return doc.get(key)
    if hasattr(doc, "get"):
        return doc.get(key)
    return getattr(doc, key, None)


def _set(doc, key, value):
    if isinstance(doc, dict):
        doc[key] = value
    elif hasattr(doc, "set"):
        doc.set(key, value)
    else:
        setattr(doc, key, value)


def _raise(msg: str) -> None:
    try:
        import frappe

        frappe.throw(msg)
    except ImportError:
        raise PermissionError(msg) from None
