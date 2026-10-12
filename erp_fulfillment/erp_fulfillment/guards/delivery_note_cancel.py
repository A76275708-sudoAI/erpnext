"""G2 — default ban Delivery Note cancel; admin override via audited path only."""

from __future__ import annotations

ERR_DN_CANCEL = "ERP_V1_DN_CANCEL_FORBIDDEN"
ADMIN_ROLE = "ERP v1 管理员"


def assert_delivery_note_cancel_allowed(allow_admin_override: bool = False) -> None:
    if allow_admin_override:
        return
    msg = (
        f"{ERR_DN_CANCEL}: 已发货 Delivery Note 默认禁止取消；"
        "纠错请走退货 DN；管理员须 force_cancel_delivery_note + reason。"
    )
    _raise(msg)


def before_cancel(doc, method=None):
    """hooks.py → Delivery Note.before_cancel"""
    allow = False
    try:
        import frappe

        allow = bool(getattr(frappe.flags, "erp_v1_allow_dn_cancel", False))
    except ImportError:
        allow = False
    assert_delivery_note_cancel_allowed(allow_admin_override=allow)


def _raise(msg: str) -> None:
    try:
        import frappe

        frappe.throw(msg, title=ERR_DN_CANCEL)
    except ImportError:
        raise PermissionError(msg) from None
