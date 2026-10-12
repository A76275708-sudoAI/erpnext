"""Frappe hooks for ERP v1 fulfillment guards + fixtures.

Wire these into a site via `bench --site <site> install-app erp_fulfillment`.
Until then, guards remain importable as pure Python (see tests/).
"""

app_name = "erp_fulfillment"
app_title = "ERP Fulfillment"
app_publisher = "A76275708-sudoAI"
app_description = "ERP v1 fulfillment adapters and hard guards"
app_email = "A76275708-sudoAI@users.noreply.github.com"
app_license = "mit"

# Export / sync Custom Fields + Roles introduced in fixtures/erp_v1
# Paths are relative to this app; import script also reads repo-root fixtures.
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "in", ["ERP v1", "ERP Fulfillment"]]],
    },
    {
        "dt": "Role",
        "filters": [["name", "like", "ERP v1%"]],
    },
]

doc_events = {
    "Sales Order": {
        "validate": "erp_fulfillment.guards.sales_order_validate.validate_sales_order",
    },
    "Delivery Note": {
        "before_cancel": "erp_fulfillment.guards.delivery_note_cancel.before_cancel",
    },
}

# Whitelisted admin override for audited DN cancel (G2 exception path)
override_whitelisted_methods = {}

# Scheduled / background: none in D6
# scheduler_events = {}


# —— ERP v1 modern Desk UI (Figma p8BBd7RMOYfcLIgDssazw7) ——
# Reversible: delete these four lines + public/css|js desk_modern.* and clear-cache.
app_include_css = ["/assets/erp_fulfillment/css/desk_modern.css?v=2"]
app_include_js = ["/assets/erp_fulfillment/js/desk_modern.js?v=2"]
web_include_css = ["/assets/erp_fulfillment/css/desk_modern.css?v=2"]
web_include_js = ["/assets/erp_fulfillment/js/desk_modern.js?v=2"]
