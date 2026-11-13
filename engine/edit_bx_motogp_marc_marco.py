"""BX - MotoGP: MARC vs MARCO, the title contenders collide (2026 Qatar GP sprint) - first non-F1 master edit (Desmond, Nov
12-13: other series fill the gaps; varied camera angles; live cutouts; YouTube <= 60 s). 55.6 s, square in 1080x1920, 25 fps
(the source's own rate).
  A  the call, one continuous run (MotoGP's own pictures - start, trackside, aerial, replays): "In the slipstream goes
     Bezzecchi, 355 km an hour... he runs in wide! Oh, there's contact, and Bezzecchi goes down!... is he out of the world
     championship chase?"
  B  drop on Montagem Kali: race moments from every angle - head-on start, wide, top-down onboard, crowd, telephoto
     battles, night aerial, pit wall, fireworks, celebration - each hit its own move
  C  "No further action. It has been declared by the stewards. A racing incident."
  D  Aprilia boss Massimo Rivola's sarcastic applause, cut out LIVE while he claps, RACING INCIDENT? behind him, the
     commentator explaining it.
Sources: MotoGP YouTube dBf-CVXVLwk (Marc vs Marco), 0CIRv1O6Ghs (best moments). No grade.
Usage: SRC=<sources folder> SCRATCH=<dir with bra/marcmarco.json> DEX_FPS=25 python3 edit_bx_motogp_marc_marco.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
SQ = 'crop=1080:1080:420:0'
FILES = {'m': (src('dBf-CVXVLwk'), SQ), 'b': (src('0CIRv1O6Ghs'), SQ)}
FIX = {'BETSECKI': 'BEZZECCHI', 'BETSECKI,': 'BEZZECCHI,', "BETSECKI'S": "BEZZECCHI'S", 'BECSECHI': 'BEZZECCHI', 'BESTSEES': 'BEZZECCHI SEES',
       'MARK': 'MARC', 'MARQUEZ': 'MÁRQUEZ', 'MARQUEZ,': 'MÁRQUEZ,', 'RIVA': 'RIVOLA', "RIVA'S": "RIVOLA'S", 'FIMO': 'FIM MOTOGP',
       'BREAKS': 'BRAKES', 'INSTANT.': 'INCIDENT.', 'CONTEXT,': 'CONTACT,', 'MARK,': 'MARC,', 'RIVA.': 'RIVOLA.'}
# whole-line fixes after grouping; None = no caption (unclear audio - never put words in the commentator's mouth)
LINES = {'MÁRQUEZ SO -SO': None, 'GOOD,': None, 'THERE IS THE OTHER': None, 'MARC GOES BEZZECCHI': 'MARCO BEZZECCHI'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT', 'THAT'}


def lines(a, b):
    """1-3 word caption lines from the whisper words between a and b (new line at punctuation or after 3 words)."""
    W = [w for seg in json.load(open(os.path.join(S, 'bra', 'marcmarco.json'))) for w in seg['w']]
    out, cur = [], None
    for s, e, w in W:
        if not (a <= s <= b - 0.1): continue
        w = FIX.get(w.upper(), w.upper())
        if cur is None: cur = [s, [w]]
        else: cur[1].append(w)
        if (len(cur[1]) >= 3 and w.strip('.,?!') not in HANG) or w[-1] in '.,?!':
            out.append((cur[0], ' '.join(cur[1]))); cur = None
    if cur: out.append((cur[0], ' '.join(cur[1])))
    return [(t, LINES.get(x, x)) for t, x in out if LINES.get(x, x)]


CUTS = [76.02, 76.6, 77.18, 77.92, 78.64, 79.83, 80.27, 80.71, 81.29, 81.87, 82.34, 83.06, 83.64, 84.08]
FXS = ['flash', 'whip_l', 'zoom', 'punch', 'whip_r', 'spin', 'glitch', 'shake', 'whip_u', 'zoom', 'punch', 'flash', 'whip_l', 'zoom']
# every camera type, never the same angle twice in a row: head-on start, wide grid, trackside pack, top-down onboard,
# crowd, telephoto battle, low close bike, night aerial, trackside close, pit wall, telephoto, fireworks, side close, champagne
SPOTS = [('b', 6.5), ('b', 0.5), ('b', 38.0), ('b', 62.0), ('b', 156.0), ('b', 74.0), ('b', 76.0), ('m', 120.0), ('b', 132.0),
         ('b', 104.0), ('b', 116.0), ('b', 186.0), ('b', 166.0), ('b', 200.0)]
B_SHOTS = [dict(k=k, t=t, fx=FXS[i]) for i, (k, t) in enumerate(SPOTS)]
B_SHOTS[0]['stamp'] = 'TITLE FIGHT.'
CFG = dict(name='motogp_marc_marco', files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '05_montagem_kali_slowed.mp3'),
           song_in=76.02 - 34.3, title='MARC vs MARCO|TITLE FIGHT IN QATAR', banner_in=0.6,
           segments=[dict(type='voice', k='m', a=0.2, b=34.5, words=lines(0.2, 34.5)),
                     dict(type='beats', cuts=CUTS, end=84.96, shots=B_SHOTS),
                     dict(type='voice', k='m', a=87.0, b=91.9, words=lines(87.0, 91.9)),
                     dict(type='voice', k='m', a=128.3, b=136.2, words=lines(128.3, 136.2),
                          hero=dict(start=0.75, text='RACING INCIDENT?', dur=4.3))   # only while Rivola is on screen])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'bx_motogp_marc_marco_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
