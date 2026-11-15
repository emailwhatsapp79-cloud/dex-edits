"""CU - SUPERCARS: SANDOWN, SEVEN TENTHS (Mon 16 Nov 08:00, replaces the Russell re-cut). Anton De Pasquale must win
Race 34 to make the finals; he chases Matt Payne through lapped traffic to the flag and misses by 0.7 s - a week after
running dry one lap from a Bathurst win. "The almost year."
  1 "Anton De Pasquale must, must win this race to fight for a championship."
  2 "Final few corners. Anton has thrown everything he possibly can. But it's not going to be enough."
  3 "And Anton De Pasquale missed the finals by seven tenths of a second."
  4 "And fell one lap short of a win at Bathurst. What a tough year for Anton De Pasquale. The almost year."
  outro: a new clip on every beat (Desmond Nov 15), then the end card.
Song: Funk Unico (super slowed) from 42.4 s: the build runs under the voice, the drop at 64 s lands on the outro.
Source: Supercars 'Race Highlights: Race 34 | 2026 Penrite Oil Sandown 500' (YTaXWh9o9Eg); whisper hears 'Antoine
Deepuswali' - the commentators say Anton De Pasquale.
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_cu_sandown_seven_tenths.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'s': (src('YTaXWh9o9Eg'), 'crop=1080:1080:420:0')}
W1 = [(686.18, 'ANTON DE PASQUALE'), (687.18, 'MUST, MUST WIN THIS RACE'), (689.18, 'TO FIGHT FOR A CHAMPIONSHIP.')]
W2 = [(813.42, 'FINAL FEW CORNERS.'), (815.6, 'ANTON HAS THROWN'), (816.28, 'EVERYTHING HE POSSIBLY CAN.'),
      (818.3, "BUT IT'S NOT GOING"), (818.94, 'TO BE ENOUGH.')]
W3 = [(833.24, 'AND ANTON DE PASQUALE'), (834.68, 'MISSED THE FINALS'), (835.64, 'BY SEVEN TENTHS OF A SECOND.')]
W4 = [(869.68, 'AND FELL ONE LAP SHORT'), (871.14, 'OF A WIN AT BATHURST.'), (872.34, 'WHAT A TOUGH YEAR'),
      (873.14, 'FOR ANTON DE PASQUALE.'), (874.46, 'THE ALMOST YEAR.')]
OUTRO = []   # filled after the contact sheet check
CFG = dict(name='sandown_seven_tenths', files=FILES,
           song=os.path.join(ASSETS, 'songs', 'full', '13_funk_unico_super_slowed.mp3'), song_in=42.4,
           title='SANDOWN|SEVEN TENTHS', banner_in=0.4,
           segments=[dict(type='voice', k='s', a=686.1, b=690.95, words=W1),
                     dict(type='voice', k='s', a=813.35, b=819.6, words=W2),
                     dict(type='voice', k='s', a=833.2, b=837.4, words=W3),
                     dict(type='voice', k='s', a=869.6, b=875.35, words=W4),
                     dict(type='outro', shots=OUTRO)])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cu_sandown_seven_tenths_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
