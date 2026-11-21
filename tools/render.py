#!/usr/bin/env python3
"""Render the 21 November 2026 front page (1024x1024 PNG).

Draws the whole page with Pillow: masthead, one lead story, six
illustrated stories and an also-today strip. Every picture on the page is
drawn here with shapes -- no photo, no copied artwork. Deterministic:
no clock, no randomness, fixed palette and fonts, so two runs produce
identical bytes.

Run:  python3 tools/render.py            (writes entry.png next to main.py)
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
BLUE = (37, 99, 235)
GOLD = (217, 119, 6)
GREEN = (21, 128, 61)
TEAL = (13, 148, 136)
MUTED = (85, 85, 85)
PANEL = (255, 255, 255)
SKY = (16, 24, 48)
RULE = (20, 20, 20)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- pictures

def pic_lead(draw, x, y, w, h):
    """Night sky over Poland: missile trails, burst, rooftops."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    for sx, sy, r in [(30, 26, 2), (90, 60, 2), (160, 20, 3), (230, 48, 2),
                      (300, 30, 2), (340, 80, 2), (120, 90, 1), (260, 110, 1)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(255, 255, 255))
    # missile trails: orange arcs falling left to right
    draw.line([(x + 20, y + 30), (x + 150, y + 120)], fill=(249, 115, 22), width=5)
    draw.line([(x + 90, y + 18), (x + 220, y + 108)], fill=(251, 191, 36), width=4)
    draw.line([(x + 170, y + 26), (x + 300, y + 118)], fill=(249, 115, 22), width=4)
    for cx, cy in [(150, 120), (220, 108), (300, 118)]:
        for rr, col in [(26, (249, 115, 22)), (16, (251, 191, 36)), (8, (255, 255, 255))]:
            draw.ellipse([x + cx - rr, y + cy - rr, x + cx + rr, y + cy + rr], fill=col)
    # ground + rooftops
    gy = y + h - 42
    draw.rectangle([x, gy, x + w, y + h], fill=(12, 18, 36))
    for bx, bw, bh in [(10, 70, 26), (95, 56, 34), (165, 80, 22), (260, 60, 30), (330, 44, 26)]:
        draw.rectangle([x + bx, gy - bh, x + bx + bw, gy], fill=(30, 41, 59))
        draw.polygon([(x + bx, gy - bh), (x + bx + bw // 2, gy - bh - 12),
                      (x + bx + bw, gy - bh)], fill=(51, 65, 85))
    for wx in (28, 118, 200, 282, 348):
        draw.rectangle([x + wx, gy - 16, x + wx + 8, gy - 8], fill=(251, 191, 36))


def pic_riyadh(draw, x, y, w, h):
    """Riyadh towers at night with an interception burst."""
    draw.rectangle([x, y, x + w, y + h], fill=(23, 37, 84))
    for sx, sy in [(14, 18), (60, 10), (120, 22), (40, 44)]:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 255))
    base = y + h
    for bx, bw, bh, col in [(8, 26, 78, (100, 116, 139)), (42, 34, 108, (148, 163, 184)),
                             (84, 22, 62, (100, 116, 139)), (112, 30, 92, (203, 213, 225))]:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=col)
        for wy in range(base - bh + 8, base - 6, 12):
            draw.rectangle([x + bx + 5, wy, x + bx + bw - 5, wy + 4], fill=(251, 191, 36))
    # twisted PIF-style tower
    draw.polygon([(x + 118, base - 92), (x + 138, base - 118), (x + 142, base - 92)],
                 fill=(226, 232, 240))
    # intercept burst
    cx, cy = x + w - 34, y + 34
    for rr, col in [(20, (249, 115, 22)), (12, (251, 191, 36)), (6, (255, 255, 255))]:
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    draw.line([(x + 20, y + 12), (cx - 14, cy - 8)], fill=(251, 191, 36), width=3)


def pic_markets(draw, x, y, w, h):
    """Falling chart on a red board."""
    draw.rectangle([x, y, x + w, y + h], fill=(254, 242, 242))
    draw.line([(x + 10, y + h - 22), (x + w - 8, y + h - 22)], fill=MUTED, width=2)
    draw.line([(x + 10, y + 12), (x + 10, y + h - 22)], fill=MUTED, width=2)
    pts = [(14, 26), (40, 34), (62, 30), (84, 52), (104, 66), (124, 96), (140, 118)]
    pts = [(x + px, y + py) for px, py in pts]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5], fill=RED)
    draw.text((x + 12, y + h - 40), "-3.7%", font=SANS_B(22), fill=RED)
    draw.text((x + 84, y + 12), "S&P", font=SANS_B(13), fill=MUTED)


def pic_climate(draw, x, y, w, h):
    """Globe and sun over Antalya."""
    draw.rectangle([x, y, x + w, y + h], fill=(236, 253, 245))
    cx, cy, r = x + w // 2, y + h // 2 + 6, 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(59, 130, 246))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 58, 95), width=3)
    for dx, dy, rw, rh in [(-28, -14, 34, 12), (6, 8, 40, 14), (-18, 26, 26, 10)]:
        draw.ellipse([cx + dx, cy + dy, cx + dx + rw, cy + dy + rh], fill=(34, 197, 94))
    draw.ellipse([x + w - 34, y + 12, x + w - 10, y + 36], fill=(251, 191, 36))
    for ang in range(0, 360, 45):
        import math
        x1 = x + w - 22 + int(17 * math.cos(math.radians(ang)))
        y1 = y + 24 + int(17 * math.sin(math.radians(ang)))
        x2 = x + w - 22 + int(23 * math.cos(math.radians(ang)))
        y2 = y + 24 + int(23 * math.sin(math.radians(ang)))
        draw.line([(x1, y1), (x2, y2)], fill=(251, 191, 36), width=2)


def pic_denmark(draw, x, y, w, h):
    """Danish flag cross with a shield."""
    draw.rectangle([x, y, x + w, y + h], fill=(200, 16, 46))
    draw.rectangle([x + 42, y, x + 62, y + h], fill=(255, 255, 255))
    draw.rectangle([x, y + 58, x + w, y + 78], fill=(255, 255, 255))
    draw.polygon([(x + w - 58, y + 22), (x + w - 18, y + 22), (x + w - 18, y + 62),
                  (x + w - 38, y + 84), (x + w - 58, y + 62)], fill=(30, 58, 95),
                 outline=(255, 255, 255))
    draw.line([(x + w - 50, y + 34), (x + w - 26, y + 34)], fill=(255, 255, 255), width=3)
    draw.line([(x + w - 50, y + 46), (x + w - 26, y + 46)], fill=(255, 255, 255), width=3)


def pic_israel(draw, x, y, w, h):
    """Knesset-style building under a blue Star of David."""
    draw.rectangle([x, y, x + w, y + h], fill=(239, 246, 255))
    cx, cy = x + w // 2, y + 26
    draw.polygon([(cx, cy - 14), (cx + 12, cy + 8), (cx - 12, cy + 8)], outline=BLUE, width=3)
    draw.polygon([(cx, cy + 14), (cx + 12, cy - 8), (cx - 12, cy - 8)], outline=BLUE, width=3)
    base = y + h - 14
    draw.rectangle([x + 18, base - 58, x + w - 18, base], fill=(226, 232, 240),
                   outline=NAVY, width=2)
    draw.polygon([(x + 14, base - 58), (x + w // 2, base - 84), (x + w - 14, base - 58)],
                 fill=(148, 163, 184), outline=NAVY)
    for i in range(5):
        cx0 = x + 28 + i * 20
        draw.rectangle([cx0, base - 44, cx0 + 10, base - 8], fill=NAVY)
    draw.rectangle([x + w // 2 - 8, base - 30, x + w // 2 + 8, base], fill=(185, 28, 28))


def pic_gaza(draw, x, y, w, h):
    """Aid boxes and rain over Gaza."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 251, 235))
    for rx in (16, 52, 88, 120):
        draw.line([(x + rx, y + 10), (x + rx - 6, y + 34)], fill=(96, 165, 250), width=3)
        draw.line([(x + rx, y + 40), (x + rx - 6, y + 64)], fill=(96, 165, 250), width=3)
    base = y + h
    for bx, by, col in [(14, base - 34, (217, 119, 6)), (52, base - 52, (185, 28, 28)),
                        (92, base - 30, (21, 128, 61))]:
        draw.rectangle([x + bx, by, x + bx + 34, base - 8], fill=col, outline=INK, width=2)
        draw.line([(x + bx, by + 12), (x + bx + 34, by + 12)], fill=(255, 255, 255), width=2)


# ---------------------------------------------------------------- page

STORIES = [
    ("MIDDLE EAST", "THREE MISSILES STOPPED OVER RIYADH",
     "Saudi defences intercept Houthi missiles fired at the capital early "
     "on Saturday \u2014 the second attack in days.", pic_riyadh),
    ("MARKETS", "WALL STREET ENTERS CORRECTION",
     "S&P 500 \u22123.7%, Dow \u2212950 points; the Nasdaq wipes out its 2026 "
     "gains as the AI sell-off deepens.", pic_markets),
    ("CLIMATE", "COP31 TALKS SPILL INTO OVERTIME",
     "The Antalya draft drops every mention of fossil fuels; a new text is "
     "due on Saturday morning.", pic_climate),
    ("EUROPE", "DENMARK EXPELS RUSSIAN ATTACH\u00c9",
     "Copenhagen says Moscow plotted to kill rapper Kyivstoner; two men are "
     "charged with attempted murder.", pic_denmark),
    ("ISRAEL", "EISENKOT TAPPED TO LEAD ISRAEL",
     "President Herzog asks the ex-army chief to form a government, passing "
     "over Netanyahu.", pic_israel),
    ("GAZA", "FOUR NATIONS PRESS ISRAEL ON GAZA AID",
     "Australia, Canada, Italy and the UK urge full access as floods add to "
     "Gaza's suffering.", pic_gaza),
]

ALSO = [
    ("CYCLONE AKVAN", "Storm crosses India's Odisha coast after landfall."),
    ("FRANCE", "Fourth weekend of cost-of-living protests nationwide."),
    ("MYANMAR", "Junta calls the ICJ genocide ruling \u2018unfair\u2019."),
    ("INDIA", "NSE becomes the world's 5th-largest listed exchange."),
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx, mx2 = 20, W - 20

    # ---- masthead
    y = 22
    hrule(d, mx, mx2, y, width=3)
    d.text((W // 2, y + 10), "THE DAY IN BRIEF", font=SERIF_B(56),
           fill=INK, anchor="ma")
    d.text((W // 2, y + 74), "SATURDAY  21  NOVEMBER  2026", font=SANS_B(30),
           fill=RED, anchor="ma")
    d.text((W // 2, y + 110), "The world in one page \u2014 Saturday's biggest stories, as reported",
           font=SANS(15), fill=MUTED, anchor="ma")
    hrule(d, mx, mx2, y + 134, width=2)
    hrule(d, mx, mx2, y + 138, width=4)

    # ---- lead: Poland
    lx, ly, lw, lh = mx, 176, W - 40, 196
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=PANEL, outline=INK, width=2)
    pic_lead(d, lx + 2, ly + 2, 372, lh - 4)
    tx = lx + 396
    d.text((tx, ly + 14), "EUROPE  \u00b7  THE LEAD", font=SANS_B(15), fill=RED)
    d.text((tx, ly + 40), "MISSILES LAND", font=SANS_B(40), fill=INK)
    d.text((tx, ly + 84), "IN POLAND", font=SANS_B(40), fill=INK)
    text_block(d, tx, ly + 132,
               "Two Russian Kh-101 missiles and a drone fall in the "
               "south-east. No one is hurt; NATO chief Rutte flies to "
               "Warsaw today.", SANS(16), lw - 396 - 18)
    d.text((tx, ly + lh - 22), "Tusk calls it a likely provocation.",
           font=SANS_B(13), fill=MUTED)

    # ---- six stories, 2 columns x 3 rows
    gy = 388
    pw, ph, gut = 486, 150, 12
    for i, (kick, head, sub, pic) in enumerate(STORIES):
        col, row = i % 2, i // 2
        px = mx + col * (pw + gut)
        py = gy + row * (ph + gut)
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL, outline=INK, width=2)
        pic(d, px + 2, py + 2, 146, ph - 4)
        tx = px + 160
        d.text((tx, py + 10), kick, font=SANS_B(12), fill=RED)
        text_block(d, tx, py + 30, head, SANS_B(19), pw - 172, leading=23)
        # sub sits under the headline block (headline wraps to at most 2 lines)
        sub_y = py + 30 + 2 * 23 + 6
        text_block(d, tx, sub_y, sub, SANS(13), pw - 172, leading=16)

    # ---- also today strip
    sy = gy + 3 * ph + 2 * gut + 12  # 886
    d.rectangle([mx, sy, mx2, sy + 66], fill=INK)
    d.text((mx + 12, sy + 8), "ALSO TODAY", font=SANS_B(14), fill=(251, 191, 36))
    col_w = (W - 40 - 24) // 4
    for i, (lead, rest) in enumerate(ALSO):
        cx = mx + 12 + i * col_w
        d.text((cx, sy + 28), lead, font=SANS_B(12), fill=(255, 255, 255))
        text_block(d, cx, sy + 44, rest, SANS(11), col_w - 12,
                   fill=(226, 232, 240), leading=13)

    # ---- footer
    fy = sy + 66 + 12  # 964
    hrule(d, mx, mx2, fy, width=2)
    d.text((mx, fy + 8), "Sources: AP, Reuters, CNN, WSJ, BBC \u2014 as reported 20\u201321 Nov 2026. "
                         "All figures as reported; no story invented.",
           font=SANS(12), fill=MUTED)
    d.text((mx2, fy + 24), "make.fun \u00b7 news-image-20261121",
           font=SANS_B(12), fill=MUTED, anchor="ra")

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    render()
