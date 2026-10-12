"""G2 admin override — force_cancel_delivery_note(dn_name, reason).

Only callable when Frappe is present. Sets frappe.flags.erp_v1_allow_dn_cancel
for the duration of cancel, writes Comment + Error Log.
"""

from __future__ import annotations


def force_cancel_delivery_note(dn_name: str, reason: str) -> str:
    if not reason or len(reason.strip()) < 10:
        raise ValueError("reason must be at least 10 characters")

    try:
        import frappe
        from frappe import _
    except ImportError as e:
        raise RuntimeError(
            "force_cancel_delivery_note requires a live Frappe site"
        ) from e

    roles = frappe.get_roles(frappe.session.user)
    if "ERP v1 管理员" not in roles and "System Manager" not in roles:
        frappe.throw(_("Only ERP v1 管理员 / System Manager may force-cancel DN"))

    frappe.flags.erp_v1_allow_dn_cancel = True
    try:
        dn = frappe.get_doc("Delivery Note", dn_name)
        dn.add_comment(
            "Comment",
            text=f"[ERP_V1_FORCE_CANCEL] by {frappe.session.user}: {reason.strip()}",
        )
        frappe.log_error(
            title=f"ERP_V1_DN_FORCE_CANCEL:{dn_name}",
            message=f"actor={frappe.session.user} reason={reason.strip()}",
        )
        dn.cancel()
        return dn_name
    finally:
        frappe.flags.erp_v1_allow_dn_cancel = False
