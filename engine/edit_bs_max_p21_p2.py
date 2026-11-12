"""BS - F1: MAX VERSTAPPEN, P21 -> P2 at Interlagos (2026 Sao Paulo GP). The first STORY-FIRST edit (EDITING_RULES top,
refs AD1-AD3): three continuous parts from F1's own "Nine Minutes Of Max Verstappen Tearing Through The Field" (1080p50,
q16mDWoytf0), every sentence finished, then a black-and-white ending - square picture in a 1080x1920 frame.
  1. hook + setup   0.0-36.3    "Instant overtake. Max Verstappen is now up 18 places... Phenomenal driving." -> he starts
                                at the back -> Max: "we'll see tomorrow how far we can move up to the front."
  2. the charge   206.2-280.8   Hamilton slides, Max through for 9th -> "instant overtake" on Piastri -> round the outside ->
                                past Albon -> "Up into seventh. Amazing."
  3. the payoff   464.5-478.6   "Norris wins... and behind him, Max Verstappen with a superlative drive. Once again, from the
                                back to the podium, up 19 places."
  ending: B&W onboard, his face, the podium - "P21 > P2." - song: Just Keep Watching (F1 movie), full track under all of it.
Usage: SRC=<folder with the mp4s> SCRATCH=<dir with bra/max.json> python3 edit_bs_max_p21_p2.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import storyedit

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, f'*{vid}*.mp4'))[0]
VOICE = [('m', 0.0, 36.3), ('m', 206.2, 280.8), ('m', 464.5, 478.6)]
FIX = {'STAPPEN': 'VERSTAPPEN', "STAPPEN'S": "VERSTAPPEN'S", 'ALBIN': 'ALBON', "ALBIN'S": "ALBON'S", 'HAJAR': 'HADJAR',
       'CARTING': 'KARTING'}
# whole-line fixes after grouping; None = no caption (too unclear to put words in the commentator's mouth)
LINES = {"HE'S QUALIFYING HOUR": 'HIS QUALIFYING HOUR', 'PAST THE BOTH.': 'PAST THEM BOTH.', "IT'S VERSTAPPEN GOING": None,
         'TO A PIASTRI HE IS.': None, 'WE GO TO THE SENNA': 'WE GO TO THE SENNA S.', "S'S.": None}
HANG = {'SO', 'THE', 'A', 'AN', 'AND', 'OF', 'TO', 'IN', 'IS', 'HE', "HE'S", 'FROM', 'FOR', 'BUT', 'WITH', 'AT', 'ON', 'IT', 'WE', 'I'}


def words_lines():
    """1-3 word caption lines from whisper words inside each part (new line at punctuation or after 3 words)."""
    W = [w for seg in json.load(open(os.path.join(S, 'bra', 'max.json'))) for w in seg['w']]
    out = []
    for part, (_, a, b) in enumerate(VOICE):
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


CFG = dict(name='max_p21_p2', files={'m': src('q16mDWoytf0')}, voice=VOICE, grade='bright', crop=420,
           ending=[('m', 289.5, 2.0), ('m', 519.0, 2.4), ('m', 522.4, 3.6)], endcap='P21 > P2.',
           song=os.path.join(ASSETS, 'songs', 'full', '22_just_keep_watching_f1_cover.mp3'), song_in=0.0, song_under=0.22,
           title='MAX VERSTAPPEN|P21 > P2 AT INTERLAGOS')

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 50))
    cfg = dict(CFG, fps=fps, words=words_lines())
    out, body, total = storyedit.render(cfg, S, os.path.join(S, 'out', f'bs_max_p21_p2_{fps}.mp4'))
    print(out, f'story {body:.1f}s, total {total:.1f}s', flush=True)
