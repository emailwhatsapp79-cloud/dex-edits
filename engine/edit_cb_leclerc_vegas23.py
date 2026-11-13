"""CB - Las Vegas 2023: Leclerc's last-chance move on Perez (gap-week build-up, Sun 15 Nov 12:00). Story-first: the whole
final fight in one unbroken commentary run - "Go Charles Leclerc at turn 12... unbelievably brave... this is the last
real corner... What a move, Charles Leclerc!... Max Verstappen wins the Las Vegas Grand Prix" - then a B&W freeze.
59.9 s (YouTube <= 60), square in 1080x1920, 25 fps, no grade. Song: Just Keep Watching (F1 cover, the 378K 'JUST KEEP
WATCHING X F1' sound) under the voice.
Sources: F1 'Race Highlights | 2023 Las Vegas Grand Prix' (Q9qSwDxF6YI); words from bra/vegas23.json (faster-whisper).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cb_leclerc_vegas23.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('Q9qSwDxF6YI'), 'crop=1080:1080:420:0')}
FIX = {'CHECO': 'CHECO', 'LIGHT': 'LIGHTS'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT',
        'THAT', 'BY', 'THIS', 'WHO', 'HIS', 'WE', "WE'VE", 'TWO'}


def lines(a, b):
    """1-3 word caption lines from the whisper words between a and b (new line at punctuation or after 3 words)."""
    W = [w for seg in json.load(open(os.path.join(S, 'bra', 'vegas23.json'))) for w in seg['w']]
    out, cur = [], None
    for s, e, w in W:
        if not (a <= s <= b - 0.1): continue
        w = FIX.get(w.upper(), w.upper())
        if w.startswith('-') and cur: cur[1][-1] += w; continue          # whisper splits 'wheel-to-wheel' into parts
        if w.startswith('-') and out: t0, x = out.pop(); cur = [t0, x.split()]; cur[1][-1] += w; continue
        if cur is None: cur = [s, [w]]
        else: cur[1].append(w)
        if (len(cur[1]) >= 3 and w.strip('.,?!') not in HANG) or w[-1] in '.,?!':
            out.append((cur[0], ' '.join(cur[1]))); cur = None
    if cur: out.append((cur[0], ' '.join(cur[1])))
    return out


CFG = dict(name='leclerc_vegas23', files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '22_just_keep_watching_f1_cover.mp3'),
           song_in=0.0, title='LECLERC|LAST CHANCE IN VEGAS', banner_in=0.6,
           segments=[dict(type='voice', k='v', a=413.2, b=471.35, words=lines(413.2, 471.35)),
                     dict(type='end', k='v', at=477.5, dur=1.7, text='WHAT A MOVE.')])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cb_leclerc_vegas23_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
