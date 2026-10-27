"""Turn a photo into an 8-bit style avatar for the neofetch panel.

Usage: python3 tools/pixelate.py my-photo.jpg [assets/avatar.png]
Needs Pillow: pip install pillow
"""
import sys
from PIL import Image, ImageOps

SIZE = 40      # pixels across; smaller = blockier
COLORS = 12    # palette size; smaller = more retro

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "assets/avatar.png"

img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
side = min(img.size)
left = (img.width - side) // 2
top = (img.height - side) // 4  # bias upward to keep the face in frame
img = img.crop((left, top, left + side, top + side))
img = ImageOps.autocontrast(img, cutoff=1)
img = img.resize((SIZE, SIZE), Image.LANCZOS)
img = img.quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
img.convert("RGB").save(out)
print("saved", out)
