"""Edit AG - rebuild of M (Bugatti Chiron Pur Sport, posted Oct 15) - Desmond: "redo with better footage".
The only official Pur Sport film is 2.1:1 letterboxed 1080p; M cropped it to a 9:16 card = ~1.8x upscale (the blur).
AG shows it 4:3 at 1080x810 = a slight DOWNscale (no upscale anywhere) over its own blur, real speed only (no
motion interpolation), no grain/punch/flash. Same story, song and cut timing as M.

Edit M - CAR. Direction: "One of 60. Built for the corners." One car - the yellow Bugatti Chiron Pur Sport -
on the mountain roads of the Hajar mountains (Bugatti's own film). Calm, long shots before the drop (one of 60,
16 cylinders, 1,500 hp, the mountains), then the drop at ~10 s cuts the corners on the beat; ends on a slow-motion
corner: BUILT FOR THE CORNERS. Song: 13 "Funk Unico (super slowed)" from 11.25 s (drop 21.241 -> 9.991)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

T = 'hatta_bugatti_final.mp4'
NAME = 'BUGATTI CHIRON PUR SPORT'
sh = lambda t, src, mode='real', cx=0.5, label='': dict(t=t, file=T, src=src, cx=cx, mode=mode, label=label)

PLAN = [                                     # real speed only -> long shots split on a hit or moved to long takes
    sh(0.000, 15.75, 'real', 0.50, NAME),    # hook: front three-quarter, golden light
    sh(0.990, 22.07, 'real', 0.50),          # from above, in the bend
    sh(1.750, 26.80, 'real', 0.45),          # the 16 on the grille
    sh(3.484, 9.10, 'real', 0.55),           # through the bend, from above
    sh(5.035, 12.70, 'real', 0.50),          # side, close
    sh(6.285, 0.10, 'real', 0.50),           # breather: the mountains
    sh(7.952, 6.80, 'real', 0.50),           # grille close-up
    sh(8.366, 20.25, 'real', 0.40),          # hands on the wheel - the build
    sh(9.130, 2.32, 'real', 0.50),           # the road ahead
    # drop
    sh(9.991, 35.85, 'real', 0.50),
    sh(10.504, 35.06, 'real', 0.50),
    sh(10.968, 14.45, 'real', 0.55),
    sh(11.753, 23.10, 'real', 0.50),
    sh(12.223, 37.40, 'real', 0.50),
    dict(sh(13.009, 11.00, 'real', 0.50), jump=True),   # later in the bend take
    sh(13.473, 19.00, 'real', 0.50),
    sh(14.254, 33.06, 'real', 0.50),         # the corner from above
    sh(15.972, 24.20, 'real', 0.40),
    sh(16.284, 17.30, 'real', 0.50),
    sh(16.750, 25.85, 'real', 0.50),
    sh(17.225, 5.30, 'real', 0.55),
    sh(18.010, 18.05, 'real', 0.40),
    sh(18.474, 3.80, 'real', 0.50),          # the driver's view
    sh(19.246, 39.05, 'real', 0.50),
    sh(20.041, 29.10, 'real', 0.50, NAME),   # the last corner
]
END = 22.6

CFG = dict(
    name='AG', layout='tall', pic_h=810, srcdir=os.path.join(ROOT, 'src_bug'), tmp=os.path.join(ROOT, 'tmp_ag'),
    song=os.path.join(ROOT, 'songs', 'named', '13_funk_unico_super_slowed.mp3'), song_offset=11.25,
    out=os.path.join(ROOT, 'out', 'edit_AG_bugatti_sharp.mp4'), end=END, plan=PLAN,
    active={T: (90, 898)}, swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.01, sat=1.05,
    grain=0.0, vig=0.2, fx={}, bg_dim=0.45,
    text=[(0.0, 1.750, 'ONE OF 60.'), (1.750, 3.484, '16 CYLINDERS.'), (5.035, 6.285, '1,500 HP.'), (6.285, 7.952, 'THE HAJAR|MOUNTAINS.'),
          (20.041 + 0.25, END, 'BUILT FOR|THE CORNERS.')],
    text_cy=1560, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
