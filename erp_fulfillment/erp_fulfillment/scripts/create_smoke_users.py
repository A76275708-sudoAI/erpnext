import frappe

def run():
    users = [
        ("erp_gendan@local.test", "跟单", "ERP v1 跟单", "erp_gendan1"),
        ("erp_cangguan@local.test", "仓管", "ERP v1 仓管", "erp_cangguan1"),
        ("erp_xiaoshou@local.test", "销售", "ERP v1 销售", "erp_xiaoshou1"),
        ("erp_kefu@local.test", "客服", "ERP v1 客服", "erp_kefu1"),
        ("erp_yunying@local.test", "运营", "ERP v1 运营", "erp_yunying1"),
        ("erp_caiwu@local.test", "财务", "ERP v1 财务", "erp_caiwu1"),
        ("erp_admin@local.test", "管理员", "ERP v1 管理员", "erp_admin1"),
    ]
    out = []
    for email, first, role, pwd in users:
        if not frappe.db.exists("Role", role):
            out.append(f"MISSING_ROLE {role}")
            continue
        if frappe.db.exists("User", email):
            user = frappe.get_doc("User", email)
            user.enabled = 1
            user.new_password = pwd
            if role not in [r.role for r in user.roles]:
                user.append("roles", {"role": role})
            user.save(ignore_permissions=True)
            out.append(f"updated {email} {role}")
        else:
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": first,
                "enabled": 1,
                "send_welcome_email": 0,
                "user_type": "System User",
                "new_password": pwd,
            })
            user.insert(ignore_permissions=True)
            user.add_roles(role)
            out.append(f"created {email} {role}")
    frappe.db.commit()
    return {"users": out}
