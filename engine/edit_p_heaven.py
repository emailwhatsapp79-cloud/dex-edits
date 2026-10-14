"""Edit P - NATURE (travel aesthetic). Direction: "I saw a piece of heaven." Alpine postcards, one per soft beat,
each matching the lyric being sung: "piece of heaven" = clouds over a green valley; "waiting impatient for me" =
an empty bench by the lake; "running far away" = the road through the mountains; "run off the wall" = a waterfall
off a cliff; "nobody knows" = mist on the peaks. Calm: no flashes, no shake - slow push-ins, saturated colour.
Song: library #29 (swissaround sound). Footage: Mixkit (free licence)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

sh = lambda t, f, src, cx=0.5, mode='real': dict(t=t, file=f'{f}.mp4', src=src, cx=cx, mode=mode)
PLAN = [
    sh(0.000, 48483, 3.0, 0.50),    # "I saw a piece of heaven" - clouds in the valley under snowy peaks
    sh(1.207, 15919, 2.0, 0.50),    # river valley and snowy mountains
    sh(2.389, 100416, 3.0, 0.50),   # green valley
    sh(3.678, 25234, 1.0, 0.45),    # "waiting impatient" - the empty bench by the lake
    sh(4.614, 100200, 10.0, 0.50),  # waterfall between green hills
    sh(5.865, 32309, 4.0, 0.50),    # "for me" - village by the lake
    sh(7.027, 35528, 5.0, 0.50),    # mountain village in the sun
    sh(8.316, 26578, 3.0, 0.50),    # twin waterfalls
    sh(9.614, 31939, 3.0, 0.50),    # the Swiss Alps in snow
    sh(10.502, 26080, 5.0, 0.50),   # "running far away" - the path across the meadow
    sh(11.668, 28915, 6.0, 0.50),   # "far away" - flying between the ranges
    sh(12.628, 100194, 4.0, 0.50),  # "run off the wall" - water off the cliff
    sh(13.981, 3383, 3.0, 0.50),    # "someday" - peak above the clouds
    sh(15.141, 3308, 2.0, 0.50),    # "nobody knows" - mist at the foot of the mountain
    sh(16.301, 48109, 5.0, 0.50),   # clouds cover the ranges
    sh(17.271, 4396, 4.0, 0.50),    # "nobody knows" - fog on the heights
    sh(18.062, 28338, 3.0, 0.50),   # the lone tree in the cloud
]
END = 18.8

CFG = dict(
    name='P', layout='full', srcdir=os.path.join(ROOT, 'src_swiss'), tmp=os.path.join(ROOT, 'tmp_p'),
    song=os.path.join(ROOT, 'songs', 'named', '29_swiss_song_lyrics.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_P_heaven.mp4'), end=END, plan=PLAN,
    swing=set(), drop=set(), punch=set(), cut_flash=False, grain=0.12, vig=0.35, warm=0.015, sat=1.32,
    text=[], text_cy=960,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
