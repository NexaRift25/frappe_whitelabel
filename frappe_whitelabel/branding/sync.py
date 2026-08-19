"""Sync appearance into Frappe's native, upgrade-safe settings."""

from __future__ import annotations

import frappe
from frappe.utils import cint

from .defaults import APP_ASSET_FAVICON, APP_ASSET_LOGO, DEFAULT_PRODUCT_NAME


def _set_if_exists(doc, fieldname: str, value) -> None:
	if fieldname in doc.meta.get_valid_columns() or doc.meta.has_field(fieldname):
		doc.set(fieldname, value)


def sync_framework_settings(settings=None, config: dict | None = None) -> None:
	if frappe.flags.get("appearance_syncing"):
		return

	config = config or {}
	product_name = config.get("product_name") or DEFAULT_PRODUCT_NAME
	logo = config.get("navbar_logo") or config.get("logo") or APP_ASSET_LOGO
	login_logo = config.get("login_logo") or logo
	favicon = config.get("favicon") or APP_ASSET_FAVICON
	splash = config.get("splash_logo") or logo
	email_footer = config.get("email_footer") or config.get("company_name") or product_name
	disable_framework_footer = cint(config.get("disable_framework_email_footer", 1))

	frappe.flags.appearance_syncing = True
	try:
		try:
			_sync_website_settings(product_name, login_logo, favicon, splash, config)
		except Exception:
			frappe.log_error(title="Appearance website settings sync failed")
		try:
			_sync_navbar_settings(logo)
		except Exception:
			frappe.log_error(title="Appearance navbar settings sync failed")
		try:
			_sync_system_settings(product_name, email_footer, disable_framework_footer)
		except Exception:
			frappe.log_error(title="Appearance system settings sync failed")
		_sync_print_style(config)
	finally:
		frappe.flags.appearance_syncing = False


def _sync_website_settings(product_name, logo, favicon, splash, config) -> None:
	if not frappe.db.exists("DocType", "Website Settings"):
		return
	doc = frappe.get_single("Website Settings")
	_set_if_exists(doc, "app_name", product_name)
	_set_if_exists(doc, "app_logo", logo)
	_set_if_exists(doc, "favicon", favicon)
	_set_if_exists(doc, "splash_image", splash)
	_set_if_exists(doc, "banner_image", logo)
	_set_if_exists(doc, "title_prefix", product_name)
	brand_html = f'<img src="{logo}" alt="{frappe.utils.escape_html(product_name)}" style="max-height:28px;">'
	_set_if_exists(doc, "brand_html", brand_html)
	footer = config.get("company_name") or product_name
	_set_if_exists(doc, "footer_powered", footer)
	_set_if_exists(doc, "copyright", footer)
	doc.flags.ignore_validate = True
	doc.flags.ignore_permissions = True
	doc.save(ignore_permissions=True)


def _sync_navbar_settings(logo) -> None:
	if not frappe.db.exists("DocType", "Navbar Settings"):
		return
	doc = frappe.get_single("Navbar Settings")
	_set_if_exists(doc, "app_logo", logo)
	if not doc.get("logo_width"):
		_set_if_exists(doc, "logo_width", 28)
	doc.flags.ignore_validate = True
	doc.flags.ignore_permissions = True
	doc.save(ignore_permissions=True)


def _sync_system_settings(product_name, email_footer, disable_framework_footer) -> None:
	if not frappe.db.exists("DocType", "System Settings"):
		return
	doc = frappe.get_single("System Settings")
	_set_if_exists(doc, "app_name", product_name)
	_set_if_exists(doc, "email_footer_address", email_footer)
	_set_if_exists(doc, "disable_standard_email_footer", disable_framework_footer)
	doc.flags.ignore_validate = True
	doc.flags.ignore_permissions = True
	doc.save(ignore_permissions=True)
	frappe.db.set_default("email_footer_address", email_footer)
	frappe.db.set_default("disable_standard_email_footer", str(cint(disable_framework_footer)))


def _sync_print_style(config) -> None:
	if not frappe.db.exists("DocType", "Print Style"):
		return
	from .css import generate_print_css

	css = generate_print_css(config)
	try:
		if frappe.db.exists("Print Style", "Appearance"):
			frappe.db.set_value("Print Style", "Appearance", "css", css)
		else:
			style = frappe.get_doc(
				{
					"doctype": "Print Style",
					"print_style_name": "Appearance",
					"css": css,
					"standard": 0,
				}
			)
			style.insert(ignore_permissions=True)
	except Exception:
		frappe.log_error(title="Appearance print style sync failed")
