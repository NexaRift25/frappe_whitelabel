# Appearance

This app is a **product identity and appearance layer** for Frappe. It does not fork Frappe or ERPNext, and it is not a white-label wrapper that only swaps a logo.

Frappe stays the framework. This app owns the product name, visual design, and the admin UI used to change that identity at runtime.

## What administrators can change from the UI

Open **Appearance** in the desk sidebar, then **Appearance Settings**.

- Product name, short name, company name, tagline, description
- Logo, dark logo, login logo, navbar logo, favicon, app icon, splash logo
- Light and dark themes, including colors and fonts
- Sidebar, navbar, buttons, cards, tables, forms, radius, page background
- Login layout, login background, login footer
- Email footer and print header text

Changes are stored in the site database and applied without editing source, CSS files, Docker files, or rebuilding the image. Reload the desk after saving to see every surface update.

## Architecture

```text
Administrator
      │
      ▼
Appearance Settings / Appearance Theme   (DocTypes, per site)
      │
      ▼
branding.service                         (read config, generate CSS)
      │
      ├── Website Settings / Navbar Settings / System Settings
      ├── /files/appearance-runtime.css
      └── bootinfo + login context
              │
              ├── Desk UI (CSS variables + layout attributes)
              └── Login / website / email / splash
```

Supported extension points used:

- `app_include_css` / `app_include_js` / `web_include_css` / `web_include_js`
- `extend_bootinfo` and `update_website_context`
- Jinja template overrides for splash and email header (app templates take precedence over Frappe)
- Native **Website Settings**, **Navbar Settings**, and **System Settings** as the runtime targets for name, logo, favicon, splash, and email footer
- Site file `/files/appearance-runtime.css` so token CSS is generated per site and does not require `bench build`

ERPNext is unchanged. Any ERPNext screen still uses Frappe's desk chrome, which this app restyles.

## Themes

Two system themes are installed by default:

- **Daylight** (light)
- **Midnight** (dark)

All themes — including system themes — can be edited and saved from the UI. Changes apply immediately when that theme is active.

- **Duplicate** — create a new theme based on an existing one
- **Activate** — switch the active light or dark theme
- **Reset to Factory** — restore a system theme’s original colors (Daylight / Midnight only)
- **Activate System Defaults** — set Daylight and Midnight as the active themes

System themes cannot be deleted. Custom themes can be deleted when they are not active.

Saving an active theme updates the desk without editing source code or redeploying.

## Upgrade safety

Frappe core is not patched. Identity is applied through hooks, DocTypes, generated CSS, and template overrides in this app.

## Known Frappe v14 limitations

These cannot be changed dynamically without copying core templates, which would drift on upgrade:

| Surface | Behavior |
| --- | --- |
| Desk HTML `<title>` in `www/app.html` | Hardcoded as `Frappe` in core. This app sets the tab title with JavaScript as soon as boot runs. |
| Desk first paint | Core `app.html` does not allow inline head injection. Tokens are applied from boot JS and `/files/appearance-runtime.css`. A brief flash of default styles can appear on a slow load. |
| Help → About | Replaced in JavaScript when **Hide Framework Branding** is enabled. |
| Sidebar on the right | Frappe v14 desk chrome is left-sidebar. This app offers style/behavior, not a true right-hand sidebar. |
| Every empty state / icon | Many icons are SVG sprites inside Frappe. Color follows theme tokens; swapping every glyph is not supported without core edits. |
| PDF letterheads | Use **Letter Head** and the generated **Appearance** print style. Complex print layouts remain Print Format work. |
| `default_mail_footer` from ERPNext | Disabled through System Settings (`disable_standard_email_footer`) so the product footer can replace "Sent via ERPNext". |

If a future requirement truly needs a core change, it should be documented as a fork/patch with an upgrade cost. This app does not do that.

## After deploy

```bash
bench --site <site> install-app frappe_whitelabel
bench --site <site> migrate
bench build --app frappe_whitelabel
bench --site <site> clear-cache
```

Then sign in as a System Manager and open **Appearance → Appearance Settings**.
