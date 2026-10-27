# Terminal Portfolio — Rough Plan

> **Goal:** A portfolio that *looks* like a calm retro terminal, but that anyone (recruiters, HR, non-technical people) can read and click through without typing a single command.

---

## 1. Core Idea

- **Look:** retro terminal (monospace font, blinking cursor, typing effect).
- **Feel:** minimal Nordic: soft colors, lots of empty space, calm, no "hacker green on black".
- **Rule #1:** Everything must work by **clicking**. Typing commands is a fun *bonus*, never required.

---

## 2. Who Is It For?

| Visitor | What they need | How we help |
|---|---|---|
| Recruiter / HR (non-technical) | Name, role, projects, resume, contact in < 30 seconds | Big clickable menu, plain English, resume button always visible |
| Hiring manager / engineer | Project details, skills, code links | Project pages with GitHub/live links |
| Curious visitor | Something fun | Optional typed commands + hidden easter eggs |

---

## 3. Making It Easy for Non-Technical People

- [ ] **Clickable menu** that looks like terminal commands: `> about` `> projects` `> resume` `> contact`
- [ ] **Plain English text.** Write `I build websites`, not `npm run build --prod`
- [ ] **Readable font size** (at least 16–18px) and good contrast
- [ ] **Short typing animation** (1–2 seconds max) with a **"Skip"** option
- [ ] **"Download Resume" button** always visible (top right corner)
- [ ] **Hint line** at the bottom: *"Click a command above, or type `help` if you like"*
- [ ] **Works on phones.** On mobile, show only the clickable menu (no keyboard needed)
- [ ] **No sound by default.** If sound is added, it's off until turned on

---

## 4. Pages / Sections

1. **Boot screen (intro):** short "starting up…" animation, then shows your name and role
   - Example: `Hello, I'm [Your Name] — [Your Role] based in [City].`
2. **About:** 3–4 short sentences about you, plus a photo (optional, could be pixel/ASCII-style)
3. **Projects:** 3–5 best projects, each with:
   - Title, one-line description, what *you* did, tools used, link (live / GitHub), screenshot
4. **Skills:** simple grouped list (no confusing skill bars or percentages)
5. **Experience:** timeline-style list (Company · Role · Years · 1-line impact)
6. **Resume:** PDF download + view online
7. **Contact:** email, LinkedIn, GitHub (clickable links, maybe a "copy email" button)

---

## 5. Visual Style (Nordic Terminal)

**Colors (soft, not neon):** final palette to be chosen
- Background: off-white / light grey *or* deep calm blue-grey (offer light + dark mode)
- Text: charcoal / soft white
- Accent: muted Nordic blue, sage green, or soft red (just one accent)

**Fonts:**
- Monospace for headings/commands (e.g., JetBrains Mono, IBM Plex Mono, Space Mono)
- Optional: a clean sans-serif for long paragraphs (easier to read)

**Effects (use lightly):**
- Blinking cursor
- Typing effect on headings only
- Very subtle scanlines / CRT glow (optional, must not hurt readability)

---

## 6. Optional "Wow" Feature (my original idea)

- After scrolling down, a **calm fishing scene** appears in the background (lake, boat, pixel or low-poly 3D style).
- Must stay **light and fast**, and get **turned off on slow phones**.
- Decide later: pixel art (easier, faster) vs. 3D (harder, heavier).

---

## 7. Fun Extras (optional, for later)

- [ ] Typed commands: `help`, `about`, `projects`, `contact`, `clear`
- [ ] Easter eggs: `fish` → mini fishing animation, `coffee`, `sudo hire me`
- [ ] Light/dark theme toggle (`theme light` / `theme dark`)
- [ ] Command history with ↑ / ↓ arrow keys

---

## 8. Tech (simple version)

- **Build with:** HTML + CSS + JavaScript (or React/Next.js if wanted)
- **Built with help from:** Claude Code
- **Host for free:** GitHub Pages, Netlify, or Vercel
- **Domain:** yourname.com (~$10–15/year, optional)

---

## 9. Content I Need to Prepare

- [ ] Name, role, location, 1-line intro
- [ ] Short "About me" (3–4 sentences)
- [ ] 3–5 projects (description, screenshots, links)
- [ ] Skills list
- [ ] Work / education history
- [ ] Resume PDF
- [ ] Contact links (email, LinkedIn, GitHub)
- [ ] Optional photo
- [ ] 2–3 inspiration sites I like (and *why*)

---

## 10. Steps / Timeline (rough)

| Step | Task | Time |
|---|---|---|
| 1 | Collect inspiration + write content | 2–3 days |
| 2 | Choose colors, fonts, light/dark | 1 day |
| 3 | Build basic layout + clickable menu | 1–2 days |
| 4 | Add terminal effects (typing, cursor, boot screen) | 1 day |
| 5 | Make it work well on phones | 1 day |
| 6 | Optional: typed commands + easter eggs | 1 day |
| 7 | Optional: fishing background on scroll | 2–4 days |
| 8 | Test with a non-technical friend | 1 day |
| 9 | Publish online | ½ day |

---

## 11. Final Checklist Before Launch

- [ ] A non-technical friend can find my resume and contact info in under 30 seconds
- [ ] Works on phone, tablet, and laptop
- [ ] Loads in under 3 seconds
- [ ] All links work
- [ ] No spelling mistakes
- [ ] Animations can be skipped and aren't annoying
