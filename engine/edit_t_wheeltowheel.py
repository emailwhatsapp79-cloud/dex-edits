"""Edit T - F1 (the whole grid, no single driver). Direction: "Wheel to wheel." Lights out (two race starts, the
turn-1 squeeze, rain spray) while the sound builds, then the drop is pure close racing between different teams on
every hit - side by side, sparks, dives into the braking zone - and it ends: THIS IS FORMULA 1.
Song: library #16 (instrumental drift sound) from 10.3 s, so the drop (14.75) lands at 4.45.
Footage: official formula1.com race highlights (Singapore, Sepang), card layout."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

OFF = 10.3
S, B = 'sgp_hl', 'bhr_hl'
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=round(t, 3), file=f + '.mp4', src=src, cx=cx, mode=mode)
s = lambda song_t: song_t - OFF
PLAN = [
    sh(0.0, S, 3.0),                    # lights out
    sh(s(11.01), B, 2.0),               # another start
    sh(s(12.25), S, 15.0),              # turn 1 squeeze
    sh(s(12.88), B, 29.7),              # spray
    sh(s(14.44), S, 19.0),
    # DROP
    sh(s(14.75), S, 273.5),             # WHEEL TO WHEEL
    sh(s(15.24), B, 106.0),
    sh(s(15.85), S, 265.5),             # sparks
    sh(s(16.33), B, 198.0),
    sh(s(16.63), S, 310.0),
    sh(s(17.26), B, 75.5),
    sh(s(17.88), S, 339.6),
    sh(s(18.57), B, 389.0),
    sh(s(19.28), S, 384.4),
    sh(s(19.94), B, 400.0),
    sh(s(20.38), S, 316.0),
    sh(s(21.01), B, 214.0),
    sh(s(21.95), S, 398.2),
    sh(s(22.90), B, 226.0, 'slow'),     # onboard breath
    sh(s(23.83), S, 296.0),
    sh(s(24.44), B, 290.0),
    sh(s(25.23), B, 42.0, 'slow'),      # THIS IS FORMULA 1.
]
END = 16.8
I_DROP = 5
TEXT = [
    (0.03, s(12.25) - 0.02, 'LIGHTS OUT.'),
    (s(12.25), s(12.88) - 0.02, 'NO GAPS.'),
    (s(12.88), s(14.44) - 0.02, 'NO FEAR.'),
    (s(14.75), s(15.85) - 0.02, 'WHEEL|TO WHEEL.'),
    (s(25.23) + 0.1, END, 'THIS IS|FORMULA 1.'),
]

CFG = dict(
    name='T', layout='card', srcdir=os.path.join(ROOT, 'src_max'), tmp=os.path.join(ROOT, 'tmp_t'),
    song=os.path.join(ROOT, 'songs', 'named', '16_xiaomi_drift_sound.mp3'), song_offset=OFF,
    out=os.path.join(ROOT, 'out', 'edit_T_wheeltowheel.mp4'), end=END, plan=PLAN,
    swing={0, I_DROP, len(PLAN) - 1}, drop={I_DROP, 12}, punch=set(range(I_DROP, len(PLAN) - 1)),
    warm=0.0, sat=1.12, grain=0.15, vig=0.5,
    fx={I_DROP: ('radial',), 7: ('xerox',), 12: ('radial',), 16: ('strobe',)},
    text=TEXT,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
