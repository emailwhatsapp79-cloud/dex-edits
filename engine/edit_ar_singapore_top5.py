"""Edit AR - F1, the whole grid: "SINGAPORE GP / TOP 5" moves (DEX template COUNTDOWN, not a trailer). Hook: 1.9 s of #1
(the two Haas cars millimetres apart) with WAIT FOR #1., then #5 -> #1, each move with its OWN broadcast commentary
(picture = what is said):
  #5 Hadjar holds on at turn 8 ("...move up to 14th")    #4 Russell into P9 ("this time to the inside... takes P9")
  #3 Leclerc's peel to the inside for P2                  #2 Antonelli past Hamilton, "up to the podium places"
  #1 Bearman vs Ocon, Haas on Haas: "Surely you can't? Yes, you can, Oli Bearman. What a move."
Footage: formula1.com 2026 Singapore GP race highlights (1280x720 -> fitted to 1080 wide = a downscale, sharp)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import countdown
from cardedit import ROOT

H = os.path.join(ROOT, 'src_max_sg', 'H.mp4')
PIECES = [
    dict(file=H, a=113.80, b=115.70, rank=1, cap='', teaser=True),
    dict(file=H, a=173.85, b=182.15, rank=5, cap='HADJAR / HOLDS THE INSIDE'),
    dict(file=H, a=262.00, b=270.75, rank=4, cap='RUSSELL / INTO P9'),
    dict(file=H, a=244.90, b=252.95, rank=3, cap='LECLERC / TAKES P2'),
    dict(file=H, a=322.90, b=329.55, rank=2, cap='ANTONELLI / ONTO THE PODIUM'),
    dict(file=H, a=112.70, b=121.95, rank=1, cap='BEARMAN VS OCON / HAAS ON HAAS'),
]
OUT = os.path.join(ROOT, 'out', 'edit_AR_singapore_top5.mp4')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for n, lt in [(0, 0.6), (1, 0.3), (1, 4.0), (2, 0.5), (2, 6.0), (3, 0.4), (3, 4.5), (4, 0.4), (4, 4.0), (5, 0.4), (5, 6.5), (5, 8.9)]:
            countdown.still(PIECES, 'SINGAPORE GP', n, lt, os.path.join(ROOT, 'out', f'AR_{n}_{lt}.jpg'))
    else:
        countdown.render(PIECES, 'SINGAPORE GP', OUT, os.path.join(ROOT, 'tmp_ar'))
