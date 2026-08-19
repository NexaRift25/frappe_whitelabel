import frappe

from frappe_whitelabel.branding.service import get_public_config


def extend_bootinfo(bootinfo=None):
	if bootinfo is None:
		return
	try:
		config = get_public_config()
	except Exception:
		frappe.log_error(title="Appearance bootinfo failed")
		return

	bootinfo["appearance"] = config
	logo = config.get("navbar_logo") or config.get("logo")
	if logo:
		bootinfo["app_logo_url"] = logo
	if config.get("product_name"):
		bootinfo["sysdefaults"] = bootinfo.get("sysdefaults") or {}
		bootinfo["sysdefaults"]["app_name"] = config["product_name"]
		bootinfo["app_name"] = config["product_name"]
