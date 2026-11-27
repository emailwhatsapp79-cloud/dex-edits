"""FB02 - FOOTBALL CHANNEL Sat 28 Nov 13:00: Arsenal's side before Sunday's Arsenal v Man City - Martinelli lifts it over Donnarumma, then 'you want your big players to step up and have big moments'. Source: Arsenal '20 Arsenal Moments of MAGIC ft... Martinelli vs Man City' (ZjepG5KLEug).
NOV 17 rules: 15-20 s, short commentary runs (Content ID: each run < 8 s), beat outro + card."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import master

S = os.environ.get('SCRATCH', '/tmp')
SRC = os.environ['SRC']
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'dex-edits-assets')
src = lambda vid: glob.glob(os.path.join(SRC, '**', f'*{vid}*.mp4'), recursive=True)[0]
FILES = {'a': (src('ZjepG5KLEug'), 'crop=1080:1080:420:0')}
NAME = 'fb02_martinelli_city.py'.replace('.py', '')
CFG = dict(name=NAME, files=FILES, song=os.path.join(ASSETS, 'songs', 'trend', 'can_i_ride_sidepiece.mp3'), song_in=40.0, title="SUNDAY: ARSENAL vs MAN CITY|MARTINELLI'S MOMENT", banner_in=0.2,
           segments=[dict(type='voice', k='a', a=3.35, b=10.45, words=[(3.38, "THERE'S A CHIP-IT-IN-BEHIND"), (5.44, 'OPPORTUNITY HERE'), (6.66, 'FOR GABRIEL MARTINELLI,'), (7.90, 'LIFTED OVER DONNARUMMA'), (9.54, "AND IT'S IN!")]),
                     dict(type='voice', k='a', a=89.9, b=92.45, pic=('a', 12.5), words=[(89.95, 'YOU WANT YOUR BIG PLAYERS'), (91.13, 'TO STEP UP IN BIG MOMENTS.')]),
                     dict(type='outro', shots=[('a', 13.5), ('a', 19.0), ('a', 15.0), ('a', 25.0), ('a', 12.0, 0.6)])])

if __name__ == '__main__':
    fps = int(os.environ.get('DEX_FPS', 25))
    out, total = master.render(dict(CFG, fps=fps), S, os.path.join(S, 'out', f'{NAME}_{fps}.mp4'))
    print(out, f'total {total:.1f}s', flush=True)
    import look; look.yt1440(out, out.replace('.mp4', '_yt1440.mp4'))
