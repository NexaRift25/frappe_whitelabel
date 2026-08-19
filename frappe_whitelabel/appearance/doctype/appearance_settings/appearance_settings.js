frappe.ui.form.on("Appearance Settings", {
	onload(frm) {
		frm.set_query("light_theme", () => ({ filters: { theme_mode: "Light" } }));
		frm.set_query("dark_theme", () => ({ filters: { theme_mode: "Dark" } }));
	},
	refresh(frm) {
		frm.disable_save = false;
		frm.add_custom_button(__("Activate System Defaults"), () => {
			frappe.confirm(__("Activate Daylight and Midnight as the active light/dark themes?"), () => {
				frappe.call({
					method: "frappe_whitelabel.api.activate_default_themes",
					callback() {
						frappe.show_alert({
							message: __("System default themes activated"),
							indicator: "green",
						});
						frm.reload_doc();
					},
				});
			});
		});
		frm.add_custom_button(__("New Custom Theme"), () => {
			frappe.prompt(
				[
					{
						fieldname: "source_theme",
						label: __("Start From"),
						fieldtype: "Link",
						options: "Appearance Theme",
						reqd: 1,
						default: frm.doc.light_theme || "Daylight",
					},
					{
						fieldname: "new_name",
						label: __("Theme Name"),
						fieldtype: "Data",
						reqd: 1,
					},
				],
				(values) => {
					frappe.call({
						method: "frappe_whitelabel.api.duplicate_theme",
						args: {
							theme_name: values.source_theme,
							new_name: values.new_name,
						},
						callback(r) {
							frappe.set_route("Form", "Appearance Theme", r.message);
						},
					});
				},
				__("Create Custom Theme")
			);
		});
		frm.add_custom_button(__("Open Light Theme"), () => {
			if (frm.doc.light_theme) {
				frappe.set_route("Form", "Appearance Theme", frm.doc.light_theme);
			}
		});
		frm.add_custom_button(__("Open Dark Theme"), () => {
			if (frm.doc.dark_theme) {
				frappe.set_route("Form", "Appearance Theme", frm.doc.dark_theme);
			}
		});
		frm.add_custom_button(__("Manage Themes"), () => {
			frappe.set_route("List", "Appearance Theme");
		});
		frm.add_custom_button(__("Reload Desk"), () => {
			window.location.reload();
		});
		appearance_preview.render_settings(frm);
	},
	after_save(frm) {
		frappe.show_alert({
			message: __("Appearance saved. Reload to apply it everywhere."),
			indicator: "green",
		});
		appearance_preview.render_settings(frm);
	},
	product_name: render_settings,
	short_name: render_settings,
	tagline: render_settings,
	logo: render_settings,
	login_logo: render_settings,
	navbar_logo: render_settings,
	login_layout: render_settings,
	sidebar_style: render_settings,
	navbar_style: render_settings,
	button_style: render_settings,
	card_style: render_settings,
	border_radius: render_settings,
	light_theme(frm) {
		appearance_preview.render_settings(frm);
	},
	dark_theme(frm) {
		appearance_preview.render_settings(frm);
	},
});

function render_settings(frm) {
	appearance_preview.render_settings(frm);
}
