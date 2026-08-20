"""Theme helpers for default vs custom theme behavior."""

from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import cint

from frappe_whitelabel.branding.defaults import (
	DARK_THEME_NAME,
	DEFAULT_DARK_TOKENS,
	DEFAULT_LIGHT_TOKENS,
	LIGHT_THEME_NAME,
	STANDARD_THEME_NAMES,
	TOKEN_FIELDS,
)


def is_standard_theme(theme_name: str | None) -> bool:
	return theme_name in STANDARD_THEME_NAMES


def get_default_theme_name(theme_mode: str) -> str:
	return DARK_THEME_NAME if theme_mode == "Dark" else LIGHT_THEME_NAME


def get_default_tokens(theme_name: str) -> dict | None:
	if theme_name == LIGHT_THEME_NAME:
		return DEFAULT_LIGHT_TOKENS
	if theme_name == DARK_THEME_NAME:
		return DEFAULT_DARK_TOKENS
	return None


def ensure_standard_themes() -> None:
	"""Create missing system themes only. Never overwrite saved edits."""
	if not frappe.db.exists("DocType", "Appearance Theme"):
		return

	_create_standard_theme_if_missing(DEFAULT_LIGHT_TOKENS)
	_create_standard_theme_if_missing(DEFAULT_DARK_TOKENS)


def _create_standard_theme_if_missing(tokens: dict) -> None:
	name = tokens["theme_name"]
	if frappe.db.exists("Appearance Theme", name):
		frappe.db.set_value("Appearance Theme", name, "is_standard", 1)
		return

	doc = frappe.new_doc("Appearance Theme")
	for field in TOKEN_FIELDS:
		doc.set(field, tokens.get(field))
	doc.is_standard = 1
	doc.is_active = 0
	doc.flags.ignore_permissions = True
	doc.insert(ignore_permissions=True)


def reset_theme_to_factory(theme_name: str) -> str:
	if theme_name not in STANDARD_THEME_NAMES:
		frappe.throw(_("Only system themes can be reset to factory defaults."))

	tokens = get_default_tokens(theme_name)
	if not tokens:
		frappe.throw(_("No factory defaults found for this theme."))

	theme = frappe.get_doc("Appearance Theme", theme_name)
	for field in TOKEN_FIELDS:
		if field != "theme_name":
			theme.set(field, tokens.get(field))
	theme.is_standard = 1
	theme.flags.ignore_permissions = True
	theme.save(ignore_permissions=True)
	return theme.name


def ensure_settings_use_valid_themes(settings=None) -> None:
	if not frappe.db.exists("DocType", "Appearance Settings"):
		return

	settings = settings or frappe.get_single("Appearance Settings")

	if not settings.light_theme or not frappe.db.exists("Appearance Theme", settings.light_theme):
		settings.light_theme = LIGHT_THEME_NAME
	if not settings.dark_theme or not frappe.db.exists("Appearance Theme", settings.dark_theme):
		settings.dark_theme = DARK_THEME_NAME


def sync_active_flags(settings=None) -> None:
	if not frappe.db.exists("DocType", "Appearance Settings"):
		return

	settings = settings or frappe.get_single("Appearance Settings")
	frappe.db.set_value("Appearance Theme", {"theme_mode": "Light"}, "is_active", 0)
	frappe.db.set_value("Appearance Theme", {"theme_mode": "Dark"}, "is_active", 0)

	if settings.light_theme:
		frappe.db.set_value("Appearance Theme", settings.light_theme, "is_active", 1)
	if settings.dark_theme:
		frappe.db.set_value("Appearance Theme", settings.dark_theme, "is_active", 1)


def activate_theme(theme_name: str) -> dict:
	if not frappe.db.exists("Appearance Theme", theme_name):
		frappe.throw(_("Theme {0} not found").format(theme_name))

	theme = frappe.get_doc("Appearance Theme", theme_name)
	settings = frappe.get_single("Appearance Settings")

	if theme.theme_mode == "Dark":
		settings.dark_theme = theme.name
	else:
		settings.light_theme = theme.name

	settings.flags.ignore_permissions = True
	settings.save(ignore_permissions=True)
	sync_active_flags(settings)
	return {"activated": theme.name, "mode": theme.theme_mode}


def activate_default_themes() -> dict:
	settings = frappe.get_single("Appearance Settings")
	settings.light_theme = LIGHT_THEME_NAME
	settings.dark_theme = DARK_THEME_NAME
	settings.flags.ignore_permissions = True
	settings.save(ignore_permissions=True)
	sync_active_flags(settings)
	return {
		"light_theme": LIGHT_THEME_NAME,
		"dark_theme": DARK_THEME_NAME,
	}


def duplicate_theme(theme_name: str, new_name: str | None = None) -> str:
	if not frappe.db.exists("Appearance Theme", theme_name):
		frappe.throw(_("Theme {0} not found").format(theme_name))

	source = frappe.get_doc("Appearance Theme", theme_name)
	copy = frappe.copy_doc(source)
	copy.theme_name = new_name or f"{source.theme_name} Copy"
	copy.is_standard = 0
	copy.is_active = 0
	copy.insert(ignore_permissions=True)
	return copy.name


def validate_theme(doc) -> None:
	if doc.is_new():
		# Factory Daylight/Midnight inserts are allowed; custom themes cannot reuse those names.
		if doc.theme_name in STANDARD_THEME_NAMES and not cint(doc.is_standard):
			frappe.throw(_("System theme names are reserved. Choose a different name."))
		if frappe.db.exists("Appearance Theme", doc.theme_name):
			frappe.throw(_("Theme {0} already exists.").format(doc.theme_name))
		return

	before = doc.get_doc_before_save()
	if before and cint(before.is_standard) and not cint(doc.is_standard):
		frappe.throw(_("System themes cannot be converted to custom themes."))

	if not cint(doc.is_standard) and doc.theme_name in STANDARD_THEME_NAMES:
		frappe.throw(_("This name is reserved for a system theme. Choose another name."))

	if doc.has_value_changed("theme_mode"):
		settings = frappe.get_single("Appearance Settings") if frappe.db.exists("DocType", "Appearance Settings") else None
		if settings and doc.name in (settings.light_theme, settings.dark_theme):
			frappe.throw(_("Change the active theme before switching its mode."))
