"""Load, cache, and apply appearance configuration."""

from __future__ import annotations

import os

import frappe
from frappe.utils import cint, cstr

from .css import generate_css, generate_print_css
from .defaults import (
	APP_ASSET_FAVICON,
	APP_ASSET_LOGO,
	DARK_THEME_NAME,
	DEFAULT_DARK_TOKENS,
	DEFAULT_LAYOUT,
	DEFAULT_LIGHT_TOKENS,
	DEFAULT_PRODUCT_NAME,
	LAYOUT_FIELDS,
	LIGHT_THEME_NAME,
	TOKEN_FIELDS,
	default_settings,
	font_stack,
)

RUNTIME_CSS_NAME = "appearance-runtime.css"
CACHE_KEY = "appearance_public_config"


def _safe_get_single(doctype: str):
	if not frappe.db:
		return None
	if not frappe.db.exists("DocType", doctype):
		return None
	try:
		return frappe.get_cached_doc(doctype, doctype)
	except Exception:
		return None


def _theme_tokens(theme_name: str | None, fallback: dict) -> dict:
	tokens = dict(fallback)
	if not theme_name or not frappe.db.exists("DocType", "Appearance Theme"):
		return tokens
	if not frappe.db.exists("Appearance Theme", theme_name):
		return tokens
	try:
		theme = frappe.get_cached_doc("Appearance Theme", theme_name)
	except Exception:
		return tokens
	for field in TOKEN_FIELDS:
		value = theme.get(field)
		if value not in (None, ""):
			tokens[field] = value
	return tokens


def _layout_from_settings(settings) -> dict:
	layout = dict(DEFAULT_LAYOUT)
	if not settings:
		return layout
	for field in LAYOUT_FIELDS:
		value = settings.get(field)
		if value not in (None, ""):
			layout[field] = value
	return layout


def get_appearance_config() -> dict:
	cached = frappe.cache().get_value(CACHE_KEY)
	if cached:
		return cached

	settings = _safe_get_single("Appearance Settings")
	defaults = default_settings()
	config = dict(defaults)

	if settings:
		for key in defaults:
			value = settings.get(key)
			if value not in (None, ""):
				config[key] = value
		config["layout"] = _layout_from_settings(settings)
		config["custom_css"] = settings.get("custom_css") or ""
		config["login_show_tagline"] = cint(settings.get("login_show_tagline"))
		config["hide_framework_branding"] = cint(settings.get("hide_framework_branding"))
		config["hide_help_links"] = cint(settings.get("hide_help_links"))
		config["disable_framework_email_footer"] = cint(settings.get("disable_framework_email_footer"))
	else:
		config["layout"] = dict(DEFAULT_LAYOUT)

	config["light_tokens"] = _theme_tokens(
		config.get("light_theme") or LIGHT_THEME_NAME,
		DEFAULT_LIGHT_TOKENS,
	)
	config["dark_tokens"] = _theme_tokens(
		config.get("dark_theme") or DARK_THEME_NAME,
		DEFAULT_DARK_TOKENS,
	)

	# Always fall back to protected defaults if an active theme was removed.
	if frappe.db.exists("DocType", "Appearance Theme"):
		if config.get("light_theme") and not frappe.db.exists("Appearance Theme", config["light_theme"]):
			config["light_theme"] = LIGHT_THEME_NAME
			config["light_tokens"] = dict(DEFAULT_LIGHT_TOKENS)
		if config.get("dark_theme") and not frappe.db.exists("Appearance Theme", config["dark_theme"]):
			config["dark_theme"] = DARK_THEME_NAME
			config["dark_tokens"] = dict(DEFAULT_DARK_TOKENS)

	for key in ("logo", "logo_dark", "login_logo", "navbar_logo", "favicon", "app_icon", "splash_logo"):
		config[key] = config.get(key) or (APP_ASSET_FAVICON if key == "favicon" else APP_ASSET_LOGO)

	config["product_name"] = config.get("product_name") or DEFAULT_PRODUCT_NAME
	config.update(config["layout"])
	config["css_version"] = cstr(getattr(settings, "modified", None) or "1")
	config["font_stack"] = font_stack(config["light_tokens"].get("font_family"))
	config["heading_font_stack"] = font_stack(
		config["light_tokens"].get("heading_font") or config["light_tokens"].get("font_family")
	)

	frappe.cache().set_value(CACHE_KEY, config)
	return config


def get_public_config() -> dict:
	config = get_appearance_config()
	public_keys = [
		"product_name",
		"short_name",
		"company_name",
		"tagline",
		"description",
		"logo",
		"logo_dark",
		"login_logo",
		"navbar_logo",
		"favicon",
		"app_icon",
		"splash_logo",
		"login_background",
		"login_layout",
		"login_show_tagline",
		"login_footer_text",
		"hide_framework_branding",
		"hide_help_links",
		"browser_title_suffix",
		"css_version",
		"font_stack",
		"heading_font_stack",
		"light_tokens",
		"dark_tokens",
		"layout",
	]
	return {key: config.get(key) for key in public_keys}


def get_jinja_branding() -> dict:
	try:
		config = get_appearance_config()
	except Exception:
		config = default_settings()
		config["light_tokens"] = dict(DEFAULT_LIGHT_TOKENS)

	logo = config.get("logo") or APP_ASSET_LOGO
	try:
		from frappe.utils import get_url

		if logo and logo.startswith("/"):
			logo = get_url(logo)
	except Exception:
		pass

	return {
		"product_name": config.get("product_name") or DEFAULT_PRODUCT_NAME,
		"logo": logo,
		"favicon": config.get("favicon") or APP_ASSET_FAVICON,
		"primary_color": (config.get("light_tokens") or DEFAULT_LIGHT_TOKENS).get("primary_color"),
		"tagline": config.get("tagline") or "",
		"company_name": config.get("company_name") or "",
		"email_footer": config.get("email_footer") or "",
	}


def runtime_css_path() -> str:
	folder = frappe.get_site_path("public", "files")
	os.makedirs(folder, exist_ok=True)
	return os.path.join(folder, RUNTIME_CSS_NAME)


def write_runtime_css(config: dict | None = None) -> str:
	config = config or get_appearance_config()
	css = generate_css(config)
	path = runtime_css_path()
	try:
		with open(path, "w", encoding="utf-8") as handle:
			handle.write(css)
	except OSError:
		frappe.log_error(title="Could not write appearance-runtime.css")
	return f"/files/{RUNTIME_CSS_NAME}?v={config.get('css_version') or '1'}"


def get_runtime_css() -> str:
	return generate_css(get_appearance_config())


def get_print_css() -> str:
	return generate_print_css(get_appearance_config())


def clear_appearance_cache() -> None:
	frappe.cache().delete_value(CACHE_KEY)
	frappe.clear_cache()
	try:
		from frappe.website.utils import clear_cache as clear_website_cache

		clear_website_cache()
	except Exception:
		pass


def apply_appearance(settings=None) -> None:
	from .sync import sync_framework_settings

	clear_appearance_cache()
	config = get_appearance_config()
	write_runtime_css(config)
	sync_framework_settings(settings, config)
	clear_appearance_cache()
	get_appearance_config()
