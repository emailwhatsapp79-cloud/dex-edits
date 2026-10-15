"""Edit AJ - F1, MAX VERSTAPPEN, TRAILER format (Desmond's idea, Oct 15: "like a movie trailer ... the person saying the
thing, then footage of him driving ... sounds"). Singapore GP 2026: his 250th start, pole, sprint win, then the Grand
Prix win - the one circuit he had never won at (formula1.com / Sky race reports).
Sound = real voices over a dark instrumental (APHØTIC - Thalassophobia, full song 78.24 -> 100.3, drop 88.01 = 9.77):
  2.55  commentator "...and his first here in Singapore"        (pole)       - parc ferme, P1 car
  4.70  "...sensational pole lap by you"                          (radio)      - Max climbs out
  6.94  "Max Verstappen wins the Singapore Grand Prix" - "Prix" ON the drop - lights out, night race
  16.25 GP on the radio "Yes Max, we've had a very long time in the making of that one" - Max & GP
  19.28 the crowd: "Max Verstappen!" - the podium (picture = sound, same clip)
Layout 'full' at native 1080x1920 (official @f1 TikTok clips), captions cropped off with `active`."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

HELM, P1, OUT_, HTL = 'f1_7694673917193063682', 'f1_7694669963944103190', 'f1_7695081243175554326', 'f1_7694957322287713558'
SPR, PF, WIN, GP, POD = 'f1_7694997103784791298', 'f1_7694989403172719894', 'f1_7695423602358881558', 'f1_7695768714691595542', 'f1_7695428044822957334'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
PLAN = [
    sh(0.00, HELM, 15.60),      # the helmet - 250 STARTS.
    sh(2.40, P1, 0.30),         # pole: the car rolls into parc ferme   "...his first here in Singapore"
    sh(4.55, OUT_, 0.10, cx=0.3),     # he climbs out                          "...sensational pole lap"
    sh(6.85, HTL, 1.52),        # race night, the grid                   "Max Verstappen wins the Singapore..."
    sh(8.70, P1, 3.85),         # walking under the lights               "...Grand Prix" -> DROP
    sh(9.77, SPR, 5.22),        # DROP: the race, flat out
    sh(10.56, HTL, 4.83),
    sh(11.35, HTL, 8.20),       # the Red Bull at speed
    sh(12.53, HTL, 5.86),
    dict(sh(12.93, HTL, 6.70), jump=True),
    sh(13.72, SPR, 6.66),       # the Dutch fans
    sh(14.51, PF, 0.30),        # P1
    dict(sh(15.69, OUT_, 4.20), jump=True),   # standing in his helmet
    sh(16.48, GP, 10.00),       # with GP                                "Yes Max, a very long time in the making"
    sh(17.67, GP, 12.80),       # champagne
    sh(19.25, POD, 0.03),       # the podium - "Max Verstappen!"
]
END = 22.05
TEXT = [(0.15, 2.35, '250 STARTS.'), (20.0, END, 'SINGAPORE.|FINALLY.')]

CFG = dict(
    name='AJ', layout='full',
    active={P1 + '.mp4': (0, 1370), OUT_ + '.mp4': (0, 1330), PF + '.mp4': (0, 1380), GP + '.mp4': (0, 1400),
            POD + '.mp4': (0, 1270)},
    srcdir=os.path.join(ROOT, 'src_max_sg'), tmp=os.path.join(ROOT, 'tmp_aj'),
    song=os.path.join(ROOT, 'songs', 'max_trailer.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AJ_max_trailer.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.25,
    fx={}, text=TEXT, text_cy=1450, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
