"""Edit AW - FOOTBALL, JUDE BELLINGHAM - "THE RUN" (light + dense). One story: his solo run vs France at the World Cup
(FOX: "one of the best solo runs of this World Cup"). Sound #37 Montagem Rune (slowed phonk): the slow 7.4 s build IS
the run, in ONE real-speed take - the ball hits the net ON the drop (7.42) - then a cut on every kick: the celebration,
the smile, the crest, the team. Hook text asks a question (comments).
Footage: official @fifaworldcup pitch-side clips (1080p, measured sharp at 100%)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

A, B = 'fifaworldcup_7664049020788165910', 'fifaworldcup_7694290728993738006'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
J = lambda d: dict(d, jump=True)
K = [7.42, 7.88, 8.50, 9.13, 9.89, 10.52, 11.12, 11.75, 12.36, 12.98, 13.60, 14.21, 14.84]
PLAN = [
    sh(0.00, A, 16.18),             # THE RUN - one take: past the defenders, the finish, the net ON the drop
    sh(K[1], A, 24.70),             # he wheels away
    J(sh(K[2], A, 26.40)),
    J(sh(K[3], A, 28.20)),          # arms out
    J(sh(K[4], A, 30.60)),          # the smile
    J(sh(K[5], A, 32.00)),          # still celebrating (B close-up measured soft)
    sh(K[6], A, 34.30),             # the team arrives
    J(sh(K[7], A, 37.00)),
    J(sh(K[8], A, 40.00)),
    J(sh(K[9], A, 43.00)),
    J(sh(K[10], A, 46.00)),         # -> BELLINGHAM.
]
END = 15.40
TEXT = [(0.15, 2.60, 'BEST SOLO RUN|OF THE WORLD CUP?'), (K[10], END, 'BELLINGHAM.')]

CFG = dict(
    name='AW', layout='full', active={},
    srcdir=os.path.join(ROOT, 'src_jude'), tmp=os.path.join(ROOT, 'tmp_aw'),
    song=os.path.join(ROOT, 'songs', 'rune.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AW_bellingham_run.mp4'), end=END, plan=PLAN, pad=0.06,
    swing=set(), drop=set(), punch=set(), cut_flash=True, warm=0.0, sat=1.05, grain=0.0, vig=0.25,
    fx={}, text=TEXT, text_cy=1450, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
