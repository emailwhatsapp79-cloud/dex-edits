"""Edit W - CARS. Direction: "Built like a watch." Concept transition (lesson from the Red Bull 'microscope' edit): a
Swiss watch movement ticking in macro -> the Bugatti Tourbillon's instrument cluster, which is built like a watch ->
the car itself on the drop: BUGATTI TOURBILLON. Ends: V16. / 1,800 PS. Cinematic: black frame, the 16:9 picture kept
sharp (4K/1080p press films downscaled, never upscaled), no grain. Song: #41 (instrumental, from the McLaren 720S
reference) from 4.6 s. Footage: Bugatti newsroom films (Tourbillon launch, Doha, the Tourbillon watch film)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

OFF = 4.6
WT, V16, DOHA = 'bugatti-chiron-tourbillon-get-your-motor-running', '240603_BUGATTI_LAUNCH_V16_EX_16x9-Moodcut-002', 'BUGATTI_Tourbillon_Doha_moodcut'
sh = lambda t, f, src, mode='real', cx=0.5: dict(t=round(t, 3), file=f + '.mp4', src=src, cx=cx, mode=mode)
s = lambda song_t: song_t - OFF
PLAN = [
    sh(0.0, WT, 9.0),            # the movement ticking
    sh(s(5.83), WT, 49.0),       # the watch
    sh(s(7.54), V16, 6.06, 'slow'),       # the car's instrument cluster - same idea
    sh(s(8.19), V16, 6.6, 'slow'),
    sh(s(8.78), WT, 33.0),      # the car in the dark
    sh(s(9.66), V16, 9.2),
    sh(s(10.55), DOHA, 0.05),
    # DROP
    sh(s(11.14), DOHA, 1.35),    # BUGATTI TOURBILLON
    sh(s(12.03), DOHA, 2.85),
    sh(s(13.80), DOHA, 5.0),
    sh(s(14.39), DOHA, 8.35),    # the cluster up close
    sh(s(15.28), V16, 1.75),
    sh(s(15.57), V16, 3.06, 'slow'),
    sh(s(16.16), DOHA, 6.6),
    sh(s(16.75), V16, 10.8),
    sh(s(17.64), WT, 44.6),      # back to the watch
    sh(s(18.52), V16, 0.15, 'slow'),   # V16. 1,800 PS.
]
END = 16.3
TEXT = [
    (0.04, s(7.54) - 0.02, 'BUILT LIKE|A WATCH.'),
    (s(11.14), s(12.03) - 0.02, 'BUGATTI|TOURBILLON.'),
    (s(18.52) + 0.1, END, 'V16.|1,800 PS.'),
]

def pre_fx(fr, i, t, lt):
    """Lift the shadows: the press films are graded very dark for cinema, too dark for a phone."""
    import numpy as np
    return np.clip(fr, 0, 1) ** 0.68


CFG = dict(
    name='W', layout='window', win_blur=False, win_rule=False, srcdir=os.path.join(ROOT, 'src_bug'),
    tmp=os.path.join(ROOT, 'tmp_w'), song=os.path.join(ROOT, 'songs', 'named', '41_sound.mp3'), song_offset=OFF,
    out=os.path.join(ROOT, 'out', 'edit_W_tourbillon.mp4'), end=END, plan=PLAN, win_y=656,
    swing=set(), drop={7}, punch=set(), cut_flash=False, warm=0.0, sat=1.05, grain=0.0, vig=0.0,
    fx={}, pre_fx=pre_fx, text=TEXT, text_cy=440,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
