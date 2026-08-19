(function () {
	if (window.__appearanceRuntime) {
		return;
	}
	window.__appearanceRuntime = true;

	function slug(value) {
		return String(value || "default")
			.trim()
			.toLowerCase()
			.replace(/\s+/g, "-");
	}

	function setVar(name, value) {
		if (!value) return;
		document.documentElement.style.setProperty(name, value);
	}

	function applyTokens(tokens) {
		if (!tokens) return;
		setVar("--primary-color", tokens.primary_color);
		setVar("--primary", tokens.primary_color);
		setVar("--brand-color", tokens.primary_color);
		setVar("--text-color", tokens.text_color);
		setVar("--heading-color", tokens.text_color);
		setVar("--text-muted", tokens.muted_text_color);
		setVar("--text-light", tokens.muted_text_color);
		setVar("--border-color", tokens.border_color);
		setVar("--dark-border-color", tokens.border_color);
		setVar("--navbar-bg", tokens.navbar_color);
		if (tokens.font_family && tokens.font_family !== "System UI") {
			loadFont(tokens.font_family);
			setVar("--font-stack", '"' + tokens.font_family + '", "Segoe UI", sans-serif');
		}
		if (tokens.heading_font && tokens.heading_font !== "System UI") {
			loadFont(tokens.heading_font);
		}
		if (tokens.base_font_size) {
			setVar("--text-base", tokens.base_font_size);
		}
	}

	function loadFont(family) {
		const id = "appearance-font-" + family.replace(/\s+/g, "-");
		if (document.getElementById(id)) return;
		const link = document.createElement("link");
		link.id = id;
		link.rel = "stylesheet";
		link.href =
			"https://fonts.googleapis.com/css2?family=" +
			encodeURIComponent(family) +
			":wght@400;500;600;700&display=swap";
		document.head.appendChild(link);
	}

	function applyLayout(config) {
		const layout = config.layout || config;
		const root = document.documentElement;
		root.setAttribute("data-appearance-sidebar", slug(layout.sidebar_style));
		root.setAttribute("data-appearance-navbar", slug(layout.navbar_style));
		root.setAttribute("data-appearance-buttons", slug(layout.button_style));
		root.setAttribute("data-appearance-cards", slug(layout.card_style));
		root.setAttribute("data-appearance-tables", slug(layout.table_style));
		root.setAttribute("data-appearance-forms", slug(layout.form_style));
		root.setAttribute("data-appearance-radius", slug(layout.border_radius));
		root.setAttribute("data-appearance-sidebar-behavior", slug(layout.sidebar_behavior));
		root.setAttribute("data-logo-placement", slug(layout.logo_placement));
		root.setAttribute("data-page-background", slug(layout.page_background));
		root.setAttribute("data-login-layout", slug(layout.login_layout || config.login_layout));
		root.setAttribute("data-hide-help", config.hide_help_links ? "1" : "0");
	}

	function setFavicon(url) {
		if (!url) return;
		["icon", "shortcut icon"].forEach((rel) => {
			let link = document.querySelector('link[rel="' + rel + '"]');
			if (!link) {
				link = document.createElement("link");
				link.rel = rel;
				document.head.appendChild(link);
			}
			link.href = url;
		});
	}

	function setTitle(config) {
		const name = config.product_name;
		if (!name) return;
		if (!document.title || document.title === "Frappe" || document.title === "Login") {
			document.title = name;
		}
		const suffix = config.browser_title_suffix;
		if (suffix && document.title.indexOf(suffix) === -1 && document.title.indexOf(name) === -1) {
			document.title = document.title + " · " + suffix;
		}
		const meta = document.querySelector('meta[name="application-name"]');
		if (meta) meta.setAttribute("content", name);
	}

	function setLogos(config) {
		const logo = config.navbar_logo || config.logo;
		if (logo) {
			document.querySelectorAll("header .app-logo, .navbar .app-logo").forEach((img) => {
				img.src = logo;
			});
		}
		const loginLogo = config.login_logo || config.logo;
		if (loginLogo) {
			document.querySelectorAll(".page-card-head .app-logo, img.app-logo").forEach((img) => {
				if (document.body && document.body.getAttribute("data-path") === "login") {
					img.src = loginLogo;
				}
			});
		}
		const splash = config.splash_logo || config.logo;
		if (splash) {
			document.querySelectorAll(".splash img, .appearance-splash img").forEach((img) => {
				img.src = splash;
			});
		}
	}

	function currentTokens(config) {
		const theme = (document.documentElement.getAttribute("data-theme") || "light").toLowerCase();
		if (theme === "dark") {
			return config.dark_tokens || config.light_tokens;
		}
		return config.light_tokens || config.dark_tokens;
	}

	function applyAppearance(config) {
		if (!config) return;
		window.appearanceConfig = config;
		applyTokens(currentTokens(config));
		applyLayout(config);
		setFavicon(config.favicon);
		setTitle(config);
		setLogos(config);
		document.dispatchEvent(new CustomEvent("appearance:applied", { detail: config }));
	}

	function loadConfig(callback) {
		if (window.frappe && frappe.boot && frappe.boot.appearance) {
			callback(frappe.boot.appearance);
			return;
		}
		fetch("/api/method/frappe_whitelabel.api.get_branding")
			.then((response) => response.json())
			.then((data) => callback(data.message || {}))
			.catch(() => callback({}));
	}

	loadConfig(applyAppearance);

	document.addEventListener("theme-change", () => {
		if (window.appearanceConfig) {
			applyTokens(currentTokens(window.appearanceConfig));
		}
	});

	const observer = new MutationObserver(() => {
		if (window.appearanceConfig) {
			applyTokens(currentTokens(window.appearanceConfig));
		}
	});
	observer.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

	window.appearance = {
		apply: applyAppearance,
		load: loadConfig,
	};
})();
