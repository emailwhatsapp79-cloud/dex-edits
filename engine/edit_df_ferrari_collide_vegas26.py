"""DF - F1 LAS VEGAS 2026: FERRARI VS FERRARI (Mon 23 Nov 12:00). Leclerc dives down the inside and the two Ferraris
collide - and it was not their first clash of the night (Hamilton went off avoiding Leclerc earlier). "whose fault? 👇"
NOV 17 rules: ~18 s, cold open on the contact, short commentary runs, beat outro + card.
  1 "The Ferraris make contact."                       (the contact)
  2 "Charles Leclerc and Lewis Hamilton collide."              (replay)
  3 "Another skirmish between the Scarlet pair."              (picture: their first clash, Hamilton off the road)
Source: F1 'Race Highlights | 2026 Las Vegas Grand Prix' (Vyk_6bNm7lo). Song: Ramalama (Roisin Murphy).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_df_ferrari_collide_vegas26.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('Vyk_6bNm7lo'), 'crop=1080:1080:420:0')}
W1 = [(348.01, 'THE FERRARIS'), (348.91, 'MAKE CONTACT.')]
W2 = [(350.15, 'CHARLES LECLERC'), (351.53, 'AND LEWIS HAMILTON'), (353.11, 'COLLIDE.')]
W3 = [(357.55, 'ANOTHER SKIRMISH'), (359.47, 'BETWEEN THE'), (360.59, 'SCARLET PAIR.')]
CFG = dict(name='ferrari_collide_vegas26', files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'ramalama_roisin_murphy.mp3'),
           song_in=113.0, title='FERRARI VS FERRARI|LECLERC AND HAMILTON COLLIDE', banner_in=0.2,
           segments=[dict(type='voice', k='v', a=347.9, b=349.95, words=W1, pic=('v', 351.0)),   # open on the spin, not the aerial; F1 logo wipe at 353.5
                     dict(type='voice', k='v', a=349.95, b=353.95, words=W2, pic=('v', 355.6)),
                     dict(type='voice', k='v', a=357.45, b=361.7, words=W3, pic=('v', 131.0)),
                     dict(type='outro', shots=[('v', 351.5), ('v', 356.0), ('v', 133.5), ('v', 129.0), ('v', 357.5, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'df_ferrari_collide_vegas26_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
