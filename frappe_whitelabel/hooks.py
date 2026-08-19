app_name = "frappe_whitelabel"
app_title = "Appearance"
app_publisher = "Nexarift Software Solution"
app_description = "Database-driven product identity, theming, and desk/login appearance for Frappe"
app_email = "anamul@nexarift.com"
app_license = "MIT"
app_logo_url = "/assets/frappe_whitelabel/images/logo.svg"

app_include_css = [
	"/assets/frappe_whitelabel/css/brand.css",
	"/assets/frappe_whitelabel/css/theme.css",
	"/assets/frappe_whitelabel/css/components.css",
	"/files/appearance-runtime.css",
]
app_include_js = [
	"/assets/frappe_whitelabel/js/branding.js",
	"/assets/frappe_whitelabel/js/ui-customization.js",
	"/assets/frappe_whitelabel/js/preview.js",
]

web_include_css = [
	"/assets/frappe_whitelabel/css/brand.css",
	"/assets/frappe_whitelabel/css/theme.css",
	"/assets/frappe_whitelabel/css/components.css",
	"/files/appearance-runtime.css",
]
web_include_js = [
	"/assets/frappe_whitelabel/js/branding.js",
	"/assets/frappe_whitelabel/js/ui-customization.js",
]

email_css = ["/assets/frappe_whitelabel/css/email.css"]

jinja = {
	"methods": [
		"frappe_whitelabel.branding.service.get_jinja_branding",
	]
}

after_install = "frappe_whitelabel.install.after_install"
after_migrate = "frappe_whitelabel.install.after_migrate"

extend_bootinfo = ["frappe_whitelabel.boot.extend_bootinfo"]
update_website_context = ["frappe_whitelabel.website.update_website_context"]
