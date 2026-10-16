"""Edit AN - FOOTBALL, HAALAND trailer v2 (Desmond: rebuild, "do your peak"). Norway 2-1 Brazil, World Cup R16.
v1 (AM) failed the sharpness rule (soft cold open, FOX captions forced square boxes). AN uses ONLY shots that measure
sharp: FIFA pitch-side camera (400-600), the behind-the-goal angle of goal 2 (FIFA "First Class", 70-150), the sharp
parts of FIFA's match highlights. Everything full screen.
  0-2.8   cold open: the strike, the net, the net from behind      "He's got another one!"  (song at full blast)
  2.8     black: ROUND OF 16. / BRAZIL VS NORWAY.
  5.6     Haaland waiting, hands on hips (pitch-side, cropped 1.4x)   "...just a phenomenal goalscorer"
  9.13    goal 1 as called: "...lifted it up to HAALAND!" = THE DROP (11.47) - "He plunders again!"
  15.0    the calm
  17.6    goal 2: wide, then from behind the net                     "Haaland! Oh, wonderful!" - "He has nailed it for Norway!"
  23.3    "Extraordinary! Just phenomenal!"
  33.46   the song breaks: "The Northern Lights are shining!" -> INTO THE QUARTERFINALS.
Song: APHOTIC - Thalassophobia (cold open 197.78, story from 79.34, drop 88.01, break 110.0)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H as FH

FW, FC = 'fifaworldcup_7659198448788442390', 'fifaworldcup_7659326928083766531'
R, C = 'fifaworldcup_7659173738222538006', 'fifaworldcup_7664943856579808534'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
PLAN = [
    dict(sh(0.00, FW, 43.75), jump=True),   # COLD OPEN: the strike, close            "He's got another one!"
    dict(sh(0.80, FW, 28.80), jump=True),   # the ball in the net
    dict(sh(1.75, FC, 15.00), jump=True),   # the net from behind
    dict(t=2.80, file=None, src=0.0, cx=0.5, mode='black'),   # ROUND OF 16. / BRAZIL VS NORWAY.
    sh(5.60, C, 0.20, cx=0.45),             # Haaland waiting, hands on hips          "...just a phenomenal goalscorer"
    sh(9.13, FW, 26.30),                    # goal 1                                  "...lifted it up to HAALAND!" = DROP
    sh(12.61, FW, 29.92),                   # the net                                 "He plunders again!"
    sh(14.80, R, 4.00, cx=0.47),            # the calm
    sh(17.60, FC, 8.95),                    # goal 2, wide                            "Haaland! Oh, wonderful!"
    sh(19.85, FC, 11.50),                   # goal 2 from behind the net              "He has nailed it for Norway!"
    sh(23.30, FW, 35.28),                   # the replay                              "Extraordinary!
    dict(sh(24.42, C, 3.90, cx=0.45), jump=True),   #                                  Just phenomenal!"
    dict(sh(26.40, R, 10.60, cx=0.47), jump=True),  # walking
    dict(sh(28.60, R, 0.50, cx=0.47), jump=True),
    dict(sh(31.73, C, 5.95, cx=0.45), jump=True),
    dict(sh(33.46, R, 7.00, cx=0.47), jump=True),   # the break: "The Northern Lights are shining!" - QUARTERFINALS
]
for p in PLAN:
    if p['mode'] == 'black': p['file'] = None
END = 36.55
TEXT = [(2.90, 4.20, 'ROUND OF 16.'), (4.25, 5.50, 'BRAZIL|VS NORWAY.'), (35.00, END, 'INTO THE|QUARTERFINALS.')]

def L(off, words):
    return [(round(t + off, 3), w) for t, w in words]
SUBS = [
    L(-3.72, [(4.52, "He's"), (4.72, 'got'), (4.94, 'another'), (5.28, 'one!')]),
    L(3.55, [(2.50, 'Just'), (3.72, 'a'), (3.98, 'phenomenal'), (4.44, 'goalscorer.')]),
    L(-17.27, [(26.52, 'Away'), (26.74, 'from'), (26.92, 'his'), (27.06, 'man,'), (27.36, 'shoulder'), (27.60, 'up,')]),
    L(-17.27, [(27.94, 'and'), (27.98, "he's"), (28.10, 'lifted'), (28.32, 'it'), (28.48, 'up'), (28.62, 'to'), (28.74, 'HAALAND!')]),
    L(-17.27, [(30.24, 'He'), (30.68, 'plunders'), (31.12, 'again!')]),
    L(-24.10, [(42.16, 'Haaland!'), (43.20, 'Oh,'), (43.50, 'wonderful!')]),
    L(-25.15, [(45.80, 'He'), (46.48, 'has'), (47.16, 'nailed'), (47.70, 'it'), (48.04, 'for'), (48.26, 'Norway!')]),
    L(16.05, [(8.02, 'Extraordinary!'), (9.06, 'Just'), (9.52, 'phenomenal!')]),
    L(16.58, [(17.08, 'The'), (17.16, 'Northern'), (17.50, 'Lights'), (18.08, 'are'), (18.50, 'shining!')]),
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
    name='AN', layout='full',
    active={C + '.mp4': (400, 1371), R + '.mp4': (420, 1371)},
    srcdir=os.path.join(ROOT, 'src_haaland'), tmp=os.path.join(ROOT, 'tmp_an'),
    song=os.path.join(ROOT, 'songs', 'haaland_v2.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AN_haaland_v2.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.2,
    fx={}, text=TEXT, text_cy=860, crf=12, overlay=subtitles,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
