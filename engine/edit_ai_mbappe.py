"""Edit AI - FOOTBALL, MBAPPE (rotation after Messi/Ronaldo), Oct 19 12:00. Direction: "Level with Messi."
ONE tournament (2026 World Cup), only sharp official clips (@fifaworldcup pitch-side + FIFA's native super-slow-mo,
@foxsports broadcast close-ups cropped above their captions).
Song: VIOLENTO (Slowed) - Kobe Mane, FULL song 57.3 -> 82.08 (the quiet build right before the drop at 62.28, ends on
a phrase, fade). Key actions ON the 808 hits:
  build      -> his face, then the penalty run-up; the ball hits the net ON the drop (4.98)
  6.42       -> pitch-side behind the goal: the ball hits the net, he runs at the camera
  9.98       -> the scream
  14.18      -> the break in the song = FIFA's super-slow-mo of the Sweden strike: contact ON 14.18, the ball flies
                through the break, hits the net ON 18.51
  end        -> walking off: LEVEL WITH MESSI."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

M19, P2, ST = 'fifaworldcup_7658814821957111062', 'fifaworldcup_7668397627783826710', 'fifaworldcup_7652164117159021846'
CREW = 'fifaworldcup_7654394854063213826'
M21, PEN, SWE = 'foxsports_7663995315489361182', 'foxsports_7658806846983097630', 'foxsports_7657309363220008222'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
PLAN = [
    sh(0.00, M21, 10.40),           # his face
    sh(1.81, PEN, 2.63, cx=0.3),    # the penalty: run-up, contact, NET ON THE DROP 4.98
    sh(5.71, M19, 1.89),            # behind the goal: net ON 6.42, he runs at the camera
    sh(7.84, SWE, 10.92),           # laughing
    sh(8.53, PEN, 7.40),            # he turns away to celebrate
    sh(9.98, SWE, 12.30),           # the scream
    sh(10.39, M19, 7.90),           # arms up to the fans
    sh(11.36, ST, 11.80),           # with Deschamps
    sh(12.86, SWE, 5.00),           # the team
    sh(13.49, P2, 9.03),            # super-slow-mo: contact ON 14.18 ... net ON 18.51
    sh(18.51, ST, 5.70),            # the scream, close
    sh(19.83, CREW, 0.20),          # the team
    sh(21.27, M19, 11.60, jump=True),   # walking to the fans
    sh(22.65, CREW, 22.00),         # walking off - the end
]
END = 24.78
TEXT = [(22.85, END, 'LEVEL WITH|MESSI.')]

CFG = dict(
    name='AI', layout='full',
    active={M21 + '.mp4': (0, 1360), PEN + '.mp4': (0, 1370), SWE + '.mp4': (0, 1360)},
    srcdir=os.path.join(ROOT, 'src_mbappe'), tmp=os.path.join(ROOT, 'tmp_ai'),
    song=os.path.join(ROOT, 'songs', 'mbappe_violento.mp3'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_AI_mbappe.mp4'), end=END, plan=PLAN, pad=0.08,
    swing=set(), drop=set(), punch=set(), cut_flash=False, warm=0.0, sat=1.04, grain=0.0, vig=0.2,
    fx={}, text=TEXT, text_cy=1500, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
