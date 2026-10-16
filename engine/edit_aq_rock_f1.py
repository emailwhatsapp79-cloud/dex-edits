"""Edit AQ - F1, the whole grid - format "LYRIC EDIT" (Batch I1 'We Will Rock You x F1', posted for the US GP). Each sung
word stamped big on its own shot, the picture = the word:
  BUDDY / BOY -> 20-year-old Kimi (interview smile, lifted on the podium)   BIG NOISE -> the start, the pack into T1
  PLAYING IN THE STREET -> Singapore street circuit at night   GONNA BE A BIG MAN SOMEDAY -> Lewis with a photo of
  himself as a kid -> Lewis in red   GOT MUD ON YOUR FACE -> GP sprayed with champagne   BIG DISGRACE -> "off the road
  goes Hamilton"   KICKING YOUR CAN -> Antonelli past Hamilton, "yes you CAN, Ollie Bearman"   ALL OVER THE PLACE ->
  Leclerc's pass, P1 board   SING IT -> the Dutch fans   WE WILL, WE WILL, ROCK YOU -> Leclerc, Ferrari, Max on top
  end -> AUSTIN. OCT 23-25 (posted Oct 20, race week).
Sound: library #52 (the TikTok sound itself). Layout 'tall' (3:4) so every clip's burned caption is cropped off; 720p
broadcast shots as a sharp 16:9 window."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

HELM, HTL, SPR, WIN = 'f1_7694673917193063682', 'f1_7694957322287713558', 'f1_7694997103784791298', 'f1_7695423602358881558'
POD, GP, PF, FER = 'f1_7695428044822957334', 'f1_7695768714691595542', 'f1_7694989403172719894', 'f1_7695063981081283862'
LEC, P1, OUT, KPOD = 'f1_7695435478115388694', 'f1_7694669963944103190', 'f1_7695081243175554326', 'f1_7643587480364551446'
KI, HAM, REV = 'f1_7695413467167100182', 'mercedesamgf1_7427481467107675425', 'f1_7694610596188278038'
sh = lambda t, f, src, cx=0.5, **k: dict(t=t, file=f + '.mp4', src=src, cx=cx, mode='real', **k)
win = lambda t, src, **k: sh(t, 'H', src, layout='window', **k)
PLAN = [
    sh(0.00, P1, 0.40),             # the car rolls in
    dict(sh(1.72, HTL, 8.60), jump=True),   # the grandstand
    win(2.39, 4.00),                # the red lights
    dict(win(3.16, 6.90), jump=True),   # lights out
    win(3.51, 13.95),               # turn 1 from above
    sh(5.15, HTL, 7.00),            # YOU'RE
    sh(6.40, KI, 5.30),             # BUDDY - Kimi
    sh(6.86, KPOD, 3.00),           # BOY - lifted on the podium
    win(7.62, 11.50),               # BIG
    sh(7.80, HTL, 3.60),            # NOISE
    sh(8.24, SPR, 5.30),            # PLAYING
    win(9.02, 330.50),              # STREET
    sh(9.70, HAM, 3.00),            # GONNA BE - Lewis with a photo of himself as a kid
    dict(sh(10.18, HAM, 7.90), jump=True),   # BIG
    sh(10.42, FER, 2.00),           # MAN - Lewis in red
    sh(10.80, REV, 10.00),          # SOMEDAY
    sh(11.64, GP, 8.00),            # GOT
    dict(sh(11.94, GP, 12.70), jump=True),   # MUD - the champagne bottle
    dict(sh(12.72, GP, 13.70), jump=True),   # FACE - Max, soaked, smiling (WIN 25 had a burned radio caption)
    win(13.48, 296.40),             # BIG - off the road goes Hamilton
    dict(win(13.80, 297.30), jump=True),     # DISGRACE
    win(14.96, 324.40),             # KICKING - Antonelli past Hamilton
    win(15.56, 117.50),             # CAN - "yes you can, Ollie Bearman"
    win(16.42, 246.00),             # OVER - Leclerc's pass
    sh(16.98, PF, 3.00),            # PLACE - the P1 board
    sh(17.60, SPR, 7.00),           # SING IT - the Dutch fans
    sh(17.98, LEC, 6.00),           # WE
    sh(18.40, FER, 4.60),           # WILL
    sh(19.42, OUT, 3.00),           # WE - Max back on top
    sh(19.84, P1, 9.00),            # WILL
    sh(20.54, POD, 4.50),           # ROCK
    sh(21.12, GP, 6.00),            # YOU - Max, close
    sh(21.58, POD, 10.50),          # AUSTIN.
]
END = 23.55
# Desmond, Oct 16: start the song later - cut the 3 s intro, open on LIGHTS OUT on the 3.14 stomp
OFF = 3.14
PLAN = [dict(p, t=max(0.0, round(p['t'] - OFF, 3))) for p in PLAN if p['t'] >= 3.16]; PLAN[0]['t'] = 0.0
END = round(END - OFF, 2)
W_ = [(5.68, "YOU'RE"), (6.40, 'BUDDY'), (6.86, 'BOY'), (7.62, 'BIG'), (7.80, 'NOISE'), (8.24, 'PLAYING'), (9.02, 'STREET'),
      (9.70, 'GONNA BE'), (10.18, 'BIG'), (10.42, 'MAN'), (10.80, 'SOMEDAY'), (11.64, 'GOT'), (11.94, 'MUD'), (12.72, 'FACE'),
      (13.48, 'BIG'), (13.80, 'DISGRACE'), (14.96, 'KICKING'), (15.56, 'CAN'), (16.42, 'OVER'), (16.98, 'PLACE'),
      (17.60, 'SING IT'), (17.98, 'WE'), (18.40, 'WILL'), (19.42, 'WE'), (19.84, 'WILL'), (20.54, 'ROCK'), (21.12, 'YOU'),
      (21.75, 'AUSTIN.|OCT 23-25')]
W_ = [(round(t - OFF, 2), w) for t, w in W_]
TEXT = [(t, (W_[i + 1][0] - 0.02) if i + 1 < len(W_) else END, w) for i, (t, w) in enumerate(W_)]

CFG = dict(
    name='AQ', layout='tall', win_y=656,
    active={HELM + '.mp4': (480, 1440), HTL + '.mp4': (480, 1440), SPR + '.mp4': (570, 1350), WIN + '.mp4': (0, 1440),
            POD + '.mp4': (0, 1320), GP + '.mp4': (0, 1400), PF + '.mp4': (0, 1380), FER + '.mp4': (0, 1400),
            LEC + '.mp4': (0, 1430), P1 + '.mp4': (0, 1390), OUT + '.mp4': (0, 1400), KPOD + '.mp4': (0, 1440),
            KI + '.mp4': (0, 1420), HAM + '.mp4': (0, 1430), REV + '.mp4': (0, 1420)},
    srcdir=os.path.join(ROOT, 'src_rock'), tmp=os.path.join(ROOT, 'tmp_aq'),
    song=os.path.join(ROOT, 'songs', 'rock_f1.mp3'), song_offset=OFF,
    out=os.path.join(ROOT, 'out', 'edit_AQ_rock_f1.mp4'), end=END, plan=PLAN, pad=0.06,
    swing=set(), drop=set(), punch=set(), cut_flash=True, warm=0.0, sat=1.06, grain=0.0, vig=0.3, bg_dim=0.4,
    fx={}, text=TEXT, text_cy=960, crf=12,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
