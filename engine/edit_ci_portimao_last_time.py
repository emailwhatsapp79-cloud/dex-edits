"""CI - MotoGP: last time at Portimão (Wed 18 Nov 12:00; the race is back 20-22 Nov). Story-first, one commentary run over
the last laps of the 2025 Portuguese GP: Di Giannantonio forces it up the inside of Zarco, "absolutely brilliant
Bezzecchi... wins the Grand Prix of Portugal... from start to finish", Alex Márquez holds off Acosta for second, B&W
freeze on Bezzecchi standing on the pegs. ~43 s, square in 1080x1920, 25 fps. Song: Funk Único (slowed) under the voice.
Sources: MotoGP 'MotoGP HIGHLIGHTS 2025 Portuguese GP' (vP51RMuSUsk); words bra/portimao25.json.
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_ci_portimao_last_time.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('vP51RMuSUsk'), 'crop=1080:1080:420:0')}
FIX = {'BETSECHI': 'BEZZECCHI', 'BETSECHI.': 'BEZZECCHI.', 'PORTAMOUAS.': 'PORTIMÃO.', 'DIGIA': 'DIGGIA', 'AGURA': 'OGURA',
       'ANZARCO.': 'ZARCO.', 'DIGIA.': 'DIGGIA.', 'ANZARCO': 'ZARCO', 'JOE': 'JOHANN', 'QUATTARARO': 'QUARTARARO', 'MARQUEZ': 'MÁRQUEZ'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT',
        'THAT', 'BY', 'THIS', 'WHO', 'HIS', 'WE', "WE'VE", 'TWO'}


def lines(a, b):
    """1-3 word caption lines from the whisper words between a and b (new line at punctuation or after 3 words)."""
    W = [w for seg in json.load(open(os.path.join(S, 'bra', 'portimao25.json'))) for w in seg['w']]
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


CFG = dict(name='portimao_last_time', files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '13_funk_unico_super_slowed.mp3'),
           song_in=0.0, title='PORTIMÃO 2025|LIGHTS TO FLAG', banner_in=0.6,
           segments=[dict(type='voice', k='v', a=620.4, b=662.8, words=lines(620.4, 662.8)),
                     dict(type='end', k='v', at=664.5, dur=2.0, text='BACK THIS WEEKEND.')])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'ci_portimao_last_time_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
