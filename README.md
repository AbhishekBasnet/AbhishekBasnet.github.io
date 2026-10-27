# Abhishek Basnet — Portfolio

A terminal-style personal portfolio with a calm Nordic look. Plain HTML, CSS and JavaScript: no build step, no dependencies.

Live: https://asyncabhi.me (custom domain via `CNAME`), fallback https://abhishekbasnet.github.io

## Preview locally

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Project structure

```
index.html                 All page content (edit text here)
css/
  tokens.css               Colours, fonts, sizes (light + dark themes)
  base.css                 Element defaults: body, headings, links, buttons
  layout.css               Page skeleton: top bar, menu/sidebar, columns, breakpoints
  components/              One file per page part
    boot.css  fetch.css  timeline.css  cards.css  skills.css  contact.css  cli.css
js/
  theme.js                 Light/dark toggle (loaded first, exposes window.Portfolio.theme)
  boot.js                  Startup animation
  nav.js                   Highlights the current section in the menu
  contact.js               Copy-email button, footer year
  cli.js                   Optional typed commands (help, fish, theme, ...)
assets/
  avatar.png               512x512 pixel-art scene in the neofetch panel
tools/
  draw_avatar.py           Generates assets/avatar.png from code
  pixelate.py              Turns a real photo into a pixel-art avatar
docs/
  portfolio-plan.md        Original plan and content checklist
```

## Common edits

| I want to...                     | Edit                                                    |
|----------------------------------|---------------------------------------------------------|
| Change text, projects, jobs      | `index.html` (look for `DRAFT` / `TODO` comments)       |
| Change colours or fonts          | `css/tokens.css`                                        |
| Change the `user@host:~$` prompt | `css/tokens.css`: `--prompt-user`, `--prompt-host`      |
| Change email                     | `index.html`: the `mailto:` link with `id="email-link"` |
| Change resume file               | `index.html`: the link with `id="resume-link"`          |
| Add a new section                | `index.html`: add `<section id="x">` and a menu link `<a href="#x">` (the `x` command works automatically) |
| Add a typed command              | `js/cli.js`, `commands` object                          |
| Regenerate the avatar            | `pip install pillow numpy && python3 tools/draw_avatar.py` |
| Use my own photo as avatar       | `python3 tools/pixelate.py photo.jpg`                   |

## Deploy

GitHub Pages serves the `main` branch. Work on the `draft` branch, then merge into `main` to publish.
