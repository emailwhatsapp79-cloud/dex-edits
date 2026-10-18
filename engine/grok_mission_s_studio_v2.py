"""CAR v2 - Porsche Mission S, studio only. One car, one place.
The pier film also contains the 550 Spyder, the launch crowd and the Brooklyn Bridge.
Those are not in this cut. Hook (rear, the wheel in frame) -> light bar, wheel, cockpit,
gauges, gear, the Mission S badge, the engine deck -> the hero rear. Refs N7 / N9 / N12.
HORIZONTAL 1920x1080, a downscale of the official 4K 25 fps newsroom film. No crop, no upscale.
Song #91, instrumental (N12 used the same sound with no lyric line)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import wideedit

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.path.join(S, 'dexsrc', 'mission_s.mp4')
ASSETS = os.environ.get('DEX_ASSETS', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets'))
# edit t is the frame the cut lands on (never more than one frame off the hit).
# Each source span sits inside one studio take. Takes used, in order:
# 59.88-63.28 rear, 54.84-57.88 lamp, 66.92-67.88 wheel, 63.28-66.92 cockpit,
# 71.40-77.20 gauges, 77.20-78.88 gear, 78.88-80.64 badge, 80.64-83.24 deck, 87.84-90.72 hero.
SHOTS = [
    (0.000, 60.12, 'MISSION S'),
    (3.000, 55.20, ''),
    (5.333, 67.02, ''),
    (6.200, 63.80, ''),
    (8.200, 72.25, ''),
    (10.033, 77.42, ''),
    (11.133, 79.15, ''),
    (12.500, 81.15, ''),
    (14.400, 88.20, ''),
]
CFG = dict(
    song=os.path.join(ASSETS, 'songs', '91_porsche_911_gt3_cup_sav_edits001.mp3'),
    off=0.0, end=16.500, size=(1920, 1080),
    font=os.path.join(wideedit.ROOT, 'fonts', 'Anton.ttf'), fs=132,
    shots=[(t, SRC, st, w) for t, st, w in SHOTS])

if __name__ == '__main__':
    wideedit.run(CFG, 'grok_mission_s_studio_v2', sys.argv)
