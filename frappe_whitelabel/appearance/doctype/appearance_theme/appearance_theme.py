# Copyright (c) 2026, Nexarift Software Solution and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint

from frappe_whitelabel.branding.service import apply_appearance
from frappe_whitelabel.branding.themes import validate_theme


class AppearanceTheme(Document):
	def validate(self):
		validate_theme(self)

	def on_update(self):
		if self._is_in_use():
			apply_appearance()

	def on_trash(self):
		if cint(self.is_standard):
			frappe.throw(_("System themes cannot be deleted."))
		if self._is_in_use():
			frappe.throw(_("This theme is currently active. Activate another theme before deleting it."))

	def _is_in_use(self) -> bool:
		if not frappe.db.exists("DocType", "Appearance Settings"):
			return False
		settings = frappe.get_single("Appearance Settings")
		return self.name in (settings.light_theme, settings.dark_theme)
