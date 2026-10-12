# ERP v1 fixtures

Import when a site/bench exists. Until then these JSON files are the field/role contract.

## Files

| File | DocType |
|------|---------|
| `custom_fields.json` | Custom Field list |
| `roles.json` | Role list |

## Import (D6)

```bash
# dry-run — no Frappe required
python erp_fulfillment/scripts/import_fixtures.py --dry-run

# live (bench site)
export ERP_V1_FIXTURES_DIR="$(pwd)/fixtures/erp_v1"
bench --site <site> execute erp_fulfillment.scripts.import_fixtures.run

# legacy one-shot (also fine)
bench --site <site> import-doc fixtures/erp_v1/custom_fields.json
bench --site <site> import-doc fixtures/erp_v1/roles.json
```

Or rely on app `hooks.py` fixtures export after `install-app erp_fulfillment`:

```python
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "in", ["ERP v1", "ERP Fulfillment"]]]},
    {"dt": "Role", "filters": [["name", "like", "ERP v1%"]]},
]
```

`module` on Custom Fields is `ERP v1`; the import script creates that Module Def if missing.

See `docs/erp-v1/install.md`.
