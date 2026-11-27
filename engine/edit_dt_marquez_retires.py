"""DT - MOTOGP (F1 channel) Sat 28 Nov 08:00: Marc Marquez announces his retirement in Valencia, five days after his 8th MotoGP title - he goes out on top. Source: MotoGP 'Marc Marquez announces his retirement before FP1 in Valencia' (m3usITpq-Os).
NOV 17 rules: 15-20 s, short commentary runs (Content ID: each run < 8 s), beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'m': (src('m3usITpq-Os'), 'crop=1080:1080:420:0')}
NAME = 'dt_marquez_retires.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'full', '19_destroy_it_all_yuji_slowed.mp3'), song_in=0.0, title="MARC MARQUEZ RETIRES|5 DAYS AFTER HIS 8TH TITLE", banner_in=0.2,
           segments=[dict(type='voice', k='m', a=106.55, b=111.0, words=[(106.59, 'MARC MARQUEZ'), (107.87, 'IS RETIRING.'), (109.39, "HE'S STEPPING AWAY FROM MOTOGP.")]),
                     dict(type='voice', k='m', a=100.65, b=106.4, words=[(100.71, 'EIGHT WORLD CHAMPIONSHIPS.'), (102.21, 'THIS IS THE FINAL FAREWELL.'), (105.61, "IT'S THE LAST GOODBYE.")]),
                     dict(type='voice', k='m', a=228.45, b=233.75, words=[(228.49, 'MARC MARQUEZ,'), (229.83, 'THE 33-YEAR-OLD SUPERSTAR,'), (231.89, 'IS GOING OUT ON TOP.')]),
                     dict(type='outro', shots=[('m', 92.0), ('m', 104.0), ('m', 96.0), ('m', 110.0), ('m', 231.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
