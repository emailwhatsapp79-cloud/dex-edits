"""Edit AH - rebuild of I ("One car. One road. One day.", Taycan GTS, posted Oct 13) - Desmond: "redo ... with
better footage". The film was already 4K (Porsche p337658); the blur came from edit I itself: zoom/whip/spin
transitions (motion blur on every cut), slow-mo by motion interpolation, grain. Same story (midday -> golden hour ->
night), same song (#20) and beat grid, rebuilt clean on cardedit: layout 'tall' (3:4 from 4K = a downscale), hard cuts
on the beat, real speed only. Night has only short takes in the film, so the night part cuts faster on the grid."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

T = 'p337658'
sh = lambda t, src, cx=0.5: dict(t=t, file=T + '.mp4', src=src, cx=cx, mode='real')
PLAN = [
    sh(0.00, 98.40, 0.50),    # front, centred - ONE ROAD.
    sh(1.31, 79.60, 0.55),    # ONE DAY.
    sh(2.53, 83.40, 0.50),
    sh(3.71, 86.60, 0.50),
    sh(4.67, 114.20, 0.50),
    sh(5.90, 95.80, 0.50),
    sh(6.96, 69.00, 0.50),    # parked in the field
    sh(8.05, 126.10, 0.50),   # hand on the paddle - the build
    sh(8.68, 122.90, 0.50),   # DROP
    sh(9.59, 128.05, 0.55),
    sh(10.50, 129.50, 0.55),
    sh(11.42, 132.60, 0.50),
    sh(12.42, 37.75, 0.50),   # with the driver in the field
    sh(13.41, 33.60, 0.45),   # on the track
    sh(14.49, 137.30, 0.45),  # golden hour
    sh(15.38, 139.98, 0.55),  # sunset
    sh(15.88, 140.75, 0.50),  # the last light
    sh(16.32, 152.35, 0.50),  # nightfall, from above
    sh(17.35, 150.03, 0.50),  # the street at night
    sh(18.31, 151.27, 0.50),  # GTS dial
    sh(18.77, 146.87, 0.50),
    sh(19.39, 145.35, 0.50),  # dial
    sh(19.75, 148.39, 0.50),
    sh(20.30, 143.70, 0.50),  # the end - title
]
END = 21.83
TEXT = [(0.03, 1.29, 'ONE ROAD.'), (1.31, 2.51, 'ONE DAY.'), (14.49, 15.36, 'GOLDEN HOUR'), (16.32, 17.33, 'NIGHTFALL'),
        (20.50, END, 'PORSCHE|TAYCAN GTS')]

CFG = dict(
    name='AH', layout='tall', srcdir=os.path.join(ROOT, 'src_car'), tmp=os.path.join(ROOT, 'tmp_ah'),
    song=os.path.join(ROOT, 'songs', 'named', '20_mbappe_malvini_sound.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AH_taycan_oneday.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.05, grain=0.0, vig=0.25,
    fx={}, text=TEXT, text_cy=960, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
