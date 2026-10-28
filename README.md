# Abhishek Man Basnet — Portfolio

A terminal-style personal portfolio with a calm Nordic look. Plain HTML, CSS and JavaScript: no build step, no dependencies.

Live: https://abhishekbasnet.github.io

## Preview locally

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Project structure

```
index.html                 All page content (edit text here)
404.html                   Shown by GitHub Pages for any missing URL (absolute paths only)
css/
  fonts.css                Self-hosted @font-face rules (DM Sans, IBM Plex Mono)
  tokens.css               Colours, fonts, sizes (light + dark themes)
  base.css                 Element defaults: body, headings, links, buttons
  layout.css               Page skeleton: top bar, menu/sidebar, columns, breakpoints
  components/              One file per page part
    boot.css  sky.css  theme-switch.css  fetch.css  timeline.css  cards.css  education.css  skills.css  contact.css  cli.css  notfound.css
js/
  theme.js                 Light/dark toggle (loaded first, exposes window.Portfolio.theme)
  boot.js                  Startup animation
  nav.js                   Highlights the current section in the menu
  fetch.js                 Opens/closes the neofetch quick-facts dialog
  contact.js               Copy-email button, footer year
  cli.js                   Optional typed commands (help, fish, theme, ...)
assets/
  avatar.png               128x128 pixel-art scene in the neofetch dialog
  resume.pdf               CV behind the Resume button (replace this file to update it)
  favicon.svg              Browser-tab icon
  og-image.png             Link-preview card, apple-touch-icon.png: phone home-screen icon
  fonts/                   woff2 files + their SIL OFL licences
tools/
  draw_avatar.py           Generates assets/avatar.png from code
  pixelate.py              Turns a real photo into a pixel-art avatar
  draw_social.py           Generates og-image.png and apple-touch-icon.png
docs/
  portfolio-plan.md        Original plan and content checklist
```

## Common edits

| I want to...                     | Edit                                                    |
|----------------------------------|---------------------------------------------------------|
| Change text, projects, jobs      | `index.html` (look for `DRAFT` / `TODO` comments)       |
| Change colours or fonts          | `css/tokens.css` (font files: `css/fonts.css`)          |
| Change the daily sky backdrop    | Its look: `css/components/sky.css`. The art itself is built daily by `scripts/build_assets.py` in the [profile repo](https://github.com/AbhishekBasnet/AbhishekBasnet) |
| Update the link-preview image    | Edit text in `tools/draw_social.py`, then run it        |
| Change the `user@host:~$` prompt | `css/tokens.css`: `--prompt-user`, `--prompt-host`      |
| Change email                     | `index.html`: the `mailto:` link with `id="email-link"` |
| Update resume                    | Replace `assets/resume.pdf` (keep the name)             |
| Add a new section                | `index.html`: add `<section id="x">` and a menu link `<a href="#x">` (the `x` command works automatically) |
| Add a typed command              | `js/cli.js`, `commands` object                          |
| Regenerate the avatar            | `pip install pillow && python3 tools/draw_avatar.py` |
| Use my own photo as avatar       | `python3 tools/pixelate.py photo.jpg`                   |

## Deploy

GitHub Pages serves the `main` branch. Work on the `draft` branch, then merge into `main` to publish.
