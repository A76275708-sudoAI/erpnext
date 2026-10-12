"""Guard stubs for ERP v1 (G1 offline push ban, G2 DN cancel ban).

D6: prefer `erp_fulfillment.guards` (wired in hooks). This module re-exports
the same API for engineers who still import erpnext.erp_v1_stubs.guards.
"""

from __future__ import annotations

try:
    from erp_fulfillment.guards import (  # type: ignore
        ERR_DN_CANCEL,
        ERR_OFFLINE_PUSH,
        assert_delivery_note_cancel_allowed,
        assert_platform_push_allowed,
        is_offline_channel,
    )
except ImportError:
    OFFLINE_PREFIX = "OFFLINE_"
    ERR_OFFLINE_PUSH = "ERP_V1_OFFLINE_PUSH_FORBIDDEN"
    ERR_DN_CANCEL = "ERP_V1_DN_CANCEL_FORBIDDEN"

    def is_offline_channel(channel_type: str | None) -> bool:
        return bool(channel_type) and str(channel_type).startswith(OFFLINE_PREFIX)

    def assert_platform_push_allowed(
        channel_type: str | None,
        requires_platform_push: int | bool | None,
    ) -> None:
        offline = is_offline_channel(channel_type)
        push_flag = int(requires_platform_push or 0)
        if offline or push_flag == 0:
            raise PermissionError(
                f"{ERR_OFFLINE_PUSH}: 线下渠道禁止平台发货回传 "
                f"(channel_type={channel_type!r}, requires_platform_push={push_flag})."
            )

    def assert_delivery_note_cancel_allowed(allow_admin_override: bool = False) -> None:
        if allow_admin_override:
            return
        raise PermissionError(
            f"{ERR_DN_CANCEL}: 已发货 Delivery Note 默认禁止取消；"
            "纠错请走退货 DN；管理员须 force_cancel_delivery_note + reason。"
        )

__all__ = [
    "ERR_OFFLINE_PUSH",
    "ERR_DN_CANCEL",
    "is_offline_channel",
    "assert_platform_push_allowed",
    "assert_delivery_note_cancel_allowed",
]
