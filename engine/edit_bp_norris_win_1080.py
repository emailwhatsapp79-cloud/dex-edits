"""BP - F1: NORRIS WINS IN BRAZIL, rebuilt in the 4K LOOK from 1080p sources (Nov 11 2026). Same story and sound as BM
(#162 Funk Loading, line -> drop "P1."), now from the FORMULA 1 YouTube uploads (1920x1080, same cut and timecodes as the
formula1.com 720p file BM used), cropped to 4:3 at native 1440x1080 (removes the timing tower, no upscale), 'cine' grade,
CAS sharpen, solid bold italic captions. Cold open: the commentary call over his slow-mo helmet walk. Outro: Norris' own words
(Drivers React After The Race) over his face, then the podium.
Sources (dex-edits-assets release footage-2026-11-sao-paulo, FOOTAGE.md): lkb5kqDJYXk race highlights, jpwFNmUzWn8 reactions.
Usage: SRC=<folder with the two mp4s> python3 edit_bp_norris_win_1080.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import linedrop

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
SONGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets', 'songs')
src = lambda vid: glob.glob(os.path.join(SRC, f'*{vid}*.mp4'))[0]
CFG = dict(name='norriswin1080', song=glob.glob(os.path.join(SONGS, '162_*.mp3'))[0], drop=8.0, beat=60 / 123, shake=True,
    size=(1440, 1080), crop='crop=1440:1080:330:0', crop_keys=['r', 'ni'], cap=(70, 0.8), big_size=0.2, grade='cine',
    files={'r': src('lkb5kqDJYXk'), 'ni': src('jpwFNmUzWn8')},
    talk=[('r', 419.62, 423.55, 0, 'ni', 19.00), ('r', 424.05, 426.58, 0)],   # cold open: the call over his slow-mo helmet walk (sharpest shot first)
    words=[('r', 419.67, '|LANDO NORRIS'), ('r', 421.25, '|WILL GO BACK TO BACK'), ('r', 422.87, 'IN BRAZIL.'),
           ('r', 424.11, '|IN THE WET,'), ('r', 425.03, 'IN THE DRY.'), ('r', 426.29, "|HE'S")],
    big=('P1.', 2),
    after=[(2, 'r', 2.00, 6.84), (2, 'r', 18.00, 22.24), (2, 'r', 228.60, 230.04), (2, 'r', 149.00, 164.00),
           (2, 'r', 438.10, 442.96), (2, 'r', 410.00, 413.36)], fade=1.2,
    outro=('ni', 34.40, 42.30, [('ni', 34.40, '|THEREFORE PROBABLY'), ('ni', 34.96, '|ONE OF THE BEST WINS'), ('ni', 35.58, "I'VE HAD."),
                                 ('ni', 37.80, '|ENJOYABLE,'), ('ni', 38.74, '|A CONSTANT CHALLENGE,'),
                                 ('ni', 40.44, '|BUT PROBABLY ONE OF'), ('ni', 41.36, '|THE MOST REWARDING.')],
           [('ni', 34.40, 3.4), ('r', 459.50, 99)]))

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    out, drop, end = linedrop.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bp_norriswin1080_{fps}.mp4'))
    print(out, f'drop {drop:.2f} end {end:.2f}')
