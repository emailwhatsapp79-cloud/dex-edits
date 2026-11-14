"""CG - Las Vegas 2025: Max wins, Norris limps home... then both McLarens are disqualified (Tue 17 Nov 18:00). Story-first,
two commentary runs: Norris nursing a problem, told to lift and coast to the flag; the last corner, "Max Verstappen wins
the Las Vegas Grand Prix... Lando Norris hangs on". Ending stamp = what happened hours later (fact: Norris and Piastri
were disqualified for excessive plank wear). ~58 s, square in 1080x1920, 25 fps. Song: Flashing Lights under the voice.
Sources: F1 'Race Highlights | 2025 Las Vegas Grand Prix' (uQc-pW3QLuI); words bra/vegas25.json.
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cg_vegas25_dsq.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('uQc-pW3QLuI'), 'crop=1080:1080:420:0')}
FIX = {'ESTAPPEN': 'VERSTAPPEN', 'ESTAPPEN,': 'VERSTAPPEN,'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT',
        'THAT', 'BY', 'THIS', 'WHO', 'HIS', 'WE', "WE'VE", 'TWO'}


def lines(a, b):
    """1-3 word caption lines from the whisper words between a and b (new line at punctuation or after 3 words)."""
    # whisper gave no punctuation here: also end a line at the end of each whisper segment (= sentence)
    W = [(*w, i == len(seg['w']) - 1) for seg in json.load(open(os.path.join(S, 'bra', 'vegas25.json'))) for i, w in enumerate(seg['w'])]
    out, cur = [], None
    for s, e, w, last in W:
        if not (a <= s <= b - 0.1): continue
        w = FIX.get(w.upper(), w.upper())
        if w.startswith('-') and cur: cur[1][-1] += w; continue          # whisper splits 'wheel-to-wheel' into parts
        if w.startswith('-') and out: t0, x = out.pop(); cur = [t0, x.split()]; cur[1][-1] += w; continue
        if cur is None: cur = [s, [w]]
        else: cur[1].append(w)
        if (len(cur[1]) >= 3 and w.strip('.,?!') not in HANG) or w[-1] in '.,?!' or last:
            out.append((cur[0], ' '.join(cur[1]))); cur = None
    if cur: out.append((cur[0], ' '.join(cur[1])))
    return out


CFG = dict(name='vegas25_dsq', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'flashing_lights_kanye.mp3'),
           song_in=21.0, title='LAS VEGAS 2025|THE TWIST', banner_in=0.6,
           segments=[dict(type='voice', k='v', a=324.4, b=349.0, words=lines(324.4, 349.0)),
                     dict(type='voice', k='v', a=379.2, b=410.25, words=lines(379.2, 410.25)),
                     dict(type='end', k='v', at=436.5, dur=2.6, text='BOTH McLARENS: DISQUALIFIED.')])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cg_vegas25_dsq_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
