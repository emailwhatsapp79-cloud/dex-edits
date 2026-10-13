"""Edit N - F1. Direction: "They said he was done. Back to back." Max Verstappen went winless all season, then won
Sepang (the Bahrain GP in Malaysia, Oct 4) and Singapore (Oct 11). Built like the "Formula Max" reference edit
(same sound): one long slow-motion shot for the intro (no cuts until the drop at 9.77 s), then every snare is a cut
with the reference's effects - white flash, photocopy frames, colour/black-and-white strobe, radial zoom blur.
Official formula1.com footage (720p) in the 4:5 card layout."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cardedit
from cardedit import ROOT

sh = lambda t, f, src, mode='real', cx=0.5, label='': dict(t=t, file=f + '.mp4', src=src, cx=cx, mode=mode, label=label)

PLAN = [
    sh(0.000, 'sgp_win', 8.40, 'hero', 0.45, 'MAX VERSTAPPEN'),   # intro: parc ferme, slow
    sh(4.893, 'sgp_onb', 6.00, 'hero', 0.50, 'MAX VERSTAPPEN'),   # his onboard, slow
    sh(7.589, 'sgp_pole', 0.10, 'slow', 0.45, 'MAX VERSTAPPEN'),  # the Red Bull at night, slow
    # drop - Sepang
    sh(9.770, 'bhr_win', 0.10, 'real', 0.55),       # the chequered flag
    sh(10.232, 'bhr_pole', 2.80, 'real', 0.50),     # the garage
    sh(10.687, 'bhr_restart', 17.30, 'real', 0.55),
    sh(11.300, 'bhr_recover', 13.95, 'real', 0.50),
    sh(11.615, 'bhr_restart', 24.00, 'real', 0.50), # past the Mercedes
    sh(12.226, 'bhr_recover', 34.05, 'real', 0.50),
    sh(12.700, 'bhr_pole', 0.05, 'real', 0.40),
    # Singapore
    sh(13.154, 'sgp_sprint', 0.10, 'real', 0.40),
    sh(13.754, 'sgp_start', 0.10, 'real', 0.50),
    sh(14.063, 'sgp_win', 0.10, 'real', 0.50),      # the flag
    sh(14.669, 'sgp_win', 23.88, 'real', 0.50),     # BIGGEST HIT: Max celebrates
    sh(15.133, 'sgp_start', 13.96, 'real', 0.50),
    sh(15.597, 'sgp_sprint', 3.40, 'real', 0.50),
    sh(16.199, 'bhr_recover', 39.45, 'real', 0.50),
    sh(16.516, 'bhr_recover', 23.05, 'real', 0.50),
    sh(17.124, 'sgp_sprint', 6.70, 'real', 0.50),   # the orange fans
    sh(17.591, 'sgp_start', 17.90, 'real', 0.50),
    sh(18.032, 'bhr_recover', 17.30, 'real', 0.50),
    sh(18.655, 'bhr_pole', 10.56, 'hero', 0.30),    # Max, helmet on - the last look
]
END = 19.4

CFG = dict(
    name='N', layout='card', srcdir=os.path.join(ROOT, 'src_max'), tmp=os.path.join(ROOT, 'tmp_n'),
    song=os.path.join(ROOT, 'songs', 'named', '23_formula_max_f1edits.wav'), song_offset=0.0,
    out=os.path.join(ROOT, 'out', 'edit_N_max.mp4'), end=END, plan=PLAN,
    swing={13}, drop={3, 13}, punch=set(range(3, 21)), warm=0.0, sat=1.1,
    fx={3: ('xerox',), 4: ('strobe',), 6: ('radial',), 8: ('bw',), 10: ('xerox',), 13: ('radial', 'xerox'),
        15: ('strobe',), 16: ('radial',), 18: ('bw',), 19: ('strobe',)},
    text=[(0.4, 4.6, 'NO WINS|ALL SEASON.'), (4.6, 9.77, 'THEY SAID|HE WAS DONE.'),
          (9.77, 11.30, 'SEPANG.|P1.'), (13.154, 14.669, 'SINGAPORE.|P1.'), (14.669, 16.516, 'BACK|TO BACK.'),
          (17.124, END, "HE'S BACK.")],
    text_cy=975,
)

if __name__ == '__main__':
    cardedit.run(CFG, sys.argv)
