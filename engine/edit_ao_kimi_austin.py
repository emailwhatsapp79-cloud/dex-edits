"""Edit AO - F1, KIMI ANTONELLI: "Austin." (Oct 21, the F1 slot before the US GP). Batch K1 format (2.9M views): an
interview hook with kinetic words. Singapore 2026: P3 means he can clinch the title at the next race, in Austin.
  0-3.2   cold open: "And through goes Antonelli, on the power!" (Singapore, past Hamilton) - Aura Farming at full blast
  3.2     black: the interviewer, BIG words one by one: "The next race in AUSTIN, you could clinch the WORLD CHAMPIONSHIP.
          How does that FEEL?"
  8.35    Kimi, close: "Can I? Really?" - "Well, let's not worry about that. Let's try to do the best weekend as possible
          and FINISH THE JOB." - the drop lands right after "job." (15.8)
  15.8    the wins on the beat: China, Japan, Canada, Miami, Monaco, Monza, Spain (720p broadcast -> sharp 16:9 window)
  26.0    "Antonelli getting past the reigning world champion and a seven-time world champion" over that exact pass
  31.0    the podium, lifted up - AUSTIN. FINISH THE JOB.
Song: Aura Farming - Mustafa Saboori (full, cold open 79.0, story 66.4 -> drop 79.0 = 15.8)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H as FH

KI, MAL, POD = 'f1_7695413467167100182', 'mercedesamgf1_7692783629138677014', 'f1_7643587480364551446'
F1 = '../src_f1/'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
win = lambda t, f, src, **k: sh(t, f, src, layout='window', **k)
PLAN = [
    win(0.00, '../src_max_sg/H', 323.30),                # COLD OPEN: side by side ... through goes Antonelli
    dict(t=3.20, file=None, src=0.0, cx=0.5, mode='black'),   # the question, big words on black
    sh(8.35, KI, 4.95, layout='square'),                 # Kimi: "Can I? Really? ... let's not worry about that"
    sh(12.30, MAL, 6.25, layout='tall'),                 # parc ferme, the helmet               "...the best weekend"
    sh(14.60, MAL, 2.40, layout='tall'),                 # the team                             "...finish the job."
    win(15.80, F1 + 'china', 3.05),                      # DROP - the wins                      20 YEARS OLD.
    win(16.87, F1 + 'japan', 3.80),
    win(17.94, F1 + 'canada', 0.10),                     #                                      8 WINS.
    win(19.01, F1 + 'miami', 4.10),
    win(20.08, F1 + 'monaco', 3.00),
    win(21.15, F1 + 'monza', 0.05),
    sh(22.22, POD, 3.50, layout='tall'),                 # lifted on the podium
    win(23.29, F1 + 'spain', 6.00),
    win(24.36, F1 + 'china', 15.10),
    win(25.43, F1 + 'japan', 11.45),
    win(26.00, '../src_max_sg/H', 327.62),   # "getting past the reigning world champion
    win(29.00, '../src_max_sg/H', 331.12),               #   and a seven-time world champion"
    dict(sh(31.00, POD, 6.00, layout='tall'), jump=True),     # AUSTIN. FINISH THE JOB.
]
for p in PLAN:
    if p['mode'] == 'black': p['file'] = None
END = 34.15
TEXT = [(15.85, 16.85, '20 YEARS OLD.'), (17.95, 18.95, '8 WINS.'), (31.20, END, 'AUSTIN.|FINISH THE JOB.')]

def L(off, words):
    return [(round(t + off, 3), w) for t, w in words]
SUBS = [
    L(-325.50, [(325.50, 'And'), (326.06, 'through'), (326.34, 'goes'), (326.66, 'Antonelli,'), (327.24, 'on'), (327.54, 'the'), (327.68, 'power!')]),
    L(3.40, [(4.70, 'Can'), (4.80, 'I?'), (5.54, 'Really?')]),
    L(3.40, [(6.72, 'Well,'), (7.22, "let's"), (7.92, 'not'), (8.02, 'worry'), (8.28, 'about'), (8.48, 'that.')]),
    L(3.40, [(9.30, "Let's"), (9.74, 'try'), (9.92, 'to'), (10.06, 'do'), (10.18, 'the'), (10.28, 'best'), (10.46, 'weekend'), (10.72, 'as'), (10.90, 'possible')]),
    L(3.40, [(11.26, 'and'), (11.58, 'finish'), (11.94, 'the'), (12.12, 'job.')]),
    L(-303.99, [(330.14, 'Antonelli'), (330.80, 'getting'), (331.02, 'past'), (331.36, 'the'), (331.52, 'reigning'), (331.78, 'world'), (332.02, 'champion')]),
    L(-303.99, [(332.44, 'and'), (332.88, 'a'), (333.04, 'seven-time'), (333.52, 'world'), (333.74, 'champion.')]),
]
# the interviewer's question on black: big kinetic words, key words in Mercedes teal
BIG = [L(3.40, [(0.00, 'THE'), (0.22, 'NEXT'), (0.40, 'RACE'), (0.68, 'IN'), (1.24, '*AUSTIN,')]),
       L(3.40, [(2.00, 'YOU'), (2.18, 'COULD'), (2.42, 'CLINCH'), (2.82, 'THE'), (2.90, '*WORLD'), (3.06, '*CHAMPIONSHIP.')]),
       L(3.40, [(4.08, 'HOW'), (4.16, 'DOES'), (4.26, 'THAT'), (4.44, '*FEEL?')])]
TEAL = (0, 215, 182)
BIGF = ImageFont.truetype('/home/user/dex-edits/fonts/Anton.ttf', 120)


def big_words(a, t):
    cur = None
    for k, ws in enumerate(BIG):
        nxt = BIG[k + 1][0][0] if k + 1 < len(BIG) else 8.35
        if ws[0][0] - 0.03 <= t < nxt: cur = ws
    if cur is None: return a
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    shown = [w for tt, w in cur if tt <= t + 0.02]
    lines, line = [], []
    for w in shown:
        if line and d.textlength(' '.join(x.lstrip('*') for x in line + [w]), font=BIGF) > 940: lines.append(line); line = []
        line.append(w)
    lines.append(line)
    y = 900 - (len(lines) - 1) * 70
    for ln in lines:
        x = (W - d.textlength(' '.join(x.lstrip('*') for x in ln), font=BIGF)) / 2
        for w in ln:
            d.text((x, y), w.lstrip('*'), font=BIGF, fill=TEAL if w.startswith('*') else (255, 255, 255))
            x += d.textlength(w.lstrip('*') + ' ', font=BIGF)
        y += 140
    return np.asarray(im).astype(np.float32) / 255
FONT = ImageFont.truetype(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts', 'Archivo.ttf')
                          if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts', 'Archivo.ttf'))
                          else '/home/user/dex-edits/fonts/Archivo.ttf', 62)
try: FONT.set_variation_by_axes([800])
except Exception: pass
SUB_Y = 1500


def subtitles(a, f, t, i, lt):
    if 3.2 <= t < 8.35: return big_words(a, t)
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
    name='AO', layout='full', win_y=656,
    active={KI + '.mp4': (110, 1250), MAL + '.mp4': (0, 1440), POD + '.mp4': (0, 1440)},
    srcdir=os.path.join(ROOT, 'src_kimi'), tmp=os.path.join(ROOT, 'tmp_ao'),
    song=os.path.join(ROOT, 'songs', 'kimi_trailer.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AO_kimi_austin.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.2,
    fx={}, text=TEXT, text_cy=860, crf=12, overlay=subtitles,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
