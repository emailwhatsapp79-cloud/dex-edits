"""CL - Abu Dhabi 2025: Lando Norris, world champion (Thu 19 Nov 12:00). Story-first, two runs: the title call ("this will be
a victory lap for Lando Norris... Lando Norris is the Formula One World Champion") over his family in tears, then the
radio ("it's the Promised Land for Lando - Lando, this is Zak from McLaren, is this the world champion hotline? - thank
you guys, oh my god") over his helmet, B&W freeze on Norris with his face in his hands. ~44 s, square in 1080x1920,
25 fps. Song: Purple Rain (intro) under the voice.
Sources: F1 'Race Highlights | 2025 Abu Dhabi Grand Prix' (S-LMSpzlnc0); words bra/abudhabi25.json.
Usage: SRC=<sources folder> SCRATCH=<work dir> python3 edit_cl_norris_champion_ad25.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('S-LMSpzlnc0'), 'crop=1080:1080:420:0')}
FIX = {'ZACH': 'ZAK'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT',
        'THAT', 'BY', 'THIS', 'WHO', 'HIS', 'WE', "WE'VE", 'TWO'}


def lines(a, b):
    """1-3 word caption lines from the whisper words between a and b (new line at punctuation or after 3 words)."""
    # whisper gave no punctuation here: also end a line at the end of each whisper segment (= sentence)
    W = [(*w, i == len(seg['w']) - 1) for seg in json.load(open(os.path.join(S, 'bra', 'abudhabi25.json'))) for i, w in enumerate(seg['w'])]
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


# no punctuation in this transcript: caption lines written by hand, each timed to its first word in bra/abudhabi25.json
PHRASES = ['BUT THIS WILL BE', 'A VICTORY LAP', 'FOR LANDO NORRIS.', 'OSCAR PIASTRI', 'WILL COME OVER THE LINE NEXT,',
           'BUT THE MOMENT', 'HAS NEARLY ARRIVED', 'FOR LANDO NORRIS,', 'WHO HAS GROWN RESILIENT', 'TO STAND CENTRE STAGE',
           'IN FORMULA ONE.', 'AND AFTER 24 ROUNDS,', 'LANDO NORRIS', 'IS THE FORMULA ONE', 'WORLD CHAMPION.',
           "IT'S THE PROMISED LAND", 'FOR LANDO.', 'LANDO, THIS IS ZAK', 'FROM McLAREN.', 'IS THIS THE WORLD',
           'CHAMPION HOTLINE?', 'THANK YOU,', 'GUYS.', 'OH MY GOD.']


def hand_lines(a, b, phrases):
    W = [w for seg in json.load(open(os.path.join(S, 'bra', 'abudhabi25.json'))) for w in seg['w'] if a <= w[0] <= b - 0.1]
    out, k = [], 0
    norm = lambda x: x.upper().strip('.,?!').replace('MCLAREN', 'MCLAREN')
    for ph in phrases:
        first = norm(ph.split()[0])
        for j in range(k, len(W)):
            if norm(W[j][2]) == first or (first == 'ZAK' and norm(W[j][2]) == 'ZACH'):
                out.append((W[j][0], ph)); k = j + len(ph.split()) - 1; break
    return out


CFG = dict(name='norris_champion_ad25', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'purple_rain_prince.mp3'),
           song_in=0.0, title='LANDO NORRIS|WORLD CHAMPION', banner_in=0.6,
           segments=[dict(type='voice', k='v', a=361.95, b=386.0, words=hand_lines(361.95, 386.0, PHRASES[:15])),
                     dict(type='voice', k='v', a=406.35, b=424.2, words=hand_lines(406.35, 424.2, PHRASES[15:])),
                     dict(type='end', k='v', at=486.5, dur=2.2, text='WORLD CHAMPION.')])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cl_norris_champion_ad25_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
