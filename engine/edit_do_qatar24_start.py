"""DO - QATAR 2024 FLASHBACK (Thu 26 Nov 18:00): Lando looks like he goes past both Russell and Max at the start - Max gets his elbows out and keeps it.
Source: F1 official highlights (NGSPg5ns2-0). NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('NGSPg5ns2-0'), 'crop=1080:1080:420:0')}
NAME = 'do_qatar24_start.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'housewife_tate_mcrae.mp3'), song_in=30.0, title="QATAR 2024|LANDO VS MAX INTO TURN 1", banner_in=0.2,
           segments=[dict(type='voice', k='v', a=17.5, b=26.6, words=[(17.60, 'LANDO NORRIS'), (18.02, 'FIGHTING ON THE INSIDE,'), (19.76, "LANDO'S GOING PAST"), (20.50, 'THE PAIR OF THEM!'), (21.44, 'HOW DID HE DO THAT?'), (22.94, "HE DIDN'T,"), (23.94, 'BECAUSE VERSTAPPEN'), (24.98, 'GOT HIS ELBOWS OUT.')]),
                     dict(type='voice', k='v', a=28.7, b=34.75, words=[(28.76, "IT'S VERSTAPPEN AND NORRIS"), (29.70, 'AT THE HEAD OF THE FIELD,'), (30.74, 'MAX GOING WHEEL TO WHEEL'), (32.78, 'WITH HIS RIVAL.')]),
                     dict(type='outro', shots=[('v', 19.0), ('v', 24.0), ('v', 21.0), ('v', 27.0), ('v', 31.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
