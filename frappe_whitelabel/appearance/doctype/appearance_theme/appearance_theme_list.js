frappe.listview_settings["Appearance Theme"] = {
	add_fields: ["theme_mode", "is_standard", "is_active", "primary_color"],
	get_indicator(doc) {
		if (doc.is_active) {
			return [__("Active"), "green", "is_active,=,1"];
		}
		if (doc.is_standard) {
			return [__("System"), "blue", "is_standard,=,1"];
		}
		return [__("Custom"), "gray", "is_standard,=,0"];
	},
	onload(listview) {
		listview.page.add_inner_button(__("New Theme"), () => {
			frappe.new_doc("Appearance Theme");
		});

		listview.page.add_inner_button(__("Activate System Defaults"), () => {
			frappe.confirm(__("Activate Daylight and Midnight as the active light/dark themes?"), () => {
				frappe.call({
					method: "frappe_whitelabel.api.activate_default_themes",
					callback() {
						frappe.show_alert({
							message: __("System default themes activated"),
							indicator: "green",
						});
						listview.refresh();
					},
				});
			});
		});
	},
	button: {
		show(doc) {
			return !doc.is_active;
		},
		get_label() {
			return __("Activate");
		},
		get_description() {
			return __("Apply this theme");
		},
		action(doc) {
			frappe.call({
				method: "frappe_whitelabel.api.activate_theme",
				args: { theme_name: doc.name },
				callback() {
					frappe.show_alert({ message: __("Theme activated"), indicator: "green" });
					cur_list.refresh();
				},
			});
		},
	},
};
