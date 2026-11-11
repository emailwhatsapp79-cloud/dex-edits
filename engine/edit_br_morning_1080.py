"""BR - the morning (08:00 Lagos) posts of Thu 12 / Fri 13 REDONE in the bright [4K] look from the 1080p FORMULA 1 YouTube
uploads (Desmond, Nov 11). BP's morning edits (engine/edit_bp_morning_week.py) used separate 720p formula1.com clips; the same
moments are in the 1080p race highlights (lkb5kqDJYXk), cropped to 4:3 at native 1440x1080 (no timing tower, no upscale),
50 fps, grade 'bright', solid captions.
  piastri  Thu 12  "Oh, that's instant. Instant overtake for Max Verstappen, not hanging around" -> INSTANT. (#161)
Usage: SRC=<folder with the mp4s> SCRATCH=<dir> python3 edit_br_morning_1080.py piastri"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
song = lambda n: glob.glob(os.path.join(SONGS, n + '_*.mp3'))[0]
src = lambda vid: glob.glob(os.path.join(SRC, f'*{vid}*.mp4'))[0]
BASE = dict(size=(1440, 1080), files={'r': src('lkb5kqDJYXk')}, cap=(70, 0.8), shake=True, crop='crop=1440:1080:330:0',
            crop_keys=['r'], grade='bright', fade=2.6, fade_curve='hsin', vfade=1.2, hold=1.8)
CFG = {
    'piastri': dict(song=song('161'), drop=7.0, beat=60 / 136, big=('INSTANT.', 2), ttail=0.08,
        # cold open: the call over the close three-wide (Alpine / McLaren / Red Bull), then the pass's own wide shot
        talk=[('r', 73.20, 75.50, 0, 'r', 104.45), ('r', 75.50, 77.50, 0)],
        words=[('r', 73.26, "|OH, THAT'S INSTANT."), ('r', 74.30, '|INSTANT OVERTAKE'), ('r', 75.48, '|FOR MAX VERSTAPPEN,'),
               ('r', 76.50, '|NOT HANGING AROUND.')],
        after=[(2, 'r', 73.00, 73.95), (2, 'r', 74.00, 74.95), (2, 'r', 89.00, 89.95), (2, 'r', 83.60, 85.40),
               (2, 'r', 100.00, 102.40), (4, 'r', 94.50, 99.90, 0.6)]),
}

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 50))
    for name in sys.argv[1:]:
        out, drop, end = linedrop.render(dict(BASE, **CFG[name], name=name, fps=fps), S, os.path.join(S, 'out', f'bq_{name}_{fps}.mp4'))
        print(out, f'drop {drop:.2f} end {end:.2f}', flush=True)
