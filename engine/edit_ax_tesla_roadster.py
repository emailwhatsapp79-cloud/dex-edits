"""Edit AX v2 - CAR, TESLA ROADSTER - TRAILER with Elon's real voice + the real event sound (no F1 song; Desmond Oct 17:
"why is it on F1 song... can't we do better"). Official Tesla livestream replay in 4K -> 9:16 = downscale, sharp.
  "Flying cars are real." (over the car upside down on the wall) -> the stunt in REAL TIME with the live sound:
  up the wall, launch, landing, "Well, it worked." -> the barrel roll from above under "the future promised us flying cars,
  but instead we got 140 characters." -> "Well, not anymore." -> the jump over the Semi + the explosion -> ROADSTER.
Audio = songs/tesla_live.wav, stitched from the livestream segments in shot order (each shot carries its own sound
except the voice-over lines)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

A, B, C, D = 'k4_718', 'k4_1625', 'k4_1258', 'k4_1036'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
PLAN = [
    sh(0.00, A, 23.00),                         # FLYING CARS ARE REAL. - upside down on the wall
    dict(sh(1.90, A, 22.50), jump=True),        # the stunt, real time: the wall, the launch, the landing, "well, it worked."
    sh(11.15, B, 4.50),                         # the barrel roll from above (voice-over)
    dict(sh(14.75, A, 41.60), jump=True),       # "well, not anymore." - it lands
    sh(15.85, B, 23.60, layout='window'),       # the jump over the Semi + the explosion - full 16:9 band (the car crosses the whole frame)
    sh(21.85, D, 4.50),                         # ROADSTER.
]
END = 24.35
TEXT = [(0.05, 1.85, 'FLYING CARS|ARE REAL.'), (10.00, 11.10, 'WELL, IT WORKED.'),
        (11.20, 13.30, 'THE FUTURE PROMISED US|FLYING CARS'), (13.34, 14.70, 'BUT WE GOT|140 CHARACTERS.'),
        (14.78, 15.82, 'WELL,|NOT ANYMORE.'), (22.20, END, 'ROADSTER.')]
CFG = dict(
    name='AX', layout='full', active={},
    srcdir=os.path.join(ROOT, 'src_tsla4k'), tmp=os.path.join(ROOT, 'tmp_ax'),
    song=os.path.join(ROOT, 'songs', 'tesla_live.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AX_tesla_roadster.mp4'), end=END, plan=PLAN, pad=0.06,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.25,
    fx={}, text=TEXT, text_cy=1500, crf=12,
)
if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
