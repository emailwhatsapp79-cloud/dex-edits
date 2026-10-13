"""Edit M - CAR. Direction: "One of 60. Built for the corners." One car - the yellow Bugatti Chiron Pur Sport -
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

PLAN = [
    sh(0.000, 15.75, 'slow', 0.50, NAME),    # hook: front three-quarter, golden light
    sh(1.750, 26.80, 'real', 0.45),          # the 16 on the grille
    sh(3.484, 9.10, 'real', 0.55),           # through the bend, from above
    sh(5.035, 12.70, 'real', 0.50),          # side, close
    sh(6.285, 0.10, 'real', 0.50),           # breather: the mountains
    sh(7.952, 6.80, 'real', 0.50),           # grille close-up
    sh(8.366, 20.25, 'slow', 0.40),          # hands on the wheel - the build
    # drop
    sh(9.991, 35.85, 'real', 0.50),
    sh(10.504, 22.10, 'real', 0.50),
    sh(10.968, 14.45, 'real', 0.55),
    sh(11.753, 23.10, 'real', 0.50),
    sh(12.223, 37.40, 'real', 0.50),
    sh(13.009, 33.10, 'real', 0.50),
    sh(13.473, 19.00, 'real', 0.50),
    sh(14.254, 35.05, 'hero', 0.50),
    sh(15.972, 24.20, 'real', 0.40),
    sh(16.284, 17.30, 'real', 0.50),
    sh(16.750, 25.85, 'real', 0.50),
    sh(17.225, 5.30, 'real', 0.55),
    sh(18.010, 18.05, 'real', 0.40),
    sh(18.474, 3.80, 'real', 0.50),          # the driver's view
    sh(19.246, 39.05, 'real', 0.50),
    sh(20.041, 29.10, 'slow', 0.50, NAME),   # the last corner, slow
]
END = 22.6

CFG = dict(
    name='M', layout='card', srcdir=os.path.join(ROOT, 'src_bug'), tmp=os.path.join(ROOT, 'tmp_m'),
    song=os.path.join(ROOT, 'songs', 'named', '13_funk_unico_super_slowed.mp3'), song_offset=11.25,
    out=os.path.join(ROOT, 'out', 'edit_M_bugatti.mp4'), end=END, plan=PLAN,
    active={T: (90, 898)}, swing={7, 22}, drop={7}, punch=set(range(8, 21)) - {14}, warm=0.02, sat=1.08,
    text=[(0.0, 1.750, 'ONE OF 60.'), (1.750, 3.484, '16 CYLINDERS.'), (5.035, 6.285, '1,500 HP.'),
          (6.285, 7.952, 'THE HAJAR|MOUNTAINS.'), (20.041 + 0.25, END, 'BUILT FOR|THE CORNERS.')],
    text_cy=975,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
