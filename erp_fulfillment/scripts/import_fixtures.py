#!/usr/bin/env python3
"""Import fixtures/erp_v1/custom_fields.json and roles.json into a Frappe site.

Usage (on a machine with bench + site):

  # preferred — via bench execute after install-app
  bench --site <site> execute erp_fulfillment.scripts.import_fixtures.run

  # or direct (bench env activated, site set):
  python apps/erp_fulfillment/scripts/import_fixtures.py --site <site>

  # dry-run / path check (no Frappe required):
  python erp_fulfillment/scripts/import_fixtures.py --dry-run

Resolves fixture files from (first hit wins):
  1) $ERP_V1_FIXTURES_DIR
  2) <repo-root>/fixtures/erp_v1
  3) <app>/../fixtures/erp_v1  (when nested in this fork)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
APP_ROOT = SCRIPT_DIR.parent
REPO_ROOT = APP_ROOT.parent  # erpnext fork root when packaged as sibling


def resolve_fixtures_dir() -> Path:
    env = os.environ.get("ERP_V1_FIXTURES_DIR")
    candidates = []
    if env:
        candidates.append(Path(env))
    candidates.extend(
        [
            REPO_ROOT / "fixtures" / "erp_v1",
            APP_ROOT / "fixtures" / "erp_v1",
            Path.cwd() / "fixtures" / "erp_v1",
        ]
    )
    for c in candidates:
        if (c / "custom_fields.json").is_file() and (c / "roles.json").is_file():
            return c
    raise FileNotFoundError(
        "Could not find fixtures/erp_v1/{custom_fields,roles}.json. "
        f"Tried: {[str(x) for x in candidates]}"
    )


def load_json(path: Path) -> list:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path} must be a JSON array")
    return data


def ensure_module_def(module_name: str = "ERP v1") -> None:
    import frappe

    if frappe.db.exists("Module Def", module_name):
        return
    # Module Def may need an app name; attach to erp_fulfillment when installed
    app = "erp_fulfillment"
    if "erp_fulfillment" not in frappe.get_installed_apps():
        app = "erpnext"
    doc = frappe.get_doc(
        {
            "doctype": "Module Def",
            "module_name": module_name,
            "app_name": app,
        }
    )
    doc.insert(ignore_permissions=True)
    frappe.db.commit()


def upsert_docs(rows: list, doctype_hint: str | None = None) -> tuple[int, int]:
    import frappe

    created = updated = 0
    for row in rows:
        dt = row.get("doctype") or doctype_hint
        if not dt:
            raise ValueError(f"row missing doctype: {row!r}")
        name = row.get("name") or row.get("role_name")
        if not name:
            raise ValueError(f"row missing name: {row!r}")
        if frappe.db.exists(dt, name):
            doc = frappe.get_doc(dt, name)
            doc.update({k: v for k, v in row.items() if k not in ("doctype",)})
            doc.save(ignore_permissions=True)
            updated += 1
        else:
            doc = frappe.get_doc(row)
            doc.insert(ignore_permissions=True)
            created += 1
    frappe.db.commit()
    return created, updated


def run(fixtures_dir: str | None = None) -> dict:
    """Entry for `bench execute erp_fulfillment.scripts.import_fixtures.run`."""
    # When executed via bench, this module may be imported as erp_fulfillment.scripts...
    # Ensure path resolution still works by using env override if needed.
    if fixtures_dir:
        os.environ["ERP_V1_FIXTURES_DIR"] = fixtures_dir
    d = resolve_fixtures_dir()
    ensure_module_def("ERP v1")
    roles = load_json(d / "roles.json")
    fields = load_json(d / "custom_fields.json")
    rc, ru = upsert_docs(roles, "Role")
    fc, fu = upsert_docs(fields, "Custom Field")
    return {
        "fixtures_dir": str(d),
        "roles_created": rc,
        "roles_updated": ru,
        "custom_fields_created": fc,
        "custom_fields_updated": fu,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Import ERP v1 fixtures")
    p.add_argument("--site", help="Frappe site name (sets frappe.init)")
    p.add_argument("--fixtures-dir", help="Override fixtures/erp_v1 path")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Only resolve + validate JSON (no Frappe)",
    )
    args = p.parse_args(argv)

    if args.fixtures_dir:
        os.environ["ERP_V1_FIXTURES_DIR"] = args.fixtures_dir

    d = resolve_fixtures_dir()
    roles = load_json(d / "roles.json")
    fields = load_json(d / "custom_fields.json")
    print(f"fixtures_dir={d}")
    print(f"roles={len(roles)} custom_fields={len(fields)}")

    if args.dry_run:
        print("dry-run OK")
        return 0

    try:
        import frappe
    except ImportError:
        print(
            "ERROR: frappe not importable. Use --dry-run, or run inside bench:\n"
            "  bench --site <site> execute erp_fulfillment.scripts.import_fixtures.run\n"
            "See docs/erp-v1/install.md",
            file=sys.stderr,
        )
        return 2

    if args.site:
        # Best-effort init when not already in bench execute context
        bench_path = os.environ.get("FRAPPE_BENCH_ROOT", os.getcwd())
        frappe.init(site=args.site, sites_path=os.path.join(bench_path, "sites"))
        frappe.connect()

    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
