#!/usr/bin/env python3
"""Draw 'The World in One Day - Friday 20 November 2026'.

A hand-drawn vector newspaper front page (1024x1024) summing up six
verified stories from Friday 20 November 2026:
  1. Trump, Xi and Putin meet in Shenzhen (first three-way summit)
  2. ICJ rules Myanmar committed genocide against the Rohingya
  3. Cyclone Akvan nears Odisha, India; mass evacuations
  4. Russian strikes damage Austrian and Dutch embassies in Kyiv
  5. Tanker burns after hitting a mine east of the Strait of Hormuz
  6. Anthropic debuts on the stock market
Only PIL (stdlib-adjacent, preinstalled) is used; the output is
deterministic, so repeated runs write identical bytes.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (26, 26, 26)
RED = (176, 42, 32)
BLUE = (31, 78, 121)
TEAL = (18, 110, 105)
GOLD = (184, 134, 11)
GREY = (90, 86, 78)
LIGHT = (233, 226, 208)
SKY = (214, 231, 240)
SEA = (52, 110, 140)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, width, text, fnt, fill=INK, leading=1.22,
               align="left"):
    """Draw wrapped text; returns the y just below the block."""
    for line in wrap(draw, text, fnt, width):
        if align == "center":
            lx = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel(draw, x, y, w, h, fill=(255, 255, 255)):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=INK, width=2)
    return x, y, w, h


def kicker(draw, x, y, label, fill=RED):
    f = SANS_B(17)
    draw.text((x, y), label.upper(), font=f, fill=fill)
    return y + 24


def person(draw, cx, gy, s, suit, skin=(232, 190, 150), hair=(70, 60, 55)):
    """Simple suited figure standing on ground line gy, centred at cx."""
    w = 34 * s
    # legs
    draw.rectangle([cx - w * 0.45, gy - 52 * s, cx - w * 0.08, gy],
                   fill=(40, 40, 44))
    draw.rectangle([cx + w * 0.08, gy - 52 * s, cx + w * 0.45, gy],
                   fill=(40, 40, 44))
    # jacket
    draw.polygon([(cx - w * 0.62, gy - 52 * s), (cx + w * 0.62, gy - 52 * s),
                  (cx + w * 0.5, gy - 108 * s), (cx - w * 0.5, gy - 108 * s)],
                 fill=suit)
    # shirt + tie
    draw.polygon([(cx - 7 * s, gy - 108 * s), (cx + 7 * s, gy - 108 * s),
                  (cx + 4 * s, gy - 78 * s), (cx - 4 * s, gy - 78 * s)],
                 fill=(245, 245, 240))
    draw.polygon([(cx - 3 * s, gy - 106 * s), (cx + 3 * s, gy - 106 * s),
                  (cx + 3 * s, gy - 84 * s), (cx, gy - 78 * s),
                  (cx - 3 * s, gy - 84 * s)], fill=RED)
    # head
    draw.ellipse([cx - 15 * s, gy - 138 * s, cx + 15 * s, gy - 106 * s],
                 fill=skin, outline=INK, width=2)
    draw.arc([cx - 15 * s, gy - 140 * s, cx + 15 * s, gy - 112 * s],
             180, 360, fill=hair, width=int(6 * s))
    # eyes
    draw.point([(cx - 6 * s, gy - 122 * s), (cx + 6 * s, gy - 122 * s)],
               fill=INK)


def flag(draw, x, y, w, h, kind):
    """Small waving flag on a pole at (x, y) top-left of the cloth."""
    draw.line([(x, y), (x, y + h + 26)], fill=INK, width=3)
    if kind == "us":
        draw.rectangle([x, y, x + w, y + h], fill=(240, 240, 235),
                       outline=INK, width=1)
        for i in range(4):
            draw.rectangle([x, y + i * h / 4, x + w, y + (i + 0.5) * h / 4],
                           fill=(178, 34, 52))
        draw.rectangle([x, y, x + w * 0.45, y + h * 0.5], fill=(30, 50, 110))
    elif kind == "cn":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16),
                       outline=INK, width=1)
        draw.text((x + 4, y + 2), "*", font=SANS_B(16), fill=(255, 220, 0))
    elif kind == "ru":
        draw.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 240),
                       outline=INK, width=1)
        draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 60, 160))
        draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 30, 30))
    elif kind == "in":
        draw.rectangle([x, y, x + w, y + h / 3], fill=(255, 153, 51),
                       outline=INK, width=1)
        draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(245, 245, 240))
        draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(19, 136, 8))
        draw.ellipse([x + w / 2 - 6, y + h / 2 - 6, x + w / 2 + 6,
                      y + h / 2 + 6], outline=(0, 40, 120), width=2)


def draw_summit(draw, x, y, w, h):
    """Three leaders seated at a summit table, three flags behind."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # hall backdrop
    draw.rectangle([x, y + h - 24, x + w, y + h], fill=(120, 96, 70))
    draw.rectangle([x + 14, y + 12, x + w - 14, y + 62], fill=(250, 246, 236),
                   outline=INK, width=2)
    draw.text((x + 22, y + 24), "SHENZHEN", font=SANS_B(22), fill=INK)
    draw.text((x + 22, y + 48), "TRILATERAL SUMMIT", font=SANS(13),
              fill=GREY)
    # flags
    flag(draw, x + w - 150, y + 78, 34, 22, "us")
    flag(draw, x + w - 104, y + 78, 34, 22, "cn")
    flag(draw, x + w - 58, y + 78, 34, 22, "ru")
    # table
    gy = y + h - 24
    draw.rectangle([x + 30, gy - 26, x + w - 30, gy - 8], fill=(96, 62, 32),
                   outline=INK, width=2)
    # seated figures: heads + shoulders above the table
    for cx, suit, hair in ((x + 90, (30, 50, 110), (220, 220, 210)),
                           (x + w // 2, (150, 30, 30), (40, 40, 40)),
                           (x + w - 90, (40, 60, 90), (200, 200, 200))):
        draw.ellipse([cx - 21, gy - 68, cx + 21, gy - 28], fill=(232, 190, 150),
                     outline=INK, width=2)
        draw.arc([cx - 21, gy - 70, cx + 21, gy - 38], 180, 360, fill=hair,
                 width=7)
        draw.polygon([(cx - 31, gy - 26), (cx + 31, gy - 26),
                      (cx + 24, gy - 56), (cx - 24, gy - 56)], fill=suit)
        draw.polygon([(cx - 6, gy - 56), (cx + 6, gy - 56), (cx, gy - 40)],
                     fill=(245, 245, 240))
    # documents on the table
    for dx in (x + 150, x + w // 2 - 20, x + w - 185):
        draw.rectangle([dx, gy - 20, dx + 34, gy - 9], fill=(255, 255, 255),
                       outline=INK, width=1)


def draw_court(draw, x, y, w, h):
    """Courthouse front with columns and a scales-of-justice emblem."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 222, 205))
    # pediment + columns
    draw.polygon([(x + 12, y + 34), (x + w - 12, y + 34),
                  (x + w / 2, y + 8)], fill=(250, 246, 236), outline=INK)
    for cx in (x + 34, x + w / 2 - 22, x + w / 2 + 22, x + w - 34):
        draw.rectangle([cx - 9, y + 34, cx + 9, y + h - 16], fill=(250, 246, 236),
                       outline=INK, width=2)
    draw.rectangle([x + 12, y + h - 16, x + w - 12, y + h - 8], fill=INK)
    # scales
    cx, cy = x + w / 2, y + h / 2 + 18
    draw.line([(cx, cy - 26), (cx, cy + 16)], fill=INK, width=3)
    draw.line([(cx - 26, cy - 22), (cx + 26, cy - 22)], fill=INK, width=3)
    draw.line([(cx - 26, cy - 22), (cx - 36, cy - 2)], fill=INK, width=2)
    draw.line([(cx - 26, cy - 22), (cx - 16, cy - 2)], fill=INK, width=2)
    draw.line([(cx + 26, cy - 22), (cx + 16, cy - 2)], fill=INK, width=2)
    draw.line([(cx + 26, cy - 22), (cx + 36, cy - 2)], fill=INK, width=2)
    draw.arc([cx - 44, cy - 6, cx - 28, cy + 10], 0, 180, fill=INK, width=2)
    draw.arc([cx + 28, cy - 6, cx + 44, cy + 10], 0, 180, fill=INK, width=2)
    draw.ellipse([cx - 5, cy - 30, cx + 5, cy - 20], fill=GOLD, outline=INK)


def draw_cyclone(draw, x, y, w, h):
    """Spiral storm over a coastline with rain and an evacuation arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(200, 216, 228))
    # sea + coast
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=SEA)
    draw.polygon([(x, y + h - 34), (x + w * 0.55, y + h - 34),
                  (x + w * 0.42, y + h), (x, y + h)], fill=(222, 196, 140))
    draw.text((x + 8, y + h - 28), "ODISHA COAST", font=SANS_B(12),
              fill=(60, 40, 20))
    # spiral bands
    cx, cy = x + w * 0.62, y + h * 0.44
    for r, col in ((64, (255, 255, 255)), (50, (180, 200, 215)),
                   (36, (255, 255, 255)), (22, (140, 165, 185))):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col,
                 width=10)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(90, 110, 130))
    # rain streaks
    for rx, ry in ((x + 20, y + 14), (x + 44, y + 30), (x + w - 30, y + 18),
                   (x + w - 52, y + 40)):
        draw.line([(rx, ry), (rx - 5, ry + 14)], fill=(90, 120, 150), width=3)
    # evacuation arrow inland
    draw.line([(x + 30, y + h - 52), (x + 74, y + h - 52)], fill=RED, width=4)
    draw.polygon([(x + 74, y + h - 60), (x + 88, y + h - 52),
                  (x + 74, y + h - 44)], fill=RED)
    draw.text((x + 8, y + h - 74), "EVACUATIONS", font=SANS_B(12), fill=RED)


def draw_kyiv(draw, x, y, w, h):
    """City skyline at dusk with a blast star over a damaged building."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 196, 150))
    # buildings
    for bx, bw, bh, col in ((x + 8, 44, 66, (120, 110, 100)),
                            (x + 58, 40, 88, (96, 88, 80)),
                            (x + 104, 46, 58, (130, 118, 106)),
                            (x + 156, 42, 78, (104, 94, 86)),
                            (x + 204, 48, 62, (124, 112, 100))):
        draw.rectangle([bx, y + h - bh - 22, bx + bw, y + h - 22], fill=col,
                       outline=INK, width=2)
        for wy in range(y + h - bh - 12, y + h - 30, 14):
            for wx in range(bx + 7, bx + bw - 6, 12):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 220, 120))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(70, 66, 60))
    # blast star over the middle building
    bx, by = x + 78, y + h - 72
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        draw.line([(bx, by), (bx + 26 * math.cos(a), by + 26 * math.sin(a))],
                  fill=(255, 140, 0), width=4)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 200, 60),
                 outline=(200, 60, 0), width=2)
    # smoke
    for sx, sy, sr in ((bx - 30, by - 22, 9), (bx + 26, by - 30, 11),
                       (bx + 6, by - 38, 8)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(120, 116, 110))


def draw_tanker(draw, x, y, w, h):
    """Oil tanker on a swell, fire plume, and a naval mine in the water."""
    draw.rectangle([x, y, x + w, y + h], fill=(206, 224, 234))
    # waves
    for wy in (y + h - 44, y + h - 26, y + h - 10):
        for k in range(5):
            wx = x + 8 + k * 52
            draw.arc([wx, wy - 8, wx + 40, wy + 8], 180, 360, fill=SEA,
                     width=3)
    # hull
    hy = y + h - 62
    draw.polygon([(x + 18, hy), (x + w - 18, hy), (x + w - 34, hy + 26),
                  (x + 34, hy + 26)], fill=(120, 30, 30), outline=INK, width=2)
    draw.rectangle([x + 150, hy - 22, x + w - 60, hy], fill=(240, 236, 226),
                   outline=INK, width=2)
    draw.rectangle([x + w - 78, hy - 44, x + w - 52, hy], fill=(250, 246, 236),
                   outline=INK, width=2)
    # fire plume from the deck, scaled to the scene height
    ph = min(52, int(h * 0.42))
    fx, fy = x + 84, hy - 6
    draw.polygon([(fx - 22, fy), (fx - 8, fy - ph), (fx + 2, fy - ph // 2),
                  (fx + 12, fy - ph - 6), (fx + 26, fy)], fill=(255, 140, 0),
                 outline=(200, 60, 0), width=2)
    draw.polygon([(fx - 8, fy), (fx - 2, fy - ph // 2), (fx + 10, fy)],
                 fill=(255, 210, 60))
    # smoke, kept inside the scene
    for sx, sy, sr in ((fx - 6, fy - ph - 8, 10), (fx + 12, fy - ph - 16, 11),
                       (fx + 28, fy - ph - 8, 8)):
        if sy - sr >= y + 4:
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                         fill=(110, 106, 100))
    # naval mine, lower right
    mx, my = x + w - 46, y + h - 24
    draw.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(40, 44, 48),
                 outline=INK, width=2)
    for dx, dy in ((-11, 0), (11, 0), (0, -11), (0, 11), (-8, -8), (8, 8),
                   (-8, 8), (8, -8)):
        draw.line([(mx + dx * 0.7, my + dy * 0.7),
                   (mx + dx * 1.25, my + dy * 1.25)], fill=INK, width=2)


def draw_market(draw, x, y, w, h):
    """Rising stock chart over a trading floor, with a green arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(228, 238, 226))
    # grid
    for gx in range(x + 12, x + w - 8, 34):
        draw.line([(gx, y + 10), (gx, y + h - 30)], fill=(200, 212, 198),
                  width=1)
    for gy in range(y + 12, y + h - 28, 26):
        draw.line([(x + 10, gy), (x + w - 10, gy)], fill=(200, 212, 198),
                  width=1)
    # rising line
    pts = [(x + 16, y + h - 52), (x + 70, y + h - 66), (x + 120, y + h - 58),
           (x + 170, y + h - 84), (x + 220, y + h - 96), (x + w - 18, y + 26)]
    draw.line(pts, fill=(18, 130, 60), width=5, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(18, 130, 60))
    # arrowhead
    draw.polygon([(x + w - 18, y + 26), (x + w - 40, y + 30),
                  (x + w - 22, y + 48)], fill=(18, 130, 60))
    # ticker bars
    for i, bh in enumerate((26, 40, 34, 52)):
        bx = x + 18 + i * 26
        draw.rectangle([bx, y + h - 16 - bh, bx + 16, y + h - 16],
                       fill=(31, 78, 121))


def story_panel(draw, x, y, w, h, scene, kicker_text, headline, subhead,
                share=0.48, head_size=22, sub_size=16):
    panel(draw, x, y, w, h)
    ih = int(h * share)
    scene(draw, x + 2, y + 2, w - 4, ih)
    ty = y + ih + 8
    kicker(draw, x + 12, ty, kicker_text)
    ty += 24
    ty = text_block(draw, x + 12, ty, w - 24, headline, SERIF_B(head_size),
                    leading=1.08)
    text_block(draw, x + 12, ty + 4, w - 24, subhead, SANS(sub_size),
               fill=(60, 56, 48), leading=1.2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # double outer border
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---- masthead ----
    my = 30
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(56)
    d.text(((W - d.textlength(title, font=tf)) / 2, my), title, font=tf,
           fill=INK)
    my += 72
    rule(d, 40, my, W - 40, 3, RED)
    my += 12
    date = "FRIDAY 20 NOVEMBER 2026"
    df = SANS_B(30)
    d.text(((W - d.textlength(date, font=df)) / 2, my), date, font=df,
           fill=RED)
    my += 42
    sub = "SIX STORIES FROM AROUND THE WORLD  •  DRAWN FROM THE DAY'S REPORTING"
    sf = SANS(16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, my), sub, font=sf, fill=GREY)
    my += 28
    rule(d, 40, my, W - 40, 2)

    # ---- lead story: Shenzhen summit ----
    ly = my + 12
    lh = 290
    panel(d, 32, ly, W - 64, lh)
    hx = 52
    hy = ly + 12
    hy = text_block(d, hx, hy, W - 104, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                    SERIF_B(33), leading=1.05)
    rule(d, hx, hy + 4, W - 52, 1, GREY)
    # illustration left, text right
    iy = hy + 14
    ih = ly + lh - iy - 14
    draw_summit(d, 44, iy, 470, ih)
    tx = 534
    text_block(d, tx, iy + 6, W - 52 - tx,
               "The first three-way summit of the American, Chinese and "
               "Russian leaders opens in Shenzhen.",
               SANS_B(21), leading=1.25)
    text_block(d, tx, iy + 96, W - 52 - tx,
               "A joint peace statement and talks on nuclear arms top the "
               "agenda as the three powers meet face to face.",
               SANS(18), fill=(60, 56, 48), leading=1.3)
    d.text((tx, ly + lh - 34), "DIPLOMACY  •  CHINA", font=SANS_B(15),
           fill=RED)

    # ---- middle row: three stories ----
    ry = ly + lh + 12
    rh = 250
    cw = (W - 64 - 24) // 3
    story_panel(d, 32, ry, cw, rh, draw_court, "World court • The Hague",
                "MYANMAR COMMITTED GENOCIDE",
                "Judges rule on the Rohingya crackdown of 2017.",
                head_size=20)
    story_panel(d, 44 + cw, ry, cw, rh, draw_cyclone, "Weather • India",
                "CYCLONE AKVAN NEARS ODISHA",
                "Thousands evacuated as the storm closes on the east coast.",
                head_size=20)
    story_panel(d, 56 + 2 * cw, ry, cw, rh, draw_kyiv, "War in Ukraine",
                "EMBASSIES HIT IN KYIV STRIKES",
                "Austrian and Dutch missions hit in an attack on the capital.",
                head_size=20)

    # ---- bottom row: two stories ----
    by = ry + rh + 12
    bh = H - by - 52
    bw = (W - 64 - 12) // 2
    story_panel(d, 32, by, bw, bh, draw_tanker, "Energy • Gulf",
                "TANKER BURNS AFTER MINE STRIKE",
                "Blast east of the Strait of Hormuz disables a tanker.",
                share=0.42)
    story_panel(d, 44 + bw, by, bw, bh, draw_market, "Business • Tech",
                "ANTHROPIC'S STOCK MARKET DEBUT",
                "AI firm joins the world's most valuable companies on day one.",
                share=0.42)

    # ---- footer ----
    fy = H - 44
    rule(d, 40, fy, W - 40, 1, GREY)
    foot = "FRIDAY 20 NOVEMBER 2026  —  THE WORLD IN ONE DAY"
    ff = SANS_B(15)
    d.text(((W - d.textlength(foot, font=ff)) / 2, fy + 8), foot, font=ff,
           fill=INK)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
