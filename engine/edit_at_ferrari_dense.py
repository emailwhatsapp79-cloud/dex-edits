"""Edit AT - F1, FERRARI DOUBLE PODIUM (Singapore: Leclerc P2, Hamilton P3) - format "SHORT & DENSE" (Yamal style;
Desmond, Oct 16: "go with the yamal one", Ferrari double podium). 14.7 s.
Song: library #55 'It's race time' (f1edits.ae), full, from 0 - the voice drives the intro:
  "Hey, wake your ass up. Let's go. It's race time." -> B&W: the garage, the car rolls out ON "race time"
  "You can be my guy..." -> Charles and Lewis together on stage
  the drop (7.19) -> colour, a cut on every kick (0.47 s): parc ferme P2, Charles walking off, the handshake,
  the mechanics with the trophies, the helmet, the podium, arms up -> FORZA.
Footage: official @f1 / @ferrari vertical clips only (all measured sharp, captions cropped by the 3:4 layout)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

F, A = 'ferrari_7598510370847853847', 'f1_7694610596188278038'
P, L = 'f1_7695063981081283862', 'f1_7695435478115388694'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
K = [7.19, 7.66, 8.13, 8.60, 9.08, 9.56, 10.03, 10.50, 10.97, 11.45, 11.94, 12.40, 12.88, 13.33, 13.80, 14.28]
PLAN = [
    sh(0.00, F, 1.04),                          # "wake your ass up... it's race time" - the car rolls out
    sh(4.16, A, 9.00),                          # "you can be my guy" - Charles and Lewis
    sh(K[0], P, 1.00),                          # DROP: the Ferrari in parc ferme, P2
    sh(K[1], P, 2.10),                          # Charles walks to the car
    dict(sh(K[2], P, 3.10), jump=True),
    sh(K[3], L, 1.55),                          # Charles, cool-down room
    dict(sh(K[4], L, 0.05), jump=True),         # the handshake
    dict(sh(K[5], P, 5.55), jump=True),         # the mechanics, the trophies
    dict(sh(K[6], A, 0.05), jump=True),         # Charles and Lewis, mics
    dict(sh(K[7], P, 4.50), jump=True),         # the helmet
    dict(sh(K[8], L, 3.00), jump=True),         # out to the podium
    dict(sh(K[9], L, 4.55), jump=True),         # the 16 on the podium
    dict(sh(K[10], A, 24.60), jump=True),       # "it was fun"
    dict(sh(K[11], P, 6.10), jump=True),
    dict(sh(K[12], P, 7.05), jump=True),        # Charles and Lewis, cool-down room (A 10.6 would repeat the intro take)
    dict(sh(K[13], L, 8.30), jump=True),        # arms up -> FORZA.
]
END = 14.70
TEXT = [(K[14], END, 'FORZA.')]

CFG = dict(
    name='AT', layout='tall', active={A + '.mp4': (0, 1380), P + '.mp4': (0, 1380), L + '.mp4': (0, 1400)},
    srcdir=os.path.join(ROOT, 'src_ferd'), tmp=os.path.join(ROOT, 'tmp_at'),
    song=os.path.join(ROOT, 'songs', 'race_time.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AT_ferrari_dense.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=True, warm=0.0, sat=1.06, grain=0.0, vig=0.25, bg_dim=0.4,
    fx={0: ('bw',), 1: ('bw',)}, text=TEXT, text_cy=960, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
