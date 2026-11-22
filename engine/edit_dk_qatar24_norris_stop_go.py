"""DK - QATAR 2024 FLASHBACK (Wed 25 Nov 18:00): Lando Norris gets a 10-second stop-go for not slowing under yellows (a mirror on the straight) - effectively 35 s, his race gone, Max wins.
Source: F1 official highlights (NGSPg5ns2-0). NOV 17 rules: 15-20 s, short commentary runs, beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'v': (src('NGSPg5ns2-0'), 'crop=1080:1080:420:0')}
NAME = 'dk_qatar24_norris_stop_go.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '19_destroy_it_all_yuji_slowed.mp3'), song_in=0.0, title="QATAR 2024|NORRIS DIDN'T LIFT", banner_in=0.2,
           segments=[dict(type='voice', k='v', a=351.75, b=362.4, words=[(351.84, "IT'S A 10-SECOND"), (352.94, 'STOP-GO PENALTY'), (354.40, 'FOR LANDO NORRIS'), (355.76, 'FOR FAILING TO SLOW'), (356.96, 'UNDER YELLOW FLAGS.'), (358.12, 'THAT IS EFFECTIVELY'), (359.28, 'A 35-SECOND PENALTY'), (361.36, 'FOR LANDO NORRIS.')]),
                     dict(type='voice', k='v', a=219.15, b=224.85, words=[(219.22, "LET'S LISTEN IN"), (220.32, 'AS HE BLASTS PAST THIS.'), (221.82, 'CHECK THE BOARD.'), (222.40, 'LANDO DID NOT LIFT.')]),
                     dict(type='voice', k='v', a=436.1, b=438.6, words=[(436.18, 'MAX VERSTAPPEN WINS'), (437.10, 'THE QATAR GRAND PRIX.')]),
                     dict(type='outro', shots=[('v', 353.5), ('v', 221.0), ('v', 355.5), ('v', 430.0), ('v', 357.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
