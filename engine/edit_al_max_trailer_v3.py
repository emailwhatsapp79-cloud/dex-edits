"""Edit AL - v3 of the Verstappen trailer (Desmond: the first 4 s and the song). Cold open 0-3 s on the climax with the
song at full blast from its drop + "...the Singapore WIN!", hard cut to black + boom, then the story (AK +1.0 s) with
the music louder between voice lines; smeary helmet shots removed.

Edit AK - F1, MAX VERSTAPPEN, full TRAILER (v2 of AJ). Desmond: AJ too short, no whole story, voices unclear, no
real background song that goes high and dips under the voice. AK = the whole Singapore 2026 weekend in ~58 s:
  setup     250 STARTS. / NEVER WON IN SINGAPORE.   (helmet)
  Saturday  "...and his first here in Singapore" (pole) - "sensational pole lap" (radio) - sprint "victory at last!"
  Sunday    "One, two, three, four, five red lights in Singapore and we're underway" - "underway" = THE DROP
  race      "Late, late, late on the brakes ... the Ferrari man" over that exact Turn-1 footage,
            "clinging on to the lead by his fingertips, but he's still got it"
  finish    the music cuts out, "And finally for Max Verstappen, the Singapore win!" - "win!" = music slams back
  emotion   GP: "Yes Max, it's been a very long time in the making, that one. Pleased to see you've got it."
  ending    "...with a champagne shower, Max Verstappen. Everywhere he has visited more than once in Formula One, he is
            a Grand Prix winner. And that now includes Singapore." -> SINGAPORE. FINALLY. + the crowd
Music: Just Keep Watching (F1 The Movie) instrumental cover - the same version as the TikTok F1 sound - from 39.96
(drop 60.26 = 20.30), loud, dipped under every voice line. Official F1 race-highlights commentary (formula1.com) +
@f1 TikTok clips. Vertical 1080p clips full screen; the 720p broadcast shots as a sharp 16:9 window (downscale, no
upscale) over their own blur. Word-by-word subtitles for every line."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H as FH

HELM, P1, OUT_, HTL = 'f1_7694673917193063682', 'f1_7694669963944103190', 'f1_7695081243175554326', 'f1_7694957322287713558'
SPR, PF, WIN, GP, POD = 'f1_7694997103784791298', 'f1_7694989403172719894', 'f1_7695423602358881558', 'f1_7695768714691595542', 'f1_7695428044822957334'
HL = 'H'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
win = lambda t, src, **k: sh(t, HL, src, layout='window', **k)
PLAN = [
    sh(0.00, GP, 12.80),                    # COLD OPEN: champagne, full screen, song at full blast
    dict(win(1.20, 455.70), jump=True),     # Max on stage                         "...the Singapore WIN!"
    dict(win(2.20, 406.65), jump=True),     # the Red Bull flat out
    dict(t=3.00, file=None, src=0.0, cx=0.5, mode='black'),   # cut to black: 250 STARTS. / NEVER WON IN SINGAPORE.
    sh(5.80, P1, 0.30),                     # pole car into parc ferme      "...his first here in Singapore"
    sh(8.30, OUT_, 0.10, cx=0.3),           # climbs out                     "sensational pole lap by you"
    sh(11.30, PF, 0.30),                    # sprint P1, the flags           "victory in Singapore at last!"
    sh(13.40, P1, 3.85),                    # walking under the lights       SUNDAY.
    win(14.54, 0.00),                       # the five red lights (picture = the commentary)
    sh(21.30, SPR, 5.23),                   # DROP
    win(22.22, 10.40),                      # the pack into turn 1
    dict(win(23.14, 11.40), jump=True),     # the start, the pack
    win(23.98, 13.90),                      # turn 1 from above
    sh(25.38, HTL, 4.83),
    win(26.00, 18.10),                      # "late, late, late on the brakes... the Ferrari man" (that move)
    sh(28.85, HTL, 6.70),                   # night racing
    sh(30.70, SPR, 6.66),                   # the Dutch fans
    win(31.50, 32.10),                      # Max leading                    "clinging on by his fingertips"
    dict(sh(36.40, HTL, 8.60), jump=True),  # the Red Bull at speed
    win(37.53, 404.10),                     # "And finally for Max Verstappen..."
    sh(40.00, WIN, 20.00),                  # the car, glowing
    dict(t=41.64, file=None, src=0.0, cx=0.5, mode='black'),  # silence: "...the Singapore"
    win(42.53, 441.15),                     # "WIN!" - Max in the cockpit, music back
    sh(44.00, GP, 7.50),                    # Max & GP                       "a very long time in the making"
    dict(sh(46.00, OUT_, 4.20), jump=True), # standing in his helmet
    win(47.60, 449.00),                     # the team
    win(49.00, 452.60, jump=True),          # the champagne
    dict(sh(50.60, GP, 14.50), jump=True),                   # champagne
    win(52.60, 461.00),                     # the podium shower
    dict(win(54.20, 443.00), jump=True),    # in the cockpit, the winner
    sh(55.80, POD, 0.03),                   # the podium, the crowd - SINGAPORE. FINALLY.
]
for p in PLAN:
    if p['mode'] == 'black': p['file'] = None
END = 59.40
TEXT = [(3.10, 4.40, '250 STARTS.'), (4.45, 5.75, 'NEVER WON IN|SINGAPORE.'), (13.55, 14.45, 'SUNDAY.'),
        (58.25, END, 'SINGAPORE.|FINALLY.')]

# word-by-word subtitles: (edit time of each word, word); a new list = a new caption
def L(off, words):
    return [(round(t + off + 1.0, 3), w) for t, w in words]   # +1.0: the cold open
SUBS = [
    [(1.37, '...the'), (1.51, 'Singapore'), (2.25, 'WIN!')],
    L(1.00, [(3.80, 'And'), (3.82, 'his'), (4.04, 'first'), (4.74, 'here'), (5.02, 'in'), (5.20, 'Singapore.')]),
    L(-1.30, [(8.64, 'And'), (9.16, 'sensational'), (9.68, 'pole'), (10.30, 'lap'), (10.50, 'by'), (10.72, 'you.')]),
    L(5.68, [(4.66, "It's"), (4.88, 'victory'), (5.24, 'in'), (5.54, 'Singapore'), (6.04, 'at'), (6.38, 'last!')]),
    L(13.54, [(0.00, 'One,'), (1.14, 'two,'), (1.86, 'three,'), (2.72, 'four,'), (3.52, 'five')]),
    L(13.54, [(3.80, 'red'), (4.00, 'lights'), (4.30, 'in'), (4.48, 'Singapore...')]),
    L(13.54, [(6.76, "...and we're"), (6.98, 'underway!')]),
    L(6.90, [(18.22, 'Late,'), (18.46, 'late,'), (18.62, 'late'), (18.84, 'on'), (18.98, 'the'), (19.10, 'brakes')]),
    L(6.90, [(19.34, 'and'), (19.52, 'he'), (19.62, 'stays'), (19.84, 'ahead'), (20.22, 'of'), (20.38, 'the'), (20.50, 'Ferrari'), (20.80, 'man.')]),
    L(-3.40, [(33.96, 'Max'), (34.30, 'Verstappen,'), (34.78, 'clinging'), (35.40, 'on'), (35.82, 'to'), (36.20, 'the'), (36.32, 'lead')]),
    L(-3.40, [(36.60, 'by'), (36.88, 'his'), (37.14, 'fingertips...'), (37.88, 'but'), (38.04, "he's"), (38.26, 'still'), (38.44, 'got'), (38.68, 'it.')]),
    L(-366.47, [(403.00, 'And'), (404.46, 'finally'), (405.20, 'for'), (405.76, 'Max'), (406.06, 'Verstappen,')]),
    L(-366.47, [(407.12, 'the'), (407.26, 'Singapore'), (408.00, 'WIN!')]),
    L(28.40, [(14.66, 'Yes'), (15.02, 'Max,'), (15.72, "it's"), (15.82, 'been'), (15.92, 'a'), (15.95, 'very'), (16.10, 'long'), (16.28, 'time')]),
    L(28.40, [(16.46, 'in'), (16.62, 'the'), (16.68, 'making,'), (16.88, 'that'), (17.12, 'one.')]),
    L(28.40, [(17.58, 'Pleased'), (17.94, 'to'), (18.10, 'see'), (18.24, "you've"), (18.38, 'got'), (18.48, 'it.')]),
    L(-413.10, [(461.18, 'With'), (461.28, 'a'), (461.38, 'champagne'), (461.74, 'shower,'), (462.66, 'Max'), (462.86, 'Verstappen.')]),
    L(-413.10, [(463.60, 'Everywhere'), (464.02, 'he'), (464.66, 'has'), (464.78, 'visited'), (465.32, 'more'), (465.44, 'than'), (465.62, 'once'), (465.90, 'in'), (466.04, 'Formula'), (466.30, 'One,')]),
    L(-413.10, [(466.80, 'he'), (466.88, 'is'), (467.02, 'a'), (467.12, 'Grand'), (467.48, 'Prix'), (467.60, 'winner.')]),
    L(-413.10, [(469.10, 'And'), (469.24, 'that'), (469.38, 'now'), (469.60, 'includes'), (470.02, 'Singapore.')]),
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
    name='AL', layout='full', win_y=600,
    active={P1 + '.mp4': (0, 1370), OUT_ + '.mp4': (0, 1330), PF + '.mp4': (0, 1380), GP + '.mp4': (0, 1400),
            POD + '.mp4': (0, 1270)},
    srcdir=os.path.join(ROOT, 'src_max_sg'), tmp=os.path.join(ROOT, 'tmp_al'),
    song=os.path.join(ROOT, 'songs', 'max_trailer3.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AL_max_trailer_v3.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.2,
    fx={}, text=TEXT, text_cy=860, crf=12, overlay=subtitles,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
