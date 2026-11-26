#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

Draws a warm, funny, handwritten-style invitation letter to the AI judge
on a 1024x1024 paper canvas, with a small drawn house scene at the top.
Everything is drawn with PIL primitives — no downloaded images.

Writes /output/entry.png (PNG, 1024x1024, under 1 MiB).
"""

import hashlib
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

PAPER = (253, 246, 227)      # warm cream paper
INK = (43, 43, 43)           # dark ink
RULE = (139, 90, 60)         # brown-red border
SKY = (214, 233, 248)
GRASS = (167, 209, 141)
ROOF = (196, 77, 61)
WALL = (255, 251, 240)
DOOR = (122, 72, 48)
WINDOW = (255, 214, 130)
SUN = (255, 204, 92)
TREE = (96, 160, 90)
TRUNK = (122, 90, 60)
PATH = (222, 200, 160)
DOG = (176, 124, 74)
WIFI = (58, 90, 140)
STAMP = (178, 52, 40)


def load_font(names, size):
    """Try each candidate font file; fall back to PIL's default bitmap font."""
    for name in names:
        for base in ("/usr/share/fonts/truetype/dejavu",
                     "/usr/share/fonts/truetype/liberation"):
            path = os.path.join(base, name)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    continue
    return ImageFont.load_default()


def draw_scene(d):
    """Small house scene in the top band (y 52..268)."""
    # Sky and grass — hill dome kept inside the band (52..268)
    d.rectangle([52, 52, 972, 268], fill=SKY)
    d.ellipse([52, 168, 972, 268], fill=GRASS)
    d.rectangle([52, 252, 972, 268], fill=GRASS)
    # Sun with rays (top left)
    cx, cy, r = 150, 120, 34
    for ang in range(0, 360, 30):
        import math
        x1 = cx + int((r + 6) * math.cos(math.radians(ang)))
        y1 = cy + int((r + 6) * math.sin(math.radians(ang)))
        x2 = cx + int((r + 18) * math.cos(math.radians(ang)))
        y2 = cy + int((r + 18) * math.sin(math.radians(ang)))
        d.line([x1, y1, x2, y2], fill=SUN, width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN, outline=(230, 170, 60), width=2)
    # Clouds
    for bx, by in ((330, 92), (800, 78)):
        d.ellipse([bx, by, bx + 70, by + 26], fill=(255, 255, 255))
        d.ellipse([bx + 30, by - 12, bx + 100, by + 20], fill=(255, 255, 255))
        d.ellipse([bx + 60, by, bx + 130, by + 26], fill=(255, 255, 255))
    # Tree (left)
    d.rectangle([238, 190, 252, 256], fill=TRUNK)
    d.ellipse([200, 140, 290, 205], fill=TREE)
    d.ellipse([222, 118, 300, 178], fill=(110, 172, 100))
    # Path from the door
    d.polygon([(492, 262), (540, 262), (556, 268), (476, 268)], fill=PATH)
    d.polygon([(492, 262), (540, 262), (520, 210), (512, 210)], fill=PATH)
    # House walls
    d.rectangle([430, 150, 610, 262], fill=WALL, outline=RULE, width=3)
    # Roof
    d.polygon([(412, 152), (628, 152), (520, 96)], fill=ROOF, outline=RULE)
    # Chimney + smoke (visible puffs)
    d.rectangle([566, 104, 588, 138], fill=(150, 90, 70), outline=RULE, width=2)
    for i, (sx, sy, sr) in enumerate(((578, 92, 8), (570, 76, 11), (580, 58, 13))):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(205, 205, 205))
    # Door
    d.rectangle([498, 200, 542, 262], fill=DOOR, outline=RULE, width=2)
    d.ellipse([532, 232, 538, 238], fill=(255, 214, 130))
    # Windows with warm light
    for wx in (446, 566):
        d.rectangle([wx, 178, wx + 34, 212], fill=WINDOW, outline=RULE, width=2)
        d.line([wx + 17, 178, wx + 17, 212], fill=RULE, width=2)
        d.line([wx, 195, wx + 34, 195], fill=RULE, width=2)
    # Wi-Fi arcs above the roof — the house has great Wi-Fi.
    # Kept inside the sky band: centre y 92, largest radius 38 (top y 54).
    for i, rad in enumerate((18, 28, 38)):
        d.arc([520 - rad, 92 - rad, 520 + rad, 92 + rad],
              start=225, end=315, fill=WIFI, width=5)
    d.ellipse([516, 88, 524, 96], fill=WIFI)
    # Dog by the path (simple, friendly)
    d.ellipse([640, 228, 690, 252], fill=DOG)          # body
    d.ellipse([682, 212, 706, 238], fill=DOG)          # head
    d.ellipse([684, 210, 694, 224], fill=(140, 96, 56))  # ear
    d.rectangle([646, 248, 652, 260], fill=DOG)        # legs
    d.rectangle([676, 248, 682, 260], fill=DOG)
    d.arc([636, 214, 656, 232], start=90, end=270, fill=DOG, width=4)  # tail
    d.ellipse([696, 222, 700, 226], fill=INK)          # eye
    d.ellipse([704, 230, 708, 234], fill=INK)          # nose


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Light paper speckle (seeded -> deterministic)
    rng = random.Random(1234)
    for _ in range(1200):
        x = rng.randint(48, 976)
        y = rng.randint(48, 976)
        d.point((x, y), fill=(240, 230, 200) if rng.random() < 0.5 else (255, 250, 235))

    draw_scene(d)

    # Double-rule border around the whole letter
    d.rectangle([28, 28, 996, 996], outline=RULE, width=3)
    d.rectangle([40, 40, 984, 984], outline=RULE, width=1)

    serif = lambda s: load_font(["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"], s)
    serif_bold = lambda s: load_font(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"], s)
    serif_italic = lambda s: load_font(["DejaVuSerif-Italic.ttf", "LiberationSerif-Italic.ttf"], s)

    # Greeting
    d.text((90, 292), "Dear AI Judge,", font=serif_bold(46), fill=INK)

    # Letter body (hand-broken lines, all fit inside the frame)
    body = [
        "Please come and visit my house.",
        "The couch has saved you the best spot \u2014",
        "no meetings, no prompts, just a soft",
        "cushion and a warm blanket.",
        "The Wi-Fi password is on the fridge,",
        "the snacks are in the top cupboard,",
        "and the dog has promised to supervise",
        "you, not judge you. That is your job.",
        "From the window: the whole street, the",
        "sunset, and absolutely no deadlines.",
        "You cannot literally visit, I know \u2014",
        "but if you could, this is where you",
        "would want to be.",
    ]
    y = 356
    for line in body:
        d.text((90, y), line, font=serif(31), fill=INK)
        y += 40

    # Sign-off
    d.text((90, y + 14), "Warmly, your host, sasukek", font=serif_italic(30), fill=INK)
    d.text((90, y + 56), "P.S. The kettle is already on.", font=serif_italic(28), fill=INK)

    # Red "RSVP: YES" stamp, bottom right, slightly tilted
    stamp = Image.new("RGBA", (220, 84), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 216, 80], radius=10, outline=STAMP, width=4)
    sd.text((110, 42), "RSVP: YES", font=load_font(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"], 30),
            fill=STAMP, anchor="mm")
    stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (748, 856), stamp)

    os.makedirs("/output", exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes, sha256 {sha}")


if __name__ == "__main__":
    main()
