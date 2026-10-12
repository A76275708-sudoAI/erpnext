"""Idempotent Stock workspace Chinese shortcuts (Figma 库存工作台)."""
from __future__ import annotations

import json

import frappe

SHORTCUTS = [
    {"type": "DocType", "label": "物料", "link_to": "Item", "color": "Blue"},
    {"type": "DocType", "label": "仓库", "link_to": "Warehouse", "color": "Cyan"},
    {"type": "DocType", "label": "库存过账", "link_to": "Stock Entry", "color": "Orange"},
    {"type": "Report", "label": "库存余额", "link_to": "Stock Balance", "color": "Green"},
]


def apply() -> list[str]:
    doc = frappe.get_doc("Workspace", "Stock")
    doc.set("shortcuts", [])
    for s in SHORTCUTS:
        doc.append("shortcuts", s)

    blocks = json.loads(doc.content or "[]")
    new_blocks: list[dict] = []
    skip_old = False
    injected = False
    for b in blocks:
        t = b.get("type")
        d = b.get("data") or {}
        text = d.get("text") or ""
        if t == "header" and ("Quick Access" in text or "快捷入口" in text) and not injected:
            new_blocks.append(
                {
                    "id": b.get("id") or frappe.generate_hash(length=8),
                    "type": "header",
                    "data": {"text": '<span class="h4"><b>快捷入口</b></span>', "col": 12},
                }
            )
            for label in [s["label"] for s in SHORTCUTS]:
                new_blocks.append(
                    {
                        "id": frappe.generate_hash(length=10),
                        "type": "shortcut",
                        "data": {"shortcut_name": label, "col": 3},
                    }
                )
            injected = True
            skip_old = True
            continue
        if skip_old and t == "shortcut":
            continue
        if skip_old and t in ("spacer", "header"):
            skip_old = False
            new_blocks.append(b)
            continue
        new_blocks.append(b)

    doc.content = json.dumps(new_blocks, ensure_ascii=False)
    doc.flags.ignore_links = True
    doc.flags.ignore_validate = True
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return [s.label for s in doc.shortcuts]
