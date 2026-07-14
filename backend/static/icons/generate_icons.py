"""
Generates the IDPDR PWA icon set from the app's brand gradient
(--primary #00C2FF -> --purple #8B5CF6, matching index.html's .logo-icon).
Run once: python generate_icons.py
Requires Pillow (already in backend/requirements.txt).
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))

def gradient(size, c1=(0, 194, 255), c2=(139, 92, 246)):
    img = Image.new("RGB", (size, size), c1)
    px = img.load()
    for y in range(size):
        t = y / size
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        for x in range(size):
            px[x, y] = (r, g, b)
    return img

def rounded_mask(size, radius_ratio=0.22):
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * radius_ratio), fill=255)
    return mask

def make_icon(size, path, maskable=False, pad_ratio=0.0):
    canvas = gradient(size)
    if maskable:
        # Maskable icons need full-bleed background with content in the
        # "safe zone" (inner ~80%) since OS may crop to a circle/squircle.
        img = canvas
    else:
        mask = rounded_mask(size)
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        img.paste(canvas, (0, 0), mask)

    draw = ImageDraw.Draw(img)
    label = "IDPDR"
    font_size = int(size * (0.20 if maskable else 0.22))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]), label, fill="white", font=font)

    # Small cross/pill glyph above the text for a medical-ish mark
    cx, cy = size / 2, size * (0.32 if maskable else 0.30)
    r = size * 0.09
    draw.rounded_rectangle([cx - r, cy - r / 3, cx + r, cy + r / 3], radius=r / 3, fill="white")
    draw.rounded_rectangle([cx - r / 3, cy - r, cx + r / 3, cy + r], radius=r / 3, fill="white")

    img.save(path)

if __name__ == "__main__":
    make_icon(192, os.path.join(HERE, "icon-192.png"))
    make_icon(512, os.path.join(HERE, "icon-512.png"))
    make_icon(512, os.path.join(HERE, "icon-maskable-512.png"), maskable=True)
    make_icon(180, os.path.join(HERE, "apple-touch-icon.png"))
    make_icon(32, os.path.join(HERE, "favicon-32.png"))
    print("Icons generated in", HERE)
