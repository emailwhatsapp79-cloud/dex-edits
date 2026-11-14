"""CJ - Las Vegas 2024: Mercedes one-two, Russell from pole (Wed 18 Nov 18:00). Story-first, two commentary runs: Hamilton
flying through ("look at the speed... it will shake out to be a Mercedes one-two... no contest between the two greats")
and the finish ("out of the penultimate corner, he's left the entire field behind... George Russell wins the Las Vegas
Grand Prix... second place for Lewis Hamilton"), B&W freeze. ~44 s, square in 1080x1920, 25 fps. Song: Montagem Kali
(slowed) under the voice.
Sources: F1 'Race Highlights | 2024 Las Vegas Grand Prix' (sNd1-1GjMDY); words bra/vegas24.json.
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cj_mercedes_one_two_vegas24.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('sNd1-1GjMDY'), 'crop=1080:1080:420:0')}
FIX = {'LAPFORD': 'LAPPED,'}
# None = no caption: the radio line after 'my god' is unclear - never put words in a driver's mouth
LINES = {'A MERCEDES ONE-TWO. NO': 'A MERCEDES ONE-TWO.', 'CONTEST BETWEEN THE TWO GREATS': 'NO CONTEST BETWEEN THE TWO GREATS'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT',
        'THAT', 'BY', 'THIS', 'WHO', 'HIS', 'WE', "WE'VE", 'TWO'}


def lines(a, b):
    """1-3 word caption lines from the whisper words between a and b (new line at punctuation or after 3 words)."""
    W = [w for seg in json.load(open(os.path.join(S, 'bra', 'vegas24.json'))) for w in seg['w']]
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


CFG = dict(name='mercedes_one_two_vegas24', files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '05_montagem_kali_slowed.mp3'),
           song_in=0.0, title='VEGAS 2024|MERCEDES ONE-TWO', banner_in=0.6,
           segments=[dict(type='voice', k='v', a=280.1, b=297.6, words=lines(280.1, 297.6)),
                     dict(type='voice', k='v', a=392.5, b=417.4, words=lines(392.5, 417.4)),
                     dict(type='end', k='v', at=409.5, dur=2.0, text='MERCEDES 1-2.')])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cj_mercedes_one_two_vegas24_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
