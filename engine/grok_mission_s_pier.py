"""CAR - Porsche Mission S, one car, one place (the Queens pier, Manhattan behind it).
Arrival -> details -> the hero front. Refs N7 / N9 / N12. HORIZONTAL 1920x1080, a downscale of the
official 4K 25 fps newsroom film (newstv 341406). No crop, no upscale. Song #91 (LIBRARY lists no
lyric line; the N12 GT3 Cup edit used it as instrumental). Cuts on the beat grid. Title on the hook only.
Soft defocus takes (src ~46s, ~51s, ~55s) are not used."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.path.join(S, 'dexsrc', 'mission_s.mp4')
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets'))
# edit t, source t, word. Each span sits inside one detected take and stays sharp.
SHOTS = [
    (0.00, 14.55, 'MISSION S'),   # hook: sharp front three-quarter
    (1.86, 11.95, ''),            # the pier, the skyline behind the car
    (3.51, 38.70, ''),            # rear three-quarter
    (5.33, 63.45, ''),            # headlight
    (7.28, 69.15, ''),            # the nose
    (8.67, 58.20, ''),            # the side
    (10.033, 80.80, ''),          # the rear — beat 10.049, one frame early
    (11.59, 61.05, ''),           # along the flank
    (13.24, 74.90, ''),           # the wheel and the side
    (15.12, 88.10, ''),           # the pier and the car
    (16.51, 92.50, ''),           # hero front, hold to the fade
]
CFG = dict(
    song=os.path.join(ASSETS, 'songs', '91_porsche_911_gt3_cup_sav_edits001.mp3'),
    off=0.0, end=18.00, size=(1920, 1080),
    font=os.path.join(wideedit.ROOT, 'fonts', 'Anton.ttf'), fs=132,
    shots=[(t, SRC, st, w) for t, st, w in SHOTS])

if __name__ == '__main__':
    wideedit.run(CFG, 'grok_mission_s_pier', sys.argv)
