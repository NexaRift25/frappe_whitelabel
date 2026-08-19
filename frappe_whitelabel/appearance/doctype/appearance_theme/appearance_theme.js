frappe.ui.form.on("Appearance Theme", {
	refresh(frm) {
		frm.enable_save();
		frm.set_df_property("is_active", "read_only", 1);

		if (frm.doc.is_standard) {
			frm.set_intro(
				__(
					"System theme. You can edit and save all values directly. Use <b>Reset to Factory</b> to undo changes. System themes cannot be deleted."
				),
				"blue"
			);
			if (!frm.is_new()) {
				frm.add_custom_button(__("Reset to Factory"), () => {
					frappe.confirm(__("Restore this system theme to factory defaults?"), () => {
						frappe.call({
							method: "frappe_whitelabel.api.reset_theme",
							args: { theme_name: frm.doc.name },
							callback() {
								frm.reload_doc();
								frappe.show_alert({
									message: __("Theme restored to factory defaults"),
									indicator: "green",
								});
							},
						});
					});
				});
			}
		} else {
			frm.set_intro("");
			if (!frm.doc.is_active && !frm.is_new()) {
				frm.add_custom_button(__("Delete"), () => {
					frappe.confirm(__("Delete this theme?"), () => frm.remove());
				});
			}
		}

		if (!frm.is_new()) {
			frm.add_custom_button(__("Activate"), () => activate_theme(frm.doc.name));
		}

		frm.add_custom_button(__("Duplicate"), () => {
			frappe.prompt(
				{
					fieldname: "new_name",
					label: __("New Theme Name"),
					fieldtype: "Data",
					reqd: 1,
					default: __("{0} Copy", [frm.doc.theme_name]),
				},
				(values) => {
					frappe.call({
						method: "frappe_whitelabel.api.duplicate_theme",
						args: { theme_name: frm.doc.name, new_name: values.new_name },
						callback(r) {
							frappe.set_route("Form", "Appearance Theme", r.message);
						},
					});
				},
				__("Duplicate Theme")
			);
		});

		appearance_preview.render_theme(frm);
	},
	primary_color: render_theme,
	secondary_color: render_theme,
	accent_color: render_theme,
	background_color: render_theme,
	surface_color: render_theme,
	text_color: render_theme,
	muted_text_color: render_theme,
	border_color: render_theme,
	navbar_color: render_theme,
	sidebar_color: render_theme,
	sidebar_text_color: render_theme,
	success_color: render_theme,
	warning_color: render_theme,
	danger_color: render_theme,
	info_color: render_theme,
	font_family: render_theme,
	heading_font: render_theme,
	theme_mode: render_theme,
});

function render_theme(frm) {
	appearance_preview.render_theme(frm);
}

function activate_theme(theme_name) {
	frappe.call({
		method: "frappe_whitelabel.api.activate_theme",
		args: { theme_name },
		freeze: true,
		callback() {
			frappe.show_alert({ message: __("Theme activated"), indicator: "green" });
			cur_frm && cur_frm.reload_doc();
		},
	});
}
