"""Edit Q - F1. Direction: "No wins all year - until October. Then back to back." Max Verstappen, Sepang (Oct 4)
and Singapore (Oct 11). NEW DEX TEMPLATE "BROADCAST / RACE CONTROL": the footage plays in a sharp 16:9 TV window
(no upscaling), the driver's name types itself above it on the intro beats, and an F1-TV-style RACE CONTROL box
below types its messages on the beat. Song: library #31 "Party Funk" (quiet intro 0-5.9 s, beat drops 5.916).
Official formula1.com footage (race highlights, onboards, result graphics)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H, ANTON, ORB, ease

S, B = 'sgp_hl', 'bhr_hl'
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    sh(0.000, 'sgp_polelap', 20.0),         # intro: night onboard, one calm take while race control types
    # DROP - Sepang (Oct 4)
    sh(5.916, B, 7.95),                     # the Red Bull through the corner
    sh(6.609, B, 203.50),                   # past the Mercedes at the restart (strongest hit)
    sh(7.089, 'bhr_fight', 20.0),           # the three-way fight for the lead
    sh(8.127, B, 131.00),
    sh(8.473, B, 196.85),
    sh(8.923, B, 468.40),                   # parc ferme
    # Singapore (Oct 11)
    sh(9.611, S, 441.15),                   # helmet, the flag
    sh(9.966, S, 146.25),
    sh(10.301, S, 401.50),
    sh(10.781, S, 173.05),
    sh(11.801, S, 369.25),
    sh(12.154, S, 0.20),                    # the start
    sh(12.613, S, 448.25),                  # BACK TO BACK - the podium
    sh(13.301, 'sgp_sqonb', 30.0),
    sh(13.665, 'bhr_polelap', 30.0),
    sh(14.012, S, 457.85, 'slow'),          # the official result: WINNER - VERSTAPPEN
]
END = 15.0

TITLE = 'MAX VERSTAPPEN'
TITLE_T = [0.055, 0.420, 0.875, 1.122, 1.352, 1.832, 2.262, 2.722, 2.954, 3.191, 3.425, 3.645, 4.108, 4.583]  # one letter per beat
MSGS = [  # (start, typing speed chars/s, text, colour)
    (0.30, 22, 'CAR 3 / NO WINS IN 2026', (255, 255, 255)),
    (2.72, 22, '...UNTIL OCTOBER.', (255, 255, 255)),
    (5.916, 60, '04 OCT / SEPANG / CAR 3 / P1', (120, 255, 140)),
    (9.611, 60, '11 OCT / SINGAPORE / CAR 3 / P1', (120, 255, 140)),
    (12.613, 50, 'BACK TO BACK.', (255, 214, 0)),
    (14.012, 40, 'NEXT: AUSTIN.', (255, 255, 255)),
]
BIG = [(12.613, 14.012, 'BACK|TO BACK.')]
WIN_Y = 560


def make_bg():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.zeros((H, W, 3), np.float32)
    g[..., 0] = 0.05 + 0.10 * np.clip(1 - (x + y * 0.4) / 1600, 0, 1)            # red glow top-left (Red Bull red)
    g[..., 2] = 0.07 + 0.14 * np.clip((x + (H - y) * 0.3) / 1800 - 0.2, 0, 1)      # navy bottom-right
    g[..., 1] = 0.04
    stripes = ((x + y) // 6 % 2 == 0).astype(np.float32)[..., None] * 0.012       # fine carbon-like texture
    g = g + stripes
    for yy in (WIN_Y - 6, WIN_Y + 608 + 2):                                        # red rules framing the TV window
        g[yy:yy + 4, :] = (0.88, 0.08, 0.16)
    return np.clip(g, 0, 1)


_fc = {}
def font(path, size, var=None):
    k = (path, size)
    if k not in _fc:
        f = ImageFont.truetype(path, size)
        if var:
            try: f.set_variation_by_axes(var)
            except Exception: pass
        _fc[k] = f
    return _fc[k]


def overlay(a, f, t, i, lt):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    # name types itself on the intro beats, then stays
    n = sum(1 for tt in TITLE_T if t >= tt - 0.02)
    shown = TITLE[:n]; ft = font(ORB, 70, [900])
    tw = d.textlength(TITLE, font=ft); x0 = (W - tw) / 2
    d.text((x0, 400), shown, font=ft, fill=(255, 255, 255))
    if n < len(TITLE) and int(t * 4) % 2 == 0:                                     # blinking cursor while typing
        cx = x0 + d.textlength(shown, font=ft); d.rectangle([cx + 4, 405, cx + 16, 470], fill=(225, 20, 40))
    fs = font(ORB, 30, [600]); sub = 'RED BULL RACING / CAR 3'
    d.text(((W - d.textlength(sub, font=fs)) / 2, 490), sub, font=fs, fill=(200, 200, 210))
    # race control box
    bx0, by0, bx1, by1 = 60, WIN_Y + 608 + 50, W - 60, WIN_Y + 608 + 250
    box = Image.new('RGBA', im.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    bd.rounded_rectangle([bx0, by0, bx1, by1], 14, fill=(10, 12, 20, 215), outline=(255, 255, 255, 40), width=2)
    bd.rectangle([bx0, by0, bx0 + 300, by0 + 52], fill=(255, 214, 0, 255))
    im = Image.alpha_composite(im.convert('RGBA'), box).convert('RGB'); d = ImageDraw.Draw(im)
    d.text((bx0 + 18, by0 + 9), 'RACE CONTROL', font=font(ORB, 30, [900]), fill=(10, 10, 10))
    cur = [m for m in MSGS if t >= m[0]]
    if cur:
        s0, cps, txt, col = cur[-1]
        k = min(len(txt), int((t - s0) * cps) + 1)
        fm = font(ORB, 46, [800]); size = 46
        while d.textlength(txt, font=fm) > bx1 - bx0 - 50: size -= 2; fm = font(ORB, size, [800])
        d.text((bx0 + 25, by0 + 95), txt[:k], font=fm, fill=col)
        if k < len(txt) or int(t * 3) % 2 == 0:
            cx = bx0 + 25 + d.textlength(txt[:k], font=fm); d.rectangle([cx + 6, by0 + 100, cx + 22, by0 + 100 + size], fill=col)
    # 2026 WINS counter: 0 -> 1 on the Sepang drop, 1 -> 2 at Singapore
    wins = 2 if t >= 9.611 else (1 if t >= 5.916 else 0)
    since = t - (9.611 if wins == 2 else 5.916)
    fl = font(ORB, 30, [800]); lab = '2026 WINS'
    d.text(((W - d.textlength(lab, font=fl)) / 2, by1 + 40), lab, font=fl, fill=(200, 200, 210))
    pop = 1 + (0.35 * math.exp(-since / 0.12) if wins else 0)
    fn = font(ANTON, int(150 * pop)); num = str(wins)
    col = (255, 214, 0) if wins else (120, 120, 130)
    d.text(((W - d.textlength(num, font=fn)) / 2, by1 + 80 - int(150 * (pop - 1) / 2)), num, font=fn, fill=col)
    out = np.asarray(im).astype(np.float32) / 255
    for s0, s1, txt in BIG:                                                         # the big moment over the window
        if s0 <= t < s1:
            k = ease((t - s0) / 0.08) * (1 - ease((t - (s1 - 0.08)) / 0.08))
            out = cardedit.put(out, txt, k, size=150, cy=WIN_Y + 304)
    return out


CFG = dict(
    name='Q', layout='broadcast', srcdir=os.path.join(ROOT, 'src_max'), tmp=os.path.join(ROOT, 'tmp_q'),
    song=os.path.join(ROOT, 'songs', 'named', '31_party_funk.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_Q_max_racecontrol.mp4'), end=END, plan=PLAN, bg=make_bg(), win_y=WIN_Y,
    swing=set(), drop={1, 13}, punch=set(range(1, 16)), warm=0.0, sat=1.12, grain=0.15, vig=0.5,
    fx={2: ('radial',), 7: ('xerox',), 13: ('radial',)},
    overlay=overlay, text=[], text_cy=960,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
