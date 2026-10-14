"""Edit V - F1, driver of the day: LEWIS HAMILTON. Direction: "41 years old. Win 106. The first one in red."
Barcelona-Catalunya GP, 14 June 2026: started P2, Ferrari's three-stop strategy, the free stop under the VSC put him
in front - his first win for Ferrari (FIA / The Race race reports). Hook: the Ferrari crossing the line + 41 YEARS
OLD., the story types one fact per hit, the drop is the win, and it ends on the Ferrari crew singing the Italian
anthem with its REAL audio (picture = sound). Layout 'window' (new): the 720p footage stays sharp in a 16:9 window
(no upscale) over a blurred copy of itself. Song: #37 Montagem Rune (slowed) 0-13.3 s, then the anthem.
Footage: official formula1.com videos (race highlights, start, VSC stop, anthem)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT, W, H, ORB

HL, ST, V, K, A = '1867987150306679134', '1867978241467370128', '1867983160603973977', '1867984150167103861', '1867988016533372888'
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    sh(0.0, HL, 442.0),          # the Ferrari crosses the line
    sh(1.53, ST, 6.2),           # the start, P2
    sh(2.88, K, 75.0),           # a Ferrari stop
    sh(4.36, V, 4.4),            # the stop under the VSC
    sh(5.88, V, 10.3),           # out of the pits in front
    # DROP
    sh(7.42, HL, 434.6),         # in the cockpit, the fist
    sh(8.07, K, 52.6),           # onboard
    sh(8.67, HL, 444.2),         # HAMILTON - winner graphic
    sh(9.12, HL, 447.0),
    sh(9.98, HL, 450.0),         # the crew
    sh(10.83, HL, 452.2),
    sh(11.45, HL, 454.6),        # the crew celebrating
    sh(12.07, K, 107.6),         # the pit wall
    sh(12.84, HL, 464.25),       # the podium
    sh(13.31, A, 27.8),          # the crew sings the anthem (real audio from here)
]
END = 19.9
TEXT = [
    (0.04, 1.51, '41 YEARS|OLD.'),
    (1.53, 2.86, 'STARTED|P2.'),
    (2.88, 4.34, 'THREE|STOPS.'),
    (4.36, 5.86, 'ONE UNDER|THE VSC.'),
    (5.88, 7.40, 'OUT IN|FRONT.'),
    (7.42, 9.10, 'WIN|106.'),
    (9.98, 12.82, 'THE FIRST|IN RED.'),
    (14.2, END, 'LEWIS|HAMILTON.'),
]

_f = {}
def overlay(a, f, t, i, lt):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    if 'o' not in _f:
        _f['o'] = ImageFont.truetype(ORB, 34)
        try: _f['o'].set_variation_by_axes([800])
        except Exception: pass
    lab = 'BARCELONA / 14 JUNE 2026' if t < 13.31 else 'SCUDERIA FERRARI / 44'
    d.text(((W - d.textlength(lab, font=_f['o'])) / 2, 656 + 608 + 40), lab, font=_f['o'], fill=(235, 30, 40))
    return np.asarray(im).astype(np.float32) / 255


CFG = dict(
    name='V', layout='window', srcdir=os.path.join(ROOT, 'src_ham'), tmp=os.path.join(ROOT, 'tmp_v'),
    song=os.path.join(ROOT, 'songs', 'ham_mix.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_V_hamilton.mp4'), end=END, plan=PLAN, win_y=656,
    swing=set(), drop={5}, punch=set(range(5, 14)), warm=0.0, sat=1.08, grain=0.1, vig=0.4,
    fx={5: ('radial',), 7: ('xerox',)}, overlay=overlay, text=TEXT, text_cy=430,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
