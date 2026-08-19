"""Default product identity, theme tokens, and option catalogs."""

from copy import deepcopy

APP_ASSET_LOGO = "/assets/frappe_whitelabel/images/logo.svg"
APP_ASSET_FAVICON = "/assets/frappe_whitelabel/images/favicon.svg"

DEFAULT_PRODUCT_NAME = "Nexarift"
DEFAULT_SHORT_NAME = "NX"
DEFAULT_TAGLINE = "Work, organized."

FONT_CATALOG = [
	"Plus Jakarta Sans",
	"IBM Plex Sans",
	"Source Sans 3",
	"Nunito",
	"Outfit",
	"Manrope",
	"DM Sans",
	"Inter",
	"Roboto",
	"Lato",
	"Open Sans",
	"Poppins",
	"System UI",
]

FONT_STACKS = {
	"Plus Jakarta Sans": '"Plus Jakarta Sans", "Segoe UI", sans-serif',
	"IBM Plex Sans": '"IBM Plex Sans", "Segoe UI", sans-serif',
	"Source Sans 3": '"Source Sans 3", "Segoe UI", sans-serif',
	"Nunito": '"Nunito", "Segoe UI", sans-serif',
	"Outfit": '"Outfit", "Segoe UI", sans-serif',
	"Manrope": '"Manrope", "Segoe UI", sans-serif',
	"DM Sans": '"DM Sans", "Segoe UI", sans-serif',
	"Inter": '"Inter", "Segoe UI", sans-serif',
	"Roboto": '"Roboto", "Segoe UI", sans-serif',
	"Lato": '"Lato", "Segoe UI", sans-serif',
	"Open Sans": '"Open Sans", "Segoe UI", sans-serif',
	"Poppins": '"Poppins", "Segoe UI", sans-serif',
	"System UI": '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
}

LIGHT_THEME_NAME = "Daylight"
DARK_THEME_NAME = "Midnight"
STANDARD_THEME_NAMES = (LIGHT_THEME_NAME, DARK_THEME_NAME)

DEFAULT_LIGHT_TOKENS = {
	"theme_name": LIGHT_THEME_NAME,
	"theme_mode": "Light",
	"primary_color": "#0F766E",
	"secondary_color": "#334155",
	"accent_color": "#D97706",
	"background_color": "#F8FAFC",
	"surface_color": "#FFFFFF",
	"text_color": "#0F172A",
	"muted_text_color": "#64748B",
	"border_color": "#E2E8F0",
	"success_color": "#059669",
	"warning_color": "#D97706",
	"danger_color": "#DC2626",
	"info_color": "#0284C7",
	"navbar_color": "#FFFFFF",
	"sidebar_color": "#FFFFFF",
	"sidebar_text_color": "#505A62",
	"font_family": "Plus Jakarta Sans",
	"heading_font": "Plus Jakarta Sans",
	"base_font_size": "14px",
	"heading_weight": "600",
	"body_weight": "400",
}

DEFAULT_DARK_TOKENS = {
	"theme_name": DARK_THEME_NAME,
	"theme_mode": "Dark",
	"primary_color": "#2DD4BF",
	"secondary_color": "#94A3B8",
	"accent_color": "#FBBF24",
	"background_color": "#0B1220",
	"surface_color": "#111827",
	"text_color": "#F1F5F9",
	"muted_text_color": "#94A3B8",
	"border_color": "#1F2937",
	"success_color": "#34D399",
	"warning_color": "#FBBF24",
	"danger_color": "#F87171",
	"info_color": "#38BDF8",
	"navbar_color": "#111827",
	"sidebar_color": "#020617",
	"sidebar_text_color": "#CBD5E1",
	"font_family": "Plus Jakarta Sans",
	"heading_font": "Plus Jakarta Sans",
	"base_font_size": "14px",
	"heading_weight": "600",
	"body_weight": "400",
}

DEFAULT_LAYOUT = {
	"sidebar_style": "Solid",
	"sidebar_behavior": "Expanded",
	"navbar_style": "Solid",
	"logo_placement": "Left",
	"button_style": "Rounded",
	"card_style": "Elevated",
	"table_style": "Comfortable",
	"form_style": "Spacious",
	"border_radius": "Medium",
	"page_background": "Muted",
	"login_layout": "Split",
	"login_show_tagline": 1,
	"hide_framework_branding": 1,
	"hide_help_links": 0,
	"disable_framework_email_footer": 1,
}

TOKEN_FIELDS = list(DEFAULT_LIGHT_TOKENS.keys())
LAYOUT_FIELDS = list(DEFAULT_LAYOUT.keys())

RADIUS_MAP = {
	"Small": {"sm": "4px", "md": "6px", "lg": "8px", "full": "999px"},
	"Medium": {"sm": "6px", "md": "8px", "lg": "12px", "full": "999px"},
	"Large": {"sm": "8px", "md": "12px", "lg": "16px", "full": "999px"},
}


def font_stack(name: str | None) -> str:
	if not name:
		return FONT_STACKS["Plus Jakarta Sans"]
	return FONT_STACKS.get(name, f'"{name}", "Segoe UI", sans-serif')


def default_settings() -> dict:
	values = {
		"product_name": DEFAULT_PRODUCT_NAME,
		"short_name": DEFAULT_SHORT_NAME,
		"company_name": "",
		"tagline": DEFAULT_TAGLINE,
		"description": "",
		"logo": APP_ASSET_LOGO,
		"logo_dark": APP_ASSET_LOGO,
		"login_logo": APP_ASSET_LOGO,
		"navbar_logo": APP_ASSET_LOGO,
		"favicon": APP_ASSET_FAVICON,
		"app_icon": APP_ASSET_LOGO,
		"splash_logo": APP_ASSET_LOGO,
		"login_background": "",
		"light_theme": LIGHT_THEME_NAME,
		"dark_theme": DARK_THEME_NAME,
		"login_footer_text": "",
		"email_footer": "",
		"print_header_text": "",
		"browser_title_suffix": "",
		"custom_css": "",
	}
	values.update(deepcopy(DEFAULT_LAYOUT))
	return values
