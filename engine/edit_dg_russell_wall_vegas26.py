"""DG - F1 LAS VEGAS 2026: RUSSELL'S WIN CHANCE GONE IN ONE CORNER (Mon 23 Nov 18:00). He had swapped the lead with Max
all night; on the last laps he brakes over debris, locks up and hits the wall - Max wins. "the debris or George? 👇"
NOV 17 rules: ~18 s, cold open on the lock-up, short commentary runs, beat outro + card.
  1 "Laid on the brakes over the debris, over the debris. He locks up, he goes off, he hits the wall. George Russell into
     the barrier and his chance of winning this race disappears."
  2 "Max Verstappen wins the Las Vegas Grand Prix."
Source: F1 'Race Highlights | 2026 Las Vegas Grand Prix' (Vyk_6bNm7lo). Song: Bow Bow Bow (Zeddy Will).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_dg_russell_wall_vegas26.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('Vyk_6bNm7lo'), 'crop=1080:1080:420:0')}
W1 = [(408.67, 'LAID ON THE BRAKES'), (409.45, 'OVER THE DEBRIS,'), (410.27, 'OVER THE DEBRIS.'), (411.33, 'HE LOCKS UP,'),
      (412.25, 'HE GOES OFF,'), (413.07, 'HE HITS THE WALL.'), (414.39, 'GEORGE RUSSELL'), (415.81, 'INTO THE BARRIER'),
      (416.89, 'AND HIS CHANCE'), (418.01, 'OF WINNING THIS RACE'), (419.27, 'DISAPPEARS.')]
W2 = [(453.02, 'MAX VERSTAPPEN WINS'), (454.46, 'THE LAS VEGAS GRAND PRIX.')]
CFG = dict(name='russell_wall_vegas26', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'bow_bow_bow_zeddy_will.mp3'),
           song_in=54.45, title="RUSSELL'S WIN CHANCE|GONE IN ONE CORNER", banner_in=0.2,
           segments=[dict(type='voice', k='v', a=408.55, b=420.2, words=W1),
                     dict(type='voice', k='v', a=452.95, b=456.25, words=W2),
                     dict(type='outro', shots=[('v', 411.0), ('v', 405.5), ('v', 446.0), ('v', 412.5), ('v', 455.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'dg_russell_wall_vegas26_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
