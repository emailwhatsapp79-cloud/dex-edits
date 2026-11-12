"""BT - F1: NORRIS, BACK TO BACK IN BRAZIL - story-first edit (EDITING_RULES top), ~1 min, square in 1080x1920.
Four continuous parts, every sentence finished, from the FORMULA 1 YouTube uploads (1080p50):
  1. hook      race 227.1-235.7  "Ah, he loses it! Kimi Antonelli from the lead of the Grand Prix! ... spins at turn one,
                                 and Lando Norris leads."
  2. tension   max  444.6-459.9  "Norris was a lot more comfortable in the lead ... No, Norris, that is the worst thing you
                                 want as a race leader. Some rain at the end, slippery on slick."
  3. the call  race 419.6-430.4  "And Lando Norris will go back to back in Brazil. In the wet, in the dry. He's P1. Norris
                                 wins the Sao Paulo Grand Prix."
  4. Norris    react 26.6-42.4   "So in terms of focus needed every single lap... one of the best wins I've had... one of the
                                 most rewarding at the same time."
  ending: B&W podium (fist, champagne, fireworks) - "BACK TO BACK." - song: Funk Unico (super slowed), full track.
Usage: SRC=<folder with the mp4s> SCRATCH=<dir with bra/*.json> python3 edit_bt_norris_story.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import storyedit

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, f'*{vid}*.mp4'))[0]
FILES = {'r': src('lkb5kqDJYXk'), 'm': src('q16mDWoytf0'), 'ni': src('jpwFNmUzWn8')}
VOICE = [('r', 227.1, 235.7), ('m', 444.6, 459.9), ('r', 419.6, 430.4), ('ni', 26.6, 42.4)]
TX = {'r': ['race.json'], 'm': ['max.json'], 'ni': ['react_norris.json']}
FIX = {'LIMBLAD': 'LINDBLAD', 'ALBANY.': 'ALBON.', 'ALBANY': 'ALBON', 'SÃO': 'SAO'}
# whole-line fixes after grouping; None = no caption
LINES = {'OF LIKE FOCUS': 'OF FOCUS', 'BUT WAS WAS': 'BUT IT WAS', 'ENJOYABLE WAS A CONSTANT': 'ENJOYABLE, A CONSTANT',
         'THE PROBABLY ONE': 'PROBABLY ONE', 'TIME': 'TIME.'}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT', 'WE', 'I'}
# words whisper missed at the start of part 4 (from a second pass on 22-29 s)
EXTRA = {'ni': [(26.66, 26.8, 'So'), (26.8, 27.58, 'in'), (27.58, 27.8, 'terms'), (27.8, 28.0, 'of')]}


def words_lines():
    """1-3 word caption lines from whisper words inside each part (new line at punctuation or after 3 words)."""
    out = []
    for part, (k, a, b) in enumerate(VOICE):
        W = [w for f in TX[k] for seg in json.load(open(os.path.join(S, 'bra', f))) for w in seg['w']] + EXTRA.get(k, [])
        W = sorted({round(w[0], 2): tuple(w) for w in W}.values())
        cur = None
        for s, e, w in W:
            if not (a <= s <= b - 0.1): continue
            w = FIX.get(w.upper(), w.upper())
            if cur is None: cur = [part, s, [w]]
            else: cur[2].append(w)
            if (len(cur[2]) >= 3 and w.strip('.,?!') not in HANG) or w[-1] in '.,?!':
                out.append((cur[0], cur[1], ' '.join(cur[2]))); cur = None
        if cur: out.append((cur[0], cur[1], ' '.join(cur[2])))
    return [(p, t, LINES.get(x, x)) for p, t, x in out if LINES.get(x, x)]


CFG = dict(name='norris_story', files=FILES, voice=VOICE, grade='bright', crop=420,
           ending=[('r', 459.6, 2.6), ('r', 462.6, 2.6), ('r', 465.6, 3.0)], endcap='BACK TO BACK.',
           song=os.path.join(ASSETS, 'songs', 'full', '13_funk_unico_super_slowed.mp3'), song_in=0.0, song_under=0.22,
           title='LANDO NORRIS|BACK TO BACK IN BRAZIL')

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 50))
    cfg = dict(CFG, fps=fps, words=words_lines())
    out, body, total = storyedit.render(cfg, S, os.path.join(S, 'out', f'bt_norris_story_{fps}.mp4'))
    print(out, f'story {body:.1f}s, total {total:.1f}s', flush=True)
