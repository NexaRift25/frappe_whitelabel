from frappe.utils import escape_html

from frappe_whitelabel.branding.service import get_appearance_config, get_public_config


def update_website_context(context):
	try:
		config = get_appearance_config()
	except Exception:
		return

	product_name = config.get("product_name")
	favicon = config.get("favicon")
	splash = config.get("splash_logo") or config.get("logo")
	logo = config.get("login_logo") or config.get("logo")

	if product_name:
		context["app_name"] = product_name
		if not context.get("title") or context.get("title") in ("Login", "Frappe"):
			context["title"] = product_name
		context["title_prefix"] = product_name
	if favicon:
		context["favicon"] = favicon
	if splash:
		context["splash_image"] = splash
	if logo:
		context["logo"] = logo
		context["banner_image"] = logo

	css = config.get("css_version") or "1"
	head = context.get("head_html") or ""
	inline = (
		f'<link rel="stylesheet" href="/assets/frappe_whitelabel/css/brand.css">'
		f'<link rel="stylesheet" href="/assets/frappe_whitelabel/css/theme.css">'
		f'<link rel="stylesheet" href="/assets/frappe_whitelabel/css/components.css">'
		f'<link rel="stylesheet" href="/files/appearance-runtime.css?v={escape_html(str(css))}">'
		f'<script src="/assets/frappe_whitelabel/js/branding.js"></script>'
		f'<script src="/assets/frappe_whitelabel/js/ui-customization.js"></script>'
		f'<meta name="application-name" content="{escape_html(product_name or "")}">'
	)
	if "appearance-runtime.css" not in head:
		context["head_html"] = inline + head

	context["appearance"] = get_public_config()
	return context
