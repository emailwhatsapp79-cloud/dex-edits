"""Edit AP - FOOTBALL, LAMINE YAMAL - format "SHORT & DENSE" (Batch K2 'The Dutch Lion', 28% likes; Desmond: not trailer,
"your pick, what would go viral"). 18 s, a cut on EVERY kick of the song (0.54 s), a white flash on each cut, no voices,
one word at the end. Built to be rewatched. Story: the stare -> his World Cup goal lands ON the drop -> the run at the
camera -> every beat a different moment of his tournament -> the trophy: WORLD CHAMPION.
Song: Party Funk (library #31, the sound of his own TikTok) full, 12.5 s on, slowed to 0.86 (phonk feel).
Footage: official @fifaworldcup clips only (pitch-side camera, 1080p), interview shot as 3:4 (caption cropped off)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

J, A, T = 'fifaworldcup_7661610678914059522', 'fifaworldcup_7653913095462554902', 'fifaworldcup_7664389890263633174'
E, D = 'fifaworldcup_7646511209147125014', 'fifaworldcup_7664307737676893462'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
K = [2.69, 3.22, 3.77, 4.29, 4.84, 5.38, 5.91, 6.45, 6.97, 7.52, 8.05, 8.59, 9.13, 9.67, 10.21, 10.73, 11.28, 11.82,
     12.34, 12.89, 13.41, 13.96, 14.49, 15.03, 15.56, 16.11, 16.65, 17.17]          # the kicks
PLAN = [
    sh(0.00, D, 0.00),                          # he walks in (B&W), the quiet intro
    sh(1.34, A, 0.65),                          # behind the goal: the slide - the ball in ON the drop (2.69)
    dict(sh(K[2], A, 3.95), jump=False),        # he runs at the camera
    sh(K[4], J, 16.40),                         # on his knees
    sh(K[5], J, 18.70),                         # the dribble
    sh(K[6], J, 20.70),
    sh(K[7], J, 25.95),                         # the wing
    dict(sh(K[8], J, 26.60), jump=True),        # strong kick: to the goal line
    dict(sh(K[9], J, 21.80), jump=True),
    sh(K[10], J, 3.95),                         # walking out to the pitch
    sh(K[11], J, 10.00),                        # the tunnel
    sh(K[12], J, 11.20),                        # the stadium
    sh(K[13], J, 5.20),                         # warm-up
    dict(sh(K[14], J, 17.60), jump=True),       # on his knees, wide
    sh(K[15], J, 30.80),                        # running, the 19
    dict(sh(K[16], J, 23.30), jump=True),
    dict(sh(K[17], A, 5.60), jump=True),        # at the camera again
    dict(sh(K[18], J, 28.20), jump=True),
    dict(sh(K[19], A, 7.20), jump=True),
    sh(K[20], J, 40.60),                        # strong kick: arms out, the 19 on his back
    dict(sh(K[21], J, 24.60), jump=True),
    dict(sh(K[22], J, 19.85), jump=True),
    dict(sh(K[23], J, 5.80), jump=True),
    sh(K[24], T, 3.40),                         # the trophy - WORLD CHAMPION.
]
END = 18.20
TEXT = [(K[25], END, 'WORLD|CHAMPION.')]

CFG = dict(
    name='AP', layout='full', active={},
    srcdir=os.path.join(ROOT, 'src_yamal'), tmp=os.path.join(ROOT, 'tmp_ap'),
    song=os.path.join(ROOT, 'songs', 'yamal_dense.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AP_yamal_dense.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=True, warm=0.0, sat=1.06, grain=0.0, vig=0.25,
    fx={0: ('bw',)}, text=TEXT, text_cy=1450, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
