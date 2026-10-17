"""AZ - 'just keep watching' Austin (sound #72, ref M6/M7 - Desmond: re-use this song): US GP race-week hype,
HORIZONTAL 1280x720 native (2025 Austin highlights, formula1.com). One lyric word per shot, no timing-tower shots.
Times below are SONG time; the edit starts at OFF."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

D = os.path.join(os.environ.get('SCRATCH', '/tmp'), 'dl_gs')
R, SP, ST, W = (os.path.join(D, f'austin_{f}.mp4') for f in ('race', 'sprint', 'starts', 'win'))
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets'))
OFF, END = 0.30, 18.70
SHOTS = [
    (0.30, R, 54.00, 'AUSTIN.'),     # the esses and the stands from above
    (0.90, SP, 2.00, 'ONE BY ONE'),  # the grid
    (1.82, ST, 0.60, 'TWIST'),       # onboard, lights out
    (3.68, R, 21.00, 'START'),       # race start, wide
    (4.40, SP, 11.00, 'TRACK'),      # turn 1 from above
    (5.56, R, 38.40, "WATCHIN'"),
    (6.46, ST, 36.40, 'MY BACK'),    # onboard in the pack
    (7.40, R, 27.50, 'KILL'),        # turn 1 chaos
    (8.32, SP, 191.00, 'BURN'),      # Ferrari onboard
    (9.46, R, 9.00, 'JUST'),         # turn 1 hill
    (9.84, SP, 47.40, 'KEEP'),       # past the tower
    (10.40, W, 7.00, "WATCHIN'"),    # Verstappen wins, team at the fence
    (11.48, ST, 12.40, 'MOVE'),
    (11.98, ST, 22.40, 'BACK'),
    (12.92, SP, 196.60, ''),
    (13.30, R, 87.00, 'HATE'),       # Williams onboard
    (14.82, R, 34.60, 'KILL'),
    (15.46, SP, 26.00, 'NIGHT'),
    (16.34, ST, 15.62, 'BURN'),      # Ferrari onboard
    (17.00, R, 42.00, 'KEEP'),
    (17.26, SP, 421.20, "WATCHIN'"), # Max, fist up
]
CFG = dict(song=os.path.join(ASSETS, 'songs', '72_f1_60s_edit_cs_ttzz.mp3'), off=OFF, end=END - OFF, size=(1280, 720),
           font=os.path.join(wideedit.ROOT, 'fonts', 'Anton.ttf'), fs=112,
           shots=[(t - OFF, src, st, w) for t, src, st, w in SHOTS])

if __name__ == '__main__':
    wideedit.run(CFG, 'az_austin_keep_watching', sys.argv)
