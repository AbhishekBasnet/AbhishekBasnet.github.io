"""Draw the neofetch avatar: a 128x128 cyberpunk developer desk seen from a ~30 degree angle.

The whole scene is generated from code (no source photo), so it is original art.
The page scales it up with `image-rendering: pixelated` (css/components/fetch.css).

Usage: python3 tools/draw_avatar.py [assets/avatar.png]
Needs: pip install pillow

Layout of this file:
  palette   - colours shared by every part of the scene
  helpers   - perspective warp and small geometry utilities
  textures  - flat images (city, screens) later warped into the scene
  scene     - room, window, desk, monitors, keyboard, props
Textures are drawn before the scene and in a fixed order: the city uses the
seeded random generator, so changing the order changes the art.
"""
import math
import random
import sys

from PIL import Image, ImageDraw

SIZE = 128
SEED = 3

# ---------- palette ----------
PINK = (255, 46, 136)
CYAN = (0, 229, 255)
PURPLE = (157, 78, 221)
AMBER = (255, 190, 70)
WHITE = (230, 225, 245)
FRAME = (12, 6, 22)
METAL = (40, 34, 56)


# ---------- helpers ----------
def new_texture(w, h, bg):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def bilinear(quad, u, v):
    """Point at (u, v) inside a quad (top-left, top-right, bottom-right, bottom-left), both in 0..1."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    x = (1 - u) * (1 - v) * x0 + u * (1 - v) * x1 + u * v * x2 + (1 - u) * v * x3
    y = (1 - u) * (1 - v) * y0 + u * (1 - v) * y1 + u * v * y2 + (1 - u) * v * y3
    return x, y


def warp(canvas, texture, quad):
    """Paint texture onto quad of canvas, nearest-pixel, by sampling it densely."""
    tw, th = texture.size
    n = 4 * max(tw, th)
    dst, src = canvas.load(), texture.load()
    for i in range(n + 1):
        u = i / n
        for j in range(n + 1):
            v = j / n
            x, y = bilinear(quad, u, v)
            xi, yi = int(x), int(y)
            if 0 <= xi < SIZE and 0 <= yi < SIZE:
                dst[xi, yi] = src[min(int(u * tw), tw - 1), min(int(v * th), th - 1)]


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def inset(quad, px):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    return [(x0 + px, y0 + px), (x1 - px, y1 + px), (x2 - px, y2 - px), (x3 + px, y3 - px)]


# ---------- textures ----------
def city_texture(rng):
    img, d = new_texture(110, 66, (0, 0, 0))
    for y in range(66):
        t = y / 65
        d.line((0, y, 109, y), fill=(int(30 + 120 * t), int(10 + 20 * t), int(60 + 60 * t)))
    d.ellipse((66, 14, 90, 38), fill=(255, 110, 170))                 # neon moon
    d.ellipse((70, 18, 86, 34), fill=(255, 150, 195))
    far = [(0, 10, 34), (9, 8, 44), (18, 12, 30), (31, 9, 50), (41, 14, 36),
           (56, 8, 46), (65, 12, 28), (78, 10, 40), (89, 9, 52), (99, 11, 34)]
    for x0, w, h in far:
        d.rectangle((x0, 66 - h, x0 + w - 1, 65), fill=(40, 22, 70))
    near = [(2, 12, 26), (16, 10, 38), (30, 14, 22), (46, 9, 32),
            (58, 14, 20), (74, 11, 30), (88, 14, 24), (102, 8, 36)]
    for x0, w, h in near:                                              # lit windows
        d.rectangle((x0, 66 - h, x0 + w - 1, 65), fill=(18, 8, 34))
        for y in range(67 - h, 64, 3):
            for x in range(x0 + 2, x0 + w - 2, 3):
                if rng.random() < 0.5:
                    d.point((x, y), fill=rng.choice([PINK, CYAN, AMBER, PURPLE]))
    d.rectangle((19, 32, 20, 44), fill=PINK)                           # neon signs
    d.rectangle((50, 38, 51, 47), fill=CYAN)
    d.rectangle((76, 40, 83, 41), fill=AMBER)
    for x, y, color, direction in [(22, 10, CYAN, 1), (52, 20, PINK, -1), (92, 8, AMBER, 1)]:
        d.rectangle((x, y, x + 8, y + 2), fill=(70, 74, 96))            # flying car
        d.rectangle((x + 2, y - 1, x + 6, y - 1), fill=(110, 116, 140))
        d.point((x + 9 if direction > 0 else x - 1, y + 1), fill=color)
        tx0, tx1 = (x - 10, x - 1) if direction > 0 else (x + 9, x + 18)
        length = tx1 - tx0 + 1
        for k, tx in enumerate(range(tx0, tx1 + 1)):                   # light trail
            f = (k + 1) / length if direction > 0 else 1 - k / length
            d.point((tx, y + 1), fill=tuple(int(c * f * 0.6) for c in color))
    for _ in range(45):                                                # rain
        x, y = rng.randrange(110), rng.randrange(60)
        d.line((x, y, x, y + 2), fill=(150, 130, 200))
    return img


def dashboard_texture():
    img, d = new_texture(36, 26, (12, 14, 30))
    d.rectangle((2, 2, 15, 11), outline=CYAN)
    d.rectangle((5, 5, 12, 8), fill=(0, 120, 140))
    d.rectangle((18, 2, 33, 4), fill=PINK)
    d.rectangle((18, 7, 29, 8), fill=PURPLE)
    d.rectangle((18, 10, 26, 11), fill=AMBER)
    for i, h in enumerate([4, 7, 5, 9, 6, 10, 8, 11, 7, 9]):
        d.rectangle((3 + i * 3, 23 - h, 4 + i * 3, 23), fill=CYAN if i % 2 else (0, 160, 190))
    return img


def waveform_texture():
    img, d = new_texture(36, 26, (18, 10, 30))
    for x in range(0, 36, 6):
        d.line((x, 0, x, 25), fill=(40, 24, 60))
    for y in range(0, 26, 6):
        d.line((0, y, 35, y), fill=(40, 24, 60))
    for x in range(36):
        d.point((x, int(12 + 7 * math.sin(x / 3.0))), fill=PINK)
        d.point((x, int(13 + 4 * math.cos(x / 2.2))), fill=AMBER)
    return img


def code_texture():
    img, d = new_texture(30, 26, (10, 16, 26))
    lines = [(1, 10, PINK), (3, 16, CYAN), (3, 12, WHITE), (5, 14, CYAN), (5, 8, AMBER),
             (3, 18, WHITE), (1, 6, PINK), (3, 13, CYAN), (3, 9, WHITE)]
    for i, (indent, length, color) in enumerate(lines):
        y = 2 + i * 3
        d.line((indent, y, indent + length, y), fill=color)
    d.rectangle((14, 23, 15, 24), fill=WHITE)                          # cursor
    return img


# ---------- scene ----------
def draw_scene():
    rng = random.Random(SEED)
    city = city_texture(rng)
    screens = [dashboard_texture(), waveform_texture(), code_texture()]

    img = Image.new("RGB", (SIZE, SIZE))
    d = ImageDraw.Draw(img)
    for y in range(SIZE):                                              # back wall
        d.line((0, y, SIZE - 1, y), fill=(24 + y // 16, 12 + y // 32, 40 + y // 10))

    window = [(4, 4), (122, 16), (122, 70), (4, 82)]                   # receding window
    warp(img, city, window)
    for a, b in [(0, 1), (3, 2), (0, 3), (1, 2)]:
        d.line((window[a], window[b]), fill=FRAME, width=2)
    for u in (0.36, 0.7):                                              # mullions
        d.line((lerp(window[0], window[1], u), lerp(window[3], window[2], u)), fill=FRAME, width=2 if u < 0.5 else 1)

    desk = [(0, 84), (128, 72), (128, 100), (0, 120)]                  # desk top + front edge
    d.polygon(desk, fill=(44, 26, 58))
    d.line((desk[0], desk[1]), fill=(80, 46, 104))
    d.polygon([(0, 120), (128, 100), (128, 106), (0, 127)], fill=(30, 18, 40))
    for x0, y0 in [(10, 86), (48, 82), (88, 78)]:                      # screen glow on desk
        d.ellipse((x0, y0, x0 + 28, y0 + 8), fill=(60, 34, 84))

    monitors = [[(4, 38), (42, 40), (42, 72), (4, 76)],                # narrower to the right
                [(45, 40), (83, 42), (83, 71), (45, 73)],
                [(86, 42), (112, 46), (112, 68), (86, 71)]]
    for quad, screen in zip(monitors, screens):
        d.polygon(quad, fill=(8, 6, 14))                               # bezel
        warp(img, screen, inset(quad, 2))
        mx = (quad[0][0] + quad[1][0]) // 2
        my = (quad[2][1] + quad[3][1]) // 2
        d.rectangle((mx - 1, my, mx + 1, my + 8), fill=METAL)          # stand
        d.polygon([(mx - 6, my + 9), (mx + 6, my + 8), (mx + 7, my + 10), (mx - 5, my + 11)], fill=METAL)

    keyboard = [(16, 98), (66, 91), (70, 100), (20, 108)]
    d.polygon([(15, 100), (68, 93), (72, 102), (19, 110)], fill=(120, 30, 120))   # RGB underglow
    d.polygon(keyboard, fill=(26, 20, 40))
    for row in range(4):                                               # keys, drawn per pixel row
        for col in range(13):
            x, y = bilinear(keyboard, (col + 0.5) / 13, (row + 0.6) / 4.4)
            t = col / 12
            color = (int(255 * (1 - t)), int(46 * (1 - t) + 229 * t), int(136 * (1 - t) + 255 * t))
            if row == 3 and 3 <= col <= 8:
                color = (200, 190, 230)                                # space bar
            d.rectangle((int(x) - 1, int(y), int(x) + 1, int(y)), fill=color)

    d.ellipse((78, 93, 85, 98), fill=METAL)                            # mouse
    d.point((81, 94), fill=CYAN)
    d.rectangle((100, 80, 107, 89), fill=(130, 74, 52))                # mug + steam
    d.rectangle((101, 80, 106, 81), fill=(70, 36, 24))
    d.rectangle((108, 82, 109, 86), fill=(130, 74, 52))
    for x, y in [(102, 77), (103, 75), (102, 73), (104, 71), (103, 69)]:
        d.point((x, y), fill=(170, 150, 200))
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/avatar.png"
    draw_scene().save(out)
    print("saved", out)
