"""Draw the neofetch avatar: a cyberpunk developer desk seen from a ~30 degree angle.

The whole scene is generated from code (no source photo), so it is original art.

Usage: python3 tools/draw_avatar.py [assets/avatar.png]
Needs: pip install pillow numpy

Layout of this file:
  palette        - colours shared by every part of the scene
  helpers        - perspective warp and small drawing utilities
  textures       - flat images (city, screens) later warped into the scene
  scene          - room, window, desk, monitors, keyboard, props
"""
import math
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SIZE = 512
random.seed(3)

# ---------- palette ----------
PINK = (255, 46, 136)
CYAN = (0, 229, 255)
PURPLE = (157, 78, 221)
AMBER = (255, 190, 70)
WHITE = (230, 225, 245)
FRAME = (12, 6, 22)
METAL = (44, 38, 62)
METAL_LIGHT = (70, 62, 94)


# ---------- helpers ----------
def perspective_coeffs(dst_quad, src_w, src_h):
    """Coefficients for Image.transform(PERSPECTIVE) mapping dst_quad back to a src_w x src_h rectangle."""
    src = [(0, 0), (src_w, 0), (src_w, src_h), (0, src_h)]
    rows, rhs = [], []
    for (x, y), (u, v) in zip(dst_quad, src):
        rows.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); rhs.append(u)
        rows.append([0, 0, 0, x, y, 1, -v * x, -v * y]); rhs.append(v)
    return np.linalg.solve(np.array(rows, float), np.array(rhs, float)).tolist()


def warp(canvas, texture, quad):
    """Paint texture onto quad (top-left, top-right, bottom-right, bottom-left) of canvas."""
    coeffs = perspective_coeffs(quad, *texture.size)
    warped = texture.transform(canvas.size, Image.PERSPECTIVE, coeffs, Image.NEAREST)
    mask = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(mask).polygon(quad, fill=255)
    canvas.paste(warped, (0, 0), mask)


def bilinear(quad, u, v):
    """Point at (u, v) inside a quad, both in 0..1."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    x = (1 - u) * (1 - v) * x0 + u * (1 - v) * x1 + u * v * x2 + (1 - u) * v * x3
    y = (1 - u) * (1 - v) * y0 + u * (1 - v) * y1 + u * v * y2 + (1 - u) * v * y3
    return x, y


def inset(quad, px):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    return [(x0 + px, y0 + px), (x1 - px, y1 + px), (x2 - px, y2 - px), (x3 + px, y3 - px)]


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def glow(canvas, shape_fn, color, blur, strength=0.55):
    """Additive soft glow drawn by shape_fn(draw) in color."""
    layer = Image.new("RGB", canvas.size, (0, 0, 0))
    shape_fn(ImageDraw.Draw(layer), color)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.blend(canvas, Image.composite(layer, canvas, layer.convert("L")), strength)


# ---------- textures ----------
def city_texture():
    w, h = 440, 264
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line((0, y, w, y), fill=mix((22, 8, 52), (170, 40, 120), y / h))
    # moon with halo
    for r, c in [(64, (120, 40, 110)), (54, (190, 70, 150)), (46, (255, 120, 175)), (38, (255, 160, 200))]:
        d.ellipse((290 - r, 100 - r, 290 + r, 100 + r), fill=c)
    for cx, cy, r in [(278, 88, 7), (300, 112, 5), (296, 82, 4)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(240, 135, 185))
    # far skyline
    x = 0
    while x < w:
        bw, bh = random.randint(22, 44), random.randint(90, 200)
        d.rectangle((x, h - bh, x + bw, h), fill=(48, 24, 82))
        if random.random() < 0.4:
            d.line((x + bw // 2, h - bh - 18, x + bw // 2, h - bh), fill=(48, 24, 82), width=2)
            d.rectangle((x + bw // 2 - 1, h - bh - 20, x + bw // 2 + 1, h - bh - 18), fill=PINK)
        x += bw + random.randint(-4, 6)
    # flying cars with light trails
    for cx, cy, color, direction in [(70, 46, CYAN, 1), (200, 84, PINK, -1), (360, 34, AMBER, 1), (140, 140, CYAN, -1)]:
        trail = range(1, 60)
        for k in trail:
            tx = cx - direction * (k + 18)
            d.point((tx, cy + 4), fill=mix((0, 0, 0), color, max(0.0, 0.7 - k / 60)))
            d.point((tx, cy + 5), fill=mix((0, 0, 0), color, max(0.0, 0.4 - k / 60)))
        d.polygon([(cx - 18, cy + 8), (cx + 18, cy + 8), (cx + 14, cy + 2), (cx - 14, cy + 2)], fill=(84, 88, 116))
        d.polygon([(cx - 8, cy + 2), (cx + 8, cy + 2), (cx + 5, cy - 3), (cx - 5, cy - 3)], fill=(120, 128, 160))
        d.rectangle((cx - 4, cy - 2, cx + 4, cy + 1), fill=(150, 220, 255))
        head = cx + 18 * direction
        d.rectangle((head - 2, cy + 4, head + 2, cy + 6), fill=WHITE)
        d.rectangle((cx - 12, cy + 9, cx + 12, cy + 10), fill=color)
    # near buildings with lit windows, signs and a billboard
    x = -6
    while x < w:
        bw, bh = random.randint(40, 64), random.randint(70, 150)
        top = h - bh
        d.rectangle((x, top, x + bw, h), fill=(18, 8, 34))
        d.line((x, top, x + bw, top), fill=(60, 30, 90))
        for wy in range(top + 8, h - 4, 10):
            for wx in range(x + 6, x + bw - 6, 9):
                if random.random() < 0.55:
                    d.rectangle((wx, wy, wx + 4, wy + 5), fill=random.choice([PINK, CYAN, AMBER, PURPLE, (90, 60, 130)]))
        if random.random() < 0.6:
            sx = x + bw - 8
            d.rectangle((sx, top + 14, sx + 4, top + 60), fill=random.choice([PINK, CYAN]))
        x += bw + random.randint(2, 10)
    d.rectangle((40, 150, 120, 186), fill=(10, 4, 20), outline=CYAN, width=2)
    for i, c in enumerate([PINK, PINK, CYAN, PINK, AMBER]):
        d.rectangle((50 + i * 13, 160, 58 + i * 13, 176), fill=c)
    # rain
    for _ in range(220):
        rx, ry = random.randrange(w), random.randrange(h)
        d.line((rx, ry, rx - 2, ry + 9), fill=(170, 150, 220))
    return img


def dashboard_texture():
    img = Image.new("RGB", (192, 132), (10, 12, 28))
    d = ImageDraw.Draw(img)
    d.rectangle((6, 6, 92, 58), outline=CYAN, width=2)
    d.rectangle((14, 14, 84, 50), fill=(0, 90, 110))
    d.ellipse((30, 18, 66, 46), outline=CYAN, width=3)
    d.arc((30, 18, 66, 46), 0, 250, fill=PINK, width=4)
    for i, (c, ln) in enumerate([(PINK, 80), (PURPLE, 60), (AMBER, 44), (CYAN, 70)]):
        d.rectangle((102, 8 + i * 13, 102 + ln, 15 + i * 13), fill=c)
    for i, hgt in enumerate([24, 40, 30, 52, 36, 58, 46, 62, 40, 50, 34, 56, 44, 60]):
        d.rectangle((8 + i * 13, 126 - hgt, 16 + i * 13, 126), fill=CYAN if i % 2 else (0, 150, 180))
    return img


def waveform_texture():
    img = Image.new("RGB", (192, 132), (18, 10, 32))
    d = ImageDraw.Draw(img)
    for x in range(0, 192, 16):
        d.line((x, 0, x, 132), fill=(44, 26, 66))
    for y in range(0, 132, 16):
        d.line((0, y, 192, y), fill=(44, 26, 66))
    prev_a = prev_b = None
    for x in range(192):
        a = (x, 60 + 34 * math.sin(x / 13))
        b = (x, 70 + 20 * math.cos(x / 9))
        if prev_a:
            d.line((prev_a, a), fill=PINK, width=3)
            d.line((prev_b, b), fill=AMBER, width=2)
        prev_a, prev_b = a, b
    d.text((6, 4), "SIGNAL 98%", fill=CYAN)
    return img


def code_texture():
    img = Image.new("RGB", (160, 132), (10, 16, 26))
    d = ImageDraw.Draw(img)
    lines = [
        (0, [(PINK, 24), (WHITE, 40)]), (1, [(CYAN, 30), (WHITE, 22), (AMBER, 18)]),
        (2, [(WHITE, 46)]), (2, [(CYAN, 20), (PINK, 28)]), (1, [(AMBER, 36)]),
        (1, [(PINK, 18), (WHITE, 50)]), (2, [(CYAN, 40), (WHITE, 14)]), (0, [(PINK, 12)]),
        (0, [(PINK, 24), (WHITE, 30)]), (1, [(CYAN, 52)]),
    ]
    for i, (indent, tokens) in enumerate(lines):
        y = 6 + i * 12
        d.rectangle((4, y, 12, y + 4), fill=(70, 80, 100))  # line number
        x = 20 + indent * 12
        for color, ln in tokens:
            d.rectangle((x, y, x + ln, y + 4), fill=color)
            x += ln + 6
    d.rectangle((20, 6 + len(lines) * 12, 26, 6 + len(lines) * 12 + 6), fill=WHITE)  # cursor
    return img


# ---------- scene ----------
def draw_scene():
    img = Image.new("RGB", (SIZE, SIZE))
    d = ImageDraw.Draw(img)
    for y in range(SIZE):                                       # back wall
        d.line((0, y, SIZE, y), fill=mix((26, 12, 44), (40, 20, 62), y / SIZE))

    window = [(16, 16), (496, 64), (496, 284), (16, 332)]       # receding window
    warp(img, city_texture(), window)
    img = glow(img, lambda g, c: g.polygon(window, fill=c), (120, 40, 140), 20, 0.25)
    d = ImageDraw.Draw(img)
    for a, b in [(0, 1), (3, 2), (0, 3), (1, 2)]:
        d.line((window[a], window[b]), fill=FRAME, width=8)
    for u in (0.36, 0.7):                                        # mullions
        d.line((bilinear(window, u, 0), bilinear(window, u, 1)), fill=FRAME, width=6 if u < 0.5 else 4)
    d.line((bilinear(window, 0, 0.42), bilinear(window, 1, 0.42)), fill=FRAME, width=3)
    for k in range(3):                                          # glass reflections
        x = 60 + k * 26
        d.line((x, 40, x + 40, 120), fill=(70, 50, 110), width=2)

    desk = [(0, 336), (512, 288), (512, 400), (0, 480)]          # desk top + front edge
    d.polygon(desk, fill=(46, 28, 62))
    for k in range(1, 7):                                       # wood grain
        d.line((bilinear(desk, 0, k / 7), bilinear(desk, 1, k / 7)), fill=(52, 32, 70), width=1)
    d.line((desk[0], desk[1]), fill=(96, 56, 124), width=2)
    d.polygon([(0, 480), (512, 400), (512, 424), (0, 512)], fill=(30, 18, 42))

    monitors = [
        ([(16, 152), (168, 160), (168, 288), (16, 304)], dashboard_texture(), CYAN),
        ([(180, 160), (332, 168), (332, 284), (180, 292)], waveform_texture(), PINK),
        ([(344, 168), (448, 184), (448, 272), (344, 284)], code_texture(), CYAN),
    ]
    for quad, _, color in monitors:                              # light spill on desk
        cx = (quad[0][0] + quad[1][0]) / 2
        img = glow(img, lambda g, c, cx=cx: g.ellipse((cx - 70, 316, cx + 70, 360), fill=c), color, 18, 0.35)
    d = ImageDraw.Draw(img)
    for quad, texture, _ in monitors:
        mx = (quad[0][0] + quad[1][0]) // 2
        my = (quad[2][1] + quad[3][1]) // 2
        d.rectangle((mx - 5, my - 4, mx + 5, my + 34), fill=METAL)             # stand
        d.polygon([(mx - 28, my + 36), (mx + 26, my + 32), (mx + 30, my + 40), (mx - 24, my + 44)], fill=METAL)
        depth = [quad[1], (quad[1][0] + 6, quad[1][1] + 4), (quad[2][0] + 6, quad[2][1] - 2), quad[2]]
        d.polygon(depth, fill=(20, 16, 30))                                    # monitor thickness
        d.polygon(quad, fill=(8, 6, 14))                                       # bezel
        warp(img, texture, inset(quad, 7))
        d = ImageDraw.Draw(img)
        d.line((quad[3], quad[2]), fill=METAL_LIGHT, width=2)

    keyboard = [(64, 392), (264, 364), (280, 400), (80, 432)]
    underglow = [(58, 398), (270, 368), (288, 410), (74, 442)]
    img = glow(img, lambda g, c: g.polygon(underglow, fill=c), PURPLE, 10, 0.8)
    d = ImageDraw.Draw(img)
    d.polygon(keyboard, fill=(28, 22, 42))
    rows, cols = 5, 15
    for r in range(rows):
        for k in range(cols):
            span = 6 if r == rows - 1 and 4 <= k <= 9 else 1
            if r == rows - 1 and 5 <= k <= 9:
                continue
            u0, u1 = (k + 0.12) / cols, (k + span - 0.12) / cols
            v0, v1 = (r + 0.18) / rows, (r + 0.82) / rows
            key = [bilinear(keyboard, u0, v0), bilinear(keyboard, u1, v0), bilinear(keyboard, u1, v1), bilinear(keyboard, u0, v1)]
            color = WHITE if span > 1 else mix(PINK, CYAN, k / (cols - 1))
            d.polygon(key, fill=color)

    d.polygon([(300, 368), (380, 356), (392, 392), (312, 404)], fill=(34, 24, 50))   # mouse pad
    d.ellipse((330, 366, 356, 386), fill=METAL_LIGHT)
    d.line((343, 368, 343, 374), fill=CYAN, width=2)

    d.rectangle((404, 300, 436, 340), fill=(140, 80, 56))                          # mug
    d.ellipse((404, 294, 436, 306), fill=(150, 88, 62))
    d.ellipse((408, 297, 432, 304), fill=(70, 36, 24))
    d.arc((428, 306, 448, 330), -90, 90, fill=(140, 80, 56), width=5)
    for k in range(3):                                                             # steam
        pts = [(414 + k * 7 + 4 * math.sin(t / 3 + k), 290 - t) for t in range(0, 40, 2)]
        d.line(pts, fill=(170, 150, 205), width=2)
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/avatar.png"
    draw_scene().save(out)
    print("saved", out)
