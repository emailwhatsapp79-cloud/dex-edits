"""CM - Las Vegas 2023: Max vs Leclerc into turn one, and the penalty (Fri 20 Nov 08:00 - Vegas qualifying is that night).
Story-first, three commentary runs: "It is showtime!... the top two go off the road!", Leclerc's radio ("he wasn't in front
of the apex and he pushed me wide, so he needs to give that position back") and the verdict ("Max Verstappen is given the
five second penalty for forcing another driver off the track"), B&W freeze. ~47 s, square in 1080x1920, 25 fps.
Song: Flashing Lights under the voice.
Sources: F1 'Race Highlights | 2023 Las Vegas Grand Prix' (Q9qSwDxF6YI); words bra/vegas23.json.
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cm_vegas23_turn_one.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('Q9qSwDxF6YI'), 'crop=1080:1080:420:0')}
FIX = {'CHECO': 'CHECO', 'LIGHT': 'LIGHTS'}
LINES = {'WITH CHARLES-ECLAIR CASSIE': 'WITH CHARLES LECLERC', 'INITIALLY FROM CHARLES-ECLAIR BUT HE GLANCES': 'INITIALLY FROM CHARLES LECLERC,',
         'IN THE MIRROR,': 'BUT HE GLANCES IN THE MIRROR,'}
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
    return [(t, LINES.get(x, x)) for t, x in out if LINES.get(x, x)]


CFG = dict(name='vegas23_turn_one', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'flashing_lights_kanye.mp3'),
           song_in=21.0, title='LAS VEGAS 2023|TURN ONE', banner_in=0.6,
           segments=[dict(type='voice', k='v', a=0.0, b=25.9, words=lines(0.0, 25.9)),
                     dict(type='voice', k='v', a=39.3, b=55.4, words=lines(39.3, 55.4)),
                     dict(type='voice', k='v', a=102.6, b=108.2, words=lines(102.6, 108.2)),
                     dict(type='end', k='v', at=106.0, dur=2.0, text='5-SECOND PENALTY.')])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cm_vegas23_turn_one_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
