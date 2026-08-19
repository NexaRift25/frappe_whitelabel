window.appearance_preview = {
	frame(options) {
		const o = options || {};
		const primary = o.primary_color || "#0F766E";
		const bg = o.background_color || "#F8FAFC";
		const surface = o.surface_color || "#FFFFFF";
		const text = o.text_color || "#0F172A";
		const muted = o.muted_text_color || "#64748B";
		const navbar = o.navbar_color || "#FFFFFF";
		const sidebar = o.sidebar_color || "#0F172A";
		const sidebarText = o.sidebar_text_color || "#E2E8F0";
		const font = o.font_family || "Plus Jakarta Sans";
		const radius = o.border_radius === "Large" ? "16px" : o.border_radius === "Small" ? "6px" : "12px";
		const name = o.product_name || "Product";
		const tagline = o.tagline || "A distinct workspace";
		const logo = o.logo || "/assets/frappe_whitelabel/images/logo.svg";

		return `
			<div class="appearance-preview-frame" style="font-family:'${font}',sans-serif;background:${bg};color:${text}">
				<div class="pv-nav" style="background:${navbar};border-bottom:1px solid ${o.border_color || "#e2e8f0"}">
					<img src="${logo}" style="height:22px;width:auto">
					<strong>${frappe.utils.escape_html(name)}</strong>
					<span style="margin-left:auto;color:${muted};font-size:12px">${frappe.utils.escape_html(tagline)}</span>
				</div>
				<div class="pv-body">
					<div class="pv-side" style="background:${sidebar};color:${sidebarText}">
						<div style="opacity:.7;font-size:11px;margin-bottom:8px">MENU</div>
						<div style="padding:8px 10px;border-radius:${radius};background:${primary};color:#fff">Home</div>
						<div style="padding:8px 10px;margin-top:6px;opacity:.85">Reports</div>
						<div style="padding:8px 10px;margin-top:6px;opacity:.85">Settings</div>
					</div>
					<div class="pv-main">
						<div class="pv-card" style="background:${surface};border-radius:${radius};border:1px solid ${o.border_color || "#e2e8f0"}">
							<div style="font-weight:600;margin-bottom:8px">Overview</div>
							<div style="color:${muted};font-size:12px;margin-bottom:12px">This is how the desk will feel with the current branding.</div>
							<span class="pv-btn" style="background:${primary};border-radius:${radius}">Primary action</span>
							<span class="pv-btn" style="background:${o.accent_color || "#D97706"};border-radius:${radius};margin-left:6px">Accent</span>
						</div>
						<div class="pv-card" style="background:${surface};border-radius:${radius};border:1px solid ${o.border_color || "#e2e8f0"}">
							<div style="display:flex;gap:8px">
								<span style="color:${o.success_color || "#059669"}">Success</span>
								<span style="color:${o.warning_color || "#D97706"}">Warning</span>
								<span style="color:${o.danger_color || "#DC2626"}">Danger</span>
								<span style="color:${o.info_color || "#0284C7"}">Info</span>
							</div>
						</div>
					</div>
				</div>
			</div>
		`;
	},

	render_theme(frm) {
		if (!frm || !frm.fields_dict.preview_html) return;
		frm.get_field("preview_html").$wrapper.html(this.frame(frm.doc));
	},

	render_settings(frm) {
		if (!frm || !frm.fields_dict.preview_html) return;
		const draw = (tokens) => {
			frm.get_field("preview_html").$wrapper.html(
				this.frame(Object.assign({}, tokens || {}, frm.doc))
			);
		};
		if (!frm.doc.light_theme) {
			draw({});
			return;
		}
		frappe.db.get_doc("Appearance Theme", frm.doc.light_theme).then(draw).catch(() => draw({}));
	},
};
