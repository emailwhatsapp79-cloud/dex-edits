"""Edit AF - rebuild of F (Taycan GTS E-Shift, posted Oct 13) - Desmond: "redo ... with better footage".
The footage was already 4K (Porsche press film p337658); the blur came from the old engine (every shot slowed with
motion interpolation, push-zooms, grain, glow). Same story, same song and timing, rebuilt on cardedit:
layout 'tall' (3:4 from 4K = a DOWNscale), every shot real speed, no grain, light grade.
Direction: "Electric. Silent. Boring? - not anymore." Drop 5.5 = the rev needle snaps."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

T = 'p337658'
sh = lambda t, src, cx=0.5, mode='real': dict(t=t, file=T + '.mp4', src=src, cx=cx, mode=mode)
PLAN = [                      # one source take per shot (the old plan reused slowed-down short takes)
    sh(0.00, 98.90, 0.50),    # car at camera - ELECTRIC.
    sh(1.20, 129.50, 0.50),   # on the road - SILENT.
    sh(2.30, 73.00, 0.50),    # dial at 0 - BORING?
    sh(3.30, 92.30, 0.50),    # hand to the paddle - NOT ANYMORE.
    sh(4.10, 143.70, 0.45),   # paddle pull - "destroy it all"
    sh(5.50, 118.60, 0.60),   # DROP: the speedo - E-SHIFT
    sh(6.29, 152.35, 0.50),   # night, from above
    sh(7.29, 33.60, 0.45),    # track
    sh(8.34, 20.35, 0.50),    # paddle
    sh(8.86, 138.31, 0.45),   # GTS dial
    sh(9.38, 83.40, 0.50),    # car on the road
    sh(10.43, 124.10, 0.45),  # the driver
    sh(11.35, 128.05, 0.50),  # car at camera
    sh(12.31, 46.00, 0.50),   # the dash
    sh(12.82, 86.60, 0.50),   # car on the road
    sh(13.84, 126.10, 0.50),  # paddle tap
    sh(14.40, 114.30, 0.50),  # corner at camera
    sh(15.58, 89.20, 0.55),   # speedo
    sh(16.60, 95.80, 0.50),   # car on the road
    sh(17.67, 132.60, 0.50),  # drives away
    sh(18.74, 55.10, 0.50),   # the button
    sh(19.37, 135.30, 0.50),  # sunset
    sh(20.97, 48.30, 0.50),   # dial
    sh(22.13, 67.50, 0.50),   # the car on the road - title
]
END = 25.2
TEXT = [(0.03, 1.18, 'ELECTRIC.'), (1.20, 2.28, 'SILENT.'), (2.30, 3.28, 'BORING?'), (3.30, 4.08, 'NOT ANYMORE.'),
        (5.50, 7.27, 'E-SHIFT'), (22.30, END, 'TAYCAN GTS')]

CFG = dict(
    name='AF', layout='tall', srcdir=os.path.join(ROOT, 'src_car'), tmp=os.path.join(ROOT, 'tmp_af'),
    song=os.path.join(ROOT, 'songs', 'named', '19_destroy_it_all_yuji_slowed.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AF_taycan_sharp.mp4'), end=END, plan=PLAN,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.25,
    fx={}, text=TEXT, text_cy=960, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
