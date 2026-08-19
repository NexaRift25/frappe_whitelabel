import frappe
from frappe import _

from frappe_whitelabel.branding.service import (
	apply_appearance,
	get_appearance_config,
	get_public_config,
	get_runtime_css,
)
from frappe_whitelabel.branding.themes import (
	activate_default_themes as _activate_default_themes,
	activate_theme as _activate_theme,
	duplicate_theme as _duplicate_theme,
	reset_theme_to_factory as _reset_theme_to_factory,
)


@frappe.whitelist(allow_guest=True)
def get_branding():
	return get_public_config()


@frappe.whitelist(allow_guest=True)
def theme_css():
	frappe.local.response["type"] = "txt"
	frappe.local.response["content_type"] = "text/css; charset=utf-8"
	frappe.local.response["message"] = get_runtime_css()
	return get_runtime_css()


@frappe.whitelist()
def preview_bundle(light_theme=None, dark_theme=None):
	frappe.only_for("System Manager")
	config = get_appearance_config()
	if light_theme:
		from frappe_whitelabel.branding.service import _theme_tokens
		from frappe_whitelabel.branding.defaults import DEFAULT_LIGHT_TOKENS

		config["light_tokens"] = _theme_tokens(light_theme, DEFAULT_LIGHT_TOKENS)
	if dark_theme:
		from frappe_whitelabel.branding.service import _theme_tokens
		from frappe_whitelabel.branding.defaults import DEFAULT_DARK_TOKENS

		config["dark_tokens"] = _theme_tokens(dark_theme, DEFAULT_DARK_TOKENS)
	return {
		"config": get_public_config()
		| {
			"light_tokens": config["light_tokens"],
			"dark_tokens": config["dark_tokens"],
		}
	}


@frappe.whitelist()
def activate_theme(theme_name: str):
	frappe.only_for("System Manager")
	result = _activate_theme(theme_name)
	apply_appearance()
	return result


@frappe.whitelist()
def activate_default_themes():
	frappe.only_for("System Manager")
	result = _activate_default_themes()
	apply_appearance()
	return result


@frappe.whitelist()
def duplicate_theme(theme_name: str, new_name: str | None = None):
	frappe.only_for("System Manager")
	return _duplicate_theme(theme_name, new_name)


@frappe.whitelist()
def reset_theme(theme_name: str):
	frappe.only_for("System Manager")
	result = _reset_theme_to_factory(theme_name)
	apply_appearance()
	return result
