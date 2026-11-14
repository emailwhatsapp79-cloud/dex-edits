"""CF - NASCAR 2026 Championship, Homestead-Miami (Tue 17 Nov 12:00; first NASCAR edit). Story-first, two commentary runs:
the last-lap fight ("Blaney tries to go low and Reddick blocks... Ryan Blaney sweeps right around the outside with one lap
to go") and the finish ("Ryan Blaney victorious... Kyle Larson is a three-time NASCAR Cup Series champion... generational
talents"), Larson's burnout, B&W freeze. ~52.5 s, square in 1080x1920, 30 fps. Source is 720p (downloaded at 720p on a slow
hotspot), crop 720x720 scaled 1.5x. Song: Bow Bow Bow (Zeddy Will - Trend 48, on TikTok + YouTube) under the voice.
Sources: NASCAR 'Cup Series Highlights | 2026 Championship at Homestead-Miami' (WsIlcxfpzAM); words bra/nascar26.json.
Usage: SRC=<sources folder> SCRATCH=<work dir> DEX_FPS=30 python3 edit_cf_nascar_championship.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('WsIlcxfpzAM'), 'crop=720:720:280:0,scale=1080:1080:flags=lanczos')}
FIX = {'BRIAN': 'RYAN'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT',
        'THAT', 'BY', 'THIS', 'WHO', 'HIS', 'WE', "WE'VE", 'TWO'}


def lines(a, b):
    """1-3 word caption lines from the whisper words between a and b (new line at punctuation or after 3 words)."""
    W = [w for seg in json.load(open(os.path.join(S, 'bra', 'nascar26.json'))) for w in seg['w']]
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


CFG = dict(name='nascar_championship', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'bow_bow_bow_zeddy_will.mp3'),
           song_in=0.0, title='NASCAR 2026|THE CHAMPIONSHIP', banner_in=0.6,
           segments=[dict(type='voice', k='v', a=1470.8, b=1488.6, words=lines(1470.8, 1488.6)),
                     dict(type='voice', k='v', a=1518.6, b=1551.3, words=lines(1518.6, 1551.3)),
                     dict(type='end', k='v', at=1546.5, dur=2.0, text='THREE-TIME CHAMPION.')])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 30))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cf_nascar_championship_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
