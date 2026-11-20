#!/usr/bin/env python3
"""Front page for Thursday 19 November 2026 — drawn from scratch with Pillow.

Deterministic: fixed seed, no timestamps, no network, no downloaded assets.
Usage: python3 gen_image.py [variant] [output.png]
Variant 1: lead story top, 3x2 grid below (default).
Variant 2: lead story left column, 2x3 grid right.
Variant 3: lead story top with wide banner art, 3x2 grid, dark masthead.
Variant 4: lead story top, 2x3 grid, warm palette.
Variant 5: lead story top, 3x2 grid, high-contrast ink palette.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


def centered(draw, cx, y, text, fnt, color):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=color)
    return y + int(fnt.size * 1.18)


# ---------------------------------------------------------------- illustrations
def draw_flags(d, x, y, w, h):
    """Three flag poles: US, China, Russia — flat rectangles with stripes."""
    pole_w = 6
    fw = (w - 40) // 3
    fh = int(fw * 0.62)
    cols = [
        [("#B22234", 7), ("#FFFFFF", 6)],  # US stripes
        [("#DE2910", 1)],                  # China red
        [("#FFFFFF", 1), ("#0039A6", 1), ("#D52B1E", 1)],  # Russia tricolour
    ]
    stars = [(30, 18), (14, 14)]
    for i, bands in enumerate(cols):
        fx = x + 20 + i * (fw + 10)
        total = sum(n for _, n in bands)
        yy = y
        for color, n in bands:
            bh = fh * n / total
            d.rectangle([fx, yy, fx + fw, yy + bh], fill=color)
            yy += bh
        d.rectangle([fx, y, fx + fw, y + fh], outline="#111111", width=2)
        if i == 0:  # US blue canton + dots
            d.rectangle([fx, y, fx + fw * 0.42, y + fh * 0.54], fill="#3C3B6E")
            for sx in range(3):
                for sy in range(2):
                    d.ellipse([fx + 6 + sx * 12, y + 5 + sy * 11,
                               fx + 11 + sx * 12, y + 10 + sy * 11], fill="white")
        if i == 1:  # China stars
            for sx, sy in stars:
                d.ellipse([fx + sx - 5, y + sy - 5, fx + sx + 5, y + sy + 5],
                          fill="#FFDE00")
        # pole
        d.rectangle([fx - 3, y + fh, fx + 3, y + h], fill="#333333")
    # ground line under the poles
    d.rectangle([x + 8, y + h - 4, x + w - 8, y + h], fill="#333333")


def draw_scales(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 - 10
    d.rectangle([cx - 4, cy - 60, cx + 4, cy + 55], fill="#8A6D2B")
    d.rectangle([cx - 55, cy - 62, cx + 55, cy - 54], fill="#8A6D2B")
    d.ellipse([cx - 12, cy - 78, cx + 12, cy - 54], fill="#C9A227")
    for s in (-1, 1):
        px = cx + s * 52
        d.line([cx + s * 52, cy - 58, px, cy - 8], fill="#8A6D2B", width=3)
        d.line([cx + s * 52, cy - 58, px - 16, cy - 8], fill="#8A6D2B", width=3)
        d.line([cx + s * 52, cy - 58, px + 16, cy - 8], fill="#8A6D2B", width=3)
        d.pieslice([px - 26, cy - 10, px + 26, cy + 18], 0, 180, fill="#C9A227",
                   outline="#8A6D2B", width=2)
    d.rectangle([cx - 45, cy + 55, cx + 45, cy + 63], fill="#8A6D2B")


def draw_rocket_chart(d, x, y, w, h):
    # rising bars + arrow
    base = y + h - 30
    vals = [0.25, 0.4, 0.35, 0.6, 0.75, 1.0]
    bw = w // 8
    for i, v in enumerate(vals):
        bx = x + 20 + i * (bw + 6)
        bh = int((h - 60) * v)
        d.rectangle([bx, base - bh, bx + bw, base], fill="#1B7A3D")
    d.line([x + 14, base - 20, x + w - 30, y + 18], fill="#B3271E", width=7)
    d.polygon([(x + w - 30, y + 18), (x + w - 52, y + 16), (x + w - 30, y + 40)],
              fill="#B3271E")
    d.text((x + 16, y + 2), "$", font=font(BOLD, 34), fill="#1B7A3D")


def draw_fall_chart(d, x, y, w, h):
    base = y + h - 30
    vals = [1.0, 0.85, 0.9, 0.6, 0.45, 0.3]
    bw = w // 8
    for i, v in enumerate(vals):
        bx = x + 20 + i * (bw + 6)
        bh = int((h - 60) * v)
        d.rectangle([bx, base - bh, bx + bw, base], fill="#B3271E")
    d.line([x + 14, y + 22, x + w - 30, base - 16], fill="#111111", width=7)
    d.polygon([(x + w - 30, base - 16), (x + w - 54, base - 20),
               (x + w - 32, base - 40)], fill="#111111")


def draw_bridge(d, x, y, w, h):
    # bridge arch + blast burst
    d.rectangle([x + 10, y + h - 46, x + w - 10, y + h - 34], fill="#555555")
    d.arc([x + 30, y + 30, x + w - 30, y + h - 20], 180, 360, fill="#333333",
          width=8)
    for px in (x + 60, x + w // 2, x + w - 60):
        d.rectangle([px - 4, y + h - 90, px + 4, y + h - 34], fill="#333333")
    bx, by = x + w // 2, y + 46
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 14, 34
        a = math.radians(ang)
        d.line([bx + r1 * math.cos(a), by + r1 * math.sin(a),
                bx + r2 * math.cos(a), by + r2 * math.sin(a)],
               fill="#E8A020", width=6)
    d.ellipse([bx - 16, by - 16, bx + 16, by + 16], fill="#E8A020",
              outline="#B3271E", width=3)


def draw_flood(d, x, y, w, h):
    # flooded street first, then house, cloud, and rain on top
    d.rectangle([x + 20, y + h - 52, x + w - 20, y + h - 10], fill="#2E6DA4")
    d.polygon([(x + w // 2 - 55, y + h - 52), (x + w // 2, y + h - 96),
               (x + w // 2 + 55, y + h - 52)], fill="#B3271E")
    d.rectangle([x + w // 2 - 40, y + h - 52, x + w // 2 + 40, y + h - 26],
                fill="#8A5A2B")
    d.ellipse([x + 30, y + 8, x + 110, y + 58], fill="#5B7A99")
    d.ellipse([x + 80, y + 0, x + 170, y + 52], fill="#5B7A99")
    d.rectangle([x + 40, y + 34, x + 160, y + 58], fill="#5B7A99")
    for rx in range(x + 40, x + 180, 26):
        d.line([rx, y + 66, rx - 8, y + 92], fill="#7FB3D5", width=5)


def draw_tennis(d, x, y, w, h):
    # player silhouette + racket + ball
    cx = x + w // 2
    d.ellipse([cx - 16, y + 8, cx + 16, y + 40], fill="#111111")  # head
    d.line([cx, y + 40, cx - 6, y + 88], fill="#111111", width=12)  # torso
    d.line([cx - 4, y + 88, cx - 26, y + h - 22], fill="#111111", width=10)
    d.line([cx - 4, y + 88, cx + 22, y + h - 30], fill="#111111", width=10)
    d.line([cx, y + 52, cx - 42, y + 30], fill="#111111", width=9)  # arm
    d.ellipse([cx - 78, y + 2, cx - 30, y + 50], outline="#B3271E", width=7)
    d.line([cx - 54, y + 26, cx - 40, y + 32], fill="#B3271E", width=5)
    d.ellipse([x + w - 96, y + 20, x + w - 68, y + 48], fill="#C9E021",
              outline="#111111", width=2)
    d.arc([x + w - 96, y + 20, x + w - 68, y + 48], 200, 340, fill="white",
          width=3)
    d.rectangle([x + 10, y + h - 14, x + w - 10, y + h - 8], fill="#1B7A3D")


ART = {
    "flags": draw_flags,
    "scales": draw_scales,
    "rocket": draw_rocket_chart,
    "fall": draw_fall_chart,
    "bridge": draw_bridge,
    "flood": draw_flood,
    "tennis": draw_tennis,
}

STORIES = [
    dict(kicker="JUSTICE", art="scales",
         head="MYANMAR GUILTY OF GENOCIDE",
         sub="World Court's first genocide ruling"),
    dict(kicker="TECH", art="rocket",
         head="ANTHROPIC IPO SMASHES RECORDS",
         sub="Priced $83, opened $111.50, closed up 17%"),
    dict(kicker="MARKETS", art="fall",
         head="DOW PLUNGES 1,100 POINTS",
         sub="S&P falls for a sixth straight session"),
    dict(kicker="WAR", art="bridge",
         head="CRIMEA BRIDGE HIT A THIRD TIME",
         sub="Ukraine strikes rail span; trains halted"),
    dict(kicker="WEATHER", art="flood",
         head="SOUTH FLORIDA UNDER WATER",
         sub="State of emergency as 15 in. of rain falls"),
    dict(kicker="SPORT", art="tennis",
         head="ALCARAZ BEATS MEDVEDEV IN TURIN",
         sub="6-2, 6-4 to reach the ATP Finals semis"),
]

LEAD = dict(
    kicker="WORLD  •  SUMMIT IN SHENZHEN",
    art="flags",
    head="TRUMP, XI AND PUTIN MEET",
    sub="First three-way summit of the great powers ends with a “peace declaration” — but no deal on Ukraine or Iran",
)


def panel(d, box, story, pal, head_size=25, sub_size=17, art_h=110):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill="white", outline=pal["line"], width=2)
    d.rectangle([x, y, x + w, y + 30], fill=pal["accent"])
    d.text((x + 10, y + 5), story["kicker"], font=font(BOLD, 16),
           fill="white")
    ART[story["art"]](d, x + 12, y + 38, w - 24, art_h)
    # auto-fit: shrink headline until head + sub fit the remaining height
    avail = h - 30 - art_h - 14
    hs = head_size
    while hs >= 17:
        hf = font(BOLD, hs)
        sf = font(REG, sub_size)
        hl = wrap(d, story["head"], hf, w - 24)
        sl = wrap(d, story["sub"], sf, w - 24)
        need = len(hl) * int(hs * 1.18) + 2 + len(sl) * int(sub_size * 1.18)
        if need <= avail:
            break
        hs -= 1
    ty = y + 38 + art_h + 6
    ty = text_block(d, x + 12, ty, story["head"], font(BOLD, hs),
                    pal["ink"], w - 24)
    text_block(d, x + 12, ty + 2, story["sub"], font(REG, sub_size),
               pal["muted"], w - 24)


def masthead(d, pal, dark=False):
    if dark:
        d.rectangle([0, 0, W, 148], fill=pal["ink"])
        name_c, date_c, rule_c = "white", "#FFD9A0", "#C9A227"
    else:
        name_c, date_c, rule_c = pal["ink"], pal["accent"], pal["ink"]
    centered(d, W // 2, 18, "THE WORLD TODAY", font(BOLD, 66), name_c)
    centered(d, W // 2, 92, "THURSDAY 19 NOVEMBER 2026",
             font(BOLD, 32), date_c)
    d.rectangle([24, 140, W - 24, 144], fill=rule_c)
    d.rectangle([24, 146, W - 24, 148], fill=rule_c)


def build(variant):
    palettes = {
        1: dict(bg="#FAF6EE", ink="#111111", accent="#B3271E", line="#111111",
                muted="#444444"),
        2: dict(bg="#F4F1EA", ink="#14213D", accent="#1B3A6B", line="#14213D",
                muted="#3A4763"),
        3: dict(bg="#FAF6EE", ink="#111111", accent="#B3271E", line="#111111",
                muted="#444444"),
        4: dict(bg="#FFF8E7", ink="#3B2F1E", accent="#8A5A2B", line="#3B2F1E",
                muted="#6B5A44"),
        5: dict(bg="#FFFFFF", ink="#000000", accent="#C00000", line="#000000",
                muted="#333333"),
    }
    pal = palettes[variant]
    img = Image.new("RGB", (W, H), pal["bg"])
    d = ImageDraw.Draw(img)

    if variant == 2:
        # lead left column, 2x3 grid right
        masthead(d, pal)
        lx, ly, lw, lh = 24, 160, 380, 820
        d.rectangle([lx, ly, lx + lw, ly + lh], fill="white",
                    outline=pal["line"], width=3)
        d.rectangle([lx, ly, lx + lw, ly + 34], fill=pal["accent"])
        d.text((lx + 12, ly + 6), LEAD["kicker"], font=font(BOLD, 15),
               fill="white")
        ART["flags"](d, lx + 20, ly + 60, lw - 40, 190)
        ty = text_block(d, lx + 16, ly + 280, LEAD["head"], font(BOLD, 40),
                        pal["ink"], lw - 32)
        text_block(d, lx + 16, ty + 8, LEAD["sub"], font(REG, 21),
                   pal["muted"], lw - 32)
        gx, gy = 420, 160
        cw, chh = 284, 262
        for i, s in enumerate(STORIES):
            cx = gx + (i % 2) * (cw + 12)
            cy = gy + (i // 2) * (chh + 14)
            panel(d, (cx, cy, cw, chh), s, pal, head_size=22, sub_size=15,
                  art_h=96)
        d.text((24, 992), "THE WORLD TODAY  •  19 NOVEMBER 2026",
               font=font(REG, 15), fill=pal["muted"])
        return img

    dark = variant == 3
    masthead(d, pal, dark=dark)
    # lead panel
    lx, ly, lw, lh = 24, 164, W - 48, 300
    d.rectangle([lx, ly, lx + lw, ly + lh], fill="white",
                outline=pal["line"], width=3)
    d.rectangle([lx, ly, lx + lw, ly + 36], fill=pal["accent"])
    d.text((lx + 12, ly + 7), LEAD["kicker"], font=font(BOLD, 18), fill="white")
    ax = lx + 16
    ART["flags"](d, ax, ly + 66, 400, 180)
    tx = lx + 440
    ty = text_block(d, tx, ly + 64, LEAD["head"], font(BOLD, 46), pal["ink"],
                    lw - 456)
    text_block(d, tx, ty + 10, LEAD["sub"], font(REG, 22), pal["muted"],
               lw - 456)
    # grid
    gy = 484
    if variant == 4:
        # warm palette, same 3x2 grid as the others (2x3 overflowed the page)
        cw, chh = 316, 244
        for i, s in enumerate(STORIES):
            cx = 24 + (i % 3) * (cw + 8)
            cy = gy + (i // 3) * (chh + 10)
            panel(d, (cx, cy, cw, chh), s, pal, head_size=24, sub_size=16,
                  art_h=100)
    else:
        cw, chh = 316, 244
        for i, s in enumerate(STORIES):
            cx = 24 + (i % 3) * (cw + 8)
            cy = gy + (i // 3) * (chh + 10)
            panel(d, (cx, cy, cw, chh), s, pal, head_size=24, sub_size=16,
                  art_h=100)
    d.text((24, 992), "THE WORLD TODAY  •  19 NOVEMBER 2026",
           font=font(REG, 15), fill=pal["muted"])
    return img


def main():
    variant = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    out = sys.argv[2] if len(sys.argv) > 2 else "entry.png"
    img = build(variant)
    img.save(out, optimize=True)
    print(out, img.size, len(open(out, "rb").read()), "bytes")


if __name__ == "__main__":
    main()
