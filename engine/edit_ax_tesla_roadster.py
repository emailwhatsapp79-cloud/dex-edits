"""Edit AX - CAR, TESLA ROADSTER (unveil Oct 15 2026, SpaceX McGregor) - "TESLA MADE A CAR THAT FLIES."
Official Tesla livestream replay in 4K (3840x2160) -> 9:16 crop = DOWNscale, razor sharp. Sound #23 (calm build, DROP 9.77).
  hook: the car in mid-air from above -> the build: up the vertical wall, through the truss, the run-in from above ->
  DROP: the barrel roll -> the landing in smoke -> the jump over the Semi -> the explosion of smoke -> 0-60 launch -> ROADSTER."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

A, B, C, D = 'k4_718', 'k4_1625', 'k4_1258', 'k4_1036'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
PLAN = [
    sh(0.00, B, 13.60),             # HOOK: the car in mid-air, from above
    sh(1.90, A, 23.00),             # up the vertical wall, upside down
    dict(sh(5.00, A, 33.60), jump=True),             # through the truss
    dict(sh(7.00, A, 36.00), jump=True),             # the run-in, from above
    sh(9.77, B, 5.50),              # DROP: the barrel roll
    dict(sh(11.30, A, 41.20), jump=True),            # the landing in smoke
    sh(12.70, B, 26.20),            # the jump over the Semi
    dict(sh(14.06, B, 29.00), jump=True),            # the smoke explodes
    sh(15.50, C, 13.00),            # 0-60 in under a second
    sh(17.40, D, 4.50),             # ROADSTER.
]
END = 19.30
TEXT = [(0.05, 1.85, 'TESLA MADE A CAR|THAT FLIES.'), (17.45, END, 'ROADSTER.')]
CFG = dict(
    name='AX', layout='full', active={},
    srcdir=os.path.join(ROOT, 'src_tsla4k'), tmp=os.path.join(ROOT, 'tmp_ax'),
    song=os.path.join(ROOT, 'songs', 'formula_max.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AX_tesla_roadster.mp4'), end=END, plan=PLAN, pad=0.06,
    swing=set(), drop={4}, punch=set(), cut_flash=True, warm=0.0, sat=1.04, grain=0.0, vig=0.25,
    fx={}, text=TEXT, text_cy=1500, crf=12,
)
if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
