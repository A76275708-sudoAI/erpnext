"""Guard stubs for ERP v1 (G1 offline push ban, G2 DN cancel ban).

Engineers: copy into erp_fulfillment.guards and register via hooks.
These functions raise frappe.ValidationError-style messages when frappe is available.
"""

from __future__ import annotations


OFFLINE_PREFIX = "OFFLINE_"
ERR_OFFLINE_PUSH = "ERP_V1_OFFLINE_PUSH_FORBIDDEN"
ERR_DN_CANCEL = "ERP_V1_DN_CANCEL_FORBIDDEN"


def is_offline_channel(channel_type: str | None) -> bool:
    return bool(channel_type) and str(channel_type).startswith(OFFLINE_PREFIX)


def assert_platform_push_allowed(
    channel_type: str | None,
    requires_platform_push: int | bool | None,
) -> None:
    """G1: reject PlatformShipPushed for offline / push-disabled orders."""
    offline = is_offline_channel(channel_type)
    push_flag = int(requires_platform_push or 0)
    if offline or push_flag == 0:
        raise PermissionError(
            f"{ERR_OFFLINE_PUSH}: 线下渠道禁止平台发货回传 "
            f"(channel_type={channel_type!r}, requires_platform_push={push_flag})."
        )


def assert_delivery_note_cancel_allowed(allow_admin_override: bool = False) -> None:
    """G2: default reject DN cancel; admin path must set allow_admin_override after audit."""
    if allow_admin_override:
        return
    raise PermissionError(
        f"{ERR_DN_CANCEL}: 已发货 Delivery Note 默认禁止取消；"
        "纠错请走退货 DN；管理员须 force_cancel_delivery_note + reason。"
    )
