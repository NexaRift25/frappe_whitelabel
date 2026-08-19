import frappe

from frappe_whitelabel.branding.defaults import DARK_THEME_NAME, LIGHT_THEME_NAME, default_settings
from frappe_whitelabel.branding.service import apply_appearance
from frappe_whitelabel.branding.themes import (
	activate_default_themes,
	ensure_settings_use_valid_themes,
	ensure_standard_themes,
	sync_active_flags,
)


def after_install():
	ensure_standard_themes()
	ensure_appearance_settings()
	activate_default_themes()
	apply_appearance()


def after_migrate():
	ensure_standard_themes()
	ensure_appearance_settings()
	ensure_settings_use_valid_themes()
	try:
		sync_active_flags()
		apply_appearance()
	except Exception:
		frappe.log_error(title="Appearance migrate apply failed")


def ensure_appearance_settings():
	if not frappe.db.exists("DocType", "Appearance Settings"):
		return
	doc = frappe.get_single("Appearance Settings")
	defaults = default_settings()
	changed = False
	for key, value in defaults.items():
		if doc.get(key) in (None, ""):
			doc.set(key, value)
			changed = True
	if not doc.light_theme:
		doc.light_theme = LIGHT_THEME_NAME
		changed = True
	if not doc.dark_theme:
		doc.dark_theme = DARK_THEME_NAME
		changed = True
	if changed:
		doc.flags.ignore_permissions = True
		doc.save(ignore_permissions=True)
