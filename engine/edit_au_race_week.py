"""Edit AU - F1, AUSTIN RACE WEEK - format "RACE WEEK" (reference M1 @ctrllx, 614k / 11.4k shares). 28 s, sound #63 full.
  0-5.43   black, the sung words typed huge with the footage INSIDE the letters: YOU / SHOULD / KNOW (mask_text)
  5.43-9.45  a driver per kick: Max (pole portrait), Kimi, Charles, Lewis
  9.45-13.18 the start: red lights, lights out, turn 1 from above
  13.18-17.17 strobe burst: a cut every 0.25 s through the overtakes
  17.17-21.66 the drop: a cut on every kick - parc ferme, champagne, trophies, arms up
  21.66-28 the breath, then AUSTIN. RACE WEEK.
Footage: official @f1 / team vertical clips (3:4, captions cropped) + formula1.com highlights as a sharp 16:9 window."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

F, A, P, L = 'ferrari_7598510370847853847', 'f1_7694610596188278038', 'f1_7695063981081283862', 'f1_7695435478115388694'
RB1, RB2, OUT, P1 = 'redbullracing_7695048934607162646', 'redbullracing_7695052304977874198', 'f1_7695081243175554326', 'f1_7694669963944103190'
GP, POD, KPOD, HTL = 'f1_7695768714691595542', 'f1_7695428044822957334', 'f1_7643587480364551446', 'f1_7694957322287713558'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
win = lambda t, src, **k: sh(t, 'H', src, layout='window', **k)
J = lambda d: dict(d, jump=True)
BURST = [113.8, 173.9, 244.9, 262.0, 296.4, 322.9, 330.5, 178.6, 249.6, 266.6, 300.6, 327.2, 117.6, 340.2, 350.2, 360.2]
KICK = [17.17, 17.89, 18.38, 18.85, 19.34, 19.84, 20.33, 20.84, 21.33]
PLAN = [
    sh(0.00, F, 0.00),                              # inside the letters: the Ferrari garage, the car rolls out
    sh(5.43, RB1, 1.60),                            # Max - the pole portrait
    sh(6.70, KPOD, 4.00),                           # Kimi - lifted on the podium
    sh(8.07, L, 1.55),                              # Charles
    sh(9.45, HTL, 8.60),                            # the grandstand at night
    win(10.40, 4.00),                               # the red lights
    J(win(11.30, 6.90)),                            # lights out
    J(win(12.20, 13.95)),                           # turn 1 from above
] + [J(win(13.18 + 0.25 * k, BURST[k])) for k in range(16)] + [
    sh(KICK[0], P, 1.00),                           # DROP: the Ferrari in parc ferme
    sh(KICK[1], OUT, 3.00),                         # Max out of the car
    sh(KICK[2], GP, 13.70),                         # champagne
    sh(KICK[3], L, 8.30),                           # Charles, arms up
    sh(KICK[4], POD, 6.50),                         # the trophy in the air
    J(sh(KICK[5], P, 5.55)),                        # the mechanics, the trophies
    sh(KICK[6], RB2, 17.50),                        # Max, cool-down, waving
    J(sh(KICK[7], A, 0.05)),                        # Charles and Lewis
    sh(KICK[8], P1, 0.40),                          # the car rolls into parc ferme
    J(sh(21.66, HTL, 2.60)),                        # the breath: the night grandstand -> AUSTIN. RACE WEEK.
]
END = 27.95
CFG = dict(
    name='AU', layout='tall', win_y=656,
    active={A + '.mp4': (0, 1380), P + '.mp4': (0, 1380), L + '.mp4': (0, 1400), OUT + '.mp4': (0, 1400),
            P1 + '.mp4': (0, 1390), GP + '.mp4': (0, 1400), POD + '.mp4': (0, 1320), KPOD + '.mp4': (0, 1440),
            HTL + '.mp4': (480, 1440)},
    srcdir=os.path.join(ROOT, 'src_rw'), tmp=os.path.join(ROOT, 'tmp_au'),
    song=os.path.join(ROOT, 'songs', 'race_week.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AU_race_week.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=True, warm=0.0, sat=1.08, grain=0.0, vig=0.35, bg_dim=0.35,
    fx={}, mask_text=[(0.0, 0.80, 'YOU'), (0.80, 1.32, 'YOU|SHOULD'), (1.32, 5.43, 'YOU|SHOULD|KNOW')],
    text=[(24.75, END, 'AUSTIN.|RACE WEEK.')], text_cy=960, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
