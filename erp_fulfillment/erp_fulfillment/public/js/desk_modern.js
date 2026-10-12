/**
 * ERP v1 modern Desk polish (pairs with desk_modern.css).
 * Light-touch: font class, theme marker, optional Stock shortcut label hints.
 */
(function () {
  function apply() {
    try {
      document.body.classList.add("erp-v1-modern-theme");
      // Prefer Chinese system font stack already in CSS; nudge documentElement lang if zh
      if (!document.documentElement.getAttribute("lang")) {
        document.documentElement.setAttribute("lang", "zh-CN");
      }
    } catch (e) {
      console.warn("erp_fulfillment desk_modern:", e);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply);
  } else {
    apply();
  }

  // Re-apply after Frappe desk boot (route changes remount body classes sometimes)
  if (window.frappe && frappe.after_ajax) {
    frappe.after_ajax(apply);
  }
  document.addEventListener("page-change", apply);
})();
