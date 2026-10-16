"""Edit AS - FOOTBALL, VINICIUS JR - format "LIGHT EDIT" (Batch H: few cuts, no text, the footage and the song carry
it). Song: library #6 Brazilian funk from 5.5 s - the lyric drives the picture:
  "devagar, devagar" (slowly, slowly) -> Vini dancing slowly in the World Cup warm-up
  "vai, vai, vai..." (go, go, go) -> the attack builds; "joga pro lado" -> the drop (8.25) = the ball in the net
  then straight to the ending: smiling with his Player of the Match trophy (15.7 s, three shots).
Footage: official @fifaworldcup (warm-up, POTM, 1080p pitch-side) + @foxsports goal (caption cropped, 3:4)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

WU, POTM, GOAL = 'fifaworldcup_7656862541368298774', 'fifaworldcup_7651047774196092182', 'foxsports_7651016269382110494'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
PLAN = [
    sh(0.00, WU, 3.40),                         # "devagar, devagar" - the slow dance
    sh(4.86, GOAL, 3.96, layout='square'),        # "vai, vai, vai" - the attack; the ball in ON the drop (8.25)
    sh(9.12, POTM, 0.40),                       # the trophy, then the smile - the end
]
# FOX celebration close-ups measured soft (motion blur, HARD RULE) - cut; the edit ends tight on the sharp POTM shot.
END = 15.70

CFG = dict(
    name='AS', layout='full', active={GOAL + '.mp4': (0, 1200)},
    srcdir=os.path.join(ROOT, 'src_vini'), tmp=os.path.join(ROOT, 'tmp_as'),
    song=os.path.join(ROOT, 'songs', 'vini_funk.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AS_vini_light.mp4'), end=END, plan=PLAN, pad=0.06,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.01, sat=1.06, grain=0.0, vig=0.25, bg_dim=0.45,
    fx={}, text=[], crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
