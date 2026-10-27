"""Draw the link-preview image and the home-screen icon from the site's own fonts and avatar.

Outputs:
  assets/og-image.png          1200x630 card shown when the site is shared (LinkedIn, WhatsApp, ...)
  assets/apple-touch-icon.png  180x180 icon for phone home screens
The browser-tab icon is the hand-written assets/favicon.svg.

Usage: python3 tools/draw_social.py
Needs: pip install pillow  (with WOFF2 support, standard in current wheels)
Run it again after changing the name, role or avatar.
"""
from PIL import Image, ImageDraw, ImageFont

# Same values as css/tokens.css (dark theme) so the card matches the site.
BG = (31, 37, 43)
PANEL = (37, 44, 51)
TEXT = (223, 228, 226)
MUTED = (148, 160, 168)
ACCENT = (143, 181, 204)
SAGE = (163, 191, 168)

NAME = "Abhishek Man Basnet"
ROLE = "Software Engineer"
DETAIL = "Flutter · Django · Go"
URL = "abhishekbasnet.github.io"
PROMPT = "abhishek@dev:~$ whoami"

SANS = "assets/fonts/dm-sans-latin-wght-normal.woff2"
MONO = "assets/fonts/ibm-plex-mono-latin-500-normal.woff2"


def sans(size, weight):
    font = ImageFont.truetype(SANS, size)
    axes = font.get_variation_axes()
    font.set_variation_by_axes([weight if a["name"] in (b"Weight", "Weight") else a["default"] for a in axes])
    return font


def og_image():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)

    side = 320
    avatar = Image.open("assets/avatar.png").convert("RGB").resize((side, side), Image.NEAREST)
    ax, ay = w - side - 72, (h - side) // 2
    d.rounded_rectangle((ax - 12, ay - 12, ax + side + 12, ay + side + 12), radius=18, fill=PANEL)
    img.paste(avatar, (ax, ay))

    x = 72
    d.text((x, 150), PROMPT, font=ImageFont.truetype(MONO, 28), fill=SAGE)
    d.text((x, 200), NAME, font=sans(64, 700), fill=TEXT)
    d.text((x, 290), ROLE, font=sans(40, 500), fill=ACCENT)
    d.text((x, 345), DETAIL, font=sans(32, 400), fill=MUTED)
    d.line((x, 430, x + 80, 430), fill=ACCENT, width=4)
    d.text((x, 455), URL, font=sans(28, 500), fill=MUTED)
    img.save("assets/og-image.png", optimize=True)


def touch_icon():
    size = 180
    img = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(img)
    d.text((size // 2, size // 2), ">_", font=ImageFont.truetype(MONO, 84), fill=ACCENT, anchor="mm")
    img.save("assets/apple-touch-icon.png", optimize=True)


if __name__ == "__main__":
    og_image()
    touch_icon()
    print("saved assets/og-image.png and assets/apple-touch-icon.png")
