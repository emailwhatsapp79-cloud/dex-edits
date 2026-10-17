"""Edit AV - CAR, 911 'TRIBUTE TO TRANSFAGARASAN' - format SINGLE-CAR SPOTTING (reference L1 GT2 RS, 23% likes;
Desmond Oct 17: "the car edit should make sense"). The story in one line: Top Gear's "best road in the world" got its
own 911. Sound #61 (the L1 sound itself), cut on the L1 cut points (every 2 beats).
  macro headlight -> crest -> the car arrives out of the fog (held) -> the driver walks to it -> hands on the wheel ->
  the bends -> the gallery tunnel -> the badge 'TRIBUTE TO TRANSFAGARASAN 50 YEARS' -> wheel crest -> the road from above.
Footage: Porsche Newsroom press film 322803 (1080p, 3:4 'tall' = 1.33x, no burned titles used)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

T = 'p_322803'
sh = lambda t, src, cx=0.5, **k: dict(t=t, file=T + '.mp4', src=src, cx=cx, mode='real', **k)
PLAN = [                             # the film's takes are ~0.5-2 s: one take per cut, cuts on the beats of #61
    sh(0.00, 8.69),                  # headlights glowing in the fog
    sh(1.02, 7.81),                  # the headlight, macro
    sh(1.51, 17.10),                 # the car arrives out of the fog (held)
    sh(3.50, 10.98),                 # the driver walks to it
    sh(5.46, 23.70),                 # hands on the wheel
    sh(6.43, 19.30),                 # into the bends
    sh(8.36, 21.45),                 # headlights through the hairpin
    sh(9.33, 31.45),                 # the road from above
    sh(10.31, 28.65),                # TRIBUTE TO TRANSFAGARASAN - 50 YEARS
    sh(10.80, 34.93),                # the gallery - the hero, held to the end
]
END = 13.72                          # ends before the film's PORSCHE end card
CFG = dict(
    name='AV', layout='tall', active={},
    srcdir=os.path.join(ROOT, 'src_pcar'), tmp=os.path.join(ROOT, 'tmp_av'),
    song=os.path.join(ROOT, 'songs', 'gt2rs_sound.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AV_transfagarasan.mp4'), end=END, plan=PLAN, pad=0.02,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.02, sat=1.0, grain=0.0, vig=0.3, bg_dim=0.35,
    fx={}, text=[(0.10, 2.40, 'THE BEST ROAD IN THE WORLD|GOT ITS OWN 911.')], text_cy=1700, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
