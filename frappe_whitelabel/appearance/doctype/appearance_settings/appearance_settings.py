# Copyright (c) 2026, Nexarift Software Solution and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from frappe_whitelabel.branding.service import apply_appearance
from frappe_whitelabel.branding.themes import ensure_settings_use_valid_themes, sync_active_flags


class AppearanceSettings(Document):
	def validate(self):
		ensure_settings_use_valid_themes(self)
		if self.light_theme:
			mode = frappe.db.get_value("Appearance Theme", self.light_theme, "theme_mode")
			if mode and mode != "Light":
				frappe.throw(_("Light Theme must use Light mode."))
		if self.dark_theme:
			mode = frappe.db.get_value("Appearance Theme", self.dark_theme, "theme_mode")
			if mode and mode != "Dark":
				frappe.throw(_("Dark Theme must use Dark mode."))

	def on_update(self):
		if frappe.flags.get("appearance_syncing"):
			return
		sync_active_flags(self)
		apply_appearance(self)
