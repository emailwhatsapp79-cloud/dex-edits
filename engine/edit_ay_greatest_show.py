"""AY - 'the greatest show' (sound #67, ref M5 + M6): 2026 season LYRIC edit, HORIZONTAL 1280x720 at native size
(formula1.com race highlights, no crop, no upscale). One sung word per shot; only shots without the timing tower.
Arc: night grid -> starts -> onboards -> chaos -> MOMENT -> champagne -> AFTER (donuts)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

D = os.path.join(os.environ.get('SCRATCH', '/tmp'), 'dl_gs')
SG, MC, MZ, NL, AT, BK = (os.path.join(D, f + '.mp4') for f in ('singapore', 'monaco', 'monza', 'dutch', 'austria', 'baku'))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets'))
CFG = dict(
    song=os.path.join(ASSETS, 'songs', '67_the_greatest_show_f1_alee_zecca.mp3'), off=0.0, end=16.30, size=(1280, 720),
    font=os.path.join(wideedit.ROOT, 'fonts', 'Anton.ttf'), fs=112,
    shots=[
        (0.00, SG, 2.00, 'ENRAGED'),     # night grid, Singapore
        (0.68, MC, 1.00, 'BONES'),       # Monaco start
        (1.58, MZ, 13.00, 'ACHE'),       # Monza T1 from above
        (2.90, NL, 1.50, 'IGNORE'),      # Zandvoort start
        (3.82, MC, 19.50, 'BREATH'),     # Monaco harbour aerial
        (4.62, SG, 60.00, 'STEALING'),   # Singapore onboard
        (5.40, MC, 70.00, 'MIND'),       # Monaco onboard
        (6.94, BK, 16.00, 'REAL'),       # Baku start aerial
        (7.76, BK, 30.00, 'LEFT'),
        (8.08, MZ, 34.00, 'BEHIND'),     # Monza, the field strung out
        (9.76, NL, 72.00, 'FIGHT'),      # Zandvoort onboard in the smoke
        (10.96, AT, 22.00, 'COMING'),    # Austria start aerial
        (11.62, MC, 84.00, 'RUNNING'),   # Monaco onboard
        (12.10, AT, 6.00, 'NATURE'),     # Austria T1
        (13.40, SG, 14.20, 'ONLY'),      # Singapore T1 aerial
        (14.00, MC, 484.50, 'MOMENT'),   # Antonelli, Monaco winner
        (14.58, AT, 474.00, ''),         # confetti (burst)
        (14.92, MC, 481.00, ''),         # champagne (burst)
        (15.34, NL, 393.50, 'AFTER'),    # Zandvoort donuts
    ])

if __name__ == '__main__':
    wideedit.run(CFG, 'ay_greatest_show', sys.argv)
