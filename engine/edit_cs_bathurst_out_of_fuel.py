"""CS - SUPERCARS: BATHURST 1000, OUT OF FUEL ON THE LAST LAP (Wed 18 Nov 08:00, replaces the Vegas 2023 lead swaps).
Anton De Pasquale leads onto the final lap saving fuel, runs dry, Brodie Kostecki takes the win for Dick Johnson Racing.
  1 commentator: "The question is, who comes out on top? It is Chevy versus Ford at the end."
  2 commentator: "It's done, it's done. He's run out of fuel. Brodie Kostecki goes through to the race lead on the final
    lap, and Anton De Pasquale has run out of fuel. It's a mountain boil over. Extraordinary scenes."
  3 "From agony to ecstasy." (the song's break ends and the drop lands here)
  outro (Nov 15 v2, Desmond: 'a different clip on every beat'): side-by-side battles, the crash smoke, three-wide,
    the winner head-on, the burnout in slow motion, then the end card. Extra clips: 'FINAL 6 LAPS' (6aoEVfNFrE0).
Song: Ramalama (Roisin Murphy), from 105.5 s so the drop at 124 s meets "agony to ecstasy". ~27 s, 25 fps, no grade.
Names checked with a second whisper pass prompted with the driver names. The source's timing tower sits in x < 400,
so the square crop starts at 420.
Source: Supercars 'LAST LAP: Repco Bathurst 1000 | 2026' (_7gBKGd2qzU).
Usage: SRC=<sources folder> SCRATCH=<dir> python3 edit_cs_bathurst_out_of_fuel.py"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'b': (src('_7gBKGd2qzU'), 'crop=1080:1080:420:0'),
         'f': (src('6aoEVfNFrE0'), 'crop=1080:1080:420:0')}
W1 = [(9.5, 'THE QUESTION IS,'), (10.78, 'WHO COMES OUT ON TOP?'), (12.64, 'IT IS CHEVY'), (13.18, 'VERSUS FORD AT THE END.')]
W2 = [(37.66, "IT'S DONE, IT'S DONE."), (39.2, "HE'S RUN OUT OF FUEL."), (40.62, 'BRODIE KOSTECKI'),
      (41.54, 'GOES THROUGH TO THE RACE LEAD'), (42.9, 'ON THE FINAL LAP,'), (44.28, 'AND ANTON DE PASQUALE'),
      (45.78, 'HAS RUN OUT OF FUEL.'), (47.54, "IT'S A MOUNTAIN"), (48.54, 'BOIL OVER.'), (50.26, 'EXTRAORDINARY SCENES.')]
W3 = [(52.9, 'FROM AGONY'), (53.84, 'TO ECSTASY.')]
CFG = dict(name='bathurst_out_of_fuel', files=FILES,
           song=os.path.join(ASSETS, 'songs', 'trend', 'ramalama_roisin_murphy.mp3'), song_in=105.5,
           title='BATHURST 1000|OUT OF FUEL', banner_in=0.4,
           segments=[dict(type='voice', k='b', a=9.45, b=14.45, words=W1),
                     dict(type='voice', k='b', a=37.6, b=51.25, words=W2),
                     dict(type='voice', k='b', a=52.85, b=54.75, words=W3),
                     dict(type='outro', shots=[('f', 38.0), ('f', 140.0), ('f', 334.5), ('f', 448.0), ('f', 588.0), ('f', 672.0),
                                               ('f', 700.0), ('b', 132.0), ('b', 179.5, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'cs_bathurst_out_of_fuel_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
