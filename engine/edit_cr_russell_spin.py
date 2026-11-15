"""CR - Brazil 2026: Russell loses it warming the tyres (Mon 16 Nov 08:00; replaces the old horizontal Russell v7). Nov 15
style: commentary run ("Round, round goes Russell... a nightmare position... loses the car trying to warm up the tyres...
he scrapes down the barrier"), Russell's own words after the race ("probably just took too much risk, because I was
seeing an opportunity to go for the win"), action outro on the beat, DEX EDITS end card. ~29 s, square in 1080x1920,
25 fps, song under the voice the whole way.
Sources: F1 'Race Highlights | 2026 Sao Paulo GP' (lkb5kqDJYXk) + 'Drivers React After The Race' (jpwFNmUzWn8).
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cr_russell_spin.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'r': (src('lkb5kqDJYXk'), 'crop=1080:1080:420:0'), 'i': (src('jpwFNmUzWn8'), 'crop=1080:1080:420:0')}
FIX = {}
# whisper garbage in this stretch: no caption rather than words he never said
DROP = [(184.6, 187.5), (190.4, 191.9)]          # misheard stretches (source seconds)
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT',
        'THAT', 'BY', 'THIS', 'WHO', 'HIS', 'WE', "WE'VE", 'TWO'}


def lines(a, b):
    """1-3 word caption lines from the whisper words between a and b (new line at punctuation or after 3 words)."""
    W = [w for seg in json.load(open(os.path.join(S, 'bra', 'race.json'))) for w in seg['w']]
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
    return [(t, x) for t, x in out if not any(a0 <= t < b0 for a0, b0 in DROP)]


RUS = [(139.50, 'PROBABLY JUST TOOK'), (140.56, 'TOO MUCH RISK,'), (141.08, 'BECAUSE I WAS SEEING'), (142.30, 'AN OPPORTUNITY'),
       (142.78, 'TO GO FOR THE WIN.')]
CFG = dict(name='russell_spin', files=FILES, song=os.path.join(ASSETS, 'songs', '167_som_original_guilherme.mp3'),
           song_in=0.0, title='GEORGE RUSSELL|ONE MOMENT', banner_in=0.6,
           segments=[dict(type='voice', k='r', a=179.0, b=196.7, words=lines(179.0, 196.7)),
                     dict(type='voice', k='i', a=139.45, b=145.4, words=RUS),
                     dict(type='outro', shots=[('r', 160.0), ('r', 199.5), ('r', 162.5), ('r', 188.5)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cr_russell_spin_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
