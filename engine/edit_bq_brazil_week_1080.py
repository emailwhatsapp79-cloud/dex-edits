"""BQ - the rest of the Sao Paulo week (Thu 12 - Fri 13) REDONE in the bright [4K] look from the 1080p sources (Desmond,
Nov 11: "redo the remaining edits... make it well and good"). Same stories, words, songs and beats as BO
(engine/edit_bo_brazil_week.py) - the FORMULA 1 YouTube race highlights are the same cut with the same timecodes as the
formula1.com 720p file BO used - now cropped to 4:3 at native 1440x1080 (no timing tower, no upscale), 50 fps (the source's
own frame rate: smooth, no made-up frames), grade 'bright', solid captions.
The driver interviews come from "Drivers React After The Race" (jpwFNmUzWn8); OUTRO below maps each BO outro to its time
there. Sources: dex-edits-assets release footage-2026-11-sao-paulo (FOOTAGE.md).
Usage: SRC=<folder with the mp4s> SCRATCH=<dir with bra/race.json> python3 edit_bq_brazil_week_1080.py russell hulk ..."""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import linedrop
import edit_bo_brazil_week as bo

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
src = lambda vid: glob.glob(os.path.join(SRC, f'*{vid}*.mp4'))[0]
FILES = {'r': src('lkb5kqDJYXk'), 'ni': src('jpwFNmUzWn8')}
BASE = dict(size=(1440, 1080), files=FILES, cap=(70, 0.8), shake=True, crop='crop=1440:1080:330:0', crop_keys=['r', 'ni'],
            grade='bright')
# BO outro -> (interview start, end, words) in the reactions video; pics: BO's race shots, interview key renamed to 'ni'
OUTRO = {
    'russell': (139.45, 145.40, [('ni', 139.51, '|PROBABLY JUST TOOK'), ('ni', 141.43, 'TOO MUCH RISK,'), ('ni', 141.95, '|BECAUSE I WAS SEEING'),
                                 ('ni', 143.19, '|AN OPPORTUNITY'), ('ni', 143.65, '|TO GO FOR THE WIN.')]),
    'hulk': (308.95, 314.95, [('ni', 308.99, '|IT WAS A GOOD MOVE.'), ('ni', 309.67, '|SET HIM UP A BIT'), ('ni', 311.61, '|ON THE ENTRY FOR THE EXIT'),
                              ('ni', 312.97, '|WITH AN UNDERCUT.')]),
    # BO used a separate "new dad" interview; the reactions video has his race words instead - same story beat (patience -> P7)
    'leclerc': (263.85, 267.95, [('ni', 263.87, '|AT THE END,'), ('ni', 264.31, '|BY BEING PATIENT'), ('ni', 265.45, '|AND MAKING'),
                                 ('ni', 265.67, 'THE RIGHT CHOICE,'), ('ni', 266.95, '|WE ENDED UP P7.')]),
}


def race_words():
    """BO's words() reads bra/words.json {'race': [(s, e, w)]} - built here from the 1080p whisper transcript."""
    W = json.load(open(os.path.join(S, 'bra', 'race.json')))
    json.dump({'race': [w for seg in W for w in seg['w']], 'mercs': []}, open(bo.WJ, 'w'))


def cfg_for(name, fps):
    c = dict(bo.CFG[name]); c.pop('files', None)
    if 'outro' in c:
        if name not in OUTRO: raise SystemExit(f'{name}: interview not mapped yet')
        a, b, words = OUTRO[name]
        pics = [p if p[0] == 'r' else ('ni', a + (p[1] - c['outro'][1]), p[2]) for p in c['outro'][4]]
        c['outro'] = ('ni', a, b, words, pics)
    c = dict(BASE, **c, name=name, fps=fps)
    c['words'] = c.get('words') or bo.words(c['talk'])
    return c


if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 50))
    os.makedirs(os.path.dirname(bo.WJ), exist_ok=True); race_words()
    for name in sys.argv[1:]:
        out, drop, end = linedrop.render(cfg_for(name, fps), S, os.path.join(S, 'out', f'bq_{name}_{fps}.mp4'))
        print(out, f'drop {drop:.2f} end {end:.2f}', flush=True)
