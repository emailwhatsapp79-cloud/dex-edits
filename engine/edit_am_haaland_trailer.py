"""Edit AM - FOOTBALL, HAALAND, trailer format (Desmond liked the Verstappen trailer, Oct 15: "go ahead with Haaland").
World Cup 2026, round of 16: Norway 2-1 Brazil, Haaland scores both (FIFA / FOX). Story in ~42 s:
  cold open  "He's got another one!" - song at full blast (Thalassophobia 197.78)
  black      ROUND OF 16. / BRAZIL VS NORWAY.
  build      the heat, "...just a phenomenal goalscorer"
  goal 1     "...shoulder up, and he's lifted it up to HAALAND!" - "Haaland!" = THE DROP (88.01), ball in the net on it;
             "He plunders again!"
  goal 2     "Haaland! Oh, wonderful!" - "He has nailed it for Norway!" over the close replay of that strike;
             Brazil's No.10, crushed; "Extraordinary! Just phenomenal!"
  ending     the song breaks (110.0): "The Northern Lights are shining!" -> INTO THE QUARTERFINALS.
Voices are the real FIFA / FOX commentary of the same moments (picture = voice). Official @fifaworldcup / @foxsports
1080p vertical clips, full screen; FOX captions cropped off with `active`."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H as FH

FW, FIRST, HENRY = 'fifaworldcup_7659198448788442390', 'foxsports_7652125814506474782', 'foxsports_7654395520818941214'
HEAT, OSLO, ROW = 'foxsports_7659164580647587103', 'foxsports_7659168191813324062', 'foxsports_7659173408256707870'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
PLAN = [
    sh(0.00, OSLO, 9.00, layout='square'),                   # COLD OPEN: Oslo erupts                   "He's got another one!"
    dict(sh(1.50, OSLO, 11.00, layout='square'), jump=True),
    dict(t=3.00, file=None, src=0.0, cx=0.5, mode='black'),   # ROUND OF 16. / BRAZIL VS NORWAY.
    sh(6.00, HEAT, 1.00, layout='square'),                   # Haaland in the heat
    sh(8.60, HENRY, 0.40, layout='square'),   # "...just a phenomenal goalscorer"
    sh(12.05, FW, 26.24),                   # goal 1 - picture = the call: "...lifted it up to HAALAND!" = DROP
    sh(15.52, FW, 29.95),                   # the net                                  "He plunders again!"
    sh(17.40, FW, 32.40),
    sh(18.98, FW, 40.25),                   # goal 2, wide                             "Haaland! Oh, wonderful!"
    sh(22.90, FW, 44.80),                   # the strike, close                        "He has nailed it for Norway!"
    sh(26.80, FW, 49.40),                   # Brazil's No.10
    dict(sh(27.90, HENRY, 7.00, layout='square'), jump=True),   #                    "Extraordinary! Just phenomenal!"
    dict(sh(30.30, HEAT, 6.00, layout='square'), jump=True),
    dict(sh(32.30, FW, 34.30), jump=True),
    dict(sh(34.00, HENRY, 10.00, layout='square'), jump=True),
    dict(sh(35.40, OSLO, 13.00, layout='square'), jump=False),
    dict(sh(36.59, HEAT, 9.00, layout='square'), jump=True),   # the break: "The Northern Lights are shining!"
    dict(sh(39.64, OSLO, 14.12, layout='square'), jump=True),  # the song back - INTO THE QUARTERFINALS.
]
for p in PLAN:
    if p['mode'] == 'black': p['file'] = None
END = 42.50
TEXT = [(3.10, 4.50, 'ROUND OF 16.'), (4.55, 5.95, 'BRAZIL|VS NORWAY.'), (39.80, END, 'INTO THE|QUARTERFINALS.')]

def L(off, words):
    return [(round(t + off, 3), w) for t, w in words]
SUBS = [
    L(-3.72, [(4.52, "He's"), (4.72, 'got'), (4.94, 'another'), (5.28, 'one!')]),
    L(6.45, [(3.30, 'Just'), (3.72, 'a'), (3.98, 'phenomenal'), (4.44, 'goalscorer.')]),
    L(-14.14, [(26.00, 'Gets'), (26.52, 'away'), (26.74, 'from'), (26.92, 'his'), (27.06, 'man,'), (27.36, 'shoulder'), (27.60, 'up,')]),
    L(-14.14, [(27.94, 'and'), (27.98, "he's"), (28.10, 'lifted'), (28.32, 'it'), (28.48, 'up'), (28.62, 'to'), (28.74, 'HAALAND!')]),
    L(-14.14, [(30.24, 'He'), (30.68, 'plunders'), (31.12, 'again!')]),
    L(-21.27, [(42.16, 'Haaland!'), (43.20, 'Oh,'), (43.50, 'wonderful!')]),
    L(-21.90, [(46.64, 'He'), (46.90, 'has'), (47.20, 'nailed'), (47.60, 'it'), (47.90, 'for'), (48.20, 'Norway!')]),
    L(20.25, [(8.02, 'Extraordinary!'), (9.06, 'Just'), (9.52, 'phenomenal!')]),
    L(19.78, [(17.08, 'The'), (17.16, 'Northern'), (17.50, 'Lights'), (18.08, 'are'), (18.50, 'shining!')]),
]
FONT = ImageFont.truetype(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts', 'Archivo.ttf')
                          if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts', 'Archivo.ttf'))
                          else '/home/user/dex-edits/fonts/Archivo.ttf', 62)
try: FONT.set_variation_by_axes([800])
except Exception: pass
SUB_Y = 1500


def subtitles(a, f, t, i, lt):
    cur = None
    for k, ws in enumerate(SUBS):
        nxt = SUBS[k + 1][0][0] if k + 1 < len(SUBS) else 1e9
        if ws[0][0] - 0.05 <= t < min(nxt, ws[-1][0] + 0.9): cur = ws
    if cur is None: return a
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    words = [w for _, w in cur]; lines, line = [], []
    for w in words:                                            # wrap at ~900 px
        if line and d.textlength(' '.join(line + [w]), font=FONT) > 900: lines.append(line); line = []
        line.append(w)
    lines.append(line)
    y = SUB_Y - (len(lines) - 1) * 40; idx = 0
    for ln in lines:
        x = (W - d.textlength(' '.join(ln), font=FONT)) / 2
        for w in ln:
            said = cur[idx][0] <= t + 0.02
            for dx, dy in ((3, 3), (-2, 2), (2, -2), (0, 4)):
                d.text((x + dx, y + dy), w, font=FONT, fill=(0, 0, 0, 200 if said else 90))
            d.text((x, y), w, font=FONT, fill=(255, 255, 255, 255) if said else (255, 255, 255, 95))
            x += d.textlength(w + ' ', font=FONT); idx += 1
        y += 80
    return np.asarray(Image.alpha_composite(im, lay).convert('RGB')).astype(np.float32) / 255


CFG = dict(
    name='AM', layout='full',
    active={HENRY + '.mp4': (0, 865), HEAT + '.mp4': (150, 1140), OSLO + '.mp4': (1045, 875)},
    srcdir=os.path.join(ROOT, 'src_haaland'), tmp=os.path.join(ROOT, 'tmp_am'),
    song=os.path.join(ROOT, 'songs', 'haaland_trailer.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AM_haaland_trailer.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.2,
    fx={}, text=TEXT, text_cy=860, crf=12, overlay=subtitles,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
