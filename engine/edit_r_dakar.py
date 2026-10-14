"""Edit R - RALLY. Direction: "1984: Porsche won the Dakar. 38 years later they built it again."
Hook = history: the 1984 Paris-Dakar 953 in sepia while the sound is still quiet, the year stamped on screen.
The drop (3.286) slams into the new 911 Dakar bursting out of the dust, then a TERRAIN SELECTOR (new DEX template):
full-bleed vertical footage, the terrain word stamps in on its first hit (SAND / GRAVEL / SNOW) and a 3-step
selector at the bottom moves on. Ends on the Rallye-livery 953 in the sun: 911 DAKAR. / NO ROAD NEEDED.
Song: library #27 "Rally edit sound" (instrumental, quiet 0-3.0, drop 3.286, 116 BPM).
Footage: Porsche newsroom press films (911 Dakar reveal 230142, terrain film 229800, Roughroads film 229816)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H, ANTON, ORB, ease

R, T, D = 'dk_230142', 'dk_229800', 'dk_229816'
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    # 1984 - quiet intro, sepia archive
    sh(0.000, R, 16.60, 'slow', 0.80),     # the 953 in the desert
    sh(0.948, R, 18.10, 'slow', 0.50),     # the crowd around the winner
    sh(1.965, R, 32.95, 'slow', 0.40),     # Rothmans 953
    # DROP - the new one
    sh(3.286, T, 14.00, 'slow', 0.55),     # bursts out of the dust
    # SAND
    sh(3.786, T, 9.75, 'real', 0.45),
    sh(4.313, D, 29.40, 'real', 0.55),
    sh(4.822, T, 18.55, 'slow', 0.60),     # strongest hit
    sh(5.602, D, 32.20, 'real', 0.45),
    sh(6.077, T, 20.35, 'slow', 0.50),
    # GRAVEL
    sh(6.803, T, 32.50, 'real', 0.45),
    sh(7.428, T, 38.05, 'real', 0.55),
    sh(7.931, T, 41.85, 'real', 0.55),
    sh(8.446, T, 43.75, 'real', 0.50),
    sh(8.810, T, 28.75, 'real', 0.40),
    # SNOW
    sh(9.751, T, 46.30, 'real', 0.45),
    sh(10.222, T, 53.00, 'real', 0.45),
    sh(10.844, T, 55.25, 'slow', 0.55),
    sh(11.557, T, 57.30, 'slow', 0.50),
    sh(12.075, T, 50.00, 'real', 0.50),
    sh(12.591, T, 59.40, 'slow', 0.45),
    # hero
    sh(13.105, D, 57.20, 'slow', 0.60),
]
END = 15.2
I_DROP = 3
TERRAIN = [(4.313, 'SAND'), (6.803, 'GRAVEL'), (9.751, 'SNOW')]
TEXT = [
    (0.05, 0.93, '1984.'),
    (0.95, 1.95, 'PORSCHE WINS|THE DAKAR.'),
    (1.97, 3.27, '38 YEARS|LATER...'),
    (3.29, 4.30, 'THEY BUILT|IT AGAIN.'),
    (13.25, END, '911 DAKAR.'),
]


def pre_fx(fr, i, t, lt):
    """1984 archive look: sepia, crushed blacks, film flicker."""
    if i >= I_DROP: return fr
    g = fr @ np.array([0.299, 0.587, 0.114], np.float32)
    g = np.clip((g - 0.06) * 1.2, 0, 1) * (0.93 + 0.07 * math.sin(t * 47))
    return np.stack([g * 1.06, g * 0.92, g * 0.72], 2).clip(0, 1)


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
    if i < I_DROP:                                                       # archive tag
        fs = font(ORB, 30, [700]); tag = 'PARIS - DAKAR / ARCHIVE'
        d.text(((W - d.textlength(tag, font=fs)) / 2, 300), tag, font=fs, fill=(235, 220, 190))
    cur = [k for k, (s0, _) in enumerate(TERRAIN) if t >= s0]
    if cur and t < PLAN[-1]['t']:
        k = cur[-1]; s0, word = TERRAIN[k]; since = t - s0
        # terrain selector: 3 steps along the bottom, the current one lit
        fs = font(ORB, 30, [800]); y = 1700; gap = 300; x0 = W / 2 - gap
        d.line([(x0, y + 60), (x0 + 2 * gap, y + 60)], fill=(255, 255, 255), width=2)
        for j, (_, w) in enumerate(TERRAIN):
            cx = x0 + j * gap; on = j == k; r = 13 if on else 8
            d.ellipse([cx - r, y + 60 - r, cx + r, y + 60 + r], fill=(255, 196, 0) if on else (255, 255, 255))
            d.text((cx - d.textlength(w, font=fs) / 2, y), w, font=fs, fill=(255, 196, 0) if on else (220, 220, 220))
        lab = f'TERRAIN 0{k + 1} / 03'; fl = font(ORB, 28, [700])
        d.text(((W - d.textlength(lab, font=fl)) / 2, 1360), lab, font=fl, fill=(255, 255, 255))
        im_a = np.asarray(im).astype(np.float32) / 255
        # the word stamps in (scale 1.5 -> 1 in 0.1 s) and stays
        s = 1 + 0.5 * (1 - ease(since / 0.1))
        im_a = cardedit.put(im_a, word + '.', min(1, since / 0.05), size=int(190 * s), cy=1500)
        return im_a
    return np.asarray(im).astype(np.float32) / 255


def final_sub(a, t):
    s0 = 13.7
    if t < s0: return a
    return cardedit.put(a, 'NO ROAD NEEDED.', ease((t - s0) / 0.15), font=ORB, size=52, cy=1560)


def overlay_all(a, f, t, i, lt):
    return final_sub(overlay(a, f, t, i, lt), t)


CFG = dict(
    name='R', layout='full', srcdir=os.path.join(ROOT, 'src_rally'), tmp=os.path.join(ROOT, 'tmp_r'),
    song=os.path.join(ROOT, 'songs', 'named', '27_rally_love_people_inside.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_R_dakar.mp4'), end=END, plan=PLAN,
    swing=set(), drop={I_DROP, 9, 14}, punch=set(range(I_DROP, len(PLAN) - 1)), warm=0.01, sat=1.1,
    grain=0.14, vig=0.55, fx={I_DROP: ('radial',), 6: ('radial',), 11: ('xerox',), 17: ('radial',)},
    pre_fx=pre_fx, overlay=overlay_all, text=TEXT, text_cy=1150,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
