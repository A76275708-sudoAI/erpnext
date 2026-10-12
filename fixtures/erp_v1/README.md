# ERP v1 fixtures (D5 stubs)

Import when a site/bench exists. Until then these JSON files are the field/role contract.

## Files

| File | DocType |
|------|---------|
| `custom_fields.json` | Custom Field list |
| `roles.json` | Role list |

## Import hints

```bash
# single-file import (Frappe)
bench --site <site> import-doc fixtures/erp_v1/custom_fields.json
bench --site <site> import-doc fixtures/erp_v1/roles.json
```

Or register under an app `hooks.py`:

```python
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "ERP v1"]]},
    {"dt": "Role", "filters": [["name", "like", "ERP v1%"]]},
]
```

`module` on Custom Fields below is set to `ERP v1` for filtering; create that Module Def if missing, or clear module on import.
