(function () {
	function config() {
		return window.appearanceConfig || (window.frappe && frappe.boot && frappe.boot.appearance) || {};
	}

	function ready(fn) {
		if (document.readyState === "loading") {
			document.addEventListener("DOMContentLoaded", fn);
		} else {
			fn();
		}
	}

	function decorateLogin() {
		const body = document.body;
		if (!body || body.getAttribute("data-path") !== "login") return;
		const cfg = config();
		const layout = cfg.login_layout || (cfg.layout && cfg.layout.login_layout) || "Split";

		if (cfg.login_show_tagline && cfg.tagline) {
			document.querySelectorAll(".page-card-head h4").forEach((heading) => {
				if (!heading.parentNode.querySelector(".appearance-tagline")) {
					const tagline = document.createElement("p");
					tagline.className = "appearance-tagline text-muted";
					tagline.textContent = cfg.tagline;
					heading.insertAdjacentElement("afterend", tagline);
				}
			});
		}

		if (cfg.login_footer_text) {
			let footer = document.querySelector(".appearance-login-footer");
			if (!footer) {
				footer = document.createElement("p");
				footer.className = "appearance-login-footer text-muted text-center mt-3";
				const card = document.querySelector(".page-card");
				if (card) card.insertAdjacentElement("afterend", footer);
			}
			footer.textContent = cfg.login_footer_text;
		}

		if (layout === "Split" && !document.querySelector(".appearance-login-panel")) {
			body.classList.add("appearance-login-split");
			const panel = document.createElement("aside");
			panel.className = "appearance-login-panel";
			panel.innerHTML =
				"<h1>" +
				escapeHtml(cfg.product_name || "") +
				"</h1><p>" +
				escapeHtml(cfg.tagline || cfg.description || "") +
				"</p>";
			body.insertBefore(panel, body.firstChild);
		}

		if (cfg.login_logo || cfg.logo) {
			document.querySelectorAll("img.app-logo").forEach((img) => {
				img.src = cfg.login_logo || cfg.logo;
			});
		}
	}

	function escapeHtml(value) {
		return String(value || "")
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/"/g, "&quot;");
	}

	function customizeDesk() {
		if (!window.frappe) return;
		const cfg = config();
		if (!cfg.product_name) return;

		if (cfg.hide_framework_branding && frappe.ui && frappe.ui.misc) {
			frappe.ui.misc.about = function () {
				const dialog = new frappe.ui.Dialog({ title: cfg.product_name });
				dialog.$body.html(
					"<p>" +
						escapeHtml(cfg.tagline || cfg.description || "") +
						"</p><p class='text-muted'>" +
						escapeHtml(cfg.company_name || cfg.product_name) +
						"</p>"
				);
				dialog.show();
			};
		}

		$(document).on("page-change", () => {
			if (cfg.browser_title_suffix && document.title.indexOf(cfg.browser_title_suffix) === -1) {
				document.title = document.title + " · " + cfg.browser_title_suffix;
			}
			const logo = cfg.navbar_logo || cfg.logo;
			if (logo) {
				$("header .app-logo").attr("src", logo);
			}
		});

		if (cfg.hide_help_links) {
			$(".dropdown-help").hide();
		}
	}

	ready(() => {
		if (window.appearance && !window.appearanceConfig) {
			window.appearance.load((data) => {
				window.appearance.apply(data);
				decorateLogin();
				customizeDesk();
			});
		} else {
			decorateLogin();
			customizeDesk();
		}
	});

	document.addEventListener("appearance:applied", () => {
		decorateLogin();
		customizeDesk();
	});
})();
