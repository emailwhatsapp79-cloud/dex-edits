"""DL - QATAR 2024 FLASHBACK (Thu 26 Nov 12:00): one mirror on the racing line, two punctures in one lap - Hamilton, then Sainz.
Source: F1 official highlights (NGSPg5ns2-0). NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('NGSPg5ns2-0'), 'crop=1080:1080:420:0')}
NAME = 'dl_qatar24_mirror_punctures.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '22_just_keep_watching_f1_cover.mp3'), song_in=51.5, title="ONE MIRROR ON THE STRAIGHT|TWO PUNCTURES IN ONE LAP", banner_in=0.2,
           segments=[dict(type='voice', k='v', a=237.15, b=239.85, words=[(237.26, 'PUNCTURE, PUNCTURE,'), (238.40, 'FOR LEWIS HAMILTON.')]),
                     dict(type='voice', k='v', a=247.65, b=257.1, words=[(247.74, 'ANOTHER ONE!'), (248.60, 'ANOTHER ONE!'), (249.34, "IT'S TIME FOR CARLOS SAINZ!"), (251.26, 'THE MIRROR'), (251.86, 'ON THE RACING LINE.'), (253.56, 'AND CARLOS SAINZ'), (254.54, 'HAS A PUNCTURE.'), (255.36, 'TWO CARS ON ONE LAP.')]),
                     dict(type='outro', shots=[('v', 238.0), ('v', 250.0), ('v', 236.5), ('v', 252.5), ('v', 255.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
